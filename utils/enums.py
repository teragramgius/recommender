# utils/enums.py

CHANNELS = [
    "academia-industry-joint-research-mobility",
    "promoting-research-driven-spin-offs-start-ups",
    "intermediaries-knowledge-transfer-professionals",
    "engagement-citizens-public-bodies-societal-actors",
    "intellectual-property-management-standardisation",
    "knowledge-circulation-informing-policy",
]

CHANNEL_LABEL = {
    "academia-industry-joint-research-mobility": "Academia-Industry joint research & mobility",
    "promoting-research-driven-spin-offs-start-ups": "Promoting research-driven spin-offs & start-ups",
    "intermediaries-knowledge-transfer-professionals": "Intermediaries & knowledge transfer professionals",
    "engagement-citizens-public-bodies-societal-actors": "Engagement of citizens, public bodies & societal actors",
    "intellectual-property-management-standardisation": "Intellectual Property management & standardisation",
    "knowledge-circulation-informing-policy": "Knowledge circulation & informing policy",
}

DIMENSIONS = ["environmental", "organisational", "individual"]
DIMENSION_LABEL = {
    "environmental": "Environmental",
    "organisational": "Organisational",
    "individual": "Individual",
}

CARD_TYPES = {"A": "assessment", "B": "challenge", "C": "scenario", "D": "objective", "E": "principle"}
PRINCIPLES = ["E1", "E2", "E3", "E4", "E5", "E6"]

PRIORITY_QUADRANTS = ["Strategic Quick Win", "Strategic Investment", "Policy Maintenance", "Avoid"]

EVIDENCE_TYPES = ["SAT Score", "Workshop Quote", "Policy Guideline Reference", "File"]

TIME_HORIZONS = ["<1y", "1-2y", "3-5y", ">5y"]
MODALITIES = ["in-person", "online", "hybrid"]

# Seed guidelines (you can rename/edit titles later)
GUIDELINES = {
    "PG01": "Guideline 01",
    "PG02": "Guideline 02",
    "PG03": "Guideline 03",
    "PG04": "Guideline 04",
    "PG05": "Guideline 05",
    "PG06": "Guideline 06",
    "PG07": "Guideline 07",
    "PG08": "Guideline 08",
    "PG09": "Guideline 09",
    "PG10": "Guideline 10",
}
