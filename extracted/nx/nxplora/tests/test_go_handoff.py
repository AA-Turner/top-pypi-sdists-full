"""The /go HANDOFF proofs — hand off only a persisted, owner-scoped session id, never a dead link.

The web /continue joins on nx_sessions.id (== cfg["session_id"] == create_session's uuid), owner-scoped by
user_id. _storage_session_id's LOCAL fallback mints a uuid with no nx_sessions row — handing it off opens a
page that resolves to nothing. These prove /go hands off the canonical id or refuses honestly.

Run: python3 nx/cli/tests/test_go_handoff.py   (imports nx_cli — needs httpx, like test_untouchables_lock)
"""
import sys, os, io, contextlib, builtins

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))   # nx/cli on the path

import nx_cli


def _run_go_capture(cfg, input_ret="n"):
    """Run _run_go with stdin stubbed and stdout captured; also record whether input() was reached.

    `input_ret` answers the surface picker (_choose falls back to a numbered prompt
    with no TTY): "1" = web, "2" = Messages, "3" = Telegram; anything else cancels.
    The default "n" therefore CANCELS — which is what the refusal tests want, since
    a cancelled pick must still print no link.

    webbrowser.open is ALWAYS stubbed. _run_go opens the chosen deep link for real,
    and a test suite that launches Safari (or Messages, or Telegram) on every run is
    a test suite nobody will run. The stub also records the URL, which is the thing
    actually worth asserting: what would have been opened."""
    reached = {"input": False}
    opened = []
    orig = builtins.input
    builtins.input = lambda *a, **k: (reached.__setitem__("input", True), input_ret)[1]
    import webbrowser
    orig_open = webbrowser.open
    webbrowser.open = lambda url, *a, **k: (opened.append(url), True)[1]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            nx_cli._run_go(cfg)
    finally:
        builtins.input = orig
        webbrowser.open = orig_open
    # The opened URL is part of the observable result: assert against both, so a
    # regression that stops PRINTING the link but still opens it (or the reverse)
    # can't slip through.
    return buf.getvalue() + "".join(opened), reached["input"]


def test_go_refuses_without_a_persisted_session():
    # signed in (token) but no canonical session_id → honest refusal, NO /continue link, no browser prompt
    out, reached_input = _run_go_capture({"token": "t"})
    assert "/continue?nx_session=" not in out, "must not build a dead link"
    assert ("isn't saved" in out) or ("Can't hand off" in out)
    assert reached_input is False, "must refuse before offering to open a browser"


def test_go_hands_off_the_canonical_id():
    # "1" picks web — the surface whose handoff is the /continue link.
    out, _ = _run_go_capture({"token": "t", "session_id": "canon-abc-123"}, input_ret="1")
    assert "/continue?nx_session=canon-abc-123" in out


def test_go_cancelled_at_the_picker_hands_off_nothing():
    # The picker is a real decision point: backing out of it must not open or print
    # a link. This is the case that made the assertion above stale — _run_go grew a
    # surface picker, and every path now runs through it.
    out, _ = _run_go_capture({"token": "t", "session_id": "canon-abc-123"}, input_ret="n")
    assert "/continue?nx_session=" not in out, "a cancelled pick must hand off nothing"


def test_go_hands_off_the_same_session_to_every_surface():
    # web · Messages · Telegram are three doors to ONE session. If any of them
    # carried a different id, "continue on the go" would silently start a new
    # conversation on that surface — the exact failure the canonical-id rule exists
    # to prevent.
    for pick in ("1", "2", "3"):
        out, _ = _run_go_capture({"token": "t", "session_id": "canon-abc-123"}, input_ret=pick)
        assert "canon-abc-123" in out, f"surface {pick} dropped the canonical session id"


def test_go_never_hands_off_the_local_storage_fallback():
    # a local-only _storage_session_id (no nx_sessions row) must NEVER be handed off — only cfg["session_id"]
    out, reached_input = _run_go_capture({"token": "t", "_storage_session_id": "local-mint-xyz"})
    assert "local-mint-xyz" not in out, "the local fallback id must never reach the handoff URL"
    assert "/continue?nx_session=" not in out, "no canonical id → refuse, don't hand off the local mint"
    assert reached_input is False


def test_go_requires_sign_in():
    out, reached_input = _run_go_capture({})   # no token
    assert "/continue?nx_session=" not in out and reached_input is False


if __name__ == "__main__":
    for n, f in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        f(); print("  ✓ %s" % n)
    print("ALL /go HANDOFF PROOFS PASS")
