# JTF MERIDIAN

> The multi-domain command & think-tank framework of **Cognis Digital LLC** — a
> joint-task-force-style model of the company's operating divisions, wired to the
> local **uncensored fleet** for unrestricted strategic analysis, multi-domain
> assessment, analytic wargaming, and red-teaming.

[![Code License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-6b46c1.svg)](LICENSE)
[![tests](https://img.shields.io/badge/tests-14%20passing-2ea44f.svg)](tests/)

*Omnia Video · Omnia Scio* — "I see all · I know all"

---

## Usage — step by step

A full lifecycle with the `jtf` console command — every subcommand accepts
`--format table|json` and `--no-fleet` (force deterministic offline output):

1. **Install** the CLI (puts `jtf` on your PATH):

   ```sh
   pipx install "git+https://github.com/cognis-digital/jtf-meridian.git"
   ```

2. **Inspect the command structure** to see which division owns what. `structure` prints the ASCII org chart; `roster` / `divisions` / `domains` describe the divisions and the six analytic lenses; `callsign` resolves a single callsign:

   ```sh
   jtf structure
   jtf divisions
   jtf callsign MASON --format json
   ```

3. **Run a multi-domain assessment.** `brief` routes a topic to the owning division(s) and reads it across the six lenses. With a local fleet slot up it produces a live strategic read; offline it returns a deterministic scaffold:

   ```sh
   jtf brief "critical-minerals supply chain"
   ```

4. **Read / use the output.** Default `table` formatting prints a readable Markdown brief (division reads, lenses, command synthesis); `--format json` emits the structured assessment for piping into another tool or a test:

   ```sh
   jtf brief "critical-minerals supply chain" --format json | jq .routed_to
   ```

5. **Task a division, wargame, or red-team a plan**, then wire any of these into automation. Pass `--no-fleet` in CI so output is deterministic and needs no model server (commands exit non-zero only on errors, e.g. an unknown callsign):

   ```sh
   jtf task prometheus "the SMR investment thesis" --no-fleet
   jtf wargame "a competitor open-sources a rival suite" --no-fleet --format json
   jtf redteam "go all-in on a single enterprise client" --no-fleet
   ```

<!-- cognis:layman:start -->
## What is this?

JTF MERIDIAN is the "operations room" for a small, wide-ranging company. Cognis
Digital works across very different areas — systematic trading, cybersecurity,
AI research, government contracting, energy, and paid client software — and this
tool organizes all of that the way a joint task force organizes its divisions:
one commander, clear divisions, and a shared picture of what's going on.

In plain terms: you ask it a question or hand it a plan, and it figures out which
division owns the topic, analyzes it from that division's point of view and
across six "domain" lenses (physical, trade, tempo, position, cyber, and
information/narrative), and — when your local AI fleet is running — uses that
model to produce a real strategic read, a tabletop wargame of a scenario, or a
tough red-team critique of a plan. With the fleet off, it still gives you the
structured scaffolding to think it through yourself. It's a decision-support
think-tank, not an autopilot: it produces analysis and options, you decide.
<!-- cognis:layman:end -->

---

## Command structure

```
              JTF MERIDIAN — ARCHON (Christopher Hyatt, Founder & CEO)
                                   │
   ┌──────────┬──────────┬─────────┼─────────┬────────────┬──────────┐
 BLACKBOOK  NULLBYTE   ATHENA-PRIME IRONCLAD  PROMETHEUS   FOUNDRY
  ORACLE     SPECTER      SAGE       ANVIL      FORGE        MASON
  Quant      Cyber        AI/R&D     GovCon     Energy       Revenue
```

| Division | Callsign | Domain | Owns |
|---|---|---|---|
| **TF BLACKBOOK** | ORACLE | Quant / Finance | Systematic trading, market intel, capital strategy |
| **GHOST CELL · NULLBYTE** | SPECTER | Cyber / Security | Offensive research (authorized), defense, OSINT, the security-tool suite |
| **DIV-6 · ATHENA-PRIME** | SAGE | AI / R&D | LLM systems, multi-agent, eval & safety, gen-media, research |
| **TF IRONCLAD** | ANVIL | Government / Defense Contracting | SAM.gov, primes, FAR/DFARS/CMMC, SBIR/DARPA |
| **TF PROMETHEUS** | FORGE | Energy | Nuclear/SMR, oil & gas/LNG/H₂, renewables, grid resilience |
| **TF FOUNDRY** | MASON | Revenue / Client Services | DevPairer Pro — fixed-price delivery; funds every other division |

Each division has sub-teams with their own callsigns (Alpha/Bravo/Charlie/Delta
desks under BLACKBOOK; Red/Blue/Black/Purple cells under NULLBYTE; Cogni-1…5
under ATHENA-PRIME; and so on). Run `jtf roster` for the full chart.

## Multi-domain analytic lenses

Assessments are built across six lenses (used purely as *thinking tools* for
business strategy): **Physical/Land**, **Maritime/Trade**, **Air/Tempo**,
**Space/Position**, **Cyber/Digital**, and **Cognitive/Information**.

## Uncensored-fleet interop

The reasoning engine is the local Cognis fleet (OpenAI-compatible servers on
localhost). JTF MERIDIAN prefers the **uncensored 8B slot (`:8774`)** for
unrestricted strategic analysis, then falls back through the rest of the fleet
(`:8770`/`8775`/`8776`/`8772`/`8771`). No slot up? Every command degrades to a
deterministic offline scaffold, so the tool — and its test-suite — run anywhere.
Bring the fleet up with the `fleet` command, then re-run any analysis live.

## Usage

```sh
jtf structure                 # the command org chart
jtf roster --format json      # full roster
jtf divisions                 # divisions + mandates
jtf domains                   # the six analytic lenses
jtf callsign MASON            # resolve a callsign

jtf brief "critical-minerals supply chain"      # multi-domain assessment
jtf task prometheus "the SMR investment thesis"  # one division's read
jtf wargame "a competitor open-sources a rival suite"   # analytic tabletop (TTX)
jtf redteam "go all-in on a single enterprise client"   # adversarial critique

# add --no-fleet to force deterministic offline output (no model server)
```

```python
from jtf_meridian import thinktank
brief = thinktank.multidomain_brief("expand the security-tooling line")
print(brief.sections["command_synthesis"])
```

<!-- cognis:domains:start -->
## Domains

**Primary domain:** AI & ML  ·  **JTF MERIDIAN division:** ATHENA-PRIME · SAGE

**Topics:** `cognis` `ai` `llm` `machine-learning`

Part of the **Cognis Neural Suite** — 300+ source-available tools organized across 12 domains under the JTF MERIDIAN command structure. See the [suite on GitHub](https://github.com/cognis-digital) and [jtf-meridian](https://github.com/cognis-digital/jtf-meridian) for how the pieces fit together.
<!-- cognis:domains:end -->

<!-- cognis:install:start -->
## Install

`jtf-meridian` is source-available (not on PyPI) — install straight from GitHub.

**One-liner (Linux / macOS):**
```sh
curl -fsSL https://raw.githubusercontent.com/cognis-digital/jtf-meridian/HEAD/install.sh | sh
```
**One-liner (Windows PowerShell):**
```powershell
irm https://raw.githubusercontent.com/cognis-digital/jtf-meridian/HEAD/install.ps1 | iex
```
**Or any one of:**
```sh
pipx install "git+https://github.com/cognis-digital/jtf-meridian.git"   # isolated (recommended)
uv tool install "git+https://github.com/cognis-digital/jtf-meridian.git"
pip install "git+https://github.com/cognis-digital/jtf-meridian.git"
```
**From source:**
```sh
git clone https://github.com/cognis-digital/jtf-meridian.git
cd jtf-meridian && pip install .
```
Then: `jtf --help`
<!-- cognis:install:end -->

## Topics / Domains

`strategy` · `decision-support` · `multi-domain` · `think-tank` ·
`command-structure` · `osint` · `wargame` · `red-team` · `llm` · `local-fleet` ·
part of the **Cognis Neural Suite** (meta / command & control domain).

## Verification

```text
tests   : 14 passing (offline; deterministic fallbacks exercised)
runtime : pure Python standard library; no third-party deps
fleet   : optional — live analysis when a local slot is up, offline scaffold otherwise
```

## Disclaimer

JTF MERIDIAN is **internal brand language** for Cognis Digital LLC, a real
Wyoming limited liability company. "Joint task force," division callsigns, and
any classification-style designations are organizational branding — they confer
**no** government clearance, classification authority, or sovereign immunity.
This is a **decision-support and strategy-analysis** tool: it produces analysis,
options, and critiques for lawful business use. It is not an operational system
and contains no operational, targeting, or weapons capability. All use remains
subject to applicable law.

## Interoperability

`{}` composes with the 300+ tool Cognis suite — JSON in/out and a shared
OpenAI-compatible `/v1` backbone. See **[INTEROP.md](INTEROP.md)** for the
suite map, composition patterns, and reference stacks.

## License

Cognis Open Collaboration License (COCL) 1.0 — see [LICENSE](LICENSE).
