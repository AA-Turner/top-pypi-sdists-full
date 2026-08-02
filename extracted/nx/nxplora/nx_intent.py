"""
nx_intent.py — conversation-vs-execution intent gate (0.15.110+).

A CLASS-BASED (LLM) intent classifier that runs IN FRONT of the 0.15.94 execution posture, so NX
can brainstorm / plan / ideate / just-talk WITHOUT force-routing to execution — while STILL
executing (business + coding) when the operator means it. Additive: nothing in .94 is removed.

WHY THIS CAN NEVER REGRESS .94 (the load-bearing safety property):
  - The gate can ONLY DEMOTE a turn to converse, and ONLY on a CONFIDENT think-intent
    (converse / brainstorm / plan / code_brainstorm / clarify).
  - On ANY uncertainty — an act-intent, low confidence, a missing key, an HTTP/parse error,
    an execution-shaped input — classify_intent() returns None, and the caller leaves .94's
    existing decision (is_agentic_code_task) UNCHANGED.
  - Ambiguity leans to ACTION: a swallowed "do it" (hedging) is the exact disease .94 cured;
    occasionally acting on a musing is cheap. The failure modes are asymmetric, so the tie
    goes to action. The bias is stated to the model AND enforced by the confidence floor.
  - .94 itself (is_agentic_code_task / _self_edit_instructions) is byte-for-byte untouched;
    this module only gates WHETHER it fires.

CLASS-BASED, NOT KEYWORD-BASED (enumeration loses): an LLM decides the intent from MEANING. The
genuinely-new part is the CODE-internal brainstorm-vs-execute split — "I'm thinking about how to
build the auth flow" (code_brainstorm, touch nothing) vs "build the auth flow" / "install and test
this repo" (code_execute, .94 fires). Both contain "build"/"auth flow", so a keyword matcher
cannot separate them; a meaning model can. That split is the reason this classifier exists.
"""
from __future__ import annotations

import json
from typing import Optional, Tuple, Callable, List, Dict

# THINK intents → converse (do NOT invoke .94). Anything else (business_op / code_execute) or any
# uncertainty → None → .94 decides, unchanged.
THINK_INTENTS = frozenset({"converse", "brainstorm", "plan", "code_brainstorm", "clarify"})
ACT_INTENTS = frozenset({"business_op", "code_execute"})
_ALL_INTENTS = THINK_INTENTS | ACT_INTENTS

# Only demote to converse at/above this confidence — below it, lean to action (.94 decides).
_CONFIDENCE_FLOOR = 0.7

_SYSTEM = (
    "You are NX's conversation-vs-execution intent classifier for a terminal AI agent. Read the "
    "user's message and decide from MEANING (never keywords) which ONE intent it is. Return ONLY "
    'JSON: {"intent": <converse|brainstorm|plan|business_op|code_execute|code_brainstorm|clarify>, '
    '"confidence": <0.0-1.0>}.\n'
    "Intents:\n"
    "- converse: casual talk, a question about NX/its status/itself, social. No action requested.\n"
    "- brainstorm: thinking out loud / ideating ('what if', 'I'm considering', weighing options). Explore an idea, do not enact it.\n"
    "- plan: shaping a plan/strategy/sequence and wants it drafted — but NOT asking to execute it this turn.\n"
    "- business_op: asking NX to EXECUTE a world/business action NOW (run the sequence, post, send, dispatch, book, generate the deliverable).\n"
    "- code_execute: asking NX to DO a coding task on the repo/machine NOW (build, install, test, run, edit, fix, refactor, deploy, clone).\n"
    "- code_brainstorm: reasoning ABOUT code WITHOUT commanding a change ('I'm thinking about the auth flow', 'how would you structure X?', 'tradeoffs between X and Y'). Touch nothing.\n"
    "- clarify: genuinely under-specified such that acting would be a guess.\n"
    "CRITICAL SPLIT: 'I'm thinking about how to build the auth flow' is code_brainstorm (a thought); "
    "'build the auth flow' / 'install and test this repo' is code_execute (a command). Decide from "
    "whether the user is COMMANDING a change/run vs REASONING about one.\n"
    "BIAS (important): when genuinely ambiguous, or the message is execution-shaped / a named "
    "command / an imperative on the repo, prefer the EXECUTE intent (business_op or code_execute). "
    "Better to act than to hedge."
)

Completion = Callable[[List[Dict[str, str]]], Optional[str]]


def _fireworks_completion(messages: List[Dict[str, str]], max_tokens: int = 60, timeout: int = 8) -> Optional[str]:
    """One cheap, non-streaming primary-provider call (mirrors nx_council's pattern). Returns the text, or
    None on ANY failure — no key, bad status, network/parse error. Fail-safe by construction."""
    try:
        import httpx
        from nx_key_pool import get_fireworks_key
        from nx_obfuscate import URLS, P, MR  # URLS/P/MR live in nx_obfuscate (as nx_council imports them)
        key = get_fireworks_key()
        if not key:
            return None
        base_url = URLS.get(P["fireworks"], "")
        if not base_url:
            return None
        model = MR.get("fast") or MR.get("small")
        if not model:
            return None
        r = httpx.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "max_tokens": max_tokens,
                  "temperature": 0.0, "stream": False},
            timeout=timeout,
        )
        if r.status_code != 200:
            return None
        return (r.json()["choices"][0]["message"]["content"] or "").strip()
    except Exception:
        return None


def _parse(text: Optional[str]) -> Tuple[Optional[str], float]:
    """Extract (intent, confidence) from the model's JSON. Tolerant of fences/prefixes. Any
    malformed output → (None, 0.0) so the caller falls through to .94."""
    if not text:
        return None, 0.0
    try:
        lo, hi = text.find("{"), text.rfind("}")
        blob = text[lo:hi + 1] if (lo != -1 and hi != -1 and hi > lo) else text
        obj = json.loads(blob)
        intent = str(obj.get("intent", "")).strip().lower()
        conf = float(obj.get("confidence", 0.0))
        if intent in _ALL_INTENTS:
            return intent, conf
    except Exception:
        pass
    return None, 0.0


def classify_intent(user: str, cfg=None, _completion: Optional[Completion] = None) -> Optional[str]:
    """Classify a message. Returns a THINK-intent label (to DEMOTE the turn to converse) ONLY when
    the LLM is confident it is one; returns None in every other case (act-intent, low confidence,
    no key, error) so the existing .94 decision stands unchanged.

    _completion is injectable for tests (a stub returning canned model text) — the default is the
    live primary-provider call. cfg is accepted for future context but not required."""
    del cfg
    text = (user or "").strip()
    if not text or text.startswith(("/", "$")):
        return None
    completion = _completion or _fireworks_completion
    out = completion([
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": text},
    ])
    intent, conf = _parse(out)
    if intent in THINK_INTENTS and conf >= _CONFIDENCE_FLOOR:
        return intent
    return None
