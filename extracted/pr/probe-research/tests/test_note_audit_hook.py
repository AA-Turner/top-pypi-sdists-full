"""The prompt-submit delivery of the team-note audit line.

THE CHANGE THIS GUARDS (2026-09-16). The line used to be rendered into the
team-note block in `CLAUDE.md` / `AGENTS.md`. Every session of that harness reads
that file -- `claude -p`, `codex exec`, a cron job, a subagent -- and an audit
dispatched into one of those asks for a background agent it cannot spawn, on
behalf of a researcher who is not there when it finishes. Prompt submission is
the one event that means a person is present, so the dispatch moved to a
UserPromptSubmit hook.

Five properties, and all five are load-bearing:

  * the RENDER carries no advisory, or the automated readers still get one;
  * the CLI is SILENT in an automated session, measured against the real
    markers (`CODEX_CI=1` from `codex exec`, `CLAUDE_CODE_ENTRYPOINT=sdk-cli`
    from `claude -p`, `cli` from a person at the keyboard);
  * the hook asks ONCE per session, and stays silent -- never erroring into the
    researcher's turn -- when anything at all goes wrong;
  * ONE session per machine is told to audit at a time: asking claims a lease
    that every other session's ask is refused by until it expires;
  * a session whose tracking is off does not ask, because asking claims that
    lease for an audit its own line tells it to skip.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from probe.cli import agent_rules, team_note_file as tnf

_ROOT = Path(__file__).resolve().parent.parent
_HOOK = _ROOT / "plugins" / "probe-research" / "hooks" / "note_audit.py"
_HOOKS_JSON = _ROOT / "plugins" / "probe-research" / "hooks" / "hooks.json"

DUE = "<!-- audited 2020-01-01 -->\n## note\nbody"


@pytest.fixture(scope="module")
def hook():
    spec = importlib.util.spec_from_file_location("plugin_note_audit", _HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- the render must not carry it any more -----------------------------------


def test_the_rendered_block_carries_no_advisory(tmp_path, monkeypatch) -> None:
    """THE POINT OF THE CHANGE. A note that is years past its stamp and over
    budget is exactly the case that used to write a dispatch into the file every
    unattended session then read."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    health = tmp_path / "probe" / "team-note"
    health.mkdir(parents=True)
    (health / "health.json").write_text(
        json.dumps({"sources": {"claude_code": {"pct": 0.99}}}), encoding="utf-8"
    )
    # the same inputs, straight to the advisory: it still fires
    assert tnf.audit_advisory(DUE, source="claude_code", pct=0.99, baseline=None)

    # The body's own `<!-- audited ... -->` stamp rides along, as it must --
    # what may not appear is the DISPATCH.
    block = agent_rules.render_note_block(DUE, document="/n.md")
    for dispatched in ("outgrown its budget", "periodic re-check", "audit-team-note", "BACKGROUND subagent"):
        assert dispatched not in block, (dispatched, block)


def test_the_block_is_what_it_was_before_the_advisory_existed() -> None:
    """Belt and braces on the same property, from the other side: an empty
    advisory is the shape every machine now renders."""
    assert agent_rules.render_note_block("body", document="/n.md") == (
        agent_rules.render_note_block("body", document="/n.md", advisory="")
    )


# --- the automation gate ------------------------------------------------------


@pytest.mark.parametrize(
    ("env", "automated"),
    [
        ({"CODEX_CI": "1"}, True),                        # codex exec
        ({"CODEX_CI": "0"}, False),
        ({"CLAUDE_CODE_ENTRYPOINT": "sdk-cli"}, True),    # claude -p
        ({"CLAUDE_CODE_ENTRYPOINT": "sdk-py"}, True),
        ({"CLAUDE_CODE_ENTRYPOINT": "mcp"}, True),
        ({"CLAUDE_CODE_ENTRYPOINT": "cli"}, False),       # a person, measured
        ({"CLAUDE_CODE_ENTRYPOINT": "vscode"}, False),
        ({}, False),                                      # an unknown harness
    ],
)
def test_the_gate_names_the_automated_submitters(env: dict, automated: bool) -> None:
    """A DENY-LIST on purpose: the hook only fires on prompt submit, so presence
    is most of the way proven already, and an allow-list would silently disable
    the audit on every harness we have not met."""
    assert tnf.session_is_automated(env) is automated


def test_the_cli_is_silent_in_an_automated_session(tmp_path, monkeypatch) -> None:
    """Against a note that IS due: silent, and it takes no lease -- an unattended
    run holding the machine's audit would starve every session a person is in."""
    where = tmp_path / "probe" / "team-note"
    where.mkdir(parents=True)
    (where / tnf.DOCUMENT_NAME).write_text(DUE, encoding="utf-8")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.setenv("CODEX_CI", "1")
    out = subprocess.run(
        [sys.executable, "-m", "probe.cli.main", "notes", "audit-advisory"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=str(_ROOT),
        env={**dict(__import__("os").environ), "PYTHONPATH": str(_ROOT / "src")},
    )
    assert out.returncode == 0
    assert out.stdout.decode().strip() == ""
    assert not (where / "audit-lease.json").exists()


# --- one auditor per machine --------------------------------------------------
#
# THE BUG (2026-09-28). The advisory is asked once per SESSION, and the stamp that
# silences it is written by the auditor it dispatches -- so every session that
# submitted a prompt in between was told to spawn its own auditor. On a box with
# nine sessions that is nine subagents rewriting one file.


def test_the_lease_goes_to_one_session_until_it_expires(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    now = 1_000_000.0
    assert tnf.claim_audit_dispatch(now=now) is True
    assert tnf.claim_audit_dispatch(now=now + 60) is False
    assert tnf.claim_audit_dispatch(now=now + tnf.AUDIT_LEASE_SECONDS - 1) is False
    # A winner that never ran it (session closed, subagent died) is recovered
    # by expiry, not by anyone releasing it.
    assert tnf.claim_audit_dispatch(now=now + tnf.AUDIT_LEASE_SECONDS) is True


def test_simultaneous_prompts_get_one_winner(tmp_path, monkeypatch) -> None:
    """THE LOCK IS THE WHOLE FIX. Every other lease test claims one after
    another, and those pass with the lock deleted; this one does not."""
    import threading

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    gate = threading.Barrier(16)
    won: list = []

    def claim() -> None:
        gate.wait()
        won.append(tnf.claim_audit_dispatch(holder=threading.current_thread().name, now=1_000_000.0))

    threads = [threading.Thread(target=claim, name=f"session-{i}") for i in range(16)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert won.count(True) == 1, won


def test_the_holder_is_told_again_and_nobody_else(tmp_path, monkeypatch) -> None:
    """The lease is written before the line reaches the model. If the hook was
    killed or its output dropped, the claiming session was never marked and asks
    again -- and must get the line, or nobody on the box hears it for the whole
    lease. A claim with no holder cannot be re-asked."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    now = 1_000_000.0
    assert tnf.claim_audit_dispatch(holder="session-a", now=now) is True
    assert tnf.claim_audit_dispatch(holder="session-a", now=now + 60) is True
    assert tnf.claim_audit_dispatch(holder="session-b", now=now + 60) is False
    assert tnf.claim_audit_dispatch(holder=None, now=now + 60) is False

    # Expiry counts from the LAST telling (now + 60), not the first.
    assert tnf.claim_audit_dispatch(holder=None, now=now + tnf.AUDIT_LEASE_SECONDS) is False
    assert tnf.claim_audit_dispatch(holder=None, now=now + 60 + tnf.AUDIT_LEASE_SECONDS) is True
    assert tnf.claim_audit_dispatch(holder=None, now=now + 61 + tnf.AUDIT_LEASE_SECONDS) is False


def test_telling_the_holder_again_renews_the_lease(tmp_path, monkeypatch) -> None:
    """Its auditor starts from the LATEST telling, so a re-telling a second
    before expiry must not hand the audit to another session a second later."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    now = 1_000_000.0
    last = now + tnf.AUDIT_LEASE_SECONDS - 1
    assert tnf.claim_audit_dispatch(holder="session-a", now=now) is True
    assert tnf.claim_audit_dispatch(holder="session-a", now=last) is True
    assert tnf.claim_audit_dispatch(holder="session-b", now=now + tnf.AUDIT_LEASE_SECONDS) is False
    assert tnf.claim_audit_dispatch(holder="session-b", now=last + tnf.AUDIT_LEASE_SECONDS) is True


def test_a_lease_that_is_not_a_small_file_is_free(tmp_path, monkeypatch) -> None:
    """A decoder-busting nesting would raise RecursionError on every prompt, and
    a FIFO would block every prompt's hook until its timeout -- a lease no
    expiry ever clears. Both are corrupt, so both are free and get replaced."""
    import os as _os

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    lease = tnf.audit_lease_path()
    lease.parent.mkdir(parents=True)
    lease.write_text("[" * 3000 + "]" * 3000, encoding="utf-8")
    assert tnf.claim_audit_dispatch(holder="session-a", now=1_000_000.0) is True

    lease.write_text('{"claimed_at": 1000000.0, "pad": "' + "x" * 5000 + '"}', encoding="utf-8")
    assert tnf.claim_audit_dispatch(holder="session-b", now=1_000_000.0) is True

    lease.unlink()
    _os.mkfifo(lease)
    assert tnf.claim_audit_dispatch(holder="session-c", now=1_000_000.0) is True
    assert lease.is_file(), "the claim replaces what it could not read"


def test_a_clock_stepped_back_does_not_free_the_lease(tmp_path, monkeypatch) -> None:
    """On one machine a lease from the future is a clock that stepped backwards
    (NTP, a VM resuming) -- reading it as free let a second session dispatch."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    now = 1_000_000.0
    assert tnf.claim_audit_dispatch(holder="session-a", now=now) is True
    assert tnf.claim_audit_dispatch(holder="session-b", now=now - 5) is False


@pytest.mark.parametrize(
    "held",
    [
        "not json",
        "[]",
        '{"claimed_at": "yesterday"}',
        '{"claimed_at": true}',
        '{"claimed_at": NaN}',
        '{"claimed_at": 1' + "0" * 400 + "}",   # overflows float arithmetic
        '{"claimed_at": 9e12}',                  # far past any clock step
    ],
)
def test_an_unreadable_or_far_future_lease_is_free(tmp_path, monkeypatch, held: str) -> None:
    """Same direction as a corrupted stamp: a duplicate audit costs tokens, a
    lease nobody can clear silences the audit for good."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    lease = tnf.audit_lease_path()
    lease.parent.mkdir(parents=True)
    lease.write_text(held, encoding="utf-8")
    assert tnf.claim_audit_dispatch(now=1_000_000.0) is True


def test_a_lease_that_cannot_be_written_still_dispatches(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    (tmp_path / "probe").write_text("a file where the state directory should be")
    assert tnf.claim_audit_dispatch() is True


def _cli(tmp_path, *args: str, session: "str | None" = None) -> str:
    env = {
        **dict(__import__("os").environ),
        "PYTHONPATH": str(_ROOT / "src"),
        "XDG_STATE_HOME": str(tmp_path),
        "PROBE_CONFIG_PATH": str(tmp_path / "no-config.json"),
        "CLAUDE_CODE_ENTRYPOINT": "cli",
    }
    env.pop("CODEX_CI", None)
    env.pop(tnf.AUDIT_SESSION_ENV, None)
    if session is not None:
        env[tnf.AUDIT_SESSION_ENV] = session
    out = subprocess.run(
        [sys.executable, "-m", "probe.cli.main", "notes", "audit-advisory", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=str(_ROOT),
        env=env,
    )
    assert out.returncode == 0
    return out.stdout.decode().strip()


def test_the_cli_dispatches_one_session_per_machine(tmp_path) -> None:
    where = tmp_path / "probe" / "team-note"
    where.mkdir(parents=True)
    (where / tnf.DOCUMENT_NAME).write_text(DUE, encoding="utf-8")

    # A person checking the line must not silence the next real dispatch.
    assert "periodic re-check" in _cli(tmp_path, "--peek")
    assert not (where / "audit-lease.json").exists()

    assert "periodic re-check" in _cli(tmp_path, session="session-a")
    assert _cli(tmp_path, session="session-b") == "", "a second session must not be told to audit too"
    assert _cli(tmp_path) == ""
    assert "periodic re-check" in _cli(tmp_path, session="session-a"), "the holder may be told again"
    assert "periodic re-check" in _cli(tmp_path, "--peek")


def test_a_note_that_is_not_due_takes_no_lease(tmp_path) -> None:
    where = tmp_path / "probe" / "team-note"
    where.mkdir(parents=True)
    today = __import__("datetime").date.today().isoformat()
    (where / tnf.DOCUMENT_NAME).write_text(f"<!-- audited {today} -->\n## note\nbody", encoding="utf-8")
    assert _cli(tmp_path, session="session-a") == ""
    assert not (where / "audit-lease.json").exists()


# --- reading local state ------------------------------------------------------


def test_advisory_for_source_reads_the_document_and_the_last_measurement(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    where = tmp_path / "team-note"
    where.mkdir(parents=True)
    document = where / "probe-team-note.md"
    document.write_text(DUE, encoding="utf-8")

    class _Where:
        pass

    w = _Where()
    w.document = document
    monkeypatch.setattr(tnf, "paths_for", lambda settings: w)

    health = tmp_path / "probe" / "team-note"
    health.mkdir(parents=True)
    (health / "health.json").write_text(
        json.dumps({"sources": {"claude_code": {"pct": 0.95}}}), encoding="utf-8"
    )
    text = tnf.advisory_for_source("claude_code", settings=None)
    assert "outgrown its budget" in text

    # No document, no answer -- and no traceback.
    document.unlink()
    assert tnf.advisory_for_source("claude_code", settings=None) == ""


# --- the hook itself ----------------------------------------------------------


def _run_hook(
    hook, payload, monkeypatch, tmp_path, advisory: str, calls: list, *, envs: "list | None" = None
):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    # Hermetic default: this machine's own config must not decide whether the
    # hook asks. A session's explicit `.state` file still wins over it; a test
    # of the folder default deletes it.
    monkeypatch.setenv("PROBE_SESSION_STATE", "full")

    class _Result:
        returncode = 0
        stdout = advisory.encode()

    def run(*a, **k):
        calls.append(a[0])
        if envs is not None:
            envs.append(k.get("env"))
        return _Result()

    monkeypatch.setattr(hook, "_probe_bin", lambda: "/usr/bin/true")
    monkeypatch.setattr(hook.subprocess, "run", run)
    monkeypatch.setattr(hook.sys, "stdin", __import__("io").StringIO(json.dumps(payload)))
    captured = __import__("io").StringIO()
    monkeypatch.setattr(hook.sys, "stdout", captured)
    assert hook.main() == 0
    return captured.getvalue()


def test_the_hook_speaks_once_per_session(hook, tmp_path, monkeypatch) -> None:
    payload = {"session_id": "11111111-2222-3333-4444-555555555555", "hook_event_name": "UserPromptSubmit"}
    calls: list = []
    first = _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls)
    assert json.loads(first)["hookSpecificOutput"]["additionalContext"] == "> **due**"

    second = _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls)
    assert second == "", "the marker must stop the second ask"
    assert len(calls) == 1, "and the CLI is not even spawned again"


def test_a_failed_write_is_not_recorded(hook, tmp_path, monkeypatch) -> None:
    """Nothing reached the model, so the session must be asked -- and, holding
    the machine's lease, told -- again. Marking before writing left it "told"
    with nothing said while its lease silenced every other session."""
    sid = "cccccccc-dddd-eeee-ffff-000000000000"
    calls: list = []

    class _Broken:
        def write(self, _text):
            raise BrokenPipeError

        def flush(self):
            pass

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_SESSION_STATE", "full")

    class _Result:
        returncode = 0
        stdout = b"> **due**"

    monkeypatch.setattr(hook, "_probe_bin", lambda: "/usr/bin/true")
    monkeypatch.setattr(hook.subprocess, "run", lambda *a, **k: (calls.append(a[0]), _Result())[1])
    monkeypatch.setattr(hook.sys, "stdin", __import__("io").StringIO(json.dumps({"session_id": sid})))
    monkeypatch.setattr(hook.sys, "stdout", _Broken())
    assert hook.main() == 0
    assert not hook._marker(sid).exists()

    assert _run_hook(hook, {"session_id": sid}, monkeypatch, tmp_path, "> **due**", calls) != ""
    assert len(calls) == 2


def test_silence_is_not_recorded(hook, tmp_path, monkeypatch) -> None:
    """A note that is not due yet may become due later in the same session."""
    payload = {"session_id": "66666666-7777-8888-9999-aaaaaaaaaaaa"}
    calls: list = []
    assert _run_hook(hook, payload, monkeypatch, tmp_path, "", calls) == ""
    assert _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls) != ""
    assert len(calls) == 2


@pytest.mark.parametrize("state", ["read-only", "off"])
def test_a_session_that_is_not_tracking_does_not_ask(hook, tmp_path, monkeypatch, state: str) -> None:
    """ASKING CLAIMS THE MACHINE'S AUDIT. A session told to skip the audit that
    asked anyway would hold it for every other session on the box and then do
    nothing with it -- so it does not ask, and does not mark itself either: the
    switch can be turned on later in the same conversation."""
    sid = "77777777-8888-9999-aaaa-bbbbbbbbbbbb"
    payload = {"session_id": sid}
    calls: list = []
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    decision = hook._session_marker.state_path(sid)
    decision.parent.mkdir(parents=True, exist_ok=True)
    decision.write_text(state, encoding="utf-8")
    assert _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls) == ""
    assert calls == []

    decision.write_text("full", encoding="utf-8")
    assert _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls) != ""
    assert len(calls) == 1


def test_a_daemon_session_asks(hook, tmp_path, monkeypatch) -> None:
    """The daemon records a `daemon` session, so it is tracking and runs the
    audit (`notes sync` is ungated). Narrowing the gate to `full` would stop
    every daemon-mode session from ever auditing."""
    sid = "88888888-9999-aaaa-bbbb-cccccccccccc"
    calls: list = []
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    decision = hook._session_marker.state_path(sid)
    decision.parent.mkdir(parents=True, exist_ok=True)
    decision.write_text("daemon", encoding="utf-8")
    assert _run_hook(hook, {"session_id": sid}, monkeypatch, tmp_path, "> **due**", calls) != ""
    assert len(calls) == 1


def test_a_folder_that_defaults_to_read_only_does_not_ask(hook, tmp_path, monkeypatch) -> None:
    """No decision for this session yet: the folder's default decides, read
    from the payload's cwd -- the same ladder the tracking guard walks."""
    sid = "99999999-aaaa-bbbb-cccc-dddddddddddd"
    folder = tmp_path / "repo"
    (folder / ".probe").mkdir(parents=True)
    (folder / ".probe" / "config.json").write_text(
        json.dumps({"defaults": {"session_state": "read-only"}}), encoding="utf-8"
    )
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    calls: list = []
    payload = {"session_id": sid, "cwd": str(folder)}

    monkeypatch.setattr(hook._session_marker, "state_env_override", lambda: None)
    assert _run_hook(hook, payload, monkeypatch, tmp_path, "> **due**", calls) == ""
    assert calls == []


def test_a_switch_prompt_does_not_ask(hook, tmp_path, monkeypatch) -> None:
    """The prompt hooks run in parallel, so on `/probe off` this hook can read
    the state the guard is about to replace, claim the machine's audit as `on`,
    and then be told by its own line to skip it. It asks on the next prompt."""
    sid = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    calls: list = []
    switch = {"session_id": sid, "prompt": "/probe off"}
    assert _run_hook(hook, switch, monkeypatch, tmp_path, "> **due**", calls) == ""
    assert calls == []
    after = {"session_id": sid, "prompt": "carry on"}
    assert _run_hook(hook, after, monkeypatch, tmp_path, "> **due**", calls) != ""
    assert len(calls) == 1


def test_the_hook_names_its_session_to_the_cli(hook, tmp_path, monkeypatch) -> None:
    """The lease's holder, so this session is told again if this telling never
    arrives. An environment variable, never a flag an older CLI would refuse."""
    sid = "bbbbbbbb-cccc-dddd-eeee-ffffffffffff"
    calls: list = []
    envs: list = []
    _run_hook(hook, {"session_id": sid}, monkeypatch, tmp_path, "> **due**", calls, envs=envs)
    assert envs[0][tnf.AUDIT_SESSION_ENV] == sid
    assert calls[0][1:] == ["notes", "audit-advisory", "--source", "claude_code"]


def test_no_session_id_means_no_ask(hook, tmp_path, monkeypatch) -> None:
    """Without a marker this would run on every prompt of every session."""
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    calls: list = []
    assert _run_hook(hook, {}, monkeypatch, tmp_path, "> **due**", calls) == ""
    assert calls == []


def test_garbage_on_stdin_is_silent(hook, tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setattr(hook.sys, "stdin", __import__("io").StringIO("not json"))
    captured = __import__("io").StringIO()
    monkeypatch.setattr(hook.sys, "stdout", captured)
    assert hook.main() == 0
    assert captured.getvalue() == ""


@pytest.mark.parametrize(
    ("env", "source"),
    [
        ({"PROBE_AGENT": "codex"}, "codex"),
        ({"PLUGIN_ROOT": "/x"}, "codex"),                              # Codex's own variable
        ({"PLUGIN_ROOT": "/x", "CLAUDE_PLUGIN_ROOT": "/y"}, "claude_code"),
        ({}, "claude_code"),
    ],
)
def test_the_hook_names_the_right_harness(hook, monkeypatch, env: dict, source: str) -> None:
    """THE BUDGET AND THE DISPATCH BOTH DEPEND ON IT. `available_bytes` differs
    per harness, and the two sentences differ too -- Codex is told to run the
    audit itself because its sandbox reaps a detached process. Reading
    `PROBE_AGENT` alone answered `claude_code` inside Codex, because the prompt
    hooks are the one group that never exported it."""
    for name in ("PROBE_AGENT", "PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    assert hook._source() == source


def test_the_wrapper_exports_the_harness_it_detects() -> None:
    """The python half above is the belt; this is the braces, and it is what the
    other six hook groups already do."""
    hooks = json.loads(_HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    command = next(
        entry["command"]
        for group in hooks["UserPromptSubmit"]
        for entry in group["hooks"]
        if "note_audit.py" in entry["command"]
    )
    assert 'export PROBE_AGENT=codex' in command
    assert command.index("PROBE_AGENT") < command.index("exec ")


def test_it_is_registered_on_user_prompt_submit() -> None:
    """WIRING, not capability: every other test here proves the file works and
    says nothing about whether a harness ever runs it."""
    hooks = json.loads(_HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    commands = [
        entry["command"]
        for group in hooks.get("UserPromptSubmit", [])
        for entry in group.get("hooks", [])
    ]
    assert any("note_audit.py" in c for c in commands), commands
    assert not any(
        "note_audit.py" in entry["command"]
        for event, groups in hooks.items()
        if event != "UserPromptSubmit"
        for group in groups
        for entry in group.get("hooks", [])
    ), "prompt submit is the presence signal; no other event proves a person"
