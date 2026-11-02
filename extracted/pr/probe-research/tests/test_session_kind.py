"""Who drives a session, read off its transcript's head, and the flag it puts on the first batch.

Search hides a session the tap calls AUTOMATED (plan anthrogen-search-fixes W1), so only
markers a harness writes for a headless run count; anything else, an unknown entrypoint or
no marker at all, must stay searchable. The flag rides the first batch's `provenance`, which
is part of that batch's identity: a resend must be the same bytes.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from probe.cli.imports import transcripts as bt
from probe.daemon.lanes import audit as audit_mod
from probe.tap_core import session_identity as si
from probe.tap_core.session_journal import DeliveryPending, Journal
from probe.tap_core.session_kind import (
    HEAD_LINES,
    SessionKind,
    session_kind,
    transcript_kind,
)
from tests.test_backfill_transcripts_upload import FakeWire, drain, journal_for
from tests.test_daemon_audit import _line, _t3_claude_head

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "probe_events"
AUTOMATED, INTERACTIVE, UNKNOWN = SessionKind.AUTOMATED, SessionKind.INTERACTIVE, SessionKind.UNKNOWN


def _kind(text: str | bytes) -> SessionKind:
    raw = text.encode() if isinstance(text, str) else text
    return session_kind(raw.splitlines(keepends=True))


@pytest.mark.parametrize(
    ("fixture", "kind"),
    [
        ("codex", AUTOMATED),  # a real `codex exec` rollout: originator codex_exec, source exec
        ("claude_code", INTERACTIVE),  # entrypoint cli
        ("pi", UNKNOWN),  # pi writes no headless marker
        ("kimi_code", UNKNOWN),
    ],
)
def test_the_recorded_fixtures(fixture, kind):
    assert transcript_kind(FIXTURES / fixture / "raw.jsonl") is kind


#: The audit's own table (`test_daemon_audit.test_a_session_a_program_drives_never_audits`).
AUDIT_HEADS = [
    ({"type": "user", "entrypoint": "cli"}, INTERACTIVE),
    ({"type": "user", "entrypoint": "vscode"}, INTERACTIVE),
    ({"type": "user", "entrypoint": "sdk-cli"}, AUTOMATED),  # claude -p
    ({"type": "session_meta", "payload": {"originator": "codex_cli_rs"}}, INTERACTIVE),
    ({"type": "session_meta", "payload": {"originator": "codex_exec"}}, AUTOMATED),
    ({"type": "session_meta", "payload": {"originator": "codex_cli_rs", "source": {"subagent": "review"}}}, AUTOMATED),
    ({"type": "session_meta", "payload": {"originator": "T3 Code", "source": "vscode"}}, INTERACTIVE),
    ({"type": "session_meta", "payload": {"originator": "Codex Desktop", "source": "vscode"}}, INTERACTIVE),
    ({"type": "session_meta", "payload": {"originator": "T3 Code", "source": "exec"}}, AUTOMATED),
    ({"type": "user"}, UNKNOWN),
]
#: What search adds: entrypoints Claude Code writes today that the audit's allow-list does
#: not name, the Agent SDKs, a value nobody has seen yet, and heads with no marker.
HEADS = [
    *AUDIT_HEADS,
    ({"type": "user", "entrypoint": "claude-vscode"}, INTERACTIVE),
    ({"type": "user", "entrypoint": "claude-desktop"}, INTERACTIVE),
    ({"type": "user", "entrypoint": "a-launcher-from-next-year"}, INTERACTIVE),
    # Agent-SDK editors (Zed) report these while a person types: never hidden.
    ({"type": "user", "entrypoint": "sdk-py"}, UNKNOWN),
    ({"type": "user", "entrypoint": "sdk-ts"}, UNKNOWN),
    ({"type": "user", "entrypoint": " SDK-TS "}, UNKNOWN),
    ({"type": "user", "entrypoint": " SDK-CLI "}, AUTOMATED),
    ({"type": "user", "entrypoint": ""}, UNKNOWN),
    ({"type": "user", "entrypoint": None}, UNKNOWN),
    ({"type": "session_meta", "payload": {"id": "x"}}, UNKNOWN),
    ({"type": "session", "version": 3, "id": "x", "cwd": "/w"}, UNKNOWN),  # pi's header
]


@pytest.mark.parametrize(("head", "kind"), HEADS)
def test_only_known_headless_markers_are_automated(head, kind):
    assert _kind("not json\n" + _line(head)) is kind


def test_t3_code_is_a_person_however_far_down_its_tool_list_is():
    """T3 Code drives Claude through the Agent SDK (`sdk-cli`); Claude Code's own list of
    T3's tools anywhere in the head says a person is in T3. The audit's fixture, unchanged."""
    assert _kind(_t3_claude_head()) is INTERACTIVE
    assert _kind(_t3_claude_head(hooks=30)) is INTERACTIVE
    assert _kind(_t3_claude_head(tools=())) is AUTOMATED  # the same head with no T3: claude -p


def test_a_prompt_naming_t3_tools_is_not_t3():
    assert _kind(_line({"type": "user", "entrypoint": "sdk-cli",
                        "message": {"content": "call mcp__t3-code__delegate_task"}})) is AUTOMATED


def test_any_other_entrypoint_in_the_head_wins_over_sdk_cli():
    """`sdk-cli` is AUTOMATED only when the session's lines in the head say nothing else: a
    person resuming a `claude -p` run, or an Agent-SDK front end taking over, is not hidden."""
    cli, sdk_cli, sdk_ts = (_line({"type": "user", "entrypoint": e}) for e in ("cli", "sdk-cli", "sdk-ts"))
    assert _kind(cli + sdk_cli) is INTERACTIVE
    assert _kind(sdk_cli + cli) is INTERACTIVE
    assert _kind(sdk_cli + sdk_ts) is UNKNOWN
    assert _kind(sdk_cli + sdk_cli) is AUTOMATED


def test_another_session_s_lines_say_nothing_about_this_one():
    """A resumed or forked transcript opens with its ancestor's history, under the ancestor's
    `sessionId`: only the session's own lines classify it."""
    own, ancestor = str(uuid4()), str(uuid4())

    def rec(sid: str, entrypoint: str) -> str:
        return _line({"type": "user", "sessionId": sid, "entrypoint": entrypoint})

    def kind(text: str) -> SessionKind:
        return session_kind(text.encode().splitlines(keepends=True)[:HEAD_LINES], own)

    assert kind(rec(ancestor, "sdk-cli") * 3 + rec(own, "cli")) is INTERACTIVE
    assert kind(rec(ancestor, "cli") * 3 + rec(own, "sdk-cli")) is AUTOMATED
    assert kind(rec(ancestor, "sdk-cli") * HEAD_LINES + rec(own, "cli")) is UNKNOWN  # history fills the head
    assert kind(rec(own.upper(), "sdk-cli")) is AUTOMATED
    assert session_kind([rec(ancestor, "sdk-cli")]) is AUTOMATED  # no id to check: every line counts


def test_a_marker_past_the_head_is_not_read(tmp_path):
    path = tmp_path / "t.jsonl"
    filler = "".join(_line({"type": "progress", "n": i}) for i in range(HEAD_LINES))
    path.write_text(filler + _line({"type": "user", "entrypoint": "sdk-cli"}))
    assert transcript_kind(path) is UNKNOWN


def test_a_long_codex_session_meta_line_is_still_read(tmp_path):
    """Codex's first line carries the instructions (52 KB on the devbox): read whole."""
    path = tmp_path / "rollout.jsonl"
    path.write_text(_line({"type": "session_meta",
                           "payload": {"instructions": "x" * 200_000, "originator": "codex_exec"}}))
    assert transcript_kind(path) is AUTOMATED


@pytest.mark.parametrize(
    "head",
    [
        b"",
        b"\n\n",
        b"not json at all\n{\n",
        b"\xff\xfe\xfa garbage\n",
        b"[" * 200_000 + b"\n",  # nested past the parser's depth: RecursionError, skipped
        b"[1, 2]\n\"a string\"\n",
    ],
)
def test_an_empty_or_unreadable_head_is_unknown(head):
    assert _kind(head) is UNKNOWN


def test_a_transcript_that_cannot_be_read_is_unknown(tmp_path):
    assert transcript_kind(tmp_path / "gone.jsonl") is UNKNOWN
    assert transcript_kind(tmp_path) is UNKNOWN  # a directory


def test_unreadable_lines_do_not_hide_what_follows():
    assert _kind(b"[" * 200_000 + b"\n" + _t3_claude_head(tools=()).encode()) is AUTOMATED


def test_the_kind_reads_as_its_value():
    assert str(AUTOMATED) == "automated" and f"{INTERACTIVE}" == "interactive"
    assert AUTOMATED == "automated" and json.dumps(UNKNOWN) == '"unknown"'


# -- the audit keeps its own polarity (plan O7) -------------------------------------------


@pytest.mark.parametrize(("head", "kind"), AUDIT_HEADS)
def test_on_the_audits_markers_both_agree(tmp_path, head, kind):
    """Where the audit's table speaks, a program to one is a program to the other."""
    path = tmp_path / "t.jsonl"
    path.write_text("not json\n" + _line(head))
    assert (kind is AUTOMATED) is (not audit_mod.interactive(path))


def test_an_entrypoint_the_audit_does_not_list_differs_on_purpose(tmp_path):
    """The audit's allow-list reads `claude-vscode` as a program and skips it; search must not
    hide it. The audit is left as it is (plan O7): this pins both, so neither drifts silently."""
    path = tmp_path / "t.jsonl"
    path.write_text(_line({"type": "user", "entrypoint": "claude-vscode"}))
    assert audit_mod.interactive(path) is False
    assert transcript_kind(path) is INTERACTIVE


# -- the proof, and the first batch it becomes -------------------------------------------


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))


def _claude(tmp_path: Path, entrypoint: str | None, *, lines: int = 12, pad: int = 0) -> bt.Transcript:
    sid = str(uuid4())
    path = tmp_path / f"{sid}.jsonl"
    stamp = {"entrypoint": entrypoint} if entrypoint else {}
    records = [
        {"type": "user", "sessionId": sid, "cwd": "/synthetic", **stamp,
         "message": {"role": "user", "content": f"turn {i}" + "x" * pad}}
        for i in range(lines)
    ]
    path.write_bytes(b"".join(json.dumps(r).encode() + b"\n" for r in records))
    stat = path.stat()
    return bt.Transcript(path, sid, "claude_code", "/synthetic", stat.st_size, stat.st_mtime)


def _codex(tmp_path: Path, payload: dict) -> tuple[Path, str]:
    sid = str(uuid4())
    path = tmp_path / f"rollout-{sid}.jsonl"
    path.write_text(_line({"type": "session_meta", "payload": {"id": sid, "cwd": "/w", **payload}}))
    return path, sid


@pytest.mark.parametrize(("entrypoint", "automated"),
                         [("sdk-cli", True), ("cli", False), ("claude-vscode", False), (None, False)])
def test_the_claude_proof_says_whether_a_program_drives_it(tmp_path, entrypoint, automated):
    t = _claude(tmp_path, entrypoint)
    assert si.validate_identity(t.path, "claude_code", t.session_id)["automated"] is automated


@pytest.mark.parametrize(("payload", "automated"),
                         [({"originator": "codex_exec", "source": "exec"}, True),
                          ({"originator": "Codex Desktop", "source": "vscode"}, False)])
def test_the_codex_proof_says_whether_a_program_drives_it(tmp_path, payload, automated):
    path, sid = _codex(tmp_path, payload)
    assert si.validate_identity(path, "codex", sid)["automated"] is automated


def test_a_person_resuming_a_headless_run_is_not_automated(tmp_path):
    """The proof classifies the session it proves, not the history it carries (`observed_lineage`)."""
    ancestor, own = str(uuid4()), str(uuid4())
    path = tmp_path / f"{own}.jsonl"

    def rec(sid: str, entrypoint: str) -> str:
        return _line({"type": "user", "sessionId": sid, "cwd": "/synthetic", "entrypoint": entrypoint,
                      "message": {"role": "user", "content": "hi"}})

    path.write_text(rec(ancestor, "sdk-cli") * 3 + rec(own, "cli") * 3)
    proof = si.validate_identity(path, "claude_code", own)
    assert proof["observed_lineage"] == [ancestor] and proof["automated"] is False
    path.write_text(rec(ancestor, "cli") * 3 + rec(own, "sdk-cli") * 3)
    assert si.validate_identity(path, "claude_code", own)["automated"] is True


def test_the_proof_reads_the_head_past_the_window_it_proves_identity_from(tmp_path):
    """Claude's identity comes from the transcript's last 2 MB; how it runs, from its start."""
    t = _claude(tmp_path, "sdk-cli", lines=40, pad=80_000)
    assert t.size > si.SAMPLE_BYTES
    proof = si.validate_identity(t.path, "claude_code", t.session_id)
    assert proof["automated"] is True
    assert proof == si.validate_identity(t.path, "claude_code", t.session_id)


def test_the_verdict_reads_no_head(tmp_path, monkeypatch):
    """Session discovery checks every transcript on the machine with the verdict alone."""
    t = _claude(tmp_path, "sdk-cli")
    monkeypatch.setattr(si, "read_head", lambda handle: pytest.fail("the verdict read the head"))
    assert si.check_identity(t.path, "claude_code", t.session_id) is None


def _bodies(wire: FakeWire) -> list[dict]:
    return [json.loads(body) for body in wire.calls]


def test_the_first_batch_carries_the_flag_and_later_ones_do_not(tmp_path):
    wire = FakeWire()
    t = _claude(tmp_path, "sdk-cli")
    drain(journal_for(t, wire), t, wire)
    bodies = _bodies(wire)
    assert len(bodies) > 1
    assert bodies[0]["batch_seq"] == 0 and bodies[0]["provenance"]["automated"] is True
    assert all("provenance" not in body for body in bodies[1:])


def test_a_persons_first_batch_says_so(tmp_path):
    wire = FakeWire()
    t = _claude(tmp_path, "cli")
    drain(journal_for(t, wire), t, wire)
    assert _bodies(wire)[0]["provenance"]["automated"] is False


def test_a_resent_first_batch_is_the_same_bytes(tmp_path):
    """Provenance is part of the batch's identity: the server refuses a seq it already took
    with other bytes (409). A failed send, a restarted tap, then the resend: one body."""
    wire = FakeWire()
    t = _claude(tmp_path, "sdk-cli")
    journal = journal_for(t, wire)
    staged = journal.stage(t.session_id, cwd=t.cwd, historical_only=True, max_body_bytes=2600)
    wire.status = 503
    with pytest.raises(DeliveryPending):
        journal.deliver(t.session_id, wire)
    # A later pass proves the identity again and offers a fresh proof: the reservation keeps its own.
    journal.ensure(t.session_id, t.path, wire.receipts(t.session_id), historical=True,
                   provenance=si.validate_identity(t.path, "claude_code", t.session_id) | {"automated": False})
    reopened = Journal(wire.base_url, "synthetic", "claude_code")
    assert reopened.stage(t.session_id, cwd=t.cwd, historical_only=True, max_body_bytes=2600) == staged
    wire.status = 202
    reopened.deliver(t.session_id, wire)
    first, resent = wire.calls[0], wire.calls[1]
    assert first == resent == staged
    assert json.loads(resent)["provenance"]["automated"] is True
