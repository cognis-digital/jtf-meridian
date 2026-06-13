"""jtf — command-line access to the JTF MERIDIAN think-tank.

Subcommands:
  structure          show the command structure (ASCII org chart)
  roster             full roster as JSON
  divisions          list divisions + mandates
  domains            list the multi-domain analytic lenses
  callsign <C>       resolve a callsign
  brief <topic>      multi-domain assessment (fleet-backed; offline fallback)
  task <div> <txt>   ask one division to analyze something
  wargame <txt>      analytic tabletop (TTX) of a scenario
  redteam <txt>      adversarial critique of a plan

--format table|json   ·   --no-fleet  (force offline, deterministic output)
"""
from __future__ import annotations
import argparse
import json
import sys

from . import structure, domains, thinktank
from .structure import TOOL_NAME, TOOL_VERSION


def _slots(args):
    # --no-fleet => point at an unused slot list so fleet.chat returns None fast
    return [] if getattr(args, "no_fleet", False) else None


def _print(obj, fmt):
    if fmt == "json":
        print(json.dumps(obj, indent=2, default=str))
    else:
        print(obj if isinstance(obj, str) else json.dumps(obj, indent=2, default=str))


def cmd_structure(args):
    c = structure.COMMAND
    lines = [
        f"  {c['name']} — {c['commander']} ({c['principal']})",
        f"  {c['entity']}   ·   {c['motto']}",
        "",
        "  COMMAND",
        "     │",
    ]
    for d in structure.DIVISIONS:
        lines.append(f"     ├─ {d.name}  [{d.callsign}]  — {d.domain}")
        for st in d.subteams:
            lines.append(f"     │     · {st.callsign}: {st.name}")
    print("\n".join(lines))
    return 0


def cmd_roster(args):
    _print(structure.roster(), "json")
    return 0


def cmd_divisions(args):
    if args.format == "json":
        _print([d.to_dict() for d in structure.DIVISIONS], "json"); return 0
    for d in structure.DIVISIONS:
        print(f"{d.callsign:9} {d.name:22} {d.domain}")
        print(f"          {d.mandate}")
    return 0


def cmd_domains(args):
    if args.format == "json":
        _print(domains.multidomain_axes(), "json"); return 0
    for l in domains.LENSES:
        print(f"{l['name']:22} {l['focus']}")
    return 0


def cmd_callsign(args):
    r = structure.find_callsign(args.callsign)
    _print(r or {"error": f"unknown callsign '{args.callsign}'"}, args.format)
    return 0 if r else 1


def cmd_brief(args):
    a = thinktank.multidomain_brief(args.topic, slots=_slots(args))
    if args.format == "json":
        _print(a.to_dict(), "json"); return 0
    print(f"# Multi-domain brief — {a.topic}")
    print(f"(fleet: {'live' if a.fleet_used else 'offline'} · routed: "
          f"{', '.join(a.routed_to)})\n")
    for name, txt in a.sections.get("division_reads", {}).items():
        print(f"## {name}\n{txt}\n")
    md = a.sections.get("multidomain")
    print("## Multi-domain lenses")
    print(md if isinstance(md, str) else json.dumps(md, indent=2))
    print(f"\n## Command synthesis\n{a.sections.get('command_synthesis','')}")
    return 0


def cmd_task(args):
    r = thinktank.task_division(args.division, " ".join(args.text), slots=_slots(args))
    if args.format == "json":
        _print(r, "json"); return 0
    if "error" in r:
        print(r["error"]); return 1
    print(f"# {r['callsign']} · {r['division']} ({r['domain']})  "
          f"[fleet: {'live' if r['fleet_used'] else 'offline'}]\n{r['analysis']}")
    return 0


def cmd_wargame(args):
    r = thinktank.wargame(" ".join(args.text), slots=_slots(args))
    _print(r if args.format == "json" else r["ttx"], args.format)
    return 0


def cmd_redteam(args):
    r = thinktank.redteam(" ".join(args.text), slots=_slots(args))
    _print(r if args.format == "json" else r["critique"], args.format)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog=TOOL_NAME, description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"{TOOL_NAME} {TOOL_VERSION}")
    sub = p.add_subparsers(dest="command")

    def add(name, fn, help):
        sp = sub.add_parser(name, help=help)
        sp.add_argument("--format", choices=["table", "json"], default="table")
        sp.add_argument("--no-fleet", action="store_true",
                        help="force offline deterministic output (no model server)")
        sp.set_defaults(func=fn)
        return sp

    add("structure", cmd_structure, "show the command structure")
    add("roster", cmd_roster, "full roster as JSON")
    add("divisions", cmd_divisions, "list divisions + mandates")
    add("domains", cmd_domains, "list multi-domain analytic lenses")
    sp = add("callsign", cmd_callsign, "resolve a callsign"); sp.add_argument("callsign")
    sp = add("brief", cmd_brief, "multi-domain assessment of a topic"); sp.add_argument("topic")
    sp = add("task", cmd_task, "ask one division to analyze"); sp.add_argument("division"); sp.add_argument("text", nargs="+")
    sp = add("wargame", cmd_wargame, "analytic tabletop (TTX)"); sp.add_argument("text", nargs="+")
    sp = add("redteam", cmd_redteam, "adversarial critique of a plan"); sp.add_argument("text", nargs="+")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not getattr(args, "command", None):
        build_parser().print_help(); return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
