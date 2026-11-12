"""
symptom_parser.py
-----------------
NLP utility to extract symptoms from natural language text input.
Filters out common, generic, or unwanted symptoms.
"""

import re
from typing import List, Tuple

# Common/generic symptoms that appear in many diseases - use sparingly
COMMON_SYMPTOMS = {
    "fever",
    "fatigue",
    "headache",
    "nausea",
    "weakness",
    "tired",
    "tired",
    "chills",
    "sweating",
}

# Words to exclude (too generic or not medical symptoms)
UNWANTED_KEYWORDS = {
    "feel",
    "bad",
    "good",
    "sick",
    "well",
    "healthy",
    "ill",
    "fine",
    "okay",
    "alright",
    "sorry",
    "help",
    "please",
    "thanks",
    "medical",
    "doctor",
    "hospital",
    "medicine",
    "treatment",
    "diagnosis",
}


def extract_symptoms_from_text(text: str, feature_list: List[str]) -> Tuple[List[str], List[str]]:
    """
    Extract medical symptoms from natural language text.
    
    Args:
        text: Natural language description of symptoms (e.g., "I have a high fever and bad cough")
        feature_list: List of valid symptoms from the model
        
    Returns:
        Tuple of (extracted_symptoms, common_symptoms_found)
        - extracted_symptoms: List of symptoms found in text (excluding common ones)
        - common_symptoms_found: List of common symptoms found (if any)
    """
    if not text or not isinstance(text, str):
        return [], []
    
    # Expand aliases in text for better matching
    expanded_text = add_aliases_to_text(text)
    
    # Normalize text: lowercase, remove punctuation
    normalized = expanded_text.lower()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    words = set(normalized.split())
    
    extracted = []
    common_found = []
    
    # Create normalized feature map for fuzzy matching
    feature_map = {}
    for feature in feature_list:
        feature_norm = feature.replace("_", " ")
        feature_map[feature] = {
            "normalized": feature_norm,
            "words": set(feature.replace("_", " ").split()),
            "single_words": [w for w in feature.replace("_", " ").split() if len(w) > 1],
        }
    
    # Track what we've already found (to avoid duplicates)
    found_features = set()
    
    # Strategy 1: Exact phrase matching (most accurate)
    for feature, info in feature_map.items():
        if feature in found_features:
            continue
        # Check for exact matches with underscores
        if feature in normalized:
            found_features.add(feature)
            if feature in COMMON_SYMPTOMS:
                common_found.append(feature)
            else:
                extracted.append(feature)
            continue
        
        # Check for phrase match (e.g., "burning urination" matches "burning_urination")
        phrase = info["normalized"]
        if phrase in normalized:
            found_features.add(feature)
            if feature in COMMON_SYMPTOMS:
                common_found.append(feature)
            else:
                extracted.append(feature)
    
    # Strategy 2: Keyword matching (for partial mentions)
    for feature, info in feature_map.items():
        if feature in found_features:
            continue
        
        feature_words = info["single_words"]
        if len(feature_words) == 1:
            # Single-word symptoms: look for exact word match
            word = feature_words[0]
            if word in words and word not in UNWANTED_KEYWORDS:
                found_features.add(feature)
                if feature in COMMON_SYMPTOMS:
                    common_found.append(feature)
                else:
                    extracted.append(feature)
        else:
            # Multi-word symptoms require every component word unless an
            # explicit alias or the full phrase matched above.
            matching_words = sum(1 for w in feature_words if w in words)
            if matching_words == len(feature_words):
                found_features.add(feature)
                if feature in COMMON_SYMPTOMS:
                    common_found.append(feature)
                else:
                    extracted.append(feature)
    
    # Remove duplicates and sort
    extracted = sorted(list(set(extracted)))
    common_found = sorted(list(set(common_found)))
    
    return extracted, common_found


def parse_symptom_input(text: str, feature_list: List[str], include_common: bool = False) -> Tuple[List[str], dict]:
    """
    Parse user symptom input and return validated symptoms.
    
    Args:
        text: User input text describing symptoms
        feature_list: List of valid symptoms
        include_common: Whether to include common symptoms in results
        
    Returns:
        Tuple of (symptoms_list, metadata)
        - symptoms_list: List of extracted valid symptoms
        - metadata: Dict with extraction details and warnings
    """
    if not text or len(text.strip()) < 2:
        return [], {
            "success": False,
            "message": "Please enter at least 2 characters describing your symptoms.",
            "symptoms_found": 0,
            "common_symptoms": [],
        }
    
    extracted, common_found = extract_symptoms_from_text(text, feature_list)
    
    # Combine results based on include_common flag
    final_symptoms = extracted.copy()
    if include_common and common_found:
        final_symptoms.extend(common_found)
    
    final_symptoms = sorted(list(set(final_symptoms)))
    
    metadata = {
        "success": len(final_symptoms) > 0,
        "message": "",
        "symptoms_found": len(final_symptoms),
        "common_symptoms": common_found,
        "extracted_symptoms": extracted,
    }
    
    if not extracted and common_found:
        metadata["message"] = f"Found {len(common_found)} common symptom(s). Add them to improve predictions?"
    elif not final_symptoms:
        metadata["message"] = "No recognized symptoms found. Try describing symptoms more clearly."
    else:
        metadata["message"] = f"Found {len(extracted)} unique symptom(s)."
    
    return final_symptoms, metadata


# Example symptom variations for better matching
SYMPTOM_ALIASES = {
    "fever": ["temperature", "hot", "burning up", "feverish", "high temperature"],
    "high_fever": ["very high fever", "severe fever", "extremely hot", "very hot", "high temperature"],
    "mild_fever": ["low fever", "slight fever", "low temperature"],
    "headache": ["head pain", "head ache", "painful head", "throbbing head", "head hurts"],
    "cough": ["coughing", "coughed", "persistent cough", "bad cough"],
    "sore_throat": ["throat pain", "painful throat", "throat soreness", "throat hurts"],
    "fatigue": ["tired", "exhaustion", "exhausted", "very tired", "worn out", "weak"],
    "body_pain": ["body ache", "aches", "full body pain", "body aches", "muscle ache"],
    "diarrhea": ["loose stools", "loose motion", "loose bowels"],
    "vomiting": ["throwing up", "vomit", "nausea and vomiting"],
    "abdominal_pain": ["stomach pain", "tummy pain", "belly pain", "stomach ache"],
    "chest_pain": ["chest ache", "chest discomfort", "chest heaviness"],
    "shortness_of_breath": ["difficulty breathing", "trouble breathing", "can't breathe", "breathlessness"],
    "skin_rash": ["rash", "skin eruption", "bumps on skin", "red rash"],
    "itchy_eyes": ["eye itching", "itchy eye"],
    "watery_eyes": ["tears", "watery"],
    "loss_of_appetite": ["no appetite", "not hungry", "appetite loss"],
    "dizziness": ["dizzy", "lightheaded", "vertigo"],
    "muscle_pain": ["muscle ache", "sore muscles"],
    "joint_pain": ["joint ache", "achy joints"],
    "nausea": ["feeling sick", "sick to stomach", "queasy"],
    "chills": ["shivering", "shivery"],
    "sweating": ["perspiration", "night sweats"],
    "sneezing": ["sneezes", "sneezing a lot"],
    "nasal_congestion": ["stuffy nose", "blocked nose", "nasal blockage"],
    "runny_nose": ["nose running", "runny nose"],
    "burning_urination": ["painful urination", "urination pain", "burning when urinating"],
    "frequent_urination": ["frequent pee", "need to urinate often", "urinating frequently"],
    "blister": ["blisters", "painful blister"],
}



def add_aliases_to_text(text: str) -> str:
    """
    Expand symptom aliases in input text for better matching.
    E.g., "temperature" becomes "temperature fever"
    """
    expanded = text.lower()
    for symptom, aliases in SYMPTOM_ALIASES.items():
        for alias in aliases:
            if alias in expanded:
                expanded += f" {symptom}"
    return expanded
