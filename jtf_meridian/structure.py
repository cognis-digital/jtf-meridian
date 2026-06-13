"""
Canonical JTF MERIDIAN command structure.

JTF MERIDIAN is the internal command-and-control brand of Cognis Digital LLC: a
joint-task-force-style organization of the company's operating divisions. This
module is the single source of truth for that structure — command element,
divisions, sub-teams, callsigns, mandates, and the operating domains each owns.

It is *brand language* (see DISCLAIMER in the README): the designations confer no
government clearance or authority. JTF MERIDIAN is a decision-support / strategy
framework for a real Wyoming LLC, not a military operational system.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional

TOOL_NAME = "jtf-meridian"
TOOL_VERSION = "0.1.0"

MOTTO = "Omnia Video · Omnia Scio"        # "I see all · I know all"
TAGLINE = "Making Tomorrow Better Today"
COMMANDER = "ARCHON"                              # Christopher Hyatt, Founder/CEO
ENTITY = "Cognis Digital LLC"


@dataclass
class SubTeam:
    callsign: str
    name: str
    mandate: str


@dataclass
class Division:
    key: str                 # short routing key, e.g. "blackbook"
    name: str                # task-force name, e.g. "TF BLACKBOOK"
    callsign: str            # lead callsign, e.g. "ORACLE"
    domain: str              # primary operating domain
    mandate: str
    keywords: list = field(default_factory=list)   # routing hints
    subteams: list = field(default_factory=list)    # list[SubTeam]

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


COMMAND = {
    "name": "JTF MERIDIAN",
    "commander": COMMANDER,
    "principal": "Christopher Hyatt, Founder & CEO",
    "authority": "All cross-division authority; sets intent, allocates effort, "
                 "synthesizes the common operating picture.",
    "entity": ENTITY,
    "motto": MOTTO,
    "tagline": TAGLINE,
}


DIVISIONS: list[Division] = [
    Division(
        key="blackbook", name="TF BLACKBOOK", callsign="ORACLE",
        domain="Quant / Finance",
        mandate="Systematic trading, market intelligence, and capital strategy. "
                "Owns the autonomous trading stack and macro/crypto/insider signal work.",
        keywords=["trading", "market", "alpha", "quant", "finance", "crypto",
                  "macro", "portfolio", "hedge", "alpaca", "13f", "insider", "risk"],
        subteams=[
            SubTeam("ALPHA", "Alpha Desk", "HFT / intraday systematic trading (Alpaca)."),
            SubTeam("BRAVO", "Bravo Desk", "Macro regime, rates, cross-asset."),
            SubTeam("CHARLIE", "Charlie Desk", "Crypto / digital assets."),
            SubTeam("DELTA", "Delta Cell", "Congress / 13F / insider-flow tracking."),
        ],
    ),
    Division(
        key="nullbyte", name="GHOST CELL · NULLBYTE", callsign="SPECTER",
        domain="Cyber / Security",
        mandate="Offensive research (authorized), defensive engineering (NIST/CMMC), "
                "OSINT/FOIA, and vendor liaison. Owns the security-tooling suite.",
        keywords=["security", "cyber", "ctf", "pentest", "osint", "nist", "cmmc",
                  "vuln", "threat", "ioc", "soc", "blue", "red", "forensics", "malware"],
        subteams=[
            SubTeam("RED", "Red Cell", "Offensive research, CTF, authorized testing."),
            SubTeam("BLUE", "Blue Cell", "Defense, detection engineering, NIST/CMMC."),
            SubTeam("BLACK", "Black Cell", "OSINT, FOIA, open-source intelligence."),
            SubTeam("PURPLE", "Purple Cell", "Vendor liaison, purple-team exercises."),
        ],
    ),
    Division(
        key="athena", name="DIV-6 · ATHENA-PRIME", callsign="SAGE",
        domain="AI / R&D",
        mandate="Applied AI research and engineering: LLM systems, multi-agent "
                "orchestration, evaluation & safety, generative media, and research.",
        keywords=["ai", "ml", "llm", "model", "agent", "rag", "eval", "fleet",
                  "research", "embedding", "fine-tune", "inference", "prompt"],
        subteams=[
            SubTeam("COGNI-1", "Cogni-1", "LLM systems."),
            SubTeam("COGNI-2", "Cogni-2", "Multi-agent orchestration."),
            SubTeam("COGNI-3", "Cogni-3", "Evaluation & safety."),
            SubTeam("COGNI-4", "Cogni-4", "Generative media."),
            SubTeam("COGNI-5", "Cogni-5", "Research / horizon scanning."),
        ],
    ),
    Division(
        key="ironclad", name="TF IRONCLAD", callsign="ANVIL",
        domain="Government / Defense Contracting",
        mandate="Public-sector business development: SAM.gov, primes, FAR/DFARS/CMMC "
                "compliance, IC liaison, and research programs (SBIR/DARPA).",
        keywords=["government", "govcon", "sam.gov", "far", "dfars", "cmmc",
                  "sbir", "darpa", "contract", "prime", "compliance", "clearance",
                  "defense", "federal", "rfp", "proposal"],
        subteams=[
            SubTeam("FOXTROT", "Foxtrot", "SAM.gov opportunity capture."),
            SubTeam("GOLF", "Golf", "Prime contractor partnerships."),
            SubTeam("HOTEL", "Hotel", "FAR/DFARS/CMMC compliance."),
            SubTeam("INDIA", "India (IC)", "Intelligence-community business dev."),
            SubTeam("JULIET", "Juliet (DARPA)", "Research programs / SBIR / DARPA."),
        ],
    ),
    Division(
        key="prometheus", name="TF PROMETHEUS", callsign="FORGE",
        domain="Energy",
        mandate="Energy strategy and analysis across nuclear/SMR, oil & gas/LNG/H2, "
                "renewables, and grid/critical-infrastructure resilience.",
        keywords=["energy", "nuclear", "smr", "oil", "gas", "lng", "hydrogen",
                  "renewable", "solar", "wind", "grid", "power", "utility", "cisa"],
        subteams=[
            SubTeam("INDIA-N", "India (Nuclear)", "Nuclear / SMR."),
            SubTeam("JULIET-H", "Juliet (Hydrocarbon)", "Oil & gas / LNG / hydrogen."),
            SubTeam("KILO", "Kilo", "Renewables."),
            SubTeam("LIMA", "Lima", "Grid resilience / CISA / critical infrastructure."),
        ],
    ),
    Division(
        key="foundry", name="TF FOUNDRY", callsign="MASON",
        domain="Revenue / Client Services",
        mandate="The revenue engine. Public brand DevPairer Pro: fixed-price software "
                "delivery that funds every other division. 'Keep the lights on.'",
        keywords=["revenue", "client", "devpairer", "mvp", "saas", "ecommerce",
                  "delivery", "consulting", "build", "fixed-price", "cash", "billing"],
        subteams=[
            SubTeam("MASON", "DevPairer Pro", "Fixed-price MVP / SaaS / modernization delivery."),
        ],
    ),
]

_BY_KEY = {d.key: d for d in DIVISIONS}
_BY_CALLSIGN = {d.callsign.lower(): d for d in DIVISIONS}


def list_divisions() -> list[Division]:
    return list(DIVISIONS)


def get_division(key_or_callsign: str) -> Optional[Division]:
    k = (key_or_callsign or "").strip().lower()
    return _BY_KEY.get(k) or _BY_CALLSIGN.get(k)


def find_callsign(callsign: str) -> Optional[dict]:
    """Resolve a callsign to its division (and sub-team, if it is one)."""
    c = (callsign or "").strip().lower()
    d = _BY_CALLSIGN.get(c)
    if d:
        return {"division": d.name, "callsign": d.callsign, "level": "division"}
    for d in DIVISIONS:
        for st in d.subteams:
            if st.callsign.lower() == c:
                return {"division": d.name, "callsign": st.callsign,
                        "subteam": st.name, "level": "subteam", "mandate": st.mandate}
    return None


def roster() -> dict:
    """The full command roster as a serializable dict."""
    return {
        "command": COMMAND,
        "divisions": [d.to_dict() for d in DIVISIONS],
    }
