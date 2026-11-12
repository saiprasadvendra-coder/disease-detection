"""Condition information used by the educational prediction interface.

This content is general safety information, not a diagnosis or a substitute
for advice from a licensed clinician.
"""

DISCLAIMER = (
    "This tool provides educational information from a statistical model. "
    "It is not a medical diagnosis and cannot replace a qualified healthcare "
    "professional. Seek urgent care for severe or rapidly worsening symptoms."
)

OFFICIAL_RESOURCES = [
    {"name": "World Health Organization (WHO)", "url": "https://www.who.int/health-topics"},
    {"name": "Centers for Disease Control and Prevention (CDC)", "url": "https://www.cdc.gov/health-topics.html"},
]

CLINICIAN_RESOURCES = [
    {"name": "Find a clinician (Google Maps)", "url": "https://www.google.com/maps/search/doctor+near+me"},
    {"name": "Find a clinician (Bing Maps)", "url": "https://www.bing.com/maps?q=doctor+near+me"},
]

GENERAL_PRECAUTIONS = [
    "Rest, drink fluids, and monitor how your symptoms change.",
    "Do not start, stop, or share prescription medicines without medical advice.",
    "Arrange a clinician visit if symptoms persist, recur, or interfere with daily activities.",
]

CONDITION_INFO = {
    "Allergic Rhinitis": {
        "description": "An allergy-related inflammation of the nose and upper airways.",
        "common_symptoms": ["Sneezing", "Runny nose", "Nasal congestion", "Itchy or watery eyes"],
        "precautions": ["Avoid known triggers and reduce exposure to dust, smoke, and pollen."],
        "self_care": "Saline nasal rinses may help; ask a pharmacist or clinician about suitable allergy treatment.",
        "warning_signs": "Breathing difficulty, swelling of the lips or tongue, or fainting.",
        "seek_care": "Seek urgent care for severe breathing problems or a rapidly developing allergic reaction.",
    },
    "Bronchitis": {
        "description": "Inflammation of the bronchial tubes, often following a respiratory infection.",
        "common_symptoms": ["Cough", "Fatigue", "Chest discomfort", "Shortness of breath"],
        "precautions": ["Avoid smoking, vaping, and second-hand smoke."],
        "self_care": "Rest and fluids may help. A persistent or severe cough should be assessed by a clinician.",
        "warning_signs": "Blue lips, confusion, severe breathing difficulty, or chest pain.",
        "seek_care": "Get urgent help for severe breathing difficulty or chest pain.",
    },
    "COVID-19": {
        "description": "A viral respiratory illness. Symptoms can overlap with flu and other infections.",
        "common_symptoms": ["Fever", "Cough", "Fatigue", "Sore throat"],
        "precautions": ["Consider local testing and avoid close contact while acutely unwell."],
        "self_care": "Rest, fluids, and monitoring are useful; ask a clinician promptly if you are high risk.",
        "warning_signs": "Trouble breathing, persistent chest pressure, new confusion, or inability to stay awake.",
        "seek_care": "Seek emergency care for warning signs or rapidly worsening symptoms.",
    },
    "Chickenpox": {
        "description": "A contagious viral infection that commonly causes an itchy blistering rash.",
        "common_symptoms": ["Itchy rash", "Blisters", "Fever", "Fatigue"],
        "precautions": ["Avoid contact with pregnant people, newborns, and immunocompromised people until assessed."],
        "self_care": "Keep skin clean and avoid scratching; ask a clinician about safe itch relief.",
        "warning_signs": "Breathing difficulty, severe drowsiness, dehydration, or infected-looking skin lesions.",
        "seek_care": "Contact a clinician, especially for adults, pregnancy, infants, or weakened immunity.",
    },
    "Common Cold": {
        "description": "A usually mild viral infection of the upper respiratory tract.",
        "common_symptoms": ["Runny nose", "Sore throat", "Cough", "Sneezing"],
        "precautions": ["Wash hands and avoid close contact while symptomatic."],
        "self_care": "Rest, fluids, and simple symptom relief advised by a pharmacist may help.",
        "warning_signs": "Severe breathing difficulty, chest pain, confusion, or dehydration.",
        "seek_care": "Seek care if symptoms are severe, worsening, or not improving as expected.",
    },
    "Dengue Fever": {
        "description": "A mosquito-borne viral illness that can become serious.",
        "common_symptoms": ["High fever", "Headache", "Body pain", "Nausea"],
        "precautions": ["Use mosquito protection and obtain medical advice promptly for fever in an affected area."],
        "self_care": "Use only fever medicines recommended by a clinician; avoid self-medicating with aspirin.",
        "warning_signs": "Severe abdominal pain, repeated vomiting, bleeding, extreme weakness, or restlessness.",
        "seek_care": "Seek urgent medical care for warning signs or worsening fever.",
    },
    "Food Poisoning": {
        "description": "Gastrointestinal illness caused by contaminated food or drink.",
        "common_symptoms": ["Nausea", "Vomiting", "Diarrhea", "Abdominal pain"],
        "precautions": ["Use safe food preparation and frequent handwashing to reduce spread."],
        "self_care": "Replace fluids and electrolytes; avoid food or drinks that worsen symptoms.",
        "warning_signs": "Blood in stool or vomit, severe dehydration, fainting, or severe abdominal pain.",
        "seek_care": "Get prompt care for dehydration, blood, severe pain, or symptoms in a vulnerable person.",
    },
    "Gastroenteritis": {
        "description": "Inflammation of the stomach and intestines, commonly due to infection.",
        "common_symptoms": ["Diarrhea", "Vomiting", "Nausea", "Abdominal pain"],
        "precautions": ["Wash hands carefully and avoid preparing food for others while ill."],
        "self_care": "Take frequent small sips of oral rehydration fluid and rest.",
        "warning_signs": "Very little urine, dizziness, blood, severe pain, or inability to keep fluids down.",
        "seek_care": "Seek medical care if dehydration or severe symptoms develop.",
    },
    "Influenza (Flu)": {
        "description": "A contagious viral respiratory infection that can cause abrupt systemic symptoms.",
        "common_symptoms": ["Fever", "Cough", "Body pain", "Fatigue"],
        "precautions": ["Stay home while feverish and follow local infection-control guidance."],
        "self_care": "Rest and fluids may help; high-risk people should contact a clinician early.",
        "warning_signs": "Breathing difficulty, chest pain, confusion, severe weakness, or dehydration.",
        "seek_care": "Seek urgent care for warning signs or if symptoms rapidly worsen.",
    },
    "Malaria": {
        "description": "A mosquito-borne infection that requires prompt testing and treatment.",
        "common_symptoms": ["Fever", "Chills", "Sweating", "Headache"],
        "precautions": ["Seek prompt testing after fever or chills following travel or residence in a risk area."],
        "self_care": "Do not delay testing or use leftover medicines.",
        "warning_signs": "Confusion, seizures, breathing difficulty, jaundice, or extreme weakness.",
        "seek_care": "Treat suspected malaria as urgent, especially after travel to a malaria-risk area.",
    },
    "Migraine": {
        "description": "A neurological headache disorder that may include nausea and sensitivity to light or sound.",
        "common_symptoms": ["Headache", "Nausea", "Dizziness"],
        "precautions": ["Note triggers such as missed meals, dehydration, poor sleep, or bright light."],
        "self_care": "Rest in a quiet, dark room and use only medicines suitable for you as advised by a clinician.",
        "warning_signs": "Sudden worst-ever headache, weakness, confusion, fever with stiff neck, or vision loss.",
        "seek_care": "Seek emergency care for a sudden severe or neurologic headache.",
    },
    "Pneumonia": {
        "description": "An infection of the lungs that may require medical assessment and treatment.",
        "common_symptoms": ["Cough", "Fever", "Chest pain", "Shortness of breath"],
        "precautions": ["Arrange clinical assessment rather than relying on this screening result."],
        "self_care": "Rest and fluids while arranging medical advice; do not use leftover antibiotics.",
        "warning_signs": "Severe breathing difficulty, blue lips, confusion, or persistent chest pain.",
        "seek_care": "Seek urgent medical care for breathing difficulty or significant deterioration.",
    },
    "Tonsillitis": {
        "description": "Inflammation of the tonsils caused by a viral or bacterial infection.",
        "common_symptoms": ["Sore throat", "Fever", "Painful swallowing"],
        "precautions": ["Avoid sharing utensils and seek testing when bacterial infection is possible."],
        "self_care": "Drink fluids and use clinician-approved throat symptom relief.",
        "warning_signs": "Drooling, inability to swallow fluids, muffled voice, or breathing difficulty.",
        "seek_care": "Seek urgent care for airway or swallowing problems.",
    },
    "Typhoid Fever": {
        "description": "A bacterial infection that requires medical testing and prescription treatment.",
        "common_symptoms": ["Fever", "Headache", "Abdominal pain", "Fatigue"],
        "precautions": ["Use safe water and food practices and seek medical testing promptly."],
        "self_care": "Do not self-treat with leftover antibiotics; maintain hydration while seeking care.",
        "warning_signs": "Confusion, severe abdominal pain, persistent vomiting, bleeding, or dehydration.",
        "seek_care": "Arrange prompt medical assessment for persistent fever or travel-related illness.",
    },
    "Urinary Tract Infection": {
        "description": "An infection affecting the urinary tract that may require prescription treatment.",
        "common_symptoms": ["Burning urination", "Frequent urination", "Lower abdominal discomfort"],
        "precautions": ["Seek testing rather than using leftover antibiotics."],
        "self_care": "Drink fluids if normally safe for you and arrange a urine assessment.",
        "warning_signs": "Fever with back or side pain, vomiting, confusion, or pregnancy.",
        "seek_care": "Seek prompt care for fever, flank pain, pregnancy, or worsening symptoms.",
    },
}


def get_condition_info(condition: str) -> dict:
    """Return condition-specific guidance with safe fallback text."""
    info = CONDITION_INFO.get(condition)
    if info is None:
        return {
            "description": "The model found a possible match, but condition-specific information is unavailable.",
            "common_symptoms": [],
            "precautions": GENERAL_PRECAUTIONS,
            "self_care": "Arrange an assessment with a qualified healthcare professional.",
            "warning_signs": "Severe breathing difficulty, chest pain, confusion, fainting, or rapid worsening.",
            "seek_care": "Seek urgent care for warning signs.",
            "official_resources": OFFICIAL_RESOURCES,
            "clinician_resources": CLINICIAN_RESOURCES,
        }
    return {
        **info,
        "precautions": [*info["precautions"], *GENERAL_PRECAUTIONS],
        "official_resources": OFFICIAL_RESOURCES,
        "clinician_resources": CLINICIAN_RESOURCES,
    }
