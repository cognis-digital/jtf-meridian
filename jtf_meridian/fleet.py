"""
Uncensored-fleet client — JTF MERIDIAN's reasoning engine.

Talks to the local Cognis fleet (OpenAI-compatible /v1/chat/completions servers
running on localhost). Prefers the uncensored 8B slot for unrestricted strategic
analysis and red-teaming, then falls back through the rest of the fleet. If no
slot is reachable, callers degrade gracefully to offline templated output, so the
tool and its tests run with or without the fleet up.

This is the same wiring pattern used across the Cognis stack (cog4 / Mission
Control / the LinkedIn engine): POST with `/no_think`, strip any `<think>` block.
"""
from __future__ import annotations
import json
import re
import urllib.request
import urllib.error

# slot preference: uncensored 8B first (unrestricted analysis), then the rest.
DEFAULT_SLOTS = [8774, 8770, 8775, 8776, 8772, 8771]
_THINK = re.compile(r"<think>.*?</think>", re.S | re.I)


def _health(port: int, timeout: float = 1.5) -> bool:
    for path in ("/health", "/v1/models"):
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status == 200:
                    return True
        except Exception:
            continue
    return False


def first_live_slot(slots=None) -> int | None:
    # slots is None  -> use the default fleet; slots == []  -> explicitly offline.
    candidates = DEFAULT_SLOTS if slots is None else slots
    for p in candidates:
        if _health(p):
            return p
    return None


def chat(messages, slots=None, port=None, temperature=0.6, max_tokens=1400,
         timeout=120) -> str | None:
    """One chat completion against the first live fleet slot.

    Returns the assistant text (with any <think> block stripped), or None if no
    slot is reachable / the call fails — callers then use an offline fallback.
    """
    p = port or first_live_slot(slots)
    if not p:
        return None
    # nudge reasoning models to skip the visible scratchpad
    msgs = list(messages)
    if msgs and msgs[0].get("role") == "system":
        msgs[0] = {**msgs[0], "content": msgs[0]["content"] + " /no_think"}
    else:
        msgs = [{"role": "system", "content": "/no_think"}] + msgs
    payload = json.dumps({
        "messages": msgs, "temperature": temperature,
        "max_tokens": max_tokens, "stream": False,
    }).encode()
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{p}/v1/chat/completions", data=payload,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
        text = data["choices"][0]["message"]["content"]
        return _THINK.sub("", text).strip()
    except Exception:
        return None


def available(slots=None) -> bool:
    return first_live_slot(slots) is not None
