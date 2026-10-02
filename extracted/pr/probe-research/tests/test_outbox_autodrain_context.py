"""The dead-letter repair prompt in the plugin's session-start hook.

An async write that dead-letters does so AFTER the session that made it has
moved on (0.112.0 removed the SDK notes door for exactly this silence, but
every other op kind can still dead-letter: caps, permanent 4xx, unroutable
endpoints). Before this feature, a failed/ op sat in the outbox until a human
happened to run `probe outbox status` -- observed in production: a note append
dead-lettered on 19 Aug was found by hand days later.

The design is PROMPT-ONLY, deliberately. Queued ops already drain through the
guarded kick every CLI invocation performs (main._outbox_notice ->
outbox_worker.maybe_spawn), and the first draft's `outbox retry; outbox drain`
spawn ride-along was rejected in adversarial review: retry clears the auth
block and re-queues dead letters at the FIFO head, drain holds the lock across
network I/O unguarded, and both ignore `probe outbox pause`. Dead letters need
attention, not plumbing -- so the hook injects a repair prompt and the
session's agent applies judgment.

Properties pinned:

  1. Dead letters -> the repair prompt, carrying the count.
  2. Dead letters + tracking off -> the report-only variant: told what is
     stuck, directed to a read and a report, never to Probe writes.
  3. Empty or absent outbox -> silence.
  4. Queued-only -> silence: mid-flight ops are the guarded drainer's job,
     and prompting on them would nag every concurrent session.
  5. The maintenance spawn NEVER carries outbox commands, dead letters or
     not -- the rejected ride-along must not come back.
  6. PreCompact -> silence (additionalContext reaches nobody there); the
     maintenance spawn still fires.
  7. The prompt COMPOSES with other context parts, after the boundary nudge
     and before the team-note brief (the budget-eaten tail).
  8. Directory resolution mirrors probe.sdk.journal.default_dir: the
     PROBE_OUTBOX_DIR override, `~` expansion, and the per-rank suffix a
     SLURM/torchrun environment triggers.
  9. Fail-open: a counting error degrades to silence, never to a phantom
     repair job.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1] / "plugins" / "probe-research"

SESSION_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

RANK_VARS = ("SLURM_PROCID", "RANK", "OMPI_COMM_WORLD_RANK", "LOCAL_RANK")


def _load_hook():
    """Load version_check.py the way session-start.sh does (see the sibling
    tracking-off test for why the hooks dir must sit on sys.path)."""
    path = PLUGIN / "hooks" / "version_check.py"
    spec = importlib.util.spec_from_file_location("_outbox_hook_under_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    hooks_dir = str(path.parent)
    added = hooks_dir not in sys.path
    if added:
        sys.path.insert(0, hooks_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(hooks_dir)
    # Machine-probing seams stubbed out, same as the sibling hook tests.
    module._team_note_cli_too_old = lambda _binary: None
    return module


@pytest.fixture
def hook(tmp_path, monkeypatch):
    """The hook with isolated state and the spawn captured, never executed."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)
    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)
    # A rank var leaked from the host (this suite runs on training boxes too)
    # would silently redirect every count below into a rank-N subdir.
    for var in RANK_VARS:
        monkeypatch.delenv(var, raising=False)
    # Resume is the quietest source: no compact nudge, no off contract, so the
    # outbox prompt is the only candidate context part unless a test adds one.
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "resume")
    monkeypatch.setenv("PROBE_SESSION_ID", SESSION_ID)
    module = _load_hook()
    spawned: list[str] = []

    class _CapturedPopen:
        def __init__(self, argv, **_kwargs):
            spawned.append(argv[-1])

    monkeypatch.setattr(module.subprocess, "Popen", _CapturedPopen)
    module._spawned_commands = spawned
    return module


def _seed(tmp_path, subdir: str, names: list[str]) -> Path:
    outbox = tmp_path / "state" / "probe" / "outbox"
    d = outbox / subdir
    d.mkdir(parents=True, exist_ok=True)
    for name in names:
        (d / name).write_text("{}")
    return outbox


def _untrack(hook):
    assert hook._session_marker.set_tracking(SESSION_ID, False)


# ---------------------------------------------------------------------------
# The prompt.
# ---------------------------------------------------------------------------


def test_dead_letters_inject_the_repair_prompt(hook, tmp_path):
    """Property 1. failed/ ops get the agent's attention, count included."""
    _seed(tmp_path, "failed", ["100-aa.json", "200-bb.json"])

    ctx = hook._start_context()
    assert ctx == hook.OUTBOX_REPAIR_CONTEXT.format(failed=2)
    assert "2 dead-lettered" in ctx


def test_tracking_off_gets_the_report_only_variant(hook, tmp_path):
    """Property 2. An untracked session is told, but told to READ and REPORT:
    the repair steps create an artifact and a note, which is recording, which
    is what the toggle turned off."""
    _seed(tmp_path, "failed", ["100-aa.json"])
    _untrack(hook)

    ctx = hook._start_context()
    assert ctx is not None
    assert ctx.startswith(hook.TRACKING_OFF_CONTEXT)
    assert ctx.endswith(hook.OUTBOX_REPORT_ONLY_CONTEXT.format(failed=1))
    assert "artifact anchored" not in ctx  # no repair imperatives to obey


def test_empty_outbox_stays_silent(hook, tmp_path):
    """Property 3, seeded-but-empty form: the common case adds zero context."""
    _seed(tmp_path, "failed", [])
    _seed(tmp_path, "ops", [])

    assert hook._start_context() is None


def test_missing_outbox_dir_stays_silent(hook):
    """Property 3 for a machine that has never queued a write."""
    assert hook._start_context() is None


def test_queued_only_stays_silent(hook, tmp_path):
    """Property 4. Mid-flight ops belong to the guarded background drainer
    that every CLI invocation kicks; prompting on them would nag every
    session that starts while another is writing."""
    _seed(tmp_path, "ops", ["100-aa.json"])

    assert hook._start_context() is None


def test_non_json_files_do_not_count(hook, tmp_path):
    """Lock sidecars and tombstones in the state dir are not ops."""
    outbox = _seed(tmp_path, "failed", [])
    (outbox / "failed" / ".gitkeep").write_text("")
    (outbox / "failed" / "100-aa.json.tmp").write_text("{}")

    assert hook._start_context() is None


# ---------------------------------------------------------------------------
# The spawn stays plumbing-free.
# ---------------------------------------------------------------------------


def test_spawn_never_carries_outbox_commands(hook, tmp_path):
    """Property 5. The rejected retry/drain ride-along must not return:
    `outbox retry` clears the auth block and re-queues dead letters at the
    FIFO head, `outbox drain` bypasses maybe_spawn's guards, and both ignore
    an operator's pause."""
    _seed(tmp_path, "failed", ["100-aa.json"])
    _seed(tmp_path, "ops", ["200-bb.json"])

    hook._start_context()
    assert len(hook._spawned_commands) == 1
    assert "outbox" not in hook._spawned_commands[0]
    assert "agent-rules refresh" in hook._spawned_commands[0]


def test_precompact_spawns_but_says_nothing(hook, tmp_path, monkeypatch):
    """Property 6. Mid-compaction there is nobody left to read context; the
    maintenance spawn (whose CLI invocations kick the guarded drainer) still
    runs."""
    _seed(tmp_path, "failed", ["100-aa.json"])
    monkeypatch.setenv("PROBE_HOOK_EVENT", "precompact")

    assert hook._start_context() is None
    assert len(hook._spawned_commands) == 1


# ---------------------------------------------------------------------------
# Composition.
# ---------------------------------------------------------------------------


def test_prompt_follows_the_compact_nudge(hook, tmp_path, monkeypatch):
    """Property 7. Boundary context first, then the action item -- and both
    ahead of the team-note brief, whose length is what the additionalContext
    budget truncates."""
    _seed(tmp_path, "failed", ["100-aa.json"])
    monkeypatch.setenv("PROBE_SESSION_SOURCE", "compact")

    ctx = hook._start_context()
    expected = hook.COMPACT_CONTEXT + "\n\n" + hook.OUTBOX_REPAIR_CONTEXT.format(failed=1)
    assert ctx == expected


# ---------------------------------------------------------------------------
# Directory resolution mirrors the CLI (probe.sdk.journal.default_dir).
# ---------------------------------------------------------------------------


def test_probe_outbox_dir_overrides_default(hook, tmp_path, monkeypatch):
    """Property 8. A relocated outbox is honored."""
    other = tmp_path / "elsewhere"
    (other / "failed").mkdir(parents=True)
    (other / "failed" / "100-aa.json").write_text("{}")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(other))

    ctx = hook._start_context()
    assert ctx == hook.OUTBOX_REPAIR_CONTEXT.format(failed=1)


def test_probe_outbox_dir_expands_tilde(hook, tmp_path, monkeypatch):
    """Property 8. The CLI expanduser()s the override; a hook that does not
    would silently count a literal './~/...' that never exists."""
    home = tmp_path / "home"
    (home / "box" / "failed").mkdir(parents=True)
    (home / "box" / "failed" / "100-aa.json").write_text("{}")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", "~/box")

    ctx = hook._start_context()
    assert ctx == hook.OUTBOX_REPAIR_CONTEXT.format(failed=1)


def test_rank_env_selects_the_rank_subdir_of_an_explicit_outbox_dir(hook, tmp_path, monkeypatch):
    """Property 8. The CLI splits an explicit PROBE_OUTBOX_DIR per rank too, so
    the copy must: counting the rankless root misses rank-2's dead letters."""
    outbox = tmp_path / "shared"
    (outbox / "rank-2" / "failed").mkdir(parents=True)
    (outbox / "rank-2" / "failed" / "100-aa.json").write_text("{}")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(outbox))
    monkeypatch.setenv("SLURM_PROCID", "2")

    ctx = hook._start_context()
    assert ctx == hook.OUTBOX_REPAIR_CONTEXT.format(failed=1)


def test_rank_env_selects_the_rank_subdir(hook, tmp_path, monkeypatch):
    """Property 8. Inside a SLURM/torchrun allocation the journal is per-rank;
    a hook counting the rankless parent reports silence while dead letters sit
    in rank-0/ -- the first draft's exact blind spot."""
    outbox = tmp_path / "state" / "probe" / "outbox"
    (outbox / "rank-0" / "failed").mkdir(parents=True)
    (outbox / "rank-0" / "failed" / "100-aa.json").write_text("{}")
    monkeypatch.setenv("RANK", "0")

    ctx = hook._start_context()
    assert ctx == hook.OUTBOX_REPAIR_CONTEXT.format(failed=1)


# ---------------------------------------------------------------------------
# Fail-open.
# ---------------------------------------------------------------------------


def test_count_errors_degrade_to_silence(hook, monkeypatch):
    """Property 9, via the seam: resolution raising anywhere must yield 0.
    (A merely unreadable directory does not raise -- glob returns nothing --
    so this pins the except-branch itself, not a filesystem scenario.)"""

    def _boom():
        raise OSError("boom")

    monkeypatch.setattr(hook, "_outbox_dir", _boom)
    assert hook._outbox_dead_letters() == 0
    assert hook._start_context() is None
