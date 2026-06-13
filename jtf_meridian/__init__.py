"""JTF MERIDIAN — the multi-domain command & think-tank framework of Cognis Digital LLC."""
from .structure import (
    TOOL_NAME, TOOL_VERSION, COMMAND, COMMANDER, ENTITY, MOTTO, TAGLINE,
    DIVISIONS, Division, SubTeam,
    list_divisions, get_division, find_callsign, roster,
)
from . import domains, fleet, thinktank

__all__ = [
    "TOOL_NAME", "TOOL_VERSION", "COMMAND", "COMMANDER", "ENTITY", "MOTTO",
    "TAGLINE", "DIVISIONS", "Division", "SubTeam",
    "list_divisions", "get_division", "find_callsign", "roster",
    "domains", "fleet", "thinktank",
]
