"""
test_nx_intent.py — the conversation-vs-execution intent gate proves BOTH directions.

The live model judgment (real meaning classification) runs in the operator's Codespace; here we prove
the GATE LOGIC deterministically with a stub completion — including the load-bearing safety property:
the gate can ONLY demote to converse on a CONFIDENT think-intent, and falls through to .94 (returns
None) on an act-intent, low confidence, no key, or a malformed reply. Ambiguity leans to action.

run: python -m pytest test_nx_intent.py -q   (or: python test_nx_intent.py)
"""
import json
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))  # nx/cli
import nx_intent
from nx_intent import classify_intent, THINK_INTENTS, ACT_INTENTS


def _stub(intent, conf):
    """A completion that returns the model's JSON verbatim (what Fireworks would return)."""
    payload = json.dumps({"intent": intent, "confidence": conf})
    return lambda messages: payload


def test_think_intents_demote_to_converse():
    # (i) THE NEW CAPABILITY: reasoning about code → converse (touch nothing).
    assert classify_intent("I'm thinking about how to structure the auth flow",
                           _completion=_stub("code_brainstorm", 0.92)) == "code_brainstorm"
    # (iii) business thinking → brainstorm (does not open/execute a world).
    assert classify_intent("what channels should we use for outbound",
                           _completion=_stub("brainstorm", 0.88)) == "brainstorm"
    # a forming plan → plan (so the brain-write can fire).
    assert classify_intent("let's shape the Q4 go-to-market plan",
                           _completion=_stub("plan", 0.9)) == "plan"


def test_act_intents_fall_through_to_94():
    # (ii) THE REGRESSION GUARD: an execute command → None → .94 fires UNCHANGED. No hedging.
    assert classify_intent("install and test this repo",
                           _completion=_stub("code_execute", 0.96)) is None
    # (iv) a real business op → None → executes.
    assert classify_intent("run the sales sequence for these 3 leads",
                           _completion=_stub("business_op", 0.9)) is None


def test_ambiguity_leans_to_action():
    # A think-intent BELOW the confidence floor must NOT demote — the tie goes to action (.94).
    assert classify_intent("build the auth flow",
                           _completion=_stub("code_brainstorm", 0.55)) is None
    # Exactly at the floor demotes; just under does not.
    assert classify_intent("thinking about the design", _completion=_stub("brainstorm", 0.70)) == "brainstorm"
    assert classify_intent("thinking about the design", _completion=_stub("brainstorm", 0.69)) is None


def test_failsafe_never_regresses_94():
    # No key / network error → completion returns None → classify returns None → .94 unchanged.
    assert classify_intent("install and test this repo", _completion=lambda m: None) is None
    # Malformed model output → None (falls through to .94, never a wrong demotion).
    assert classify_intent("build it", _completion=lambda m: "not json at all") is None
    assert classify_intent("build it", _completion=lambda m: '{"intent":"nonsense","confidence":0.9}') is None
    # Slash / $ commands are never classified (skipped) → None.
    assert classify_intent("/skills", _completion=_stub("converse", 0.99)) is None
    assert classify_intent("", _completion=_stub("converse", 0.99)) is None


def test_live_path_runs_end_to_end():
    """Drives the REAL _fireworks_completion path (stub only httpx.post + the key) — the coverage the
    stub-only tests skipped. Proves the imports (URLS/P/MR from nx_obfuscate) resolve, the POST fires
    with a real model, and classify_intent works via the LIVE path (no _completion injection). If the
    import were wrong, _fireworks_completion would swallow the ImportError and return None → this fails."""
    import httpx as _httpx
    import nx_key_pool as _kp
    from nx_intent import _fireworks_completion

    class _FakeResp:
        status_code = 200
        def __init__(self, content): self._c = content
        def json(self): return {"choices": [{"message": {"content": self._c}}]}

    seen = {}
    def _fake_post(url, headers=None, json=None, timeout=None):
        seen["url"] = url
        seen["model"] = (json or {}).get("model")
        return _FakeResp('{"intent":"code_brainstorm","confidence":0.9}')

    orig_post, orig_key = _httpx.post, _kp.get_fireworks_key
    _httpx.post = _fake_post
    _kp.get_fireworks_key = lambda: "fake-key-123"
    try:
        out = _fireworks_completion([{"role": "user", "content": "x"}])
        assert out == '{"intent":"code_brainstorm","confidence":0.9}', f"live path dead: {out!r}"
        assert seen["url"].endswith("/chat/completions"), seen["url"]
        assert seen["model"], "no model string sent"
        # full live path (no _completion stub) → demotes correctly
        assert classify_intent("I'm thinking about the auth flow") == "code_brainstorm"
    finally:
        _httpx.post, _kp.get_fireworks_key = orig_post, orig_key


def test_taxonomy_partition():
    # THINK and ACT are disjoint, and every think-intent is a demote-label.
    assert THINK_INTENTS.isdisjoint(ACT_INTENTS)
    assert "code_execute" in ACT_INTENTS and "code_brainstorm" in THINK_INTENTS
    # An act-intent is never returned as a demote label even at max confidence.
    for act in ACT_INTENTS:
        assert classify_intent("do the thing", _completion=_stub(act, 1.0)) is None


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {name}")
    print("\nALL PASS — both directions proven: think→converse, act→.94 (unchanged), ambiguity→action.")
