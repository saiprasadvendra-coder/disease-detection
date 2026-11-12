"""
Generates a DEMONSTRATION symptom -> disease dataset for learning purposes.
IMPORTANT: This is a synthetic, simplified dataset created for teaching how
to build the pipeline (data -> training -> prediction -> web app). It is
NOT a medically validated dataset and must never be used for real diagnosis.
Each row = one patient case.
Each symptom column = 1 (present) or 0 (absent).
The last column, 'prognosis', is the disease label.
"""
import pandas as pd
import random
from pathlib import Path

random.seed(42)
# Full list of symptoms used as features (columns)
SYMPTOMS = [
    "fever", "high_fever", "mild_fever", "headache", "cough", "sore_throat",
    "fatigue", "runny_nose", "nasal_congestion", "sneezing", "body_pain",
    "joint_pain", "muscle_pain", "nausea", "vomiting", "abdominal_pain",
    "diarrhea", "chills", "sweating", "skin_rash", "itchy_eyes",
    "watery_eyes", "loss_of_appetite", "dizziness", "shortness_of_breath",
    "chest_pain", "burning_urination", "frequent_urination", "blister",
]
# Disease -> typical symptom pattern (the symptoms usually present)
# This mapping is intentionally simple and illustrative, not clinical.
DISEASE_PATTERNS = {
    "Common Cold": ["runny_nose", "nasal_congestion", "sneezing", "sore_throat", "mild_fever", "cough"],
    "Influenza (Flu)": ["high_fever", "body_pain", "fatigue", "headache", "chills", "cough", "sore_throat"],
    "COVID-19": ["fever", "cough", "fatigue", "loss_of_appetite", "shortness_of_breath", "headache", "sore_throat"],
    "Migraine": ["headache", "dizziness", "nausea", "watery_eyes", "fatigue"],
    "Food Poisoning": ["vomiting", "diarrhea", "abdominal_pain", "nausea", "fever", "fatigue"],
    "Gastroenteritis": ["diarrhea", "vomiting", "abdominal_pain", "nausea", "mild_fever", "loss_of_appetite"],
    "Allergic Rhinitis": ["sneezing", "runny_nose", "itchy_eyes", "watery_eyes", "nasal_congestion"],
    "Bronchitis": ["cough", "chest_pain", "fatigue", "mild_fever", "shortness_of_breath", "sore_throat"],
    "Urinary Tract Infection": ["burning_urination", "frequent_urination", "abdominal_pain", "mild_fever", "fatigue"],
    "Chickenpox": ["skin_rash", "blister", "fever", "fatigue", "loss_of_appetite", "headache"],
    "Dengue Fever": ["high_fever", "joint_pain", "muscle_pain", "headache", "skin_rash", "fatigue", "nausea"],
    "Typhoid Fever": ["fever", "abdominal_pain", "headache", "loss_of_appetite", "fatigue", "diarrhea"],
    "Malaria": ["high_fever", "chills", "sweating", "headache", "nausea", "fatigue", "muscle_pain"],
    "Pneumonia": ["fever", "cough", "chest_pain", "shortness_of_breath", "fatigue", "chills"],
    "Tonsillitis": ["sore_throat", "fever", "headache", "fatigue", "loss_of_appetite"],
}

ROWS_PER_DISEASE = 40  # synthetic cases generated per disease
NOISE_CHANCE = 0.15  # chance an unrelated symptom is added (real-world noise)
DROPOUT_CHANCE = 0.20  # chance a typical symptom is missing in a given case


def generate_row(disease):
    """Generate a single synthetic patient row for the given disease."""
    row = {s: 0 for s in SYMPTOMS}
    typical = DISEASE_PATTERNS[disease]
    
    # Include typical symptoms with some dropout
    for symptom in typical:
        if random.random() > DROPOUT_CHANCE:
            row[symptom] = 1
    
    # Add some noise (random unrelated symptoms)
    for symptom in SYMPTOMS:
        if symptom not in typical and random.random() < NOISE_CHANCE:
            row[symptom] = 1
    
    row["prognosis"] = disease
    return row


def main():
    """Generate and save the dataset."""
    output_path = Path(__file__).resolve().parent / "dataset" / "disease_symptoms.csv"
    output_path.parent.mkdir(exist_ok=True)
    all_rows = []
    for disease in DISEASE_PATTERNS:
        for _ in range(ROWS_PER_DISEASE):
            all_rows.append(generate_row(disease))
    
    df = pd.DataFrame(all_rows)
    # Ensure column order: symptoms first, prognosis last
    df = df[SYMPTOMS + ["prognosis"]]
    
    df.to_csv(output_path, index=False)
    print(f"Dataset created: {len(df)} rows, {len(SYMPTOMS)} symptom columns, "
          f"{df['prognosis'].nunique()} disease classes.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()