"""where each harness's transcripts live (TranscriptLocator), relocations by env var, and the roots the tap has observed."""

from __future__ import annotations

import contextlib
import os
import sqlite3
from pathlib import Path
from ....tap_core import codex_sanitize, kimi_sanitize, pi_sanitize, sanitize

CLAUDE = "claude_code"
CODEX = "codex"
PI = "pi"
KIMI = "kimi_code"

#: The ingest route per agent. The gateway binds a paired device to ONE source
#: and answers 403 for the other, which the tap's classifier treats as a
#: permanent drop -- so posting a Codex rollout to the Claude Code door does not
#: fail loudly, it fails silently. The mapping is data, not a branch, to keep
#: that impossible. Built from the harness registry's `route`, the same row
#: tap/sources.py builds its `webhook_path` from (each distribution reads its
#: own copy of the registry). A source present there but missing here was a
#: live bug once: `discover()`
#: happily finds and queues that agent's transcripts, and `upload_session`
#: KeyErrors on the very first one it tries to send -- see
#: test_ingest_path_and_sanitizer_cover_every_tap_capture_source.
def _captured_rows():
    from probe.foundation.harness_registry import get_registry

    return get_registry().captured()


INGEST_PATH = {h.id: f"/ingest/v1/sessions/{h.route}" for h in _captured_rows()}

#: The agents whose past sessions this lane can import: every captured one.
IMPORTABLE = tuple(h.id for h in _captured_rows())

#: The sanitizer modules a registry row can name (`capture.sanitizer`).
#:
#: The import lane uses them unchanged, exactly as live capture does. It used
#: to wrap them to drop Claude Code's top-level `toolUseResult` (the second,
#: full copy of every tool's output: 54% of the sanitized bytes of one measured
#: 12.9MB session) from history only. Since tap 0.9.10 the shared sanitizer
#: ships no field it does not name, for every producer, so there is nothing
#: left for this lane to drop on its own.
_SANITIZER_MODULES = {
    "sanitize": sanitize,
    "codex_sanitize": codex_sanitize,
    "pi_sanitize": pi_sanitize,
    "kimi_sanitize": kimi_sanitize,
}
SANITIZER = {h.id: _SANITIZER_MODULES[h.capture.sanitizer].sanitize_event for h in _captured_rows()}


# --- discovery ---------------------------------------------------------------


#: The explicit override per agent. Same names the tap uses, so a machine that
#: relocated one relocated both.
_ROOT_ENV = {
    CLAUDE: "PROBE_RESEARCH_TAP_PROJECTS_DIR",
    CODEX: "PRBE_CODEX_SESSIONS_DIR",
}

#: How far above a transcript its ROOT sits, as an index into `Path.parents`.
#: Claude Code files are `<root>/<cwd-slug>/<session>.jsonl`; Codex partitions
#: by date, `<root>/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl`. Derived rather than
#: assumed because these are the depths that make a LEARNED path (below) into a
#: root worth walking.
_ROOT_PARENT_INDEX = {CLAUDE: 1, CODEX: 3}


#: The directory name a root MUST have. Claude Code always writes
#: `<config>/projects`, Codex always `<CODEX_HOME>/sessions` -- both are fixed
#: by those tools, not by us -- so the name is a cheap, reliable check that a
#: derived root is a transcript tree rather than something a bad row pointed at.
_ROOT_NAME = {CLAUDE: "projects", CODEX: "sessions"}


def _tap_offsets(plugin_dir: Path) -> list[tuple[str, str]]:
    """`(path, session_id)` rows from the tap's cursor. One read, closed.

    Both things this module wants from the tap -- which sessions it already
    tracks, and where it has seen transcripts -- come from the same table, so
    they come from the same query. `closing` because `sqlite3.connect` as a
    context manager commits a TRANSACTION and leaves the handle to the garbage
    collector.
    """
    db = plugin_dir / "state.db"
    if not db.exists():
        return []
    try:
        with contextlib.closing(sqlite3.connect(f"file:{db}?mode=ro", uri=True)) as connection:
            return [
                (str(row[0]), str(row[1] or ""))
                for row in connection.execute("SELECT path, session_id FROM file_offsets")
                if row and row[0]
            ]
    except sqlite3.Error:
        return []


def learned_roots(agent: str, plugin_dir: Path) -> list[Path]:
    """Transcript roots the tap has actually OBSERVED on this machine.

    The strongest evidence available, and it costs one column of a query this
    module already makes. `file_offsets.path` holds absolute paths the tap was
    HANDED by the agent itself -- the SessionStart hook passes the real
    transcript path -- so these are ground truth no matter where the config
    directory lives, including layouts nothing here knows to guess.

    Bootstrapping limit, stated honestly: this only helps where capture has run
    at least once, and this importer exists for machines where it mostly has
    not. One row is enough to reveal a root, though, and where there are zero
    the ladder below still has `CLAUDE_CONFIG_DIR` and the default.
    """
    index = _ROOT_PARENT_INDEX[agent]
    roots: list[Path] = []
    for path, _session in _tap_offsets(plugin_dir):
        parents = Path(path).parents
        if len(parents) <= index:
            continue
        root = parents[index]
        # THE NAME CHECK IS NOT COSMETIC. The index assumes a layout, and the
        # tap does not enforce one -- it resolves a Codex rollout by rglob at
        # ANY depth, so a flat row makes `parents[3]` something like `/home`,
        # and a two-segment row makes `parents[1]` `/`. Handing either to
        # `_walk` would rglob a whole home directory and offer every `.jsonl`
        # under it as a transcript to upload. Both agents fix their own
        # directory name, so requiring it rejects every one of those without
        # rejecting any real tree.
        if root.name != _ROOT_NAME[agent]:
            continue
        if root not in roots and root.is_dir():
            roots.append(root)
    return roots


def transcript_roots(agent: str, plugin_dir: Path | None = None) -> list[Path]:
    """Every directory that might hold this agent's transcripts, best first.

    A LADDER rather than one guess, because the failure it replaces is silent:
    a machine whose config directory was relocated reported "no agent
    sessions found", which is a confident zero and indistinguishable from
    a machine that genuinely has none.

        explicit override  -- the caller said where; nothing else is consulted
        learned            -- where the tap has actually seen transcripts
        CLAUDE_CONFIG_DIR  -- the documented relocation knob (Claude Code only)
        the default        -- the guess, last

    Returns every distinct EXISTING directory, so a machine with more than one
    config dir is walked in full rather than only in its first.

    pi does not join the ladder above: it has no single relocatable directory
    to rank rungs against (see `pi_session_roots`'s docstring), so its roots
    come from `PROBE_PI_SESSION_ROOTS`/the upstream default directly, with the
    same "existing, else the first candidate" fallback the ladder ends on.
    """
    if agent == PI:
        candidates = pi_session_roots()
        existing = [root for root in candidates if root.is_dir()]
        return existing or candidates[:1]
    if agent == KIMI:
        # One root, from the registry row (its override, else under
        # KIMI_CODE_HOME): Kimi writes nowhere else.
        return [_kimi().transcript_root()]

    env = os.environ.get(_ROOT_ENV[agent])
    if env:
        # An explicit answer is an answer. Adding guesses beside it would walk
        # trees the caller deliberately excluded.
        return [Path(env)]

    roots: list[Path] = []
    if plugin_dir is not None:
        roots.extend(learned_roots(agent, plugin_dir))
    for candidate in (*_config_roots(agent), claude_root() if agent == CLAUDE else codex_root()):
        if candidate not in roots:
            roots.append(candidate)
    existing = [root for root in roots if root.is_dir()]
    # Nothing exists: hand back the FIRST candidate so the caller's "Looked in"
    # names something real rather than an empty list.
    return existing or roots[:1]
from probe.shared.harness.harnesses.claude_code.transcripts import _config_roots, claude_root  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.codex.transcripts import codex_root  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.kimi_code.transcripts import _kimi  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.transcripts import pi_session_roots  # noqa: E402 -- pieces need each other; the front door loads this one first
