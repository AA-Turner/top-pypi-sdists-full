"""The daemon's side of recorder summaries (plan writer-owns-summary §3.4, §3.5):
`probe summary` and `probe visuals` through the pre-checks, the documents they
send though their argv never names them, the drafts folder the shell may write,
the status line's scope, the pin's facts, and the gates the main agent meets.
"""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

import pytest

from probe.daemon import approvals as appr
from probe.daemon import folders, precheck, scope, tools
from probe.daemon.store import Store
from probe.sdk import session_marker

FAKE_KEY = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))


class Replay:
    """`probe` never reaches a server: each command answers the stdout given for its path."""

    def __init__(self, answers: dict[str, str]) -> None:
        self.answers = answers
        self.calls: list[list[str]] = []

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, self.answers.get(" ".join(argv[:2]), json.dumps({"ok": True}))

    def server_features(self):
        return {"trash"}


def _deps(tmp_path, replay) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    return tools.Deps(
        store=Store(tmp_path / "s.sqlite", clock=time.time),
        board=appr.Board(tmp_path / "appr"),
        session_id="s",
        cwd=work,
        workdirs=[work],
        home=tmp_path,
        write_dirs=folders.note_dirs(),
        probe_env={},
        bypass=False,
        mode_known=True,
        bite_id=1,
        replay=replay,
    )


def _run(coro):
    return asyncio.run(coro)


def _draft(tmp_path, kind: str = "project", name: str = "s.md") -> Path:
    path = (
        tmp_path
        / "state"
        / "probe"
        / "summaries"
        / kind
        / "11111111-1111-4111-8111-111111111111"
        / name
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _checkout_json(
    path: Path,
    *,
    version: int = 3,
    markdown: str = "Willow SFT.\n",
    label: str = "willow",
    target: str = "project",
) -> str:
    return json.dumps(
        {
            "target": target,
            "label": label,
            "path": str(path),
            "version": version,
            "markdown": markdown,
            "you": "Richard",
            "today": "2026-10-15",
            "edited_by": None,
            "edited_at": None,
            "mode": "recorder",
        }
    )


# ---------------------------------------------------------------------------
# The pre-checks
# ---------------------------------------------------------------------------


def test_the_summary_and_visuals_commands_are_the_daemons():
    for argv in (
        ["summary", "checkout", "--project", "p"],
        ["summary", "push", "--experiment", "e"],
        ["visuals", "options", "--experiment", "e", "--project", "p"],
        ["visuals", "set", "--project", "p", "--file", "v.json"],
    ):
        parsed = precheck.parse(argv)
        assert parsed.owner == precheck.DAEMON, parsed.path


def test_steal_is_refused_as_for_notes_and_push_has_no_force(tmp_path):
    block = precheck.check(precheck.parse(["summary", "checkout", "--project", "p", "--steal"]), cwd=tmp_path)
    assert block is not None and block.check == "option"
    # No `--force` at all: it would carry erased text past the server's check.
    import typer.main

    from probe.cli.summary_cli import summary_app

    push = typer.main.get_command(summary_app).commands["push"]
    assert "--force" not in {opt for param in push.params for opt in param.opts}


def test_the_summary_option_refusal_points_to_probe_summary(tmp_path):
    block = precheck.check(
        precheck.parse(["project", "set", "p", "--summary", "verdict"]), cwd=tmp_path
    )
    assert (
        block is not None
        and "`probe summary checkout`" in block.why
        and "`probe summary push`" in block.why
    )


def test_a_visuals_file_is_scanned_like_any_file_a_command_sends(tmp_path):
    draft = _draft(tmp_path, name="s.visuals.json")
    draft.write_text(json.dumps([{"id": "x", "kind": "table", "description": f"key {FAKE_KEY}"}]))
    block = precheck.check(
        precheck.parse(["visuals", "set", "--project", "p", "--file", str(draft)]), cwd=tmp_path
    )
    assert block is not None and block.check == "secret" and "credential" in block.why
    draft.write_text(json.dumps([{"id": "x", "kind": "table"}]))
    assert (
        precheck.check(
            precheck.parse(["visuals", "set", "--project", "p", "--file", str(draft)]), cwd=tmp_path
        )
        is None
    ), "the summaries drafts are Probe's own folder, not a hidden one"


# ---------------------------------------------------------------------------
# The documents a push sends (D2)
# ---------------------------------------------------------------------------


def test_a_summary_push_sends_the_file_its_checkout_named(tmp_path):
    draft = _draft(tmp_path)
    draft.write_text("Willow SFT.\n")
    replay = Replay({"summary checkout": _checkout_json(draft)})
    deps = _deps(tmp_path, replay)
    out = _run(tools.run_probe_command(deps, ["summary", "push", "--project", "willow"]))
    assert out.startswith("not run") and "probe summary checkout" in out and replay.calls == []
    _run(tools.run_probe_command(deps, ["summary", "checkout", "--project", "willow"]))
    assert deps.store.fact("checkouts") == {"summary checkout|project=willow": str(draft)}
    draft.write_text(f"Willow SFT.\nkey {FAKE_KEY}\n")
    assert "credential" in _run(
        tools.run_probe_command(deps, ["summary", "push", "--project", "willow"])
    )
    draft.write_text("Willow SFT.\n\n## Oct 15 · Richard\n- B2decay 48.8\n")
    assert _run(
        tools.run_probe_command(deps, ["summary", "push", "--project", "willow"])
    ).startswith("[exit 0]")
    # A note's checkout under the same flags is another file.
    assert _run(tools.run_probe_command(deps, ["notes", "push", "--project", "willow"])).startswith(
        "not run"
    )


def test_a_visuals_set_without_a_file_sends_the_draft_options_wrote(tmp_path):
    draft = _draft(tmp_path, name="s.visuals.json")
    draft.write_text("[]\n")
    replay = Replay(
        {
            "visuals options": json.dumps(
                {"scope": "project", "current": [], "version": 2, "path": str(draft)}
            )
        }
    )
    deps = _deps(tmp_path, replay)
    out = _run(tools.run_probe_command(deps, ["visuals", "set", "--project", "willow"]))
    assert out.startswith("not run") and "visuals options" in out
    _run(tools.run_probe_command(deps, ["visuals", "options", "--project", "willow"]))
    draft.write_text(json.dumps([{"id": "x", "kind": "table", "title": FAKE_KEY}]))
    assert "credential" in _run(
        tools.run_probe_command(deps, ["visuals", "set", "--project", "willow"])
    )
    draft.write_text(json.dumps([{"id": "x", "kind": "table", "title": "Accuracy"}]))
    assert _run(
        tools.run_probe_command(deps, ["visuals", "set", "--project", "willow"])
    ).startswith("[exit 0]")


@pytest.mark.parametrize("argv", [["visuals", "set", "--help"], ["summary", "push", "--help"],
                                  ["visuals", "set", "--experiment", "e", "--help"]])
def test_help_on_a_document_command_is_never_refused_for_a_missing_file(tmp_path, argv):
    """Bench 10-16: `probe visuals set --help` was refused every bite ("the daemon
    only knows a visuals file from ..."), though help sends no file."""
    replay = Replay({"visuals set": "usage", "summary push": "usage"})
    out = _run(tools.run_probe_command(_deps(tmp_path, replay), argv))
    assert out.startswith("[exit 0]"), out


def test_the_shell_may_write_summary_drafts_and_the_team_note_stays_last(tmp_path):
    summaries = tmp_path / "state" / "probe" / "summaries"
    assert summaries in folders.note_dirs() and folders.note_dirs()[-1].name == "team-note"
    deps = _deps(tmp_path, Replay({}))
    draft = _draft(tmp_path)
    out = _run(
        tools.shell(deps, f"cat > {draft} <<'EOF'\nDoes a cosine decay beat a constant LR?\nEOF\n")
    )
    assert not out.startswith("not run"), out
    assert draft.read_text() == "Does a cosine decay beat a constant LR?\n"
    assert not tools._in_team_note(str(draft))


@pytest.mark.parametrize("bypass", [False, True], ids=["ask", "bypass"])
@pytest.mark.parametrize("suffix", [".base", ".meta.json", ".lock", ".owner", ".visuals.meta.json"])
def test_the_shell_never_writes_a_checkouts_bookkeeping(tmp_path, suffix, bypass):
    """Codex review: a forged `.meta.json` version would push stale text past
    the server's concurrent-edit and erasure checks. Only `probe` writes them,
    whatever the permission mode (bypass approves what the shell merely asks)."""
    import dataclasses

    deps = dataclasses.replace(_deps(tmp_path, Replay({})), bypass=bypass)
    draft = _draft(tmp_path)
    target = draft.with_name(draft.stem + suffix)
    target.write_text('{"version": 1}')
    out = _run(tools.shell(deps, f"cat > {target} <<'EOF'\n{{\"version\": 99}}\nEOF\n"))
    assert out.startswith("not run") and "only `probe` writes" in out, out
    assert target.read_text() == '{"version": 1}'


@pytest.mark.parametrize("command", [
    "cat > {target} <<EOF\n{{\"version\": 99}}\nEOF\n",                # unquoted: refused before the write check
    "cd {folder} && cat > {name} <<'EOF'\n{{\"version\": 99}}\nEOF\n",  # relative, after a cd
    "printf '{{}}' > {target}",
    "cp /dev/null {target}",
])
def test_no_command_touches_bookkeeping_even_in_bypass(tmp_path, command):
    """Codex re-review: bypass mode runs what the shell merely asks about, so
    the bookkeeping refusal must hold for every shape, not just a quoted heredoc."""
    import dataclasses

    deps = dataclasses.replace(_deps(tmp_path, Replay({})), bypass=True)
    draft = _draft(tmp_path)
    target = draft.with_name(draft.stem + ".meta.json")
    target.write_text('{"version": 1}')
    out = _run(tools.shell(deps, command.format(target=target, folder=draft.parent, name=target.name)))
    assert out.startswith("not run") and "only `probe` writes" in out, out
    assert target.read_text() == '{"version": 1}'


def test_a_summary_that_mentions_a_lock_file_is_still_written(tmp_path):
    deps = _deps(tmp_path, Replay({}))
    draft = _draft(tmp_path)
    out = _run(tools.shell(deps, f"cat > {draft} <<'EOF'\nPinned deps in uv.lock and data.base.\nEOF\n"))
    assert not out.startswith("not run"), out
    assert draft.read_text() == "Pinned deps in uv.lock and data.base.\n"


# ---------------------------------------------------------------------------
# Scope (the status line) and the pin's facts
# ---------------------------------------------------------------------------


def test_a_summary_push_names_its_entity_for_the_status_line():
    assert (
        scope.scope_ref(precheck.parse(["summary", "push", "--experiment", "b2", "--project", "w"]))
        == "b2"
    )
    assert scope.scope_ref(precheck.parse(["visuals", "set", "--project", "w"])) == "w"
    assert {"summary checkout", "visuals options"} <= scope.NO_SCOPE


def test_a_checkout_pins_the_loaded_summary_and_a_landed_push_updates_it(tmp_path):
    draft = _draft(tmp_path)
    draft.write_text("Willow SFT.\n")
    replay = Replay(
        {"summary checkout": _checkout_json(draft, version=3, markdown="Willow SFT.\n")}
    )
    deps = _deps(tmp_path, replay)
    _run(tools.run_probe_command(deps, ["summary", "checkout", "--project", "willow"]))
    pin = deps.store.fact(tools.SUMMARY_PIN)
    assert (pin["label"], pin["version"], pin["loaded"], pin["text"], pin["path"]) == (
        "willow",
        3,
        3,
        "Willow SFT.\n",
        str(draft),
    )
    draft.write_text("Willow SFT.\n\n**Where it stands (Oct 15):** B2decay leads.\n")
    replay.answers["summary push"] = json.dumps(
        {
            "target": "project",
            "label": "willow",
            "pushed": False,
            "merged": True,
            "conflicted": False,
            "version": 4,
            "detail": "",
        }
    )
    _run(tools.run_probe_command(deps, ["summary", "push", "--project", "willow"]))
    assert deps.store.fact(tools.SUMMARY_PIN)["version"] == 3, "a merge is not a landed push"
    replay.answers["summary push"] = json.dumps(
        {
            "target": "project",
            "label": "willow",
            "pushed": True,
            "merged": False,
            "conflicted": False,
            "version": 5,
            "detail": "",
        }
    )
    _run(tools.run_probe_command(deps, ["summary", "push", "--project", "willow"]))
    pin = deps.store.fact(tools.SUMMARY_PIN)
    assert pin["version"] == 5 and "B2decay leads" in pin["text"] and pin["loaded"] == 3
    # A push to another entity leaves the pin alone.
    other = _draft(tmp_path, kind="experiment")
    other.write_text("x\n")
    replay.answers["summary checkout"] = _checkout_json(other, target="experiment", label="b2")
    deps.store.set_fact(
        "checkouts", {**deps.store.fact("checkouts"), "summary checkout|experiment=b2": str(other)}
    )
    replay.answers["summary push"] = json.dumps({"pushed": True, "version": 9})
    _run(tools.run_probe_command(deps, ["summary", "push", "--experiment", "b2"]))
    assert deps.store.fact(tools.SUMMARY_PIN)["version"] == 5


# ---------------------------------------------------------------------------
# The gates the main agent meets (write gate, daemon profile, --directed: D26)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv,kind",
    [
        (["summary", "push", "--project", "p"], "write"),
        (["visuals", "set", "--project", "p", "--file", "v.json"], "write"),
        (["summary", "checkout", "--project", "p"], "read"),
        (["visuals", "options", "--project", "p"], "read"),
    ],
)
def test_the_classifier_reads_the_new_commands(argv, kind):
    assert session_marker.classify_probe_args(argv)[0] == kind


def _agent_session(monkeypatch, state: str) -> str:
    sid = "cccccccc-3333-4333-8333-cccccccccccc"
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", sid)
    session_marker.sessions_dir().mkdir(parents=True, exist_ok=True)
    (session_marker.sessions_dir() / f"{sid}.state").write_text(state)
    return sid


@pytest.mark.parametrize("state", [session_marker.STATE_READ_ONLY, session_marker.STATE_OFF])
def test_the_write_gate_refuses_a_push_and_a_set_under_read_and_off(monkeypatch, state):
    from probe.cli import write_gate

    _agent_session(monkeypatch, state)
    for argv in (["summary", "push", "--project", "p"], ["visuals", "set", "--project", "p"]):
        assert write_gate.refusal(argv, directed=False) is not None, (state, argv)
    checkout = write_gate.refusal(["summary", "checkout", "--project", "p"], directed=False)
    assert (checkout is None) == (state == session_marker.STATE_READ_ONLY), "a checkout reads"


def test_the_daemon_state_admits_a_push_only_when_directed(monkeypatch):
    from probe.cli import write_gate

    sid = _agent_session(monkeypatch, session_marker.STATE_DAEMON)
    monkeypatch.setattr(session_marker, "agent_writes_freely", lambda s, st: False)  # a live lease
    for argv in (["summary", "push", "--project", "p"], ["visuals", "set", "--project", "p"]):
        assert write_gate.refusal(argv, directed=False) is not None, argv
        assert write_gate.refusal(argv, directed=True) is None, argv
    assert sid


def test_the_daemon_profile_guard_admits_the_new_writes_with_directed():
    for argv in (
        ["summary", "push", "--project", "p", "--directed"],
        ["visuals", "set", "--experiment", "e", "--file", "v.json", "--directed"],
    ):
        assert session_marker.daemon_profile_allows(argv) == (
            True,
            "probe " + " ".join(argv[:2]),
        ), argv
        assert session_marker.daemon_profile_allows(argv[:-1])[0] is False, argv
    # A read stays the reader's (`probe ask`), directed or not.
    assert (
        session_marker.daemon_profile_allows(
            ["summary", "checkout", "--project", "p", "--directed"]
        )[0]
        is False
    )
