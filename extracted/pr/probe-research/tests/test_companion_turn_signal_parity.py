"""The turn-end signal has three writers and one reader, all naming the same files.

Writers: the tap's Stop hook (`hooks/turn-end.sh`, Claude Code and Codex) and
pi's `agent_settled` (`src/turnSignal.ts`). Reader: the worker
(`companion_worker.TURN_SUFFIX`). Each writer also reads the session's switch
state from `<sid>.state`, the file the session marker writes. A rename on one
side and not the others leaves pi's or the hook's signal written where nobody
looks, with every test still green.
"""

from __future__ import annotations

import re
from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]
TAP = AGENT / "plugins" / "probe-research-tap"
TS = AGENT / "plugins" / "probe-research-pi" / "src" / "core" / "turnSignal.ts"


def _ts_string(name: str) -> str:
    match = re.search(rf'export const {name}\s*=\s*"([^"]*)";', TS.read_text(encoding="utf-8"))
    assert match, name
    return match.group(1)


def _python_string(path: Path, name: str) -> str:
    match = re.search(rf'^{name}\s*=\s*"([^"]*)"', path.read_text(encoding="utf-8"), re.M)
    assert match, name
    return match.group(1)


def test_every_writer_names_the_file_the_worker_reads():
    suffix = _python_string(TAP / "tap" / "companion_worker.py", "TURN_SUFFIX")
    assert _ts_string("TURN_SUFFIX") == suffix
    assert f'(sid + "{suffix}")' in (TAP / "hooks" / "turn-end.sh").read_text(encoding="utf-8")


def test_every_writer_reads_the_state_file_the_marker_writes():
    marker = (AGENT / "src" / "probe" / "sdk" / "session_marker.py").read_text(encoding="utf-8")
    assert '(session_id + ".state")' in marker
    assert _ts_string("STATE_SUFFIX") == ".state"
    assert '(sid + ".state")' in (TAP / "hooks" / "turn-end.sh").read_text(encoding="utf-8")
    assert '(session_id + ".state")' in (TAP / "tap" / "companion_lease.py").read_text(encoding="utf-8")
