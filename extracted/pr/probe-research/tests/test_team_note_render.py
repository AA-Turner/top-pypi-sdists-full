"""The render pipeline: one sync, both harnesses' instruction files.

Every test here redirects CLAUDE_CONFIG_DIR, CODEX_HOME and XDG_STATE_HOME into
tmp_path. Nothing in this file may touch the real ~/.claude or ~/.codex -- this
suite runs on a shared box where other agent sessions read those files live.
"""

from __future__ import annotations

import datetime as dt
import json

from dataclasses import dataclass

import pytest

from probe.cli import agent_rules, team_note_file


@dataclass
class _Settings:
    base_url: str = "https://example.invalid"
    token: str = "probe_pat_test"


@pytest.fixture
def harnesses(tmp_path, monkeypatch):
    claude = tmp_path / "claude"
    codex = tmp_path / "codex"
    claude.mkdir()
    codex.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    monkeypatch.setenv("CODEX_HOME", str(codex))
    monkeypatch.setenv("KIMI_CODE_HOME", str(tmp_path / "kimi"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    # These tests are about two instruction files; Kimi Code's third is
    # covered by `test_kimi_code_gets_the_note_beside_its_pointer`.
    monkeypatch.setattr(team_note_file, "RENDER_SOURCES", ("claude_code", "codex"))
    return claude / "CLAUDE.md", codex / "AGENTS.md"


def _opt_in(path, text: str = "") -> None:
    """`text`, then the pointer block: the file of a machine that kept the rules."""
    path.write_text(text, encoding="utf-8")
    agent_rules.install(path)


@pytest.fixture
def opted_in(harnesses):
    """Both files carry the pointer block. The note renders only beside it:
    an absent pointer is the `--no-agent-rules` opt-out."""
    for path in harnesses:
        _opt_in(path)
    return harnesses


def test_one_render_writes_both_harnesses(opted_in) -> None:
    """The measured failure this exists to fix: each harness's copy only
    refreshed when THAT harness ran, so the two drifted 7 hours apart."""
    claude_md, agents_md = opted_in
    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.ok, report.failures
    assert set(report.written) == {"claude_code", "codex"}
    document = team_note_file.paths_for(_Settings()).document
    for path in (claude_md, agents_md):
        text = path.read_text(encoding="utf-8")
        assert agent_rules.NOTE_BLOCK.begin in text
        assert "- one" in text
        # BOTH name the SAME editable file. Each naming its own was the bug:
        # three documents behind one base copy, pushed over each other at every
        # session start. Neither block may name a path under a harness home.
        assert str(document) in text
        assert str(path.parent / "probe-team-note.md") not in text


def test_an_unchanged_note_writes_nothing(opted_in) -> None:
    """`Stop` fires every turn on every session. Without this short circuit,
    13 sessions rewrite two files per turn for content that changes daily."""
    claude_md, _ = opted_in
    settings = _Settings()
    team_note_file.render_blocks("## rules\n\n- one", settings=settings)
    before = claude_md.stat().st_mtime_ns

    report = team_note_file.render_blocks("## rules\n\n- one", settings=settings)
    assert set(report.unchanged) == {"claude_code", "codex"}
    assert report.written == ()
    assert claude_md.stat().st_mtime_ns == before


def test_an_edited_note_does_write(opted_in) -> None:
    claude_md, _ = opted_in
    settings = _Settings()
    team_note_file.render_blocks("## rules\n\n- one", settings=settings)
    report = team_note_file.render_blocks("## rules\n\n- one\n- two", settings=settings)
    assert set(report.written) == {"claude_code", "codex"}
    assert "- two" in claude_md.read_text(encoding="utf-8")


def test_over_budget_writes_a_pointer_and_never_a_partial_note(opted_in) -> None:
    """Partial content under a header calling itself a copy of the team note
    reads as complete. A pointer is honest about carrying nothing."""
    claude_md, _ = opted_in
    huge = "## big\n\n" + ("x" * (team_note_file.INSTRUCTION_FILE_MAX_BYTES + 5_000))
    report = team_note_file.render_blocks(huge, settings=_Settings())

    assert set(report.pointer_only) == {"claude_code", "codex"}
    assert report.ok, report.failures
    text = claude_md.read_text(encoding="utf-8")
    assert "did not fit here" in text
    assert "xxxxx" not in text
    assert len(text) <= team_note_file.INSTRUCTION_FILE_MAX_BYTES


def test_a_file_too_full_for_even_a_pointer_is_refused_and_recorded(harnesses) -> None:
    """Refusing is the honest answer, but only if somebody hears about it."""
    claude_md, agents_md = harnesses
    for path in (claude_md, agents_md):
        _opt_in(path, "y" * (team_note_file.INSTRUCTION_FILE_MAX_BYTES - 50))

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.written == () and report.pointer_only == ()
    assert len(report.failures) == 2
    assert "too full" in report.failures[0]
    # And it survives for the next session to say out loud.
    pending = team_note_file.pending_render_failures()
    assert len(pending) == 2
    # The researcher's own bytes were not touched.
    assert claude_md.read_text(encoding="utf-8").startswith("yyyy")


def test_a_damaged_block_is_left_alone_not_repaired(harnesses) -> None:
    """Auto-repair of a file humans also edit destroys edits it did not
    understand. Two BEGIN markers is unreadable, not fixable."""
    claude_md, _ = harnesses
    poisoned = f"{agent_rules.NOTE_BLOCK.begin}\nstray\n{agent_rules.NOTE_BLOCK.begin}\nx\n{agent_rules.NOTE_BLOCK.end}\n"
    claude_md.write_text(poisoned, encoding="utf-8")

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert "claude_code" not in report.written
    assert any("damaged" in f for f in report.failures)
    assert claude_md.read_text(encoding="utf-8") == poisoned


def test_a_successful_render_clears_a_previous_failure(harnesses) -> None:
    """A stale warning is its own bug: an agent told the note failed to render
    when it has since succeeded stops trusting the warning."""
    claude_md, agents_md = harnesses
    for path in (claude_md, agents_md):
        _opt_in(path, "y" * (team_note_file.INSTRUCTION_FILE_MAX_BYTES - 50))
    team_note_file.render_blocks("## rules", settings=_Settings())
    assert team_note_file.pending_render_failures()

    for path in (claude_md, agents_md):
        _opt_in(path, "small\n")
    report = team_note_file.render_blocks("## rules", settings=_Settings())

    assert report.ok
    assert team_note_file.pending_render_failures() == []


def test_the_render_preserves_the_pointer_block_and_human_prose(harnesses) -> None:
    claude_md, _ = harnesses
    claude_md.write_text("# my rules\n\nkeep me\n", encoding="utf-8")
    agent_rules.install(claude_md)

    team_note_file.render_blocks("## note\n\nbody", settings=_Settings())

    text = claude_md.read_text(encoding="utf-8")
    assert "## Probe Research" in text
    assert "keep me" in text
    assert text.count(agent_rules.NOTE_BLOCK.begin) == 1


def test_notes_sync_actually_renders_the_blocks(opted_in, monkeypatch, capsys) -> None:
    """WIRING, not capability. Every other test in this file calls
    render_blocks directly, which proves the function works and says nothing
    about whether anything calls it. Delete the call site in `notes sync` and
    those tests all stay green; this one goes red.

    Only the network is faked.
    """
    import contextlib
    import importlib

    main = importlib.import_module("probe.cli.main")

    claude_md, agents_md = opted_in
    monkeypatch.setenv("PROBE_BASE_URL", "https://example.invalid")
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")

    @contextlib.contextmanager
    def _fake_client():
        yield object()

    monkeypatch.setattr(main, "_client", _fake_client)
    monkeypatch.setattr(
        team_note_file,
        "reconcile",
        lambda client, where: (
            team_note_file.Report(pulled=True, version=7),
            "## from the server\n\nSENTINEL-WIRED",
        ),
    )

    main.notes_sync(push_only=False, pull_only=False)

    for path in (claude_md, agents_md):
        text = path.read_text(encoding="utf-8")
        assert "SENTINEL-WIRED" in text, f"{path} never got the block"
        assert agent_rules.NOTE_BLOCK.begin in text


def test_push_only_renders_nothing_because_it_never_fetched(opted_in, monkeypatch) -> None:
    """`--push-only` is the NORMAL Stop path, fired every turn -- NOT a failure.

    This test was originally named for a failed fetch, which conflated two
    different things and quietly encoded a gap as correct behaviour: nobody
    noticed that the per-turn hook therefore never rendered at all. It asserts
    the real invariant -- a push that fetched nothing has no authoritative text,
    and rendering from the local copy instead would reintroduce exactly the
    staleness the cross-render exists to kill.

    SessionEnd is the event that reconciles and renders; see
    `test_sessionend_reconciles_while_stop_only_pushes`.
    """
    import contextlib
    import importlib

    main = importlib.import_module("probe.cli.main")

    claude_md, _ = opted_in
    monkeypatch.setenv("PROBE_BASE_URL", "https://example.invalid")
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")

    # Seed a good block first.
    team_note_file.render_blocks("## good\n\nCURRENT-CONTENT", settings=_Settings())
    before = claude_md.read_text(encoding="utf-8")

    @contextlib.contextmanager
    def _fake_client():
        yield object()

    monkeypatch.setattr(main, "_client", _fake_client)
    # push_only never yields text -- the fetch-failed shape.
    monkeypatch.setattr(
        team_note_file, "push", lambda client, where: team_note_file.Report(pushed=True, version=7)
    )

    main.notes_sync(push_only=True, pull_only=False)

    assert claude_md.read_text(encoding="utf-8") == before
    assert "CURRENT-CONTENT" in claude_md.read_text(encoding="utf-8")


def test_a_stray_import_in_the_note_is_neutralised(opted_in) -> None:
    """The note lands INSIDE CLAUDE.md, whose own content is import-parsed four
    levels deep. Dropping our own @import line did not remove this danger --
    the danger was never our line, it was the note's content."""
    claude_md, _ = opted_in
    body = "## rules\n\nSee @docs/secret.md and mail rich@example.com and `@pytest.mark.fleet_sweep`."
    team_note_file.render_blocks(body, settings=_Settings())

    text = claude_md.read_text(encoding="utf-8")
    assert "`@docs/secret.md`" in text          # escaped
    assert "rich@example.com" in text           # an email is not an import
    assert "`@pytest.mark.fleet_sweep`" in text  # already in a span, untouched
    assert "\n@docs" not in text and " @docs" not in text


def test_a_note_carrying_our_own_marker_is_refused_not_mangled(harnesses) -> None:
    claude_md, agents_md = harnesses
    claude_md.write_text("untouched\n", encoding="utf-8")
    body = f"## rules\n\nsomeone pasted {agent_rules.NOTE_BLOCK.end} in here"

    report = team_note_file.render_blocks(body, settings=_Settings())

    assert report.written == () and report.pointer_only == ()
    assert len(report.failures) == 2
    assert "managed marker" in report.failures[0]
    assert claude_md.read_text(encoding="utf-8") == "untouched\n"
    assert not agents_md.exists()


def test_escaping_is_stable_so_the_hash_does_not_thrash(opted_in) -> None:
    """The stamp is computed AFTER escaping, so an escaped body must escape to
    itself -- otherwise every render sees a different hash and writes again,
    defeating the short circuit that keeps Stop cheap."""
    claude_md, _ = opted_in
    body = "## rules\n\nSee @docs/api.md"
    settings = _Settings()
    team_note_file.render_blocks(body, settings=settings)
    before = claude_md.stat().st_mtime_ns
    report = team_note_file.render_blocks(body, settings=settings)
    assert set(report.unchanged) == {"claude_code", "codex"}
    assert claude_md.stat().st_mtime_ns == before


def test_the_budget_is_measured_in_bytes_not_code_points(opted_in) -> None:
    """REGRESSION. `project_doc_max_bytes` is a BYTE budget and the team note is
    full of em-dashes and middots, so measuring len(str) under-counts every
    non-ASCII character by one to three bytes -- in the direction that overruns
    the cap."""
    claude_md, _ = opted_in
    # Every character is 3 bytes in UTF-8, so a body that "fits" by code points
    # is three times over by bytes.
    body = "## rules\n\n" + ("中" * (team_note_file.INSTRUCTION_FILE_MAX_BYTES // 2))
    assert len(body) < team_note_file.INSTRUCTION_FILE_MAX_BYTES
    assert len(body.encode("utf-8")) > team_note_file.INSTRUCTION_FILE_MAX_BYTES

    report = team_note_file.render_blocks(body, settings=_Settings())
    assert set(report.pointer_only) == {"claude_code", "codex"}
    assert len(claude_md.read_text(encoding="utf-8").encode("utf-8")) <= team_note_file.INSTRUCTION_FILE_MAX_BYTES


def test_the_lock_is_keyed_on_the_file_not_the_credential(harnesses, monkeypatch) -> None:
    """REGRESSION, and the rule now holds for BOTH files.

    A lock has to name what it protects. This test was written when only the
    instruction file broke that rule -- `Paths.lock` was keyed on
    origin+identity, which was right for the sync's per-credential base copy and
    wrong for a user-global `CLAUDE.md`, so two contexts on one machine took two
    different locks and wrote the same file.

    The DOCUMENT then became one file per machine too, which put it in exactly
    the same position: two credentials' sessions holding two different locks
    while parking, replacing and merging one shared file. So the sync lock is
    now keyed on the document as well. The per-credential thing is the base
    copy, and it is guarded by the same lock rather than by its own.
    """
    claude_md, _ = harnesses
    a = team_note_file.paths_for(_Settings(token="probe_pat_A"))
    b = team_note_file.paths_for(_Settings(token="probe_pat_B"))
    assert a.document == b.document, "one document per machine"
    assert a.lock == b.lock, "and therefore ONE lock over it, whatever the credential"
    assert a.base != b.base, "the base copy stays per credential"

    # The instruction file they both write also resolves to ONE lock.
    assert team_note_file.instruction_lock_path(claude_md) == team_note_file.instruction_lock_path(claude_md)
    assert team_note_file.instruction_lock_path(claude_md) != team_note_file.instruction_lock_path(
        claude_md.parent / "AGENTS.md"
    )


def test_a_pointer_upgrades_back_to_the_full_note_when_space_frees_up(opted_in) -> None:
    """The form is part of the block's identity. Stamping a pointer with the body
    hash alone would make it report itself current forever, so a machine that
    trimmed its instruction file would never get the real note back."""
    claude_md, agents_md = opted_in
    # STAMPED TODAY so the audit advisory stays silent: it fires on an
    # unstamped note ("never audited"), and its bytes land inside the window
    # this test sizes, putting BOTH forms over budget and turning a pointer
    # assertion into a failure assertion. The advisory's own effect on the fit
    # decision has its own case below.
    body = f"<!-- audited {dt.date.today().isoformat()} -->\n## rules\n\n- one\n- two"
    # SIZED FROM THE RENDERED BLOCKS, not a guessed constant: the fixture has to
    # sit in the window where the pointer fits and the full block does not, and
    # that window moves whenever the preface wording changes.
    # Per harness: the two document paths differ in length, so their blocks do
    # too, and one filler size cannot put both in the window.
    for path in (claude_md, agents_md):
        doc = str(path.parent / "probe-team-note.md")
        full_len = len(agent_rules.render_note_block(body, document=doc).encode("utf-8"))
        ptr_len = len(
            agent_rules.render_note_block(body, document=doc, pointer_only=True).encode("utf-8")
        )
        assert ptr_len < full_len, "pointer must be smaller than the full block"
        rules = path.read_text(encoding="utf-8")  # the pointer block, from `opted_in`
        filler = team_note_file.INSTRUCTION_FILE_MAX_BYTES - full_len + 1 - len(rules.encode("utf-8"))
        path.write_text(rules + "z" * filler, encoding="utf-8")

    first = team_note_file.render_blocks(body, settings=_Settings())
    assert set(first.pointer_only) == {"claude_code", "codex"}
    assert "did not fit here" in claude_md.read_text(encoding="utf-8")

    # The human trims their own file; the next sync must upgrade, not skip.
    for path in (claude_md, agents_md):
        text = path.read_text(encoding="utf-8")
        marker = text.index(agent_rules.NOTE_BLOCK.begin)
        rules = text[: text.index(agent_rules.END_MARKER) + len(agent_rules.END_MARKER)]
        path.write_text(rules + "\nsmall\n\n" + text[marker:], encoding="utf-8")

    second = team_note_file.render_blocks(body, settings=_Settings())
    assert set(second.written) == {"claude_code", "codex"}, second
    assert "- two" in claude_md.read_text(encoding="utf-8")


def test_a_status_file_that_is_not_an_object_fails_open(harnesses) -> None:
    """The one path whose whole job is to fail open must not raise. A bare JSON
    list made `.get` throw AttributeError, which is not a ValueError and so
    escaped the guard."""
    path = team_note_file.render_failure_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    for junk in ('["a","b"]', '"just a string"', "42", "null"):
        path.write_text(junk, encoding="utf-8")
        assert team_note_file.pending_render_failures() == []


def test_an_undecodable_instruction_file_is_recorded_not_raised(opted_in) -> None:
    """UnicodeDecodeError is a ValueError, NOT an OSError -- the same trap
    apply_agent_rules already documents. One latin-1 byte would otherwise escape
    the handler and leave the other harness unrendered."""
    claude_md, agents_md = opted_in
    claude_md.write_bytes(b"caf\xe9 rules\n")  # latin-1, invalid utf-8

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert "claude_code" not in report.written
    assert any("claude_code" in f for f in report.failures), report.failures
    # The OTHER harness still rendered -- one bad file does not stop the sweep.
    assert "codex" in report.written
    assert agent_rules.NOTE_BLOCK.begin in agents_md.read_text(encoding="utf-8")


def test_render_blocks_takes_the_file_lock_not_the_credential_lock() -> None:
    """STATIC TRIPWIRE, and deliberately not a behavioural test.

    `test_the_lock_is_keyed_on_the_file_not_the_credential` proves the helper
    computes the right path and says NOTHING about whether render_blocks calls
    it -- swapping the call back to `where.lock` leaves that test green.

    TWO BEHAVIOURAL ATTEMPTS WERE WRITTEN AND BOTH PASSED WITH THE LOCK REMOVED,
    which is why this stands in their place. Six concurrent identical renders
    cannot show a lost update, because `write_text_atomic` lands a whole file and
    every writer produced the same bytes. Holding the lock in another process and
    mutating the file underneath does not work either: the outside write lands
    after the render regardless of ordering, so its presence proves nothing. A
    real one needs a seam inside the critical section, and test-only machinery in
    the write path is a worse trade than this.

    The proof is therefore split. The PRIMITIVE excludes -- covered by
    `test_hw_monitor.py::test_no_rank_env_falls_back_to_file_lock_single_winner`
    and `test_backfill_ledger_contention.py`. The CALL SITE uses it -- covered
    here, and mutation-checked.
    """
    import inspect

    source = inspect.getsource(team_note_file.render_blocks)
    assert "instruction_lock_path(instruction)" in source, (
        "render_blocks must lock the instruction FILE; a credential-scoped lock "
        "does not protect a user-global path"
    )
    assert "file_lock(where.lock)" not in source, (
        "where.lock is keyed on origin+identity -- correct for the sync's base "
        "copy, wrong for the shared instruction file"
    )


def test_sessionend_reconciles_while_stop_only_pushes(tmp_path) -> None:
    """BEHAVIOURAL: run the hook script with a stub `probe` and see what it calls.

    Stop fires every turn, so it must stay --push-only. SessionEnd fires once and
    reconciles, which is what re-renders the block. Before this split, an edit
    made in session N first reached the block session N+2 read: pushed at N,
    rendered at N+1's start, visible at N+2.
    """
    import os
    import subprocess
    import time
    from pathlib import Path

    script = Path(__file__).resolve().parents[1] / "plugins/probe-research/hooks/team-note-sync.sh"
    assert script.exists(), script

    seq = iter(range(100))

    def invoked(event: str | None) -> str:
        bin_dir = tmp_path / f"bin-{next(seq)}-{event or 'unset'}"
        bin_dir.mkdir()
        log = bin_dir / "invoked.txt"
        stub = bin_dir / "probe"
        stub.write_text(f'#!/usr/bin/env bash\nprintf "%s" "$*" > {log}\n')
        stub.chmod(0o755)
        env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}", HOME=str(tmp_path))
        env.pop("PROBE_HOOK_EVENT", None)
        if event:
            env["PROBE_HOOK_EVENT"] = event
        subprocess.run(["bash", str(script)], env=env, check=True, timeout=30)
        # The hook detaches on purpose, so wait for the child rather than the hook.
        for _ in range(100):
            if log.exists() and log.read_text().strip():
                return log.read_text().strip()
            time.sleep(0.05)
        return "<never invoked>"

    assert invoked("sessionend") == "notes sync"
    assert invoked(None) == "notes sync --push-only"
    # An unrecognised event takes the CHEAP path, so a future registration
    # cannot accidentally put a network pull on a per-turn hook.
    assert invoked("stop") == "notes sync --push-only"


def test_only_the_sessionend_registration_asks_for_a_reconcile() -> None:
    """The manifest half of the same invariant. Marking Stop instead would put a
    pull on every turn across every session on the machine."""
    import json
    from pathlib import Path

    manifest = json.loads(
        (Path(__file__).resolve().parents[1] / "plugins/probe-research/hooks/hooks.json").read_text()
    )
    marked = {}
    for event in ("Stop", "SessionEnd"):
        for group in manifest["hooks"][event]:
            for hook in group["hooks"]:
                if "team-note-sync.sh" in hook["command"]:
                    marked[event] = hook["command"]
    assert "PROBE_HOOK_EVENT=sessionend" in marked["SessionEnd"]
    assert "PROBE_HOOK_EVENT=sessionend" not in marked["Stop"]
    # BOTH state their mode: the variable is inherited, so leaving Stop unset
    # lets an ambient `sessionend` put a network pull on every turn.
    assert "PROBE_HOOK_EVENT=stop" in marked["Stop"]


def test_a_reconcile_whose_fetch_fails_leaves_both_files_byte_for_byte(opted_in, monkeypatch) -> None:
    """The coverage the rename gave up, restored as its own test.

    `--push-only` not rendering is a design choice. A reconcile whose FETCH
    fails is a different thing, and the invariant there is stronger: having
    already decided to render, we must not fall back to the local copy, because
    replacing current content with staler content is the one irreversible
    mistake in this path.
    """
    import contextlib
    import importlib

    main = importlib.import_module("probe.cli.main")
    claude_md, agents_md = opted_in
    monkeypatch.setenv("PROBE_BASE_URL", "https://example.invalid")
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")

    team_note_file.render_blocks("## good\n\nKNOWN-GOOD", settings=_Settings())
    before = {p: p.read_bytes() for p in (claude_md, agents_md)}

    @contextlib.contextmanager
    def _fake_client():
        yield object()

    monkeypatch.setattr(main, "_client", _fake_client)

    def _boom(client, where):
        raise RuntimeError("network is down")

    monkeypatch.setattr(team_note_file, "reconcile", _boom)

    with pytest.raises(RuntimeError):
        main.notes_sync(push_only=False, pull_only=False)

    for path, original in before.items():
        assert path.read_bytes() == original, f"{path} was rewritten on a failed fetch"
        assert b"KNOWN-GOOD" in path.read_bytes()


def test_the_sync_carries_a_stale_research_block_to_every_harness(harnesses) -> None:
    """THE MIGRATION CHANNEL, and why it hangs off this sync.

    The pointer block is written once by the wizard into a file no release can
    reach. `agent-rules refresh` existed to correct it and its docstring claimed
    the session-start hook called it -- no shipped plugin ever did, so bumping
    POINTER_VERSION corrected nothing and guidance shipped in one release was
    still missing from live sessions days later. Wiring a hook would repeat the
    fault: hooks ship in the PLUGIN, so the fix would need a plugin release AND
    a session restart. This sync is CLI-side and already fires on every Stop.
    """
    claude_md, agents_md = harnesses
    for path in (claude_md, agents_md):
        path.write_text(
            agent_rules.render_block(version=agent_rules.POINTER_VERSION - 1)
            + "\n# rules I wrote myself\n",
            encoding="utf-8",
        )

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.ok, report.failures
    assert set(report.rules_refreshed) == {"claude_code", "codex"}
    for path in (claude_md, agents_md):
        assert agent_rules.installed_version(path) == agent_rules.POINTER_VERSION
        text = path.read_text(encoding="utf-8")
        # The note landed too, and the researcher's own prose survived both.
        assert agent_rules.NOTE_BLOCK.begin in text
        assert "# rules I wrote myself" in text

    # Idempotent: a second sync finds nothing to refresh.
    again = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())
    assert again.rules_refreshed == ()


def test_the_sync_does_not_install_a_research_block_that_was_never_there(harnesses) -> None:
    """A file with no block opted out; a background sync must not opt it in --
    and that includes the NOTE. It used to render regardless ("the two blocks
    are independent"), which put Probe's text in the global CLAUDE.md of a
    customer who had passed `--no-agent-rules` (2026-10-02)."""
    claude_md, agents_md = harnesses
    for path in (claude_md, agents_md):
        path.write_text("# only my own rules\n", encoding="utf-8")

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.ok, report.failures
    assert report.rules_refreshed == () and report.written == () and report.pointer_only == ()
    assert set(report.opted_out) == {"claude_code", "codex"}
    for path in (claude_md, agents_md):
        assert path.read_text(encoding="utf-8") == "# only my own rules\n"


def test_no_file_is_created_for_a_harness_that_has_none(harnesses) -> None:
    """A Claude-only machine got a fresh ~/.codex/AGENTS.md from every sync."""
    claude_md, agents_md = harnesses
    _opt_in(claude_md)

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.written == ("claude_code",) and report.opted_out == ("codex",)
    assert not agents_md.exists()


def test_a_note_left_from_before_the_opt_out_is_removed(opted_in) -> None:
    """The opt-out used to drop the pointer and leave the note, which the next
    sync then kept current. Whatever left it there, the sync now takes it out."""
    claude_md, agents_md = opted_in
    team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())
    agent_rules.remove(claude_md)  # the old opt-out: pointer only
    assert agent_rules.NOTE_BLOCK.begin in claude_md.read_text(encoding="utf-8")

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.removed == ("claude_code",) and report.unchanged == ("codex",)
    assert agent_rules.NOTE_BLOCK.begin not in claude_md.read_text(encoding="utf-8")
    assert agent_rules.NOTE_BLOCK.begin in agents_md.read_text(encoding="utf-8")


def test_a_damaged_research_block_is_reported_as_itself_and_the_note_still_lands(
    harnesses,
) -> None:
    """It must not be reported as a damaged TEAM-NOTE block: different markers,
    different bytes, and an operator chasing the wrong block finds nothing."""
    claude_md, _ = harnesses
    claude_md.write_text(f"{agent_rules.BEGIN_MARKER}\n<!-- v1 -->\norphan\n", encoding="utf-8")

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert any("research-tracking block" in f for f in report.failures), report.failures
    assert not any("team-note block" in f for f in report.failures), report.failures
    # The note is independent of the damaged pointer block and still rendered.
    assert agent_rules.NOTE_BLOCK.begin in claude_md.read_text(encoding="utf-8")


def _note_block(text: str) -> str:
    """Just the managed team-note block, so a test can compare two renders."""
    begin, end = agent_rules.NOTE_BLOCK.begin, agent_rules.NOTE_BLOCK.end
    assert begin in text and end in text, text[:200]
    return text[text.index(begin) : text.index(end) + len(end)]


def test_the_block_cannot_be_tipped_to_pointer_by_a_due_audit(opted_in) -> None:
    """WHAT THE MOVE BOUGHT, pinned so it is not given back.

    While the advisory was rendered INTO the block it added bytes, so a note
    sitting just under its budget could be pushed to the pointer form BY the
    line telling you to audit it -- the reminder deleting the note it was about.
    That was survivable only because the advisory rode the pointer too.

    The line now travels on the UserPromptSubmit hook, so a due note and a note
    that is not due render byte-identical blocks and nothing can tip.
    """
    claude_md, _ = opted_in
    body = "<!-- audited 2026-01-01 -->\n## rules\n\n- one\n- two"
    doc = str(claude_md.parent / "probe-team-note.md")
    assert team_note_file.audit_advisory(
        body, source="claude_code", pct=0.95, baseline=None
    ), "a note over its budget must still be due"

    health = team_note_file.note_health_path()
    health.parent.mkdir(parents=True, exist_ok=True)
    health.write_text(
        json.dumps({"sources": {"claude_code": {"pct": 0.95}}}), encoding="utf-8"
    )
    team_note_file.render_blocks(body, settings=_Settings())
    due = _note_block(claude_md.read_text(encoding="utf-8"))

    health.write_text(
        json.dumps({"sources": {"claude_code": {"pct": 0.10}}}), encoding="utf-8"
    )
    team_note_file.render_blocks(body, settings=_Settings())
    quiet = _note_block(claude_md.read_text(encoding="utf-8"))

    assert "outgrown its budget" not in due
    assert due == quiet, "the block must not depend on whether an audit is due"


def test_the_first_render_on_a_fresh_machine_never_advises(opted_in) -> None:
    """BOOTSTRAP: the first render on a machine writes the measurement that every
    later size decision reads.

    The size half is derived from the LAST render's measurement, because writing
    a block changes the length it would be reporting. A machine with no health
    file has no last render, so nothing can say "over budget" yet; that render
    WRITES the measurement, and the hook that asks afterwards can. Since the
    dispatch left the block, the first half of this is now trivially true for
    every render -- what still matters, and is pinned here, is that the
    measurement lands.
    """
    claude_md, _ = opted_in
    assert not team_note_file.note_health_path().exists()

    huge = "<!-- audited 2026-01-01 -->\n## big\n\n" + ("x" * 28_000)
    first = team_note_file.render_blocks(huge, settings=_Settings())
    assert "outgrown its budget" not in claude_md.read_text(encoding="utf-8")

    # ...and the measurement it just wrote is what arms the next one.
    payload = json.loads(team_note_file.note_health_path().read_text(encoding="utf-8"))
    assert payload["sources"]["claude_code"]["pct"] >= team_note_file.AUDIT_SIZE_PCT
    assert first.ok or first.pointer_only


def test_kimi_code_is_a_render_target_from_its_registry_row() -> None:
    from probe.harness import get_registry

    assert "kimi_code" in team_note_file._render_sources()
    assert get_registry().get("kimi_code").team_note == "render"


def test_kimi_code_gets_the_note_beside_its_pointer(tmp_path, monkeypatch) -> None:
    """Kimi reads `$KIMI_CODE_HOME/AGENTS.md` (never `~/.agents/AGENTS.md`,
    which other tools read too); the note renders there, beside the pointer."""
    kimi = tmp_path / "kimi"
    kimi.mkdir()
    for name, value in {
        "CLAUDE_CONFIG_DIR": tmp_path / "claude",
        "CODEX_HOME": tmp_path / "codex",
        "KIMI_CODE_HOME": kimi,
        "XDG_STATE_HOME": tmp_path / "state",
    }.items():
        monkeypatch.setenv(name, str(value))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(team_note_file, "RENDER_SOURCES", ("kimi_code",))
    _opt_in(kimi / "AGENTS.md")

    report = team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    assert report.ok, report.failures
    assert report.written == ("kimi_code",)
    assert "- one" in (kimi / "AGENTS.md").read_text(encoding="utf-8")

