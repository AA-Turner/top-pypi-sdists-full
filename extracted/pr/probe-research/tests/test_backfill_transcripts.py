"""Discovery, selection and mapping for the transcript import lane.

The denominator here is produced by walking the disk, so these tests are about
the walk telling the truth: what it counts, what it refuses to count, and what
it refuses to GUESS. The upload half lives in test_backfill_transcripts_upload.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

from probe.cli import backfill_transcripts as bt

_TAP_DIR = Path(__file__).resolve().parent.parent / "plugins" / "probe-research-tap"
_PI_FIXTURES_DIR = _TAP_DIR / "tests" / "fixtures" / "pi"


def _write(path: Path, events: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    return path


def _cc_session(root: Path, slug: str, session_id: str, cwd: str, *, extra: int = 0) -> Path:
    events = [
        # FIRST LINE CARRIES NO CWD, on purpose: Claude Code routinely opens a
        # transcript with a queue-operation, and a reader that only looked at
        # line one would call every such session unanchorable.
        {"type": "queue-operation", "sessionId": session_id, "timestamp": "2026-08-01T00:00:00Z"},
        {
            "type": "user",
            "sessionId": session_id,
            "cwd": cwd,
            "gitBranch": "main",
            "message": {"role": "user", "content": [{"type": "text", "text": "hello"}]},
        },
    ]
    events += [
        {
            "type": "assistant",
            "cwd": cwd,
            "message": {"role": "assistant", "content": [{"type": "text", "text": f"line {i}"}]},
        }
        for i in range(extra)
    ]
    return _write(root / slug / f"{session_id}.jsonl", events)


@pytest.fixture
def roots(tmp_path, monkeypatch):
    claude = tmp_path / "claude-projects"
    codex = tmp_path / "codex-sessions"
    claude.mkdir()
    codex.mkdir()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", str(claude))
    monkeypatch.setenv("PRBE_CODEX_SESSIONS_DIR", str(codex))
    return claude, codex


def test_discovery_counts_sessions_and_reads_cwd_from_a_later_line(roots) -> None:
    claude, _ = roots
    _cc_session(
        claude,
        "-home-richy-research-os",
        "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa",
        "/home/richy/research-os",
    )

    census = bt.discover()

    assert census.sessions == 1
    assert census.candidates[0].cwd == "/home/richy/research-os"
    assert census.bytes > 0


def test_the_lossy_directory_name_is_never_used_as_the_cwd(roots) -> None:
    """`/home/a-b/c` and `/home/a/b/c` encode to the same directory name.

    The encoding replaces every separator with a dash and is not reversible, so
    a cwd derived from it would be a guess -- and a wrong cwd anchors someone's
    conversation to the wrong project. The transcript's own field is the only
    source this reads.
    """
    claude, _ = roots
    real_cwd = "/home/richy/trees/research-os/transcript-backfill"
    _cc_session(
        claude,
        "-home-richy-trees-research-os-transcript-backfill",
        "bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb",
        real_cwd,
    )

    census = bt.discover()

    assert census.candidates[0].cwd == real_cwd


def test_a_session_with_no_recorded_cwd_is_kept_but_unanchorable(roots) -> None:
    """Uploading it is still right; guessing where it belongs is not."""
    claude, _ = roots
    _write(
        claude / "-tmp" / "cccccccc-3333-4333-8333-cccccccccccc.jsonl",
        [
            {
                "type": "user",
                "sessionId": "cccccccc-3333-4333-8333-cccccccccccc",
                "message": {"role": "user", "content": "identity without cwd"},
            }
        ],
    )

    census = bt.discover()

    assert census.sessions == 1
    assert census.candidates[0].cwd is None


def test_subagent_sidechains_are_excluded_and_counted(roots) -> None:
    claude, _ = roots
    session = "dddddddd-4444-4444-8444-dddddddddddd"
    _cc_session(claude, "-proj", session, "/proj")
    _write(
        claude / "-proj" / session / "subagents" / "agent-9f2b.jsonl",
        [{"type": "user", "cwd": "/proj"}],
    )

    census = bt.discover()

    assert census.sessions == 1
    assert census.sidechains == 1


def test_sessions_the_tap_already_tracks_are_excluded(roots) -> None:
    """The importer ships exactly the COMPLEMENT of the reconciler's rule."""
    claude, _ = roots
    tracked = "eeeeeeee-5555-4555-8555-eeeeeeeeeeee"
    fresh = "ffffffff-6666-4666-8666-ffffffffffff"
    _cc_session(claude, "-proj", tracked, "/proj")
    _cc_session(claude, "-proj", fresh, "/proj")

    census = bt.discover(tracked={tracked})

    assert [t.session_id for t in census.candidates] == [fresh]
    assert census.captured_live == 1


def test_tap_tracked_sessions_reads_the_plugin_sqlite_read_only(tmp_path) -> None:
    plugin = tmp_path / "plugin"
    plugin.mkdir()
    db = plugin / "state.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE file_offsets (path TEXT PRIMARY KEY, session_id TEXT)")
        conn.execute("INSERT INTO file_offsets VALUES ('/a.jsonl', 'sess-a')")

    assert bt.tap_tracked_sessions(plugin) == {"sess-a"}


def test_a_missing_or_broken_tap_database_is_an_empty_set_not_a_crash(tmp_path) -> None:
    """Empty is the safe direction: the SERVER check is what stops a re-upload."""
    assert bt.tap_tracked_sessions(tmp_path / "nope") == set()
    broken = tmp_path / "broken"
    broken.mkdir()
    (broken / "state.db").write_text("not a database", encoding="utf-8")
    assert bt.tap_tracked_sessions(broken) == set()


def test_divergent_copies_of_one_session_are_quarantined_regardless_of_size(roots) -> None:
    claude, _ = roots
    session = "12121212-7777-4777-8777-121212121212"
    _cc_session(claude, "-small", session, "/small")
    _cc_session(claude, "-big", session, "/big", extra=40)

    census = bt.discover()

    assert census.sessions == 0
    assert census.identity_conflicts == 1
    assert census.duplicates == 1


def test_codex_rollouts_are_discovered_by_their_trailing_uuid(roots) -> None:
    _, codex = roots
    session = "01a02357-44b8-7703-8ded-974b57fd1a8a"
    _write(
        codex / "2026" / "08" / "21" / f"rollout-2026-08-21T08-01-56-{session}.jsonl",
        [
            {
                "type": "session_meta",
                "payload": {"id": session, "cwd": "/home/richy/x"},
                "timestamp": "2026-08-21T08:01:56.938Z",
            }
        ],
    )

    census = bt.discover(agents=(bt.CODEX,))

    assert census.sessions == 1
    assert census.candidates[0].session_id == session
    assert census.candidates[0].cwd == "/home/richy/x"
    assert census.candidates[0].agent == bt.CODEX


def _load_tap_sources():
    """tap/sources.py, loaded standalone.

    It is self-contained -- `import types`, `dataclasses`, `pathlib` only, no
    imports of its own `tap` package -- so it can be exec'd directly without
    putting the tap plugin (a separate distribution; see
    tap_core/__init__.py) on sys.path at all.
    """
    spec = importlib.util.spec_from_file_location(
        "_tap_sources_for_test", _TAP_DIR / "tap" / "sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    # `from __future__ import annotations` makes every dataclass field
    # annotation a STRING, and `@dataclass` resolves those by looking the
    # module up in `sys.modules[cls.__module__]` -- unregistered, that lookup
    # returns None and field resolution blows up on a perfectly good module.
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    finally:
        del sys.modules[spec.name]
    return module


def test_ingest_path_and_sanitizer_cover_every_tap_capture_source() -> None:
    """A source in tap/sources.py with no row here is exactly the bug this
    file was written to fix: "pi" shipped in the tap's own registry while
    `INGEST_PATH`/`SANITIZER` here still only knew claude_code/codex, so
    `upload_session` KeyError'd on the very first pi transcript it touched.
    Tying the two together means a future 4th source fails HERE, in a unit
    test, rather than silently in production.
    """
    sources = _load_tap_sources()

    assert set(bt.INGEST_PATH) == set(sources.SOURCES), (
        "INGEST_PATH has drifted from tap/sources.py's capture source registry"
    )
    assert set(bt.SANITIZER) == set(sources.SOURCES), (
        "SANITIZER has drifted from tap/sources.py's capture source registry"
    )
    for source_id, source in sources.SOURCES.items():
        # THE ROUTE, not just presence: the gateway binds a paired device to
        # ONE source and answers 403 (a silent permanent drop) for any other,
        # so a right-key-wrong-value row is exactly as dangerous as a missing
        # one.
        assert bt.INGEST_PATH[source_id] == source.webhook_path, (
            f"{source_id}: INGEST_PATH route does not match tap's webhook_path"
        )


# --- pi -----------------------------------------------------------------


@pytest.fixture
def pi_sessions_root(tmp_path, monkeypatch):
    root = tmp_path / "pi-sessions"
    root.mkdir()
    monkeypatch.setenv("PROBE_PI_SESSION_ROOTS", str(root))
    return root


def _copy_pi_fixture(dest_dir: Path, name: str) -> Path:
    """A REAL captured pi session, not a synthesized one.

    Same rationale as the tap's own pi_discovery tests
    (test_discovers_real_pi_fixtures_by_shape_not_filename): exercise the
    shape a pi install actually writes, not a shape this file imagined.
    """
    fixture = _PI_FIXTURES_DIR / name
    assert fixture.exists(), f"missing pi fixture: {fixture}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / name
    shutil.copy(fixture, dest)
    return dest


def test_a_real_pi_session_fixture_is_discovered_with_its_cwd(pi_sessions_root) -> None:
    _copy_pi_fixture(
        pi_sessions_root / "--Users-badlogic-workspaces-pi-mono--",
        "2026-01-16T02-31-35-233Z_8072a61b-67e6-4618-8f35-5c5616aea2be.jsonl",
    )

    census = bt.discover(agents=(bt.PI,))

    assert census.sessions == 1
    assert census.candidates[0].session_id == "8072a61b-67e6-4618-8f35-5c5616aea2be"
    assert census.candidates[0].cwd == "/Users/badlogic/workspaces/pi-mono"
    assert census.candidates[0].agent == bt.PI


def test_pi_discovery_ignores_a_non_pi_jsonl_sharing_the_same_root(pi_sessions_root) -> None:
    """pi's configured root can be shared with unrelated `.jsonl` files -- an
    embedder's own logs, per pi_discovery.py's module docstring -- unlike
    Claude Code/Codex, whose fixed, named roots this module already trusts
    wholesale. Shape, not location, has to decide for pi.
    """
    dest_dir = pi_sessions_root / "--proj--"
    _copy_pi_fixture(
        dest_dir, "2026-01-16T03-18-40-694Z_89afd3da-1fa3-45f9-87ad-a023f92372ee.jsonl"
    )
    (dest_dir / "not-a-session.jsonl").write_text(
        json.dumps({"type": "log", "msg": "unrelated"}) + "\n", encoding="utf-8"
    )

    census = bt.discover(agents=(bt.PI,))

    assert census.sessions == 1
    assert census.candidates[0].session_id == "89afd3da-1fa3-45f9-87ad-a023f92372ee"


def test_pi_session_ids_come_from_the_trailing_uuid_not_the_whole_stem(tmp_path) -> None:
    """pi filenames are `<timestamp>_<uuid>.jsonl` -- same anchored-uuid
    strategy as Codex's `rollout-<ts>-<uuid>.jsonl`, different prefix shape."""
    assert (
        bt.session_id_for(
            tmp_path / "2026-01-16T02-31-35-233Z_8072a61b-67e6-4618-8f35-5c5616aea2be.jsonl",
            bt.PI,
        )
        == "8072a61b-67e6-4618-8f35-5c5616aea2be"
    )
    # The sidechain rule applies under pi too, not just Claude Code/Codex.
    assert bt.session_id_for(tmp_path / "agent-9f2b.jsonl", bt.PI) is None


def test_pi_session_roots_env_is_pathsep_separated(tmp_path, monkeypatch) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    monkeypatch.setenv("PROBE_PI_SESSION_ROOTS", f"{a}{os.pathsep}{b}")

    roots = bt.transcript_roots(bt.PI, None)

    assert a in roots and b in roots


def test_pi_session_roots_default_to_the_upstream_location(monkeypatch) -> None:
    """No `PROBE_PI_SESSION_ROOTS` override -> the same default
    `~/.pi/agent/sessions` tap/pi_discovery.py's DEFAULT_ROOT names."""
    monkeypatch.delenv("PROBE_PI_SESSION_ROOTS", raising=False)

    assert bt.pi_session_roots() == [bt.pi_root()]
    assert bt.pi_root() == Path.home() / ".pi" / "agent" / "sessions"


def test_run_lane_includes_pi_by_default_when_it_is_paired(tmp_path, monkeypatch) -> None:
    """`wanted` used to be `[CLAUDE, CODEX]` unconditionally, so a machine with
    ONLY pi paired had its transcripts lane silently never look at pi's tree at
    all -- the actual mechanism behind "N files found · N queued" landing
    nothing: `run_lane` never asked `discover()` for pi in the first place.
    """
    from probe.cli import backfill_transcripts as transcripts_mod
    from probe.cli import capabilities

    paired = {bt.CLAUDE: ("tok-cc", "http://x"), bt.PI: ("tok-pi", "http://x")}
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: paired.get(s))
    monkeypatch.setattr(capabilities, "capture_device_id", lambda s=None: f"dev-{s}")
    monkeypatch.setattr(capabilities, "tap_plugin_dir", lambda s=None: tmp_path / str(s))

    seen: dict = {}

    def fake_discover(*, agents, **kwargs):
        seen["agents"] = list(agents)
        return bt.Census()

    monkeypatch.setattr(transcripts_mod, "discover", fake_discover)

    transcripts_mod.run_lane(client=object(), interactive=False)

    assert set(seen["agents"]) == {bt.CLAUDE, bt.PI}
    assert bt.CODEX not in seen["agents"], "codex was never paired in this test"


def test_run_lane_reports_pi_unpaired_on_a_claude_paired_machine(tmp_path, monkeypatch) -> None:
    """D3: a machine paired only for Claude Code holds Claude's `ingest_token`
    in the CLI config. pi used to resolve THAT token, land in `posters`, and
    then 403 on every `/ingest/v1/sessions/pi` upload, failing the whole pi
    import. pi must resolve nothing and be reported unpaired instead."""
    from probe.cli import backfill_transcripts as transcripts_mod

    config = tmp_path / "probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(json.dumps({"base_url": "http://x", "ingest_token": "ros_ing_claude"}))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "tap-cc"))
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path / "tap-codex"))
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "tap-pi"))
    for name in ("PROBE_INGEST_TOKEN", "PRBE_CODEX_TAP_TOKEN", "PROBE_PI_TAP_TOKEN", "PROBE_BASE_URL"):
        monkeypatch.delenv(name, raising=False)

    seen: dict = {}

    def fake_discover(*, agents, **kwargs):
        seen["agents"] = list(agents)
        return bt.Census()

    monkeypatch.setattr(transcripts_mod, "discover", fake_discover)

    transcripts_mod.run_lane(client=object(), interactive=False)

    assert seen["agents"] == [bt.CLAUDE]


def test_gate_states_the_scope_and_the_counts(roots) -> None:
    """The only screen between a person and a surprise."""
    claude, _ = roots
    _cc_session(claude, "-proj", "aaaa2222-9999-4999-8999-aaaa22223333", "/proj")
    census = bt.discover()
    census.captured_live = 2
    census.already_in_probe = 3

    text = "\n".join(bt.gate_lines(census, {}))

    assert "the whole machine" in text
    assert "1 sessions" in text or "1 session" in text
    assert "2 already captured live" in text
    assert "3 already in Probe" in text
    assert "sanitized here before upload" in text


def test_the_gate_never_promises_summaries(roots) -> None:
    """`gate_lines` IS the consent surface, so it has to be true. It promised
    "N summaries will be written locally by your agent" back when this lane
    wrote digests; the digest lane is retired server-side and this run writes
    none, so the screen must not describe work that cannot happen."""
    claude, _ = roots
    _cc_session(claude, "-proj", "aaaa3333-9999-4999-8999-aaaa33334444", "/proj")
    census = bt.discover()

    text = "\n".join(bt.gate_lines(census, {}))

    assert "summar" not in text.lower()


class _ProjectClient:
    """Resolves slugs the way the real client does, and counts the lookups."""

    def __init__(self, ids: dict[str, str]) -> None:
        self.ids = ids
        self.lookups: list[str] = []

    def resolve_project(self, slug: str) -> dict | None:
        self.lookups.append(slug)
        return {"id": self.ids[slug], "slug": slug} if slug in self.ids else None


@pytest.mark.parametrize("projects", [{"alpha": "id-alpha", "beta": "id-beta"}, {"alpha": "id-alpha"}])
def test_folder_unit_assignments_never_bind_standalone_conversations(tmp_path, monkeypatch, projects):
    """Directory proximity is not evidence of a conversation's entity ownership."""
    from probe.cli import backfill_run
    from probe.cli.backfill_ledger import Unit

    units = [
        Unit(unit_id="a", project="alpha", paths=("alpha/train.py", "alpha/eval.py")),
        Unit(unit_id="b", project="beta", paths=("beta/notes.md",)),
    ]
    client = _ProjectClient(projects)
    seen = []
    monkeypatch.setattr(bt, "run_lane", lambda **kwargs: seen.append(kwargs) or ["standalone"])
    lines = backfill_run._run_transcript_lane(
        client_factory=lambda: client, folder=tmp_path, units=units,
        interactive=False, yes=True, budget_bytes=4096,
    )
    assert lines == ["standalone"]
    # The client is forwarded -- `run_lane` needs it for the per-session server
    # check and the background identity pin -- and no agent rides along now.
    assert seen == [{"client": client, "interactive": False, "yes": True, "budget_bytes": 4096}]
    assert seen[0]["client"] is client
    assert client.lookups == [], "known and unknown file destinations must not route transcripts"


def _one_line_transcript(tmp_path: Path, session_id: str = "sid-123") -> bt.Transcript:
    path = tmp_path / f"{session_id}.jsonl"
    path.write_text(
        json.dumps(
            {
                "type": "user",
                "message": {"role": "user", "content": [{"type": "text", "text": "hello"}]},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return bt.Transcript(
        path=path,
        session_id=session_id,
        agent=bt.CLAUDE,
        cwd="/repo",
        size=path.stat().st_size,
        mtime=path.stat().st_mtime,
    )


# --- the lane, driven down to import_transcripts -----------------------------


@pytest.fixture
def lane(tmp_path, monkeypatch):
    """`run_lane` with the disk, the network and the ledger stubbed out.

    Everything between the credential lookup and `import_transcripts` is
    covered next door; what these tests are about is what the lane DECIDES and
    what it says afterwards, and both are invisible from any smaller seam.
    """
    from probe.cli import backfill_transcripts as transcripts_mod
    from probe.cli import capabilities

    monkeypatch.setattr(
        capabilities, "resolved_capture_credential", lambda s=None: ("tok", "http://x")
    )
    monkeypatch.setattr(capabilities, "capture_device_id", lambda s=None: f"dev-{s}")
    monkeypatch.setattr(capabilities, "tap_plugin_dir", lambda s=None: tmp_path / str(s))
    monkeypatch.setattr(transcripts_mod, "tap_tracked_sessions", lambda directory: set())

    transcript = _one_line_transcript(tmp_path, "s-1")
    monkeypatch.setattr(
        transcripts_mod, "discover", lambda **kw: bt.Census(candidates=[transcript])
    )
    ledger = bt.TranscriptLedger(tmp_path / "ledger.jsonl")
    monkeypatch.setattr(bt.TranscriptLedger, "for_device", classmethod(lambda cls: ledger))
    monkeypatch.setattr(transcripts_mod, "exclude_ingested", lambda census, client, **kw: census)
    monkeypatch.setattr(transcripts_mod, "fetch_ingest_state", lambda client, session_id: None)
    monkeypatch.setattr(
        transcripts_mod, "saved_session_sources", lambda sources, **kwargs: tuple(sources)
    )
    monkeypatch.setattr(transcripts_mod, "choose_sources", lambda available: available)

    seen: dict = {}

    def fake_import(census, **kwargs):
        seen.update(kwargs)
        return bt.LaneOutcome(found=1, uploaded=1)

    monkeypatch.setattr(transcripts_mod, "import_transcripts", fake_import)

    def run(**kwargs):
        kwargs.setdefault("interactive", False)
        kwargs.setdefault("client", object())
        lines = transcripts_mod.run_lane(**kwargs)
        return seen, lines

    return run


def test_saved_histories_are_detected_without_agent_binaries(roots, tmp_path, monkeypatch):
    from probe.cli import backfill as bf

    claude, codex = roots
    _cc_session(claude, "-proj", "aaaa2222-9999-4999-8999-aaaa22223333", "/proj")
    session = "bbbb2222-9999-4999-8999-bbbb22223333"
    _write(codex / "2026" / f"rollout-{session}.jsonl", [{
        "type": "session_meta", "payload": {"id": session, "cwd": "/proj"},
    }])
    monkeypatch.setenv("PROBE_PI_SESSION_ROOTS", str(tmp_path / "pi"))
    monkeypatch.setattr(bf, "which_agent", lambda agent: None)

    assert bt.saved_session_sources((bt.CLAUDE, bt.CODEX, bt.PI), plugin_dirs={}) == (
        bt.CLAUDE, bt.CODEX,
    )


def test_empty_roots_and_sidechains_are_not_offered_as_saved_histories(roots):
    claude, _ = roots
    _write(claude / "-proj" / "agent-child.jsonl", [{"type": "user"}])
    assert bt.saved_session_sources((bt.CLAUDE, bt.CODEX), plugin_dirs={}) == ()


@pytest.mark.parametrize("selected", [(bt.CLAUDE,), (bt.CODEX,), (bt.CLAUDE, bt.CODEX)])
def test_selected_histories_bound_discovery_preview_and_upload(lane, monkeypatch, selected):
    from probe.cli import capabilities, tui

    offered = []
    credentials = []
    discoveries = []

    def choose(available):
        offered.append(available)
        return selected

    def discover(*, agents, plugin_dirs, **kwargs):
        discoveries.append(tuple(agents))
        assert set(plugin_dirs) == set(selected)
        return bt.Census(candidates=[
            bt.Transcript(Path(f"/{source}.jsonl"), f"session-{source}", source, None, 10, 1)
            for source in agents
        ])

    def credential(source):
        credentials.append(source)
        return "tok", "http://x"

    def review(title, lines, choices):
        text = "\n".join(lines)
        assert f"{len(selected)} sessions" in text
        assert ("Claude Code" in text) == (bt.CLAUDE in selected)
        assert ("Codex" in text) == (bt.CODEX in selected)
        assert "pi logs" not in text
        return "import"

    monkeypatch.setattr(bt, "choose_sources", choose)
    monkeypatch.setattr(bt, "discover", discover)
    monkeypatch.setattr(capabilities, "resolved_capture_credential", credential)
    monkeypatch.setattr(tui, "review", review)
    seen, _lines = lane(interactive=True)

    assert offered == [(bt.CLAUDE, bt.CODEX, bt.PI)]
    assert credentials == list(selected)
    assert discoveries == [selected]
    assert set(seen["poster"]) == set(selected)
    assert set(seen["device_id"]) == set(selected)


@pytest.mark.parametrize("action", ["BACK", "SKIP"])
def test_leaving_history_selection_does_not_scan_or_upload(lane, monkeypatch, action):
    from probe.cli import capabilities, tui

    monkeypatch.setattr(bt, "choose_sources", lambda available: getattr(tui, action))
    monkeypatch.setattr(bt, "discover", lambda **kwargs: pytest.fail("scanned after Back"))
    monkeypatch.setattr(
        capabilities, "resolved_capture_credential", lambda source: pytest.fail("paired after Back")
    )
    seen, lines = lane(interactive=True)
    assert seen == {}
    assert lines == ["Skipped the agent sessions."]


def test_headless_explicit_sources_restrict_the_upload(lane):
    seen, _lines = lane(sources=(bt.CODEX,))
    assert set(seen["poster"]) == {bt.CODEX}


def test_source_picker_defaults_every_detected_history_to_checked(monkeypatch):
    import questionary
    from probe.cli import tui

    selected = (bt.CLAUDE, bt.CODEX)
    seen = {}
    original = questionary.checkbox

    def checkbox(message, **kwargs):
        seen["rows"] = [row for row in kwargs["choices"] if getattr(row, "value", None) in selected]
        return original(message, **kwargs)

    monkeypatch.setattr(questionary, "checkbox", checkbox)
    monkeypatch.setattr(tui, "ask", lambda question, **kwargs: list(selected))
    # sectioned is the shared layout integration; selection defaults are
    # independent of the renderer and stay testable without a terminal.
    monkeypatch.setattr(tui, "sectioned", lambda question, **kwargs: question, raising=False)
    assert bt.choose_sources(selected) == selected
    assert [row.value for row in seen["rows"]] == list(selected)
    assert all(row.checked for row in seen["rows"])


@pytest.mark.parametrize("answer", ["import", "skip"])
def test_background_handoff_queues_only_after_the_review_without_uploading(lane, monkeypatch, answer):
    from probe.cli import import_jobs, tui

    queued = []
    monkeypatch.setattr(
        import_jobs, "enqueue",
        lambda kind, payload, label: queued.append((kind, payload, label)) or {"id": "job-1"},
    )
    monkeypatch.setattr(bt, "_background_identity", lambda client: {
        "context": "default", "base_url": "http://x", "customer_id": "team", "user_id": "user",
        "workspace": None,
    })
    monkeypatch.setattr(tui, "review", lambda *a, **k: answer)
    monkeypatch.setattr(bt, "_execute_census", lambda *a, **k: pytest.fail("foreground upload"))
    seen, lines = lane(interactive=True, background=True)
    assert seen == {}
    if answer == "skip":
        assert queued == []
        return
    kind, payload, label = queued[0]
    assert kind == "transcripts"
    assert len(payload["files"]) == 1
    approved = payload["files"][0]
    assert approved["session_id"] == "s-1"
    assert approved["sha256"] == bt.prefix_hash(Path(approved["path"]), approved["size"])
    assert '"token"' not in json.dumps(payload) and '"tok"' not in json.dumps(payload)
    assert any("job-1" in line for line in lines)


def test_headless_background_flag_preserves_foreground_execution(lane, monkeypatch):
    monkeypatch.setattr(bt, "_background_payload", lambda *a, **k: pytest.fail("queued headless command"))
    seen, _lines = lane(background=True)
    assert "poster" in seen


@pytest.mark.parametrize("state,wording", [("failed", "needs attention"), ("succeeded", "already complete")])
def test_repeated_transcript_approval_reports_the_existing_job_state(lane, monkeypatch, state, wording):
    from probe.cli import import_jobs, tui

    monkeypatch.setattr(
        import_jobs, "enqueue", lambda *a, **k: {
            "id": "existing-job", "state": state,
            "error": "Restore the approved pairing." if state == "failed" else None,
        },
    )
    monkeypatch.setattr(bt, "_background_payload", lambda *a, **k: {"approved": True})
    monkeypatch.setattr(tui, "review", lambda *a, **k: "import")
    seen, lines = lane(interactive=True, background=True)
    text = "\n".join(lines)
    assert seen == {}
    assert f"Session import {wording}: existing-job" in text
    assert "Existing imports" in text
    assert "queued" not in text and "continues in the background" not in text
    assert ("Restore the approved pairing." in text) == (state == "failed")


@pytest.mark.parametrize("response", ["skip", "escape"])
def test_conversation_gate_skips_before_upload_or_ledger_write(lane, monkeypatch, tmp_path, response):
    from probe.cli import tui

    def review(title, lines, choices):
        assert title == "Agent sessions on this machine"
        assert any(value == "skip" for _, value in choices)
        return tui.BACK if response == "escape" else response

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(bt, "fetch_ingest_state", lambda *a: pytest.fail("read before consent"))
    seen, lines = lane(interactive=True)
    assert not seen
    assert lines == ["Skipped the agent sessions."]
    assert not (tmp_path / "ledger.jsonl").exists()


def test_conversation_gate_ctrl_c_aborts_before_upload(lane, monkeypatch, tmp_path):
    from probe.cli import tui

    monkeypatch.setattr(tui, "review", lambda *a: None)
    monkeypatch.setattr(bt, "fetch_ingest_state", lambda *a: pytest.fail("read before consent"))
    with pytest.raises(KeyboardInterrupt):
        lane(interactive=True)
    assert not (tmp_path / "ledger.jsonl").exists()


def test_conversation_gate_import_requires_explicit_choice_and_shows_scope(lane, monkeypatch):
    from probe.cli import tui

    def review(title, lines, choices):
        text = "\n".join(lines)
        assert "whole machine" in text
        assert "no project or experiment attached" in text
        assert choices[0] == ("Import these sessions", "import")
        return choices[0][1]  # Preserve Enter-to-import after reviewing the scope.

    monkeypatch.setattr(tui, "review", review)
    seen, _ = lane(interactive=True)
    assert seen["assignments"] == {}


@pytest.mark.parametrize("interactive,yes", [(False, False), (False, True), (True, True)])
def test_conversation_gate_preserves_headless_and_yes_behavior(lane, monkeypatch, interactive, yes):
    from probe.cli import tui

    monkeypatch.setattr(tui, "review", lambda *a: pytest.fail("unexpected prompt"))
    seen, _ = lane(interactive=interactive, yes=yes)
    assert "ledger" in seen


# --- where the transcripts are ----------------------------------------------


def _tap_db(plugin: Path, paths: list[str]) -> Path:
    plugin.mkdir(parents=True, exist_ok=True)
    db = plugin / "state.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE file_offsets (path TEXT PRIMARY KEY, session_id TEXT)")
        for i, path in enumerate(paths):
            conn.execute("INSERT INTO file_offsets VALUES (?, ?)", (path, f"s{i}"))
    return plugin


def test_the_root_is_learned_from_where_the_tap_has_seen_transcripts(tmp_path, monkeypatch) -> None:
    """The strongest evidence available, and it needs no guessing.

    `file_offsets.path` holds paths the AGENT handed the tap, so they are
    ground truth regardless of where the config directory was moved to.
    """
    monkeypatch.delenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", raising=False)
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    relocated = tmp_path / "elsewhere" / "projects"
    _cc_session(relocated, "-proj", "aaaa0001-0000-4000-8000-aaaa00000001", "/proj")
    plugin = _tap_db(
        tmp_path / "plugin",
        [str(relocated / "-proj" / "aaaa0001-0000-4000-8000-aaaa00000001.jsonl")],
    )

    assert relocated in bt.transcript_roots(bt.CLAUDE, plugin)


def test_a_relocated_config_dir_is_found_without_the_tap(tmp_path, monkeypatch) -> None:
    """CLAUDE_CONFIG_DIR is the documented knob, and nothing consulted it."""
    monkeypatch.delenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", raising=False)
    config = tmp_path / "cfg"
    (config / "projects").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))

    assert bt.transcript_roots(bt.CLAUDE, None) == [config / "projects"]


def test_an_explicit_override_is_not_second_guessed(tmp_path, monkeypatch) -> None:
    """Adding the learned and default roots beside it would walk trees the
    caller deliberately excluded."""
    explicit = tmp_path / "explicit"
    explicit.mkdir()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", str(explicit))
    plugin = _tap_db(tmp_path / "plugin", [str(tmp_path / "other" / "-p" / "x.jsonl")])

    assert bt.transcript_roots(bt.CLAUDE, plugin) == [explicit]


def test_two_config_dirs_are_both_walked(tmp_path, monkeypatch) -> None:
    """One machine can hold more than one; finding only the first is a
    silent partial answer."""
    monkeypatch.delenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", raising=False)
    monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
    first = tmp_path / "a" / "projects"
    second = tmp_path / "b" / "projects"
    _cc_session(first, "-one", "aaaa0002-0000-4000-8000-aaaa00000002", "/one")
    _cc_session(second, "-two", "aaaa0003-0000-4000-8000-aaaa00000003", "/two")
    plugin = _tap_db(
        tmp_path / "plugin",
        [
            str(first / "-one" / "aaaa0002-0000-4000-8000-aaaa00000002.jsonl"),
            str(second / "-two" / "aaaa0003-0000-4000-8000-aaaa00000003.jsonl"),
        ],
    )

    roots = bt.transcript_roots(bt.CLAUDE, plugin)
    assert first in roots and second in roots

    monkeypatch.setattr(bt, "claude_root", lambda: tmp_path / "nothing-here")
    census = bt.discover(plugin_dirs={bt.CLAUDE: plugin})
    assert census.sessions == 2, "a second config dir must not be invisible"


def test_a_codex_root_is_learned_through_its_date_partitions(tmp_path) -> None:
    """Codex nests `<root>/YYYY/MM/DD/rollout-*.jsonl`, so the root is three
    levels up rather than one -- getting the depth wrong would walk a day."""
    root = tmp_path / "sessions"
    day = root / "2026" / "08" / "21"
    day.mkdir(parents=True)
    session = "01a02357-44b8-7703-8ded-974b57fd1a8a"
    (day / f"rollout-2026-08-21T08-01-56-{session}.jsonl").write_text("{}\n")
    plugin = _tap_db(
        tmp_path / "plug",
        [str(day / f"rollout-2026-08-21T08-01-56-{session}.jsonl")],
    )

    assert bt.learned_roots(bt.CODEX, plugin) == [root]


# --- the second denominator --------------------------------------------------


def _history(root: Path, entries: list[tuple[str, str]], *, at: float | None = None) -> None:
    """`root` is the projects dir; history.jsonl sits beside it.

    `at` defaults to NOW because the count is bounded by the oldest surviving
    transcript: an entry older than that is presumed pruned, not never-written.
    """
    import time

    stamp = int((at if at is not None else time.time() + 60) * 1000)
    root.parent.mkdir(parents=True, exist_ok=True)
    (root.parent / "history.jsonl").write_text(
        "\n".join(
            json.dumps({"sessionId": sid, "project": cwd, "display": "x", "timestamp": stamp})
            for sid, cwd in entries
        )
        + "\n",
        encoding="utf-8",
    )


def test_sessions_that_left_no_transcript_are_counted_not_hidden(roots) -> None:
    """The walk's own total is not the population.

    Measured on a real machine: 201 sessions in history, 179 transcripts, 167
    in both -- so a bare walk under-reports by about 16% and says nothing.
    """
    claude, _ = roots
    present = "aaaa0004-0000-4000-8000-aaaa00000004"
    _cc_session(claude, "-proj", present, "/proj")
    _history(claude, [(present, "/proj"), ("ghost-1111", "/home/dev"), ("ghost-2222", "/x")])

    census = bt.discover()

    assert census.sessions == 1
    assert census.known_no_transcript == 2


def test_a_captured_session_is_not_counted_as_missing(roots) -> None:
    """It HAS a file; being excluded from the upload is a different fact."""
    claude, _ = roots
    tracked = "aaaa0005-0000-4000-8000-aaaa00000005"
    _cc_session(claude, "-proj", tracked, "/proj")
    _history(claude, [(tracked, "/proj")])

    census = bt.discover(tracked={tracked})

    assert census.captured_live == 1
    assert census.known_no_transcript == 0


def test_a_missing_or_torn_history_costs_nothing(roots) -> None:
    claude, _ = roots
    _cc_session(claude, "-proj", "aaaa0006-0000-4000-8000-aaaa00000006", "/proj")
    assert bt.discover().known_no_transcript == 0  # no history.jsonl at all

    import time

    recent = int((time.time() + 60) * 1000)
    (claude.parent / "history.jsonl").write_text(
        json.dumps({"sessionId": "ok-1", "timestamp": recent}) + '\n{"torn": ', "utf-8"
    )
    assert bt.discover().known_no_transcript == 1, "the torn line costs one entry, not the file"


def test_the_gate_names_the_sessions_that_left_no_transcript(roots) -> None:
    claude, _ = roots
    _cc_session(claude, "-proj", "aaaa0007-0000-4000-8000-aaaa00000007", "/proj")
    census = bt.discover()
    census.known_no_transcript = 34

    text = "\n".join(bt.gate_lines(census, {}))

    assert "34 more recent session(s) have no transcript on disk" in text


def test_a_session_older_than_every_surviving_transcript_is_not_claimed(roots) -> None:
    """History is never pruned; transcripts are (`cleanupPeriodDays`, 30 days).

    So an entry older than the oldest file still on disk was almost certainly
    DELETED rather than never written. Counting it would put a number on the
    consent screen that grows for the life of the machine while saying
    something untrue about nearly every entry in it.
    """
    claude, _ = roots
    _cc_session(claude, "-proj", "aaaa0008-0000-4000-8000-aaaa00000008", "/proj")
    _history(claude, [("ancient-1", "/old"), ("ancient-2", "/old")], at=0.0)

    assert bt.discover().known_no_transcript == 0


def test_with_no_transcripts_at_all_nothing_is_claimed(roots) -> None:
    """No surviving file means no horizon to draw, so no claim is made."""
    claude, _ = roots
    _history(claude, [("ghost", "/x")])

    census = bt.discover()

    assert census.sessions == 0
    assert census.known_no_transcript == 0


def test_codex_home_is_honoured(tmp_path, monkeypatch) -> None:
    """Codex's own relocation knob, already resolved elsewhere in this package."""
    monkeypatch.delenv("PRBE_CODEX_SESSIONS_DIR", raising=False)
    home = tmp_path / "codex-home"
    (home / "sessions").mkdir(parents=True)
    monkeypatch.setenv("CODEX_HOME", str(home))

    assert bt.codex_root() == home / "sessions"
    assert home / "sessions" in bt.transcript_roots(bt.CODEX, None)


def test_a_tilde_in_an_env_var_is_expanded(tmp_path, monkeypatch) -> None:
    """These are routinely set in a config file, where `~` arrives literally.

    Unexpanded it becomes a RELATIVE path that exists nowhere, and the honest
    "Looked in:" line would then name a directory nothing ever searched.
    """
    monkeypatch.delenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", raising=False)
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "~/alt-claude")

    root = bt.transcript_roots(bt.CLAUDE, None)[0]

    assert not str(root).startswith("~")
    assert root.is_absolute()


def test_a_relocated_dir_does_not_hide_the_original(tmp_path, monkeypatch) -> None:
    """Someone who moved their config still has months of history in the old
    place; replacing one root with the other drops that half silently."""
    monkeypatch.delenv("PROBE_RESEARCH_TAP_PROJECTS_DIR", raising=False)
    original = tmp_path / "home" / ".claude" / "projects"
    relocated = tmp_path / "data" / "claude" / "projects"
    _cc_session(original, "-old", "aaaa0009-0000-4000-8000-aaaa00000009", "/old")
    _cc_session(relocated, "-new", "aaaa000a-0000-4000-8000-aaaa0000000a", "/new")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(relocated.parent))
    monkeypatch.setattr(bt, "claude_root", lambda: original)

    roots = bt.transcript_roots(bt.CLAUDE, None)

    assert relocated in roots and original in roots
    assert bt.discover().sessions == 2


def test_an_off_layout_row_cannot_turn_a_home_directory_into_a_root(tmp_path) -> None:
    """The parent index assumes a layout the tap does not enforce.

    A Codex rollout stored flat makes `parents[3]` something like `/home`, and
    a two-segment path makes `parents[1]` `/`. Walking either would rglob a
    whole home directory and offer every `.jsonl` under it for upload. Both
    agents fix their own directory name, so the name is the guard.
    """
    plugin = _tap_db(
        tmp_path / "plug",
        [
            "/home/u/.codex/sessions/rollout-2026-08-21T08-01-56-"
            "01a02357-44b8-7703-8ded-974b57fd1a8a.jsonl",  # flat -> parents[3] == /home
            "/foo/bar.jsonl",  # shallow -> parents[1] == /
        ],
    )

    assert bt.learned_roots(bt.CODEX, plugin) == []
    assert bt.learned_roots(bt.CLAUDE, plugin) == []


def test_a_foreign_jsonl_beside_claude_sessions_is_not_a_session(tmp_path):
    """The Workflow tool drops journal.jsonl right beside real transcripts.
    Its stem used to become session id "journal", which passed discovery and
    crashed the whole run one server round-trip later ("malformed session
    id"). Non-uuid stems must die at discovery, like sidechains — this
    blocked the first real pi transcript re-run on 2026-08-29."""
    from probe.cli.backfill_transcripts import CLAUDE, session_id_for

    assert session_id_for(tmp_path / "journal.jsonl", CLAUDE) is None
    assert session_id_for(tmp_path / "notes.jsonl", CLAUDE) is None
    assert (
        session_id_for(tmp_path / "33333333-3333-4333-8333-333333333333.jsonl", CLAUDE)
        == "33333333-3333-4333-8333-333333333333"
    )
