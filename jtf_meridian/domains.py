"""
Multi-domain framework.

JTF MERIDIAN reasons across two complementary axes:

1. BUSINESS DOMAINS — the operating areas the company actually works in, each
   owned by a division (Quant, Cyber, AI/R&D, GovCon, Energy, Revenue).

2. ANALYTIC LENSES — the classic multi-domain operating environment used here
   purely as *analysis lenses* for structured assessment (land/physical,
   maritime, air, space, cyber, and the cognitive/information domain). These are
   thinking tools for a strategy think-tank, not operational/targeting constructs.

`multidomain_axes()` returns the lenses; `lens_questions()` returns the standing
questions each lens asks of any topic, which the think-tank engine uses to build
a structured brief.
"""
from __future__ import annotations

# Analytic lenses (the multi-domain operating environment, used for assessment).
LENSES = [
    {
        "key": "physical",
        "name": "Physical / Land",
        "focus": "On-the-ground assets, people, facilities, logistics, supply chain.",
        "questions": [
            "What physical assets, people, or supply chains does this touch?",
            "Where are the single points of failure?",
        ],
    },
    {
        "key": "maritime",
        "name": "Maritime / Trade",
        "focus": "Shipping lanes, trade flows, chokepoints, commodity movement.",
        "questions": [
            "Which trade flows or chokepoints are relevant?",
            "What logistics or commodity exposure exists?",
        ],
    },
    {
        "key": "air",
        "name": "Air / Tempo",
        "focus": "Speed, reach, and tempo — how fast advantage can be projected.",
        "questions": [
            "How time-sensitive is this? What is the tempo of decision?",
            "Where does speed create or erode advantage?",
        ],
    },
    {
        "key": "space",
        "name": "Space / Position",
        "focus": "Positioning, comms, sensing, GPS/timing, high-ground analogues.",
        "questions": [
            "What positioning, sensing, or communications dependencies exist?",
            "Who holds the 'high ground' (data, distribution, platform)?",
        ],
    },
    {
        "key": "cyber",
        "name": "Cyber / Digital",
        "focus": "Software, data, infrastructure, attack surface, resilience.",
        "questions": [
            "What is the attack surface and the resilience posture?",
            "What data or systems are decisive, and how are they protected?",
        ],
    },
    {
        "key": "cognitive",
        "name": "Cognitive / Information",
        "focus": "Narrative, perception, influence, decision-making, morale.",
        "questions": [
            "What is the narrative and who shapes perception?",
            "Where are the cognitive biases and decision traps?",
        ],
    },
]

_BY_KEY = {l["key"]: l for l in LENSES}


def multidomain_axes() -> list[dict]:
    return list(LENSES)


def get_lens(key: str):
    return _BY_KEY.get((key or "").strip().lower())


def lens_questions() -> dict:
    return {l["key"]: l["questions"] for l in LENSES}
