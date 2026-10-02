"""pi's copy of the `daemon` state's messages matches the Python originals.

pi has no hooks, so `plugins/probe-research-pi/src/daemonNotice.ts` carries its
own copy of what `version_check.py` says at session start and what
`tracking_guard.py` says when recording changes hands. Two copies of a
consent-adjacent message that drift apart tell the agent two different things,
so each TypeScript constant is rebuilt from its string literals and compared.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
TS = AGENT / "plugins" / "probe-research-pi" / "src" / "daemonNotice.ts"


def _load(name: str, path: Path):
    sys.path.insert(0, str(HOOKS))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(HOOKS))


def _ts_string(name: str) -> str:
    """`export const NAME = "a" + OTHER + "b";` -> "a" + OTHER's value + "b".

    A bare identifier in the concatenation is another exported string in the
    same file, resolved the same way, so pi can build one message from another
    (the flip notice from the context) exactly as the Python side does.
    """
    source = TS.read_text(encoding="utf-8")
    match = re.search(rf"export const {name}\s*=\s*(.*?);\n", source, re.S)
    assert match, name
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"|([A-Za-z_]\w*)', match.group(1))
    return "".join(literal if identifier == "" else _ts_string(identifier) for literal, identifier in parts)


def _ts_object(name: str) -> str:
    source = TS.read_text(encoding="utf-8")
    match = re.search(rf"export const {name}[^=]*=\s*\{{(.*?)\}}", source, re.S)
    assert match, name
    return match.group(1)


def _ts_reason_words() -> dict[str, str]:
    """`DAEMON_REASON_WORDS`, its `[DaemonReason.X]` keys resolved to their values."""
    reasons = dict(re.findall(r'(\w+):\s*"([^"]+)"', _ts_object("DaemonReason")))
    pairs = re.findall(r'\[DaemonReason\.(\w+)\]:\s*"((?:[^"\\]|\\.)*)"', _ts_object("DAEMON_REASON_WORDS"))
    return {reasons[name]: text for name, text in pairs}


def test_session_start_context_matches_version_check():
    version_check = _load("_vc_pi_parity", HOOKS / "version_check.py")
    marker = _load("_marker_ctx_pi_parity", HOOKS / "_session_marker.py")
    assert _ts_string("DAEMON_CONTEXT") == version_check.DAEMON_CONTEXT
    # ONE Python source: the hook reads the marker's constant, it does not keep a copy.
    assert version_check.DAEMON_CONTEXT == marker.DAEMON_CONTEXT


def test_handback_notices_match_the_guard():
    guard = _load("_guard_pi_parity", HOOKS / "tracking_guard.py")
    assert _ts_string("DAEMON_LIVE_NOTICE") == guard.FLIP_NOTICE["daemon"]
    # The flip carries the whole statement of the split, on both surfaces.
    assert _ts_string("DAEMON_CONTEXT") in _ts_string("DAEMON_LIVE_NOTICE")
    assert _ts_string("DAEMON_DEGRADED_NOTICE") == guard.DAEMON_DEGRADED_NOTICE
    assert _ts_reason_words() == guard.DAEMON_REASON_WORDS


def test_the_shared_files_are_named_alike():
    marker = _load("_marker_pi_parity", HOOKS / "_session_marker.py")
    assert _ts_string("LEASE_SUFFIX") == marker.LEASE_SUFFIX
    assert _ts_string("NOTIFIED_SUFFIX") == marker.NOTIFIED_SUFFIX
