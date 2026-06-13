"""
The JTF MERIDIAN think-tank engine.

A multi-domain, decision-support layer over the company's command structure. It
routes a question to the division(s) that own it, asks each to assess from its
mandate, builds a structured multi-domain brief, and supports analytic wargaming
(tabletop scenario exploration) and red-teaming (adversarial critique of a plan).

Every analytic function is backed by the uncensored fleet when it is reachable,
and degrades to a deterministic offline template otherwise — so results are
always produced and the test-suite runs without a model server.

Scope: strategy, analysis, and decision-support for a real LLC. This is a
think-tank, not an operational system; it produces *analysis and options*, not
actions.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict

from . import fleet, structure, domains


@dataclass
class Assessment:
    topic: str
    fleet_used: bool
    routed_to: list = field(default_factory=list)
    sections: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def route(topic: str) -> list[structure.Division]:
    """Pick the division(s) whose keywords best match the topic. Always returns
    at least one (falls back to command-wide if nothing matches)."""
    t = (topic or "").lower()
    scored = []
    for d in structure.DIVISIONS:
        score = sum(1 for kw in d.keywords if kw in t)
        if score:
            scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        # no keyword hit -> route to command (all divisions weigh in lightly)
        return structure.list_divisions()
    top = scored[0][0]
    return [d for s, d in scored if s >= max(1, top - 1)]


def _div_system(d: structure.Division) -> str:
    return (f"You are {d.callsign}, lead of {d.name} ({d.domain}) within "
            f"{structure.COMMAND['name']}, the command structure of "
            f"{structure.ENTITY}. Mandate: {d.mandate} Give sharp, honest, "
            f"decision-useful analysis from your division's perspective. Be "
            f"concrete and brief. This is business strategy analysis.")


def task_division(division: str, prompt: str, slots=None) -> dict:
    """Ask one division to analyze a prompt from its mandate."""
    d = structure.get_division(division)
    if not d:
        return {"error": f"unknown division '{division}'",
                "known": [x.key for x in structure.DIVISIONS]}
    out = fleet.chat(
        [{"role": "system", "content": _div_system(d)},
         {"role": "user", "content": prompt}], slots=slots)
    used = out is not None
    if not used:
        out = (f"[offline] {d.callsign} / {d.name} would assess this against its "
               f"mandate ({d.domain}): {d.mandate}\nKey angles: "
               + "; ".join(st.name for st in d.subteams) + ".")
    return {"division": d.name, "callsign": d.callsign, "domain": d.domain,
            "fleet_used": used, "analysis": out}


def multidomain_brief(topic: str, slots=None) -> Assessment:
    """A structured assessment of `topic` across all six analytic lenses, plus a
    routed division read and a command-level synthesis."""
    routed = route(topic)
    a = Assessment(topic=topic, fleet_used=False,
                   routed_to=[d.name for d in routed])

    # division reads
    div_reads = {}
    for d in routed[:3]:
        r = task_division(d.key, f"Assess this for {structure.ENTITY}: {topic}",
                          slots=slots)
        div_reads[d.name] = r["analysis"]
        a.fleet_used = a.fleet_used or r["fleet_used"]
    a.sections["division_reads"] = div_reads

    # multi-domain lens read
    lens_qs = "\n".join(
        f"- {l['name']}: {' '.join(l['questions'])}" for l in domains.LENSES)
    sys = (f"You are the J5 (plans) analyst for {structure.COMMAND['name']}. "
           f"Assess the topic across these multi-domain analytic lenses, one short "
           f"paragraph each. These are analysis lenses for business strategy.")
    out = fleet.chat(
        [{"role": "system", "content": sys},
         {"role": "user", "content": f"Topic: {topic}\n\nLenses:\n{lens_qs}"}],
        slots=slots)
    if out is not None:
        a.fleet_used = True
        a.sections["multidomain"] = out
    else:
        a.sections["multidomain"] = {
            l["name"]: {"focus": l["focus"], "questions": l["questions"]}
            for l in domains.LENSES}

    # command synthesis
    if a.fleet_used:
        syn = fleet.chat(
            [{"role": "system", "content":
              f"You are {structure.COMMANDER}, commander of "
              f"{structure.COMMAND['name']}. Synthesize the division and "
              f"multi-domain reads into a commander's intent: 3-5 bullets of "
              f"what matters, the main risk, and the recommended next move."},
             {"role": "user", "content":
              f"Topic: {topic}\nDivision reads: {div_reads}\n"
              f"Multi-domain: {a.sections['multidomain']}"}],
            slots=slots)
        a.sections["command_synthesis"] = syn or "(synthesis unavailable)"
    else:
        a.sections["command_synthesis"] = (
            f"[offline] Routed to {', '.join(a.routed_to)}. Bring the fleet up "
            f"(uncensored slot :8774) for a live commander's synthesis.")
    return a


def wargame(scenario: str, slots=None) -> dict:
    """Analytic tabletop (TTX) exploration of a scenario: assumptions, two or
    three courses of action with pros/cons, key risks, and indicators to watch.
    This is decision-support analysis, not an operational plan."""
    sys = (f"You are the wargame facilitator for {structure.COMMAND['name']}. "
           f"Run a TABLETOP analysis (TTX) of the scenario for {structure.ENTITY}. "
           f"Output: (1) stated assumptions, (2) 2-3 distinct courses of action "
           f"with pros/cons, (3) the top risks, (4) indicators & warnings to "
           f"watch. This is analytic decision-support, not an operational order.")
    out = fleet.chat([{"role": "system", "content": sys},
                      {"role": "user", "content": scenario}], slots=slots)
    used = out is not None
    if not used:
        out = ("[offline] TTX skeleton:\n"
               "- Assumptions: list what must be true.\n"
               "- COA-1 / COA-2 / COA-3: sketch distinct options + pros/cons.\n"
               "- Risks: what breaks each COA.\n"
               "- Indicators & warnings: what to watch for.\n"
               "Bring up the fleet (:8774) for a live facilitated wargame.")
    return {"scenario": scenario, "fleet_used": used, "ttx": out}


def redteam(plan: str, slots=None) -> dict:
    """Adversarial critique of a plan/strategy: assumptions that could be wrong,
    failure modes, second-order effects, and how a smart opponent would counter it."""
    sys = (f"You are the RED CELL of {structure.COMMAND['name']}. Adversarially "
           f"critique the plan: challenge its assumptions, find failure modes and "
           f"second-order effects, and describe how a capable competitor would "
           f"counter it. Be tough and specific; the goal is to strengthen the plan.")
    out = fleet.chat([{"role": "system", "content": sys},
                      {"role": "user", "content": plan}], slots=slots)
    used = out is not None
    if not used:
        out = ("[offline] Red-team checklist: (1) which assumptions are load-"
               "bearing and unproven? (2) what is the most likely failure mode? "
               "(3) second-order effects? (4) how would a sharp competitor "
               "counter this? Bring up the fleet (:8774) for a live red-team.")
    return {"plan": plan, "fleet_used": used, "critique": out}
