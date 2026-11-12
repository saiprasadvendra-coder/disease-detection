"""
train_model.py
--------------
Improved ML training script for Disease Detection with Symptoms.

Input:
    disease_symptoms.csv

Output:
    ../model/disease_model.pkl
    ../model/symptom_encoder.pkl
    ../model/feature_list.json
    ../model/model_metrics.json
"""

from pathlib import Path
import json
import warnings

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")


# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATASET_PATH = BASE_DIR / "disease_symptoms.csv"
MODEL_DIR = PROJECT_DIR / "model"

MODEL_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------------

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}\n"
        "Place disease_symptoms.csv in the same folder as train_model.py."
    )

df = pd.read_csv(DATASET_PATH)

print("\n========== DATASET INFORMATION ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

if "prognosis" not in df.columns:
    raise ValueError(
        "The dataset must contain a target column named 'prognosis'."
    )


# ---------------------------------------------------------
# 3. Clean and validate data
# ---------------------------------------------------------

df.columns = df.columns.str.strip().str.lower()

# Remove completely empty rows
df = df.dropna(how="all").reset_index(drop=True)

# Remove duplicate records
duplicate_count = df.duplicated().sum()
if duplicate_count > 0:
    print(f"Removing duplicate rows: {duplicate_count}")
    df = df.drop_duplicates().reset_index(drop=True)

# Replace missing symptom values with zero
symptom_columns = [
    column for column in df.columns
    if column != "prognosis"
]

if not symptom_columns:
    raise ValueError("No symptom columns were found.")

df[symptom_columns] = (
    df[symptom_columns]
    .apply(pd.to_numeric, errors="coerce")
    .fillna(0)
)

# Convert symptoms to binary values: 0 or 1
for column in symptom_columns:
    df[column] = (df[column] > 0).astype(int)

# Remove rows without a disease label
df = df.dropna(subset=["prognosis"])
df["prognosis"] = df["prognosis"].astype(str).str.strip()

if df["prognosis"].nunique() < 2:
    raise ValueError("At least two disease classes are required.")

print(f"Symptom features: {len(symptom_columns)}")
print(f"Disease classes: {df['prognosis'].nunique()}")
print("\nClass distribution:")
print(df["prognosis"].value_counts())


# ---------------------------------------------------------
# 4. Prepare X and y
# ---------------------------------------------------------

X = df[symptom_columns]
y_text = df["prognosis"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_text)

# Stratified split keeps disease classes represented
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# ---------------------------------------------------------
# 5. Define candidate models
# ---------------------------------------------------------

models = {
    "RandomForest": RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),

    "ExtraTrees": ExtraTreesClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),
}


# ---------------------------------------------------------
# 6. Cross-validation model comparison
# ---------------------------------------------------------

print("\n========== MODEL COMPARISON ==========")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

cv_results = {}

for model_name, model in models.items():
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="f1_macro",
        n_jobs=-1,
    )

    mean_score = float(scores.mean())
    std_score = float(scores.std())

    cv_results[model_name] = {
        "mean_macro_f1": mean_score,
        "std_macro_f1": std_score,
        "fold_scores": [float(score) for score in scores],
    }

    print(
        f"{model_name}: "
        f"mean macro-F1 = {mean_score:.4f}, "
        f"std = {std_score:.4f}"
    )


# Select the model with the highest mean macro-F1
best_model_name = max(
    cv_results,
    key=lambda name: cv_results[name]["mean_macro_f1"],
)

best_model = models[best_model_name]

print(f"\nSelected model: {best_model_name}")


# ---------------------------------------------------------
# 7. Train selected model
# ---------------------------------------------------------

best_model.fit(X_train, y_train)


# ---------------------------------------------------------
# 8. Evaluate on test data
# ---------------------------------------------------------

y_pred = best_model.predict(X_test)

accuracy = float(accuracy_score(y_test, y_pred))
macro_f1 = float(f1_score(y_test, y_pred, average="macro"))

print("\n========== TEST RESULTS ==========")
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro-F1: {macro_f1:.4f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0,
    )
)

confusion = confusion_matrix(y_test, y_pred).tolist()


# ---------------------------------------------------------
# 9. Save model and supporting files
# ---------------------------------------------------------

model_path = MODEL_DIR / "disease_model.pkl"
encoder_path = MODEL_DIR / "symptom_encoder.pkl"
features_path = MODEL_DIR / "feature_list.json"
metrics_path = MODEL_DIR / "model_metrics.json"

joblib.dump(best_model, model_path)

joblib.dump(label_encoder, encoder_path)

with open(features_path, "w", encoding="utf-8") as file:
    json.dump(symptom_columns, file, indent=2)

metrics = {
    "selected_model": best_model_name,
    "dataset_rows": int(len(df)),
    "feature_count": int(len(symptom_columns)),
    "class_count": int(len(label_encoder.classes_)),
    "classes": label_encoder.classes_.tolist(),
    "test_size": 0.20,
    "random_state": 42,
    "test_accuracy": accuracy,
    "test_macro_f1": macro_f1,
    "cross_validation": cv_results,
    "confusion_matrix": confusion,
}

with open(metrics_path, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

print("\n========== FILES SAVED ==========")
print(f"Model: {model_path}")
print(f"Label encoder: {encoder_path}")
print(f"Feature names: {features_path}")
print(f"Metrics: {metrics_path}")

print("\nTraining completed successfully.")