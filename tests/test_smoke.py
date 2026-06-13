"""Offline tests for jtf-meridian. No network/model server required.

The think-tank functions are forced offline (slots=[]) so they exercise the
deterministic fallback paths and the routing/structure logic.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jtf_meridian import (  # noqa: E402
    TOOL_NAME, TOOL_VERSION, DIVISIONS, list_divisions, get_division,
    find_callsign, roster, domains, thinktank,
)
from jtf_meridian.cli import main  # noqa: E402

OFF = {"slots": []}  # force offline


def test_metadata():
    assert TOOL_NAME == "jtf-meridian"
    assert TOOL_VERSION.count(".") == 2


def test_seven_divisions():
    assert len(DIVISIONS) == 6  # 6 task forces under COMMAND (command is separate)
    keys = {d.key for d in DIVISIONS}
    assert {"blackbook", "nullbyte", "athena", "ironclad", "prometheus", "foundry"} <= keys


def test_get_division_by_key_and_callsign():
    assert get_division("blackbook").callsign == "ORACLE"
    assert get_division("ORACLE").key == "blackbook"
    assert get_division("nope") is None


def test_find_callsign_division_and_subteam():
    d = find_callsign("SAGE")
    assert d and d["level"] == "division" and "ATHENA" in d["division"]
    st = find_callsign("ALPHA")
    assert st and st["level"] == "subteam" and st["subteam"] == "Alpha Desk"
    assert find_callsign("ZULU") is None


def test_roster_serializable():
    r = roster()
    json.dumps(r)  # must not raise
    assert r["command"]["commander"] == "ARCHON"
    assert len(r["divisions"]) == 6


def test_routing_keywords():
    # trading -> blackbook
    assert any(d.key == "blackbook" for d in thinktank.route("build an alpha trading signal"))
    # cmmc/security -> nullbyte or ironclad (both legit); nullbyte must be present
    assert any(d.key in ("nullbyte", "ironclad") for d in thinktank.route("CMMC compliance audit"))
    # llm/agent -> athena
    assert any(d.key == "athena" for d in thinktank.route("multi-agent LLM eval harness"))
    # unmatched -> all divisions (command-wide)
    assert len(thinktank.route("xyzzy nothing matches")) == len(DIVISIONS)


def test_domains_six_lenses():
    ax = domains.multidomain_axes()
    assert len(ax) == 6
    assert {l["key"] for l in ax} == {"physical", "maritime", "air", "space",
                                      "cyber", "cognitive"}
    assert domains.get_lens("cyber")["name"].startswith("Cyber")


def test_task_division_offline():
    r = thinktank.task_division("foundry", "should we raise prices?", **OFF)
    assert r["fleet_used"] is False
    assert "MASON" in r["analysis"] or "FOUNDRY" in r["analysis"].upper()
    assert "error" not in r


def test_task_unknown_division():
    r = thinktank.task_division("nope", "x", **OFF)
    assert "error" in r


def test_multidomain_brief_offline():
    a = thinktank.multidomain_brief("expand the security tooling line", **OFF)
    assert a.fleet_used is False
    assert a.routed_to
    assert "division_reads" in a.sections
    assert "multidomain" in a.sections
    assert "command_synthesis" in a.sections
    json.dumps(a.to_dict())


def test_wargame_and_redteam_offline():
    w = thinktank.wargame("a competitor open-sources a rival suite", **OFF)
    assert w["fleet_used"] is False and "TTX" in w["ttx"].upper()
    rt = thinktank.redteam("ship 300 repos in a week", **OFF)
    assert rt["fleet_used"] is False and "red-team" in rt["critique"].lower()


def test_cli_structure_and_divisions():
    assert main(["structure"]) == 0
    assert main(["divisions", "--format", "json"]) == 0
    assert main(["domains"]) == 0
    assert main(["roster"]) == 0


def test_cli_brief_offline():
    assert main(["brief", "critical minerals supply chain", "--no-fleet"]) == 0
    assert main(["task", "prometheus", "SMR thesis", "--no-fleet"]) == 0
    assert main(["wargame", "grid attack scenario", "--no-fleet"]) == 0
    assert main(["redteam", "all-in on one client", "--no-fleet"]) == 0


def test_cli_callsign():
    assert main(["callsign", "MASON", "--format", "json"]) == 0
    assert main(["callsign", "ZULU"]) == 1
