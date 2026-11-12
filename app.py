"""
app.py
------
Flask web application for "Disease Detection from Symptoms".
Run locally with:
python app.py
Then open: http://127.0.0.1:5000
"""
import logging
import os
from pathlib import Path

import json
import joblib
import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify
from utils.precautions import get_condition_info, DISCLAIMER
from utils.symptom_parser import parse_symptom_input
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
MODEL_DIR = BASE_DIR / "model"

MODEL_PATH = MODEL_DIR / "disease_model.pkl"
ENCODER_PATH = MODEL_DIR / "symptom_encoder.pkl"
FEATURES_PATH = MODEL_DIR / "feature_list.json"
# ---------------------------------------------------------------------
# Load model, label encoder, and the exact feature (symptom) list used
# during training. If any file is missing, we keep the app running but
# mark it as "not ready" so we can show a friendly error instead of
# crashing the whole server.
# ---------------------------------------------------------------------
model = None
label_encoder = None
feature_list = []
MODEL_READY = False
try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    if FEATURES_PATH.suffix == ".json":
        with FEATURES_PATH.open(encoding="utf-8") as f:
            feature_list = json.load(f)
    else:
        with FEATURES_PATH.open("rb") as f:
            feature_list = pickle.load(f)
    MODEL_READY = True
    app.logger.info("Model, encoder, and feature list loaded successfully.")
except FileNotFoundError as e:
    app.logger.error(f"Model files not found: {e}. Run train_model.py first.")
except Exception as e:
    app.logger.error(f"Unexpected error loading model: {e}")
def format_symptom_label(symptom_key: str) -> str:
    """Turn 'burning_urination' into 'Burning Urination' for display."""
    return symptom_key.replace("_", " ").title()


def predict_condition(selected: list[str]) -> tuple[str, float | None, list[dict]]:
    """Predict a condition and return ranked alternatives for transparency."""
    input_vector = [1 if symptom in selected else 0 for symptom in feature_list]
    input_df = pd.DataFrame([input_vector], columns=feature_list)
    probabilities = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else None
    prediction_encoded = model.predict(input_df)[0]
    disease_name = str(label_encoder.inverse_transform([prediction_encoded])[0])
    ranked = []
    if probabilities is not None:
        ranked = sorted(
            (
                {"disease": str(label_encoder.inverse_transform([index])[0]),
                 "probability": round(float(probability) * 100, 1)}
                for index, probability in enumerate(probabilities)
            ),
            key=lambda item: item["probability"],
            reverse=True,
        )[:3]
    confidence = ranked[0]["probability"] if ranked else None
    return disease_name, confidence, ranked


@app.route("/")
def home():
    if not MODEL_READY:
        return render_template(
            "index.html",
            symptoms=[],
            error="The prediction model is not available right now. Please try again later.",
        )
    symptom_options = [
        {"key": s, "label": format_symptom_label(s)} for s in feature_list
    ]
    return render_template("index.html", symptoms=symptom_options, error=None)
@app.route("/predict", methods=["POST"])
def predict():
    if not MODEL_READY:
        return render_template(
            "result.html",
            error="The prediction model is not available right now. Please try again later.",
        )
    selected = request.form.getlist("symptoms")
    # Validation: no symptoms selected
    if not selected:
        symptom_options = [
            {"key": s, "label": format_symptom_label(s)} for s in feature_list
        ]
        return render_template(
            "index.html",
            symptoms=symptom_options,
            error="Please select at least one symptom.",
        )
    # Validation: reject unknown symptoms (should not normally happen,
    # since the form only sends symptoms we generated ourselves)
    unknown = [s for s in selected if s not in feature_list]
    if unknown:
        symptom_options = [
            {"key": s, "label": format_symptom_label(s)} for s in feature_list
        ]
        return render_template(
            "index.html",
            symptoms=symptom_options,
            error="One or more selected symptoms are not recognized.",
        )
    try:
        # Build the feature vector in the exact column order used in training.
        # Using a DataFrame (not a plain list) keeps the column names attached,
        # which matches how the model was trained and avoids sklearn warnings.
        disease_name, confidence, ranked = predict_condition(selected)
        info = get_condition_info(disease_name)
        return render_template(
            "result.html",
            disease=disease_name,
            confidence=confidence,
            info=info,
            selected_symptoms=[format_symptom_label(s) for s in selected],
            alternatives=ranked[1:],
            uncertainty=confidence is not None and confidence < 60,
            disclaimer=DISCLAIMER,
            error=None,
        )
    except Exception as e:
        # Never expose the raw stack trace to the user
        app.logger.error(f"Prediction error: {e}")
        return render_template(
            "result.html",
            error="Something went wrong while analyzing your symptoms. Please try again.",
        )

@app.route("/parse-symptoms", methods=["POST"])
def parse_symptoms_from_text():
    """
    API endpoint to extract symptoms from natural language text.
    Returns JSON with extracted symptoms, common symptoms, and metadata.
    """
    if not MODEL_READY:
        return jsonify({
            "success": False,
            "message": "Model not available",
            "symptoms": [],
            "common_symptoms": [],
        }), 503
    
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    include_common = data.get("include_common", False)
    
    symptoms, metadata = parse_symptom_input(text, feature_list, include_common)
    
    return jsonify({
        "success": metadata["success"],
        "message": metadata["message"],
        "symptoms": symptoms,
        "symptom_labels": [format_symptom_label(s) for s in symptoms],
        "common_symptoms": metadata.get("common_symptoms", []),
        "symptoms_found": metadata["symptoms_found"],
    })

@app.route("/predict-from-text", methods=["POST"])
def predict_from_text():
    """
    Predict disease from natural language symptom description.
    """
    if not MODEL_READY:
        return render_template(
            "result.html",
            error="The prediction model is not available right now. Please try again later.",
        )
    
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    include_common = data.get("include_common", False)
    
    if not text:
        return jsonify({
            "success": False,
            "message": "Please describe your symptoms.",
        }), 400
    
    # Parse symptoms from text
    selected, metadata = parse_symptom_input(text, feature_list, include_common)
    
    if not selected:
        return jsonify({
            "success": False,
            "message": metadata["message"],
            "common_symptoms": metadata.get("common_symptoms", []),
        }), 400
    
    try:
        # Build feature vector
        disease_name, confidence, ranked = predict_condition(selected)
        
        info = get_condition_info(disease_name)
        
        return jsonify({
            "success": True,
            "disease": disease_name,
            "confidence": confidence,
            "alternatives": ranked[1:],
            "uncertainty": confidence is not None and confidence < 60,
            "info": info,
            "selected_symptoms": [format_symptom_label(s) for s in selected],
            "disclaimer": DISCLAIMER,
        })
    
    except Exception as e:
        app.logger.error(f"Text prediction error: {e}")
        return jsonify({
            "success": False,
            "message": "Error processing your symptoms. Please try again.",
        }), 500

@app.errorhandler(404)
def not_found(error):
    app.logger.info("Page not found: %s", error)
    return render_template("index.html", symptoms=[], error="Page not found."), 404


@app.errorhandler(500)
def server_error(error):
    app.logger.error("Server error: %s", error)
    return render_template("index.html", symptoms=[], error="Something went wrong on our end."), 500


if __name__ == "__main__":
    # Bind externally so the app works in containers and hosting platforms.
    # The reloader and debug console are disabled outside local development.
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
