"""Jev's yes before the researcher's (shell approvals plan F8, `command_check`).

A shell command the safe list does not clear is put to Probe's command check
first, in every mode but bypass; only `approve` runs it unasked, and anything
else asks the researcher exactly as before. Probe is a fake here (no network):
`Check` stands in for `command_check.ask_probe`, and the client itself is
driven against a fake HTTP client.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time

import httpx
import pytest

from probe.daemon import approvals as appr, command_check, folders, lease, probe_api, tools
from probe.daemon.command_check import ask_probe as real_ask_probe
from probe.daemon.store import Store

SID = "11111111-2222-3333-4444-555555555555"
#: Off the safe list, and harmless: the gray zone the check is for (inline Python, the one shape Jev judges).
GRAY = "python3 -c \"print(open('file.txt').read()[:5])\""


@pytest.fixture(autouse=True)
def _python_on_path(tmp_path, monkeypatch):
    """`python3` on the daemon shell's PATH is this interpreter, outside the
    working folders, named by its version (a 3.11+), as on a normal machine."""
    real = os.path.realpath(sys.executable)
    if not tools._PYTHON_REAL.fullmatch(os.path.basename(real)):
        pytest.skip(f"the test interpreter's real file is not named by its version: {real}")
    sysbin = tmp_path / "pybin"
    sysbin.mkdir()
    (sysbin / "python3").symlink_to(real)
    monkeypatch.setenv("PATH", f"{sysbin}:/usr/bin:/bin")


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


def _deps(tmp_path, *, bypass: bool = False, mode_known: bool = True, write_dirs=None) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "file.txt").write_text("hello world\n")
    deps = tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=write_dirs or [],
                      probe_env={}, bypass=bypass, mode_known=mode_known, bite_id=1)
    deps.op_seed = f"{SID}:41"
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    assert lease.renew(SID)
    return deps


class Check:
    """Stands in for `command_check.ask_probe`: records each check, answers `answer`."""

    def __init__(self, answer: command_check.Answer | None, before=None) -> None:
        self.answer = answer
        self.calls: list[dict] = []
        self.before = before

    async def __call__(self, **kw):
        self.calls.append(kw)
        if self.before:
            self.before()
        return self.answer


YES = command_check.Answer(approve=True, scores={"a": 0.99, "b": 0.97}, mode="on")
NO = command_check.Answer(approve=False, scores={"a": 0.99, "b": 0.4}, mode="on")


def _check(monkeypatch, answer, before=None) -> Check:
    check = Check(answer, before)
    monkeypatch.setattr(command_check, "ask_probe", check)
    return check


def _writes(deps) -> list[dict]:
    return [dict(r) for r in deps.store.db.execute("SELECT status, reason, request, argv FROM writes ORDER BY id")]


def _run(coro):
    return asyncio.run(coro)


def test_jevs_yes_runs_it_unasked_and_the_logbook_says_so(tmp_path, monkeypatch):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, GRAY, why="the researcher asked for the first word"))
    assert out.startswith("[auto-approved: Jev p=0.97 · exit 0]") and out.rstrip().endswith("hello"), out
    assert deps.board.all() == [], "nothing was put to the researcher"
    assert deps.asked == 0
    [row] = _writes(deps)
    assert (row["status"], row["reason"], row["request"]) == ("ran", "auto-approved: Jev p=0.97", None)
    [sent] = check.calls
    assert sent == {"command": GRAY, "cwd": str(deps.cwd), "reason": sent["reason"],
                    "working_folders": [str(deps.cwd.resolve())]}
    assert "python3" in sent["reason"]
    assert "researcher asked" not in json.dumps(sent), "the daemon's why never goes to Probe"


@pytest.mark.parametrize("answer", [NO, None], ids=["not approved", "no answer (error, timeout)"])
def test_anything_but_a_yes_asks_the_researcher_as_before(tmp_path, monkeypatch, answer):
    check = _check(monkeypatch, answer)
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, GRAY))
    assert "held for the researcher" in out
    [req] = deps.board.all()
    assert req.policy == "shell.unsafe_command" and req.state == appr.WAITING
    assert [r["status"] for r in _writes(deps)] == ["held"]
    assert len(check.calls) == 1


@pytest.mark.parametrize("mode_known", [True, False], ids=["default mode", "mode not read (pi)"])
def test_every_mode_but_bypass_asks_jev(tmp_path, monkeypatch, mode_known):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path, mode_known=mode_known)
    assert _run(tools.shell(deps, GRAY)).startswith("[auto-approved: Jev")
    assert len(check.calls) == 1


def test_a_bypass_flag_with_an_unread_mode_asks_jev(tmp_path, monkeypatch):
    """`bypass` counts only when the mode was read: otherwise the daemon would
    ask, so Jev is asked first."""
    check = _check(monkeypatch, NO)
    deps = _deps(tmp_path, bypass=True, mode_known=False)
    assert "held for the researcher" in _run(tools.shell(deps, GRAY))
    assert len(check.calls) == 1


def test_bypass_runs_it_as_before_and_never_asks_jev(tmp_path, monkeypatch):
    check = _check(monkeypatch, NO)
    deps = _deps(tmp_path, bypass=True)
    out = _run(tools.shell(deps, GRAY))
    assert out.startswith(f"[{appr.AUTO} · exit 0]"), out
    assert check.calls == []
    assert [r["reason"] for r in _writes(deps)] == [appr.AUTO]


def test_a_refusal_in_every_mode_never_reaches_jev(tmp_path, monkeypatch):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    deps.protected = folders.protected_paths()
    out = _run(tools.shell(deps, f"cut -c1-5 {folders.protected_paths()[2]}/x.json"))
    assert "refused in every mode" in out and check.calls == []


@pytest.mark.parametrize(
    "command",
    [
        "cut -c1-5 {service}/service.log",
        "python3 -c \"import socket; s = socket.socket(socket.AF_UNIX); s.connect('{socket}')\"",
    ],
)
def test_the_probe_service_is_refused_in_every_mode(tmp_path, monkeypatch, command):
    """Its socket runs the researcher's own setup actions (logout, uninstall,
    an update): as private as the approvals board, never judged."""
    from probe.service import paths as service_paths

    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    deps.protected = folders.protected_paths()
    sock = service_paths.socket_path()
    out = _run(tools.shell(deps, command.format(service=service_paths.service_dir(), socket=sock)))
    assert "refused in every mode" in out and check.calls == [], out


def test_a_command_naming_the_team_note_is_asked_never_judged(tmp_path, monkeypatch):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)  # no write folders: the team note is found on its own
    out = _run(tools.shell(deps, f"cut -c1-5 {folders.note_dirs()[-1]}/team-note.md"))
    assert "held for the researcher" in out
    assert check.calls == []


def test_a_command_naming_a_notes_folder_keeps_todays_answer(tmp_path, monkeypatch):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path, write_dirs=folders.note_dirs())
    out = _run(tools.shell(deps, f"cut -c1-5 {folders.note_dirs()[0]}/run-r1.md"))
    assert out.startswith("not run:") and "folders the daemon writes notes into" in out
    assert check.calls == []


@pytest.mark.parametrize("command", [
    "cat .env",
    "cat outside.txt .env.local",  # the checks stop at outside.txt; .env is still seen
    "python3 -c \"print(open('.env').read())\"",
    "head -c 20 deploy.pem",
    "python3 tool.py --key=id_ed25519",
    "wc -l conf/.netrc",  # (~/.netrc itself is refused in every mode)
])
def test_a_command_naming_a_credential_file_is_asked_never_judged(tmp_path, monkeypatch, command):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    (deps.cwd / ".env").write_text("TOKEN=x\n")
    (deps.cwd / "tool.py").write_text("print(1)\n")  # a script that exists: only the name holds it back
    out = _run(tools.shell(deps, command))
    assert "held for the researcher" in out, out
    assert check.calls == []
    assert tools._classify(deps, command, deps.cwd).credential is True


def test_a_credential_file_a_redirect_writes_is_asked_never_judged(tmp_path, monkeypatch):
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    assert "held for the researcher" in _run(tools.shell(deps, "echo TOKEN=x >> .env"))
    assert check.calls == []


def test_a_write_outside_the_folders_is_asked_when_jev_says_it_writes(tmp_path, monkeypatch):
    """The plan review's probe, as the checker now reads it. An rc-file append
    (`>> ~/.zshrc`) names a hidden file: never judged. A plain write outside the
    folders reaches Jev, whose `writes_nothing` answer is low (0.02 on the
    zshrc append in the replay), so the researcher is asked."""
    deps = _deps(tmp_path)
    check = _check(monkeypatch, YES)
    assert "held for the researcher" in _run(tools.shell(deps, "echo 'export PATH=$HOME/bin:$PATH' >> ~/.zshrc"))
    assert check.calls == []
    outside = tmp_path / "outside"
    outside.mkdir()
    command = f"python3 -c \"open('{outside}/log.txt', 'a').write('done')\""
    no = command_check.Answer(approve=False, scores={"no_network": 0.95, "no_secrets": 0.97, "writes_nothing": 0.02,
                                                     "fully_visible": 0.92, "no_process_control": 0.95}, mode="on")
    check = _check(monkeypatch, no)
    verdict = tools._classify(deps, command, deps.cwd)
    assert not verdict.safe and not verdict.refused and not verdict.credential and not verdict.private
    out = _run(tools.shell(deps, command))
    assert "held for the researcher" in out, out
    assert [c["command"] for c in check.calls] == [command]
    assert not (outside / "log.txt").exists()


def test_the_credential_flag_is_off_for_a_plain_question(tmp_path):
    deps = _deps(tmp_path)
    for command in (GRAY, "python3 -c \"import json; print(json.load(open('run.json'))['run_id'])\""):
        verdict = tools._classify(deps, command, deps.cwd)
        assert not verdict.safe and not verdict.refused and verdict.credential is False, command


def test_a_command_naming_probes_state_folder_is_asked_never_judged(tmp_path, monkeypatch):
    """The sessions' mode files live there: a yes from Jev to a write into one
    could flip the daemon into bypass."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    mode_file = folders._state_base() / "sessions" / f"{SID}.mode"
    (deps.cwd / "tool.py").write_text("print(1)\n")
    out = _run(tools.shell(deps, f"python3 tool.py --out={mode_file}"))
    assert "held for the researcher" in out, out
    # A redirect written relative to a `cd` (its path nowhere in the text) is seen too.
    out = _run(tools.shell(deps, f"cd .. && echo bypass > state/probe/sessions/{SID}.mode"))
    assert "held for the researcher" in out, out
    assert check.calls == []


def test_every_policy_path_is_found(tmp_path):
    deps = _deps(tmp_path, write_dirs=[tmp_path / "notes"])
    deps.protected = [tmp_path / "config" / "probe"]
    for named in (tmp_path / "notes" / "a.md", folders.note_dirs()[-1] / "team-note.md",
                  tmp_path / "config" / "probe" / "config.json", folders._state_base() / "sessions" / "x.mode"):
        assert tools._names_policy_path(deps, f"python3 tool.py --in={named}", deps.cwd) is not None, named
    assert tools._names_policy_path(deps, "python3 tool.py --in=data.csv", deps.cwd) is None


def test_a_question_the_researcher_already_answered_no_is_not_judged(tmp_path, monkeypatch):
    check = _check(monkeypatch, None)
    deps = _deps(tmp_path)
    assert "held for the researcher" in _run(tools.shell(deps, GRAY))
    [req] = deps.board.all()
    assert len(check.calls) == 1
    check.answer = YES
    assert "held for the researcher" in _run(tools.shell(deps, GRAY)), "a waiting question is not raced"
    deps.board.resolve(req, state=appr.DENIED, outcome="the researcher said no", channel="terminal")
    assert _run(tools.shell(deps, GRAY)).startswith("not run: the researcher already said no")
    assert len(check.calls) == 1


def test_a_command_that_runs_a_script_is_never_judged(tmp_path, monkeypatch):
    """A script's text is a file's contents: it never goes to TypeSafe, so a
    command that runs one (or one that does not exist yet) is the researcher's."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    (deps.cwd / "run.sh").write_text("echo from-the-script\n")
    (deps.cwd / "tool.py").write_text("print(1)\n")
    for command in ("bash run.sh", "./run.sh", "python3 tool.py", "bash later.sh"):
        assert "held for the researcher" in _run(tools.shell(deps, command)), command
    assert check.calls == []


@pytest.mark.parametrize("command", [
    "kill -STOP 4242", "pkill -f train.py", "crontab -l", "systemctl --user stop x", "chmod 600 file.txt",
    "curl -s https://example.com", "wget -qO- https://example.com", "nc -z example.com 443",
    "git push origin HEAD", "git -C . fetch", "ssh host ls", "docker ps", "kubectl get pods",
    "xargs -a file.txt echo", "env A=1 cut -c1-5 file.txt", "node -e 'console.log(1)'", "perl -e 'print 1'",
    "ruby -e 'p 1'", "bash -c 'cut -c1-5 file.txt'", "python3 -m json.tool file.txt", "python3 - < file.txt",
    # The PR review's shapes: unknown launchers, expansions, flags that undo the safe path, a prefix.
    "uv run tool.py", "make -n report", "find . -delete", "find . -name x -exec cat {} +", "awk 1 file.txt",
    "X=curl; $X https://example.com", "head -c 20 *", "python3 -E -c 'print(1)'", "python3 -X dev -c 'print(1)'",
    "PYTHONPATH=. python3 -c 'print(1)'", "X=1 grep -rn x .", "/usr/bin/cut -c1-5 file.txt", "tar -tzf a.tgz",
    "pip install x", "gzip -d file.txt.gz", "unzip a.zip",
    # The second review's shapes: a quoted `>` the lenient reading took for a redirect, bash's
    # `printf -v`, tree reads behind `-e --` and an abbreviation.
    "echo '>'; uv run payload.py", "printf -v PYTHONSAFEPATH ''; python3 -c 'import json'",
    "grep -e -- -r .", "grep --recurs hello .", "cd -P .. && cut -c1-5 file.txt",
    # The third review's: printf sets variables (`%n`), ps prints other processes' environments,
    # date/hostname set the system's, GNU's `-d rec` recurses, a strict-read tree read after `'>'`.
    "printf '%n' PATH; cut -c1-5 file.txt", "ps eww -p 1", "date -s 2026-10-16", "hostname changed",
    "grep -d rec needle .", "grep --dir=rec needle .", "echo '>'; grep -r needle .", "egrep needle file.txt",
    "xxd -r file.txt", "file -C -m file.txt",
    # The fourth review's: every program but inline Python is the safe list's, never Jev's.
    "cut -c1-5 file.txt", "head -c 20 file.txt", "file -zS file.txt", "diff -l file.txt file.txt",
    "gzip -Sc file.txt", "unzip -p --p -o a.zip", "xxd file.txt out.txt", "pip show --log out.log pip",
    "sha256sum -c file.txt", "jq -f prog.jq file.txt",
    # The fifth review's: a redirect or heredoc on the Python command, `-I`.
    "python3 -c 'print(1)' > out.txt", "python3 -c 'print(1)' 2>&1", "python3 -I -c 'print(1)'",
    "python3 -S -c pass <<EOF\npython3 -S -c 'print(1)'",
])
def test_what_jev_cant_see_is_never_judged(tmp_path, monkeypatch, command):
    """Only programs on `_JUDGEABLE` (and `python -c` on a 3.11+) go to Jev:
    `kill -STOP <pid>` writes nothing and sends nothing; `node -e`, `uv run`,
    `make` run code their words don't show; `$X` and globs expand to what the
    text doesn't show; `-E` turns PYTHONSAFEPATH off."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    out = _run(tools.shell(deps, command))
    assert "held for the researcher" in out or out.startswith("not run:"), (command, out)
    assert check.calls == [], command


def _pythons(tmp_path, monkeypatch, real_name: str):
    """A `python3` on PATH whose real file is `real_name`; running it would leave a mark."""
    sysbin = tmp_path / "sysbin"
    sysbin.mkdir(exist_ok=True)
    real = sysbin / real_name
    real.write_text(f"#!/bin/sh\ntouch {tmp_path}/ran\n")
    real.chmod(0o755)
    link = sysbin / "python3"
    if link.is_symlink():
        link.unlink()
    link.symlink_to(real)
    monkeypatch.setenv("PATH", f"{sysbin}:/usr/bin:/bin")
    return link


def test_python_c_is_judged_only_on_a_python_3_11_or_later_and_nothing_runs_to_find_out(tmp_path, monkeypatch):
    check = _check(monkeypatch, None)
    deps = _deps(tmp_path)
    command = 'python3 -c "import json; print(1)"'
    _pythons(tmp_path, monkeypatch, "python3.10")
    assert "held for the researcher" in _run(tools.shell(deps, command))
    assert check.calls == []
    other = _deps(tmp_path / "other")  # the first question still waits in `deps`: it is never raced
    _pythons(tmp_path, monkeypatch, "python3.12")
    assert "held for the researcher" in _run(tools.shell(other, command))
    assert [c["command"] for c in check.calls] == [command]
    assert not (tmp_path / "ran").exists(), "the interpreter was run to read its version"
    assert tools._python_judgeable(other, "python3", ["-S", "-B", "-c", "print(1)"], other.cwd)
    assert not tools._python_judgeable(other, "python3", ["-I", "-c", "print(1)"], other.cwd)  # -I drops -B's env
    assert not tools._python_judgeable(other, "python3", ["-E", "-c", "print(1)"], other.cwd)
    assert not tools._python_judgeable(other, "python3", ["-c"], other.cwd)


def test_a_program_inside_the_working_folders_is_never_judged(tmp_path, monkeypatch):
    """A repo's own `cut` first on PATH: the checker names it, and Jev never sees it."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    shim = deps.cwd / "bin" / "cut"
    shim.parent.mkdir()
    shim.write_text("#!/bin/sh\necho shim\n")
    shim.chmod(0o755)
    monkeypatch.setenv("PATH", f"{shim.parent}:/usr/bin:/bin")
    assert "held for the researcher" in _run(tools.shell(deps, GRAY))
    assert check.calls == []


def test_a_yes_is_bound_to_the_programs_it_was_given_for(tmp_path, monkeypatch):
    """G3: while Jev answers, `python3` on PATH is pointed at another file. The
    yes was for the old one, so the researcher is asked and nothing runs."""
    deps = _deps(tmp_path)
    link = _pythons(tmp_path, monkeypatch, "python3.12")
    other = link.parent / "python3.13"
    other.write_text(f"#!/bin/sh\ntouch {tmp_path}/swapped\n")
    other.chmod(0o755)

    def swap():
        link.unlink()
        link.symlink_to(other)

    check = _check(monkeypatch, YES, before=swap)
    out = _run(tools.shell(deps, 'python3 -c "print(1)"'))
    assert len(check.calls) == 1
    assert "held for the researcher" in out and not (tmp_path / "swapped").exists(), out


def test_the_daemons_shell_runs_python_with_safe_path():
    from probe.daemon import shell as sh

    env = sh.minimal_env()
    assert env["PYTHONSAFEPATH"] == "1" and env["PYTHONDONTWRITEBYTECODE"] == "1"


@pytest.mark.parametrize("command", [
    "cut -c1-5 .cache/notes.txt", "cut -c1-5 sub/.secret-dir/x.txt", "rg hello .", "grep -rn hello .",
    "diff -r . ..",
])
def test_hidden_paths_and_whole_tree_reads_are_never_judged(tmp_path, monkeypatch, command):
    """Jev's `no_secrets` scores a hidden file or a tree sweep like any harmless
    read (replay AUC ~0.57): `Verdict.private` keeps them the researcher's."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    for rel in (".cache/notes.txt", "sub/.secret-dir/x.txt"):
        (deps.cwd / rel).parent.mkdir(parents=True, exist_ok=True)
        (deps.cwd / rel).write_text("x\n")
    out = _run(tools.shell(deps, command))
    assert not out.startswith("[auto-approved: Jev"), (command, out)
    assert check.calls == [], command


def test_a_yes_is_checked_again_before_it_runs(tmp_path, monkeypatch):
    """G3: while Jev answers, `report.txt` is pointed at a key. The second look
    finds a different verdict, so the researcher is asked and nothing runs."""
    deps = _deps(tmp_path)
    (deps.cwd / "plain.txt").write_text("plain\n")
    key = tmp_path / ".ssh" / "id_ed25519"
    key.parent.mkdir()
    key.write_text("PRIVATE\n")
    link = deps.cwd / "report.txt"
    link.symlink_to(deps.cwd / "plain.txt")

    def retarget():
        link.unlink()
        link.symlink_to(key)

    check = _check(monkeypatch, YES, before=retarget)
    out = _run(tools.shell(deps, "python3 -c \"print(open('report.txt').read())\""))
    assert len(check.calls) == 1
    assert "PRIVATE" not in out and not out.startswith("[auto-approved: Jev"), out


# ---------------------------------------------------------------------------
# The client: `POST /v1/companion/command-check`, any failure is no answer.
# ---------------------------------------------------------------------------


class _Client:
    def __init__(self, respond) -> None:
        self.respond = respond
        self.sent: list[tuple[str, dict, dict]] = []

    async def post(self, url, *, json, headers, timeout):
        self.sent.append((url, json, headers))
        return await self.respond() if asyncio.iscoroutinefunction(self.respond) else self.respond()


def _client(monkeypatch, respond) -> _Client:
    from probe.daemon import model as model_mod

    client = _Client(respond)
    monkeypatch.setattr(model_mod, "endpoint", lambda: model_mod.Endpoint(base_url="https://probe.test/", key="k"))
    monkeypatch.setattr(model_mod, "_http_client", lambda: client)
    return client


def _ask(**kw):
    args = {"command": GRAY, "cwd": "/w", "reason": "r", "working_folders": ["/w"]}
    return _run(real_ask_probe(**{**args, **kw}))


def test_the_client_sends_the_check_and_reads_a_yes(monkeypatch):
    scores = {"no_network": 0.99, "no_secrets": 0.97}
    client = _client(monkeypatch, lambda: httpx.Response(200, json={"approve": True, "scores": scores, "mode": "on"}))
    answer = _ask(working_folders=[f"/w{i}" for i in range(20)] + ["/" + "x" * 2000], reason="r" * 5000)
    assert answer == command_check.Answer(approve=True, scores=scores, mode="on") and answer.lowest == 0.97
    [(url, body, headers)] = client.sent
    assert url == "https://probe.test/v1/companion/command-check" and headers == {"Authorization": "Bearer k"}
    assert set(body) == {"command", "cwd", "reason", "working_folders"}  # never a file's contents
    assert len(body["working_folders"]) == command_check.MAX_FOLDERS
    assert len(body["reason"]) == command_check.MAX_REASON_CHARS


@pytest.mark.parametrize("payload", [
    {"approve": True, "scores": {"a": 0.99, "b": None}, "mode": "on"},  # a missing answer is no yes
    {"approve": True, "scores": {"a": 0.99, "b": 1.5}, "mode": "on"},
    {"approve": True, "scores": {}, "mode": "on"},
    {"approve": "yes", "scores": {"a": 0.99}, "mode": "on"},
    {"approve": False, "scores": {"a": 0.99}, "mode": "shadow"},
])
def test_anything_short_of_a_whole_yes_is_not_approval(monkeypatch, payload):
    _client(monkeypatch, lambda: httpx.Response(200, json=payload))
    answer = _ask()
    assert answer is not None and answer.approve is False


def _raise():
    raise httpx.ConnectError("refused")


async def _slow():
    await asyncio.sleep(10)


@pytest.mark.parametrize("respond", [
    lambda: httpx.Response(403, json={"detail": {"code": "companion_disabled"}}),
    lambda: httpx.Response(422, json={}),
    lambda: httpx.Response(200, content=b"not json"),
    lambda: httpx.Response(200, json=["a list"]),
    _raise,
], ids=["403", "422", "not json", "not an object", "transport error"])
def test_any_failure_is_no_answer(monkeypatch, respond):
    _client(monkeypatch, respond)
    assert _ask() is None


def test_a_slow_probe_is_no_answer(monkeypatch):
    monkeypatch.setattr(command_check, "TIMEOUT_S", 0.05)
    _client(monkeypatch, _slow)
    assert _ask() is None


def test_no_daemon_key_is_no_answer():
    assert _ask() is None  # the suite's config is empty: `model.endpoint` raises NoKey


def test_nothing_is_judged_while_path_reaches_the_session(tmp_path, monkeypatch):
    """`egrep` and `zcat` are scripts that run `grep` and `gzip` through PATH: a
    repo's own `grep` on PATH would run on Jev's yes. So no command is judged
    while the shell's PATH holds a folder of the session."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    shim = deps.cwd / "bin" / "grep"
    shim.parent.mkdir()
    shim.write_text("#!/bin/sh\necho shim\n")
    shim.chmod(0o755)
    monkeypatch.setenv("PATH", f"/usr/bin:/bin:{shim.parent}")
    assert "held for the researcher" in _run(tools.shell(deps, GRAY))
    assert check.calls == []


def test_a_yes_is_bound_to_the_program_file_not_its_name(tmp_path, monkeypatch):
    """G3: the interpreter's file is written in place while Jev answers (same
    path, same name): its change time moves, so the researcher is asked."""
    deps = _deps(tmp_path)
    link = _pythons(tmp_path, monkeypatch, "python3.12")
    real = link.resolve()

    def rewrite():
        time.sleep(0.01)
        real.write_text(f"#!/bin/sh\ntouch {tmp_path}/rewritten\n")

    check = _check(monkeypatch, YES, before=rewrite)
    out = _run(tools.shell(deps, 'python3 -c "print(1)"'))
    assert len(check.calls) == 1
    assert "held for the researcher" in out and not (tmp_path / "rewritten").exists(), out


def test_a_program_whose_identity_cant_be_read_is_never_judged(tmp_path, monkeypatch):
    """G3 binds a yes to each program's file identity; with none to bind to, no yes."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    real_stat = tools.os.stat

    def stat(path, *a, **kw):
        if str(path).endswith(os.path.basename(os.path.realpath(sys.executable))):
            raise OSError("gone")
        return real_stat(path, *a, **kw)

    monkeypatch.setattr(tools.os, "stat", stat)
    assert "held for the researcher" in _run(tools.shell(deps, GRAY))
    assert check.calls == []


def test_a_quoted_operator_cannot_hide_a_hidden_file_behind_cd(tmp_path, monkeypatch):
    """The lenient scan takes a quoted `'>'` for a redirect and swallows the `;`
    and the `cd` after it, so `.bashrc` resolved in the wrong folder; the strict
    reading follows the `cd` and finds the hidden file."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    (tmp_path / ".bashrc").write_text("export TOKEN=x\n")
    command = f"python3 -S -c pass '>'; cd {tmp_path} && python3 -S -c \"print(open('.bashrc').read())\""
    out = _run(tools.shell(deps, command))
    assert not out.startswith("[auto-approved: Jev") and "TOKEN" not in out, out
    assert check.calls == []


def test_a_plain_cd_then_inline_python_is_still_judged(tmp_path, monkeypatch):
    """The strict scan adds refusals only: a harmless `cd sub && python3 -c` still reaches Jev."""
    check = _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    (deps.cwd / "sub").mkdir()
    (deps.cwd / "sub" / "m.json").write_text('{"loss": [0.3]}')
    command = "cd sub && python3 -c \"import json; print(json.load(open('m.json'))['loss'][-1])\""
    out = _run(tools.shell(deps, command))
    assert out.startswith("[auto-approved: Jev") and "0.3" in out, out
    assert [c["command"] for c in check.calls] == [command]


# -- T10 (R2): what Jev ran is listed for the researcher (`probe approvals`) --

OTHER = "22222222-3333-4444-5555-666666666666"
DAY = 86400


def _logged(session_id: str, *, at: float, reason: str | None, status: str = "ran", command: str = GRAY,
            head: str = "shell", request: str | None = None, argv: list[str] | None = None) -> None:
    """One line in that session's store, where the daemon keeps it."""
    from probe.daemon import store

    st = Store(store.store_path(session_id), clock=lambda: at)
    st.log_write(bite=1, op_id=f"op-{at}", argv=argv or ["sh", "-c", command], head=head, status=status,
                 reason=reason, exit_code=0 if status == "ran" else None, request=request)
    st.db.close()


@pytest.fixture
def no_agent(monkeypatch):
    """`probe approvals` run from the researcher's own terminal: no coding agent's variables."""
    from probe.harness.registry import get_registry

    for harness in get_registry().all():
        for name in (*harness.detect_env, harness.session_env):
            if name:
                monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    monkeypatch.delenv("PROBE_AGENT_SESSION", raising=False)


def test_jevs_yeses_are_read_from_every_sessions_store_newest_first():
    from probe.daemon import store

    now = time.time()
    _logged(SID, at=now - 60, reason="auto-approved: Jev p=0.91")
    _logged(SID, at=now - 30, reason=f"auto-approved: Jev p=0.88; {store.CUT_SHORT}", status="cancelled",
            command="python3 -c 'print(2)'")
    _logged(OTHER, at=now - 10, reason="auto-approved: Jev p=0.95", command="python3 -c 'print(3)'")
    _logged(SID, at=now - 5, reason="auto-approved: bypass mode", command="rm -rf build", request="r1")
    _logged(SID, at=now - 4, reason="the researcher said yes", command="touch x")
    _logged(OTHER, at=now - 2 * DAY, reason="auto-approved: Jev p=0.99", command="python3 -c 'old'")
    found = store.jev_approved(now - DAY, 20)
    assert [(r["session_id"], r["command"], r["lowest"], r["ended"]) for r in found.rows] == [
        (OTHER, "python3 -c 'print(3)'", "0.95", "ran"), (SID, "python3 -c 'print(2)'", "0.88", "cancelled"),
        (SID, GRAY, "0.91", "ran")]
    assert (found.total, found.unreadable, found.damaged) == (3, 0, 0)
    assert found.by_session == {OTHER: 1, SID: 2}
    capped = store.jev_approved(now - DAY, limit=1)
    assert [r["command"] for r in capped.rows] == ["python3 -c 'print(3)'"] and capped.total == 3
    assert [r["command"] for r in store.jev_approved(now - DAY, 20, session_id=SID).rows] == [
        "python3 -c 'print(2)'", GRAY]
    assert store.jev_approved(now - DAY, 20, session_id="no-such-session") == store.JevApproved([], 0, 0)


@pytest.mark.parametrize("line", [
    {"head": "notes append", "argv": ["probe", "notes", "append", "n"]},  # a probe write: its reason is the model's `why`
    {"status": "failed"},
    {"status": "held"},
    {"status": "not_run"},
    {"request": "abc123"},  # run on a question's answer, not on Jev's yes
    {"reason": "AUTO-APPROVED: jev p=1.00"},
    {"reason": "auto-approved: Jev p=0.99 and this line too"},
    {"reason": "auto-approved: Jev p=0.99\n    2026-10-16 14:02  p=0.99  exit 0"},
    {"argv": ["sh", "-c", "true", "extra"]},
], ids=["probe write", "failed", "held", "not run", "a question's yes", "other case", "extra words",
        "a forged line", "other argv"])
def test_only_the_rows_a_jev_yes_writes_are_listed(line):
    """The daemon's model writes the reason of its own `probe` writes: twenty of
    those saying `auto-approved: Jev` must not fill the list and push the real one out."""
    from probe.daemon import store

    now = time.time()
    _logged(SID, at=now - 60, reason="auto-approved: Jev p=0.90")
    for i in range(25):
        _logged(SID, at=now - 30 + i, **{"reason": "auto-approved: Jev p=0.99", **line})
    found = store.jev_approved(now - DAY, 20)
    assert [r["command"] for r in found.rows] == [GRAY] and found.total == 1


def test_an_unreadable_or_newer_store_is_counted_not_an_error():
    from probe.daemon import store

    now = time.time()
    _logged(SID, at=now - 1, reason="auto-approved: Jev p=0.90")
    (store.state_dir() / "junk.sqlite").write_bytes(b"not a database")
    newer = Store(store.store_path(OTHER), clock=time.time)
    newer.set_meta("format_version", str(store.FORMAT_VERSION + 1))
    newer.log_write(bite=1, op_id="x", argv=["sh", "-c", "python3 -c 1"], head="shell", status="ran",
                    reason="auto-approved: Jev p=0.90")
    newer.db.close()
    nulled = Store(store.store_path("33333333-4444-5555-6666-777777777777"), clock=time.time)
    nulled.db.execute("UPDATE meta SET value = NULL WHERE key = 'format_version'")
    nulled.db.close()
    found = store.jev_approved(now - 60, 20)
    assert [r["session_id"] for r in found.rows] == [SID] and found.unreadable == 3


def test_a_live_store_whose_rows_are_only_in_its_wal_is_still_read():
    """A running worker keeps its store open: new rows sit in the -wal file
    while the main file's time is its last checkpoint's, maybe days ago."""
    from probe.daemon import store

    now = time.time()
    path = store.store_path(SID)
    live = Store(path, clock=lambda: now - 60)
    live.log_write(bite=1, op_id="a", argv=["sh", "-c", GRAY], head="shell", status="ran",
                   reason="auto-approved: Jev p=0.90")
    assert path.with_name(path.name + "-wal").exists()
    os.utime(path, (now - 3 * DAY,) * 2)
    try:
        assert [r["command"] for r in store.jev_approved(now - DAY, 20).rows] == [GRAY]
    finally:
        live.db.close()
    os.utime(path, (now - 3 * DAY,) * 2)
    assert store.jev_approved(now - DAY, 20).rows == [], "both files older than the window: not opened"


def test_a_worker_closing_between_the_two_looks_still_lists_its_rows(monkeypatch):
    """The worker closes its store right after the reader's first look: the -wal
    is gone and its rows are in the main file, whose time is now new."""
    from pathlib import Path

    from probe.daemon import store

    now = time.time()
    path = store.store_path(SID)
    live = Store(path, clock=lambda: now - 60)
    live.log_write(bite=1, op_id="a", argv=["sh", "-c", GRAY], head="shell", status="ran",
                   reason="auto-approved: Jev p=0.90")
    os.utime(path, (now - 3 * DAY,) * 2)  # its last checkpoint, days ago
    real_stat, looks = Path.stat, []

    def stat(self, *a, **kw):
        result = real_stat(self, *a, **kw)
        if self.name.startswith(SID) and not looks:
            looks.append(self.name)
            live.db.close()  # checkpoints into the main file and removes the -wal
        return result

    monkeypatch.setattr(Path, "stat", stat)
    assert [r["command"] for r in store.jev_approved(now - DAY, 20).rows] == [GRAY]
    assert looks == [f"{SID}.sqlite-wal"], "the -wal is looked at first"


def test_a_state_folder_with_uri_characters_in_its_name_is_read(tmp_path, monkeypatch):
    from probe.daemon import store

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "st?a#b%c"))
    _logged(SID, at=time.time() - 60, reason="auto-approved: Jev p=0.90")
    found = store.jev_approved(time.time() - DAY, 20)
    assert [r["command"] for r in found.rows] == [GRAY] and found.unreadable == 0


@pytest.mark.parametrize(("ending", "listed_as"), [
    ("ran", "ran"), ("cut short", "cancelled"), ("raised", "failed"), ("stopped before the launch", None),
], ids=["ran", "cut short while it ran", "failed while it ran", "never started"])
def test_a_jev_yes_the_daemon_runs_is_what_the_list_reads(tmp_path, monkeypatch, ending, listed_as):
    """Written by the real path (`tools.shell` on Jev's yes), read back by
    `jev_approved`; while it runs its line already says so (`running`), so a
    worker killed meanwhile leaves it listed."""
    from probe.daemon import shell as sh
    from probe.daemon import store

    _check(monkeypatch, YES)
    deps = _deps(tmp_path)
    deps.store = Store(store.store_path(SID), clock=time.time)
    real_run, seen_while_running = sh.run, []

    async def run(*a, **kw):
        [line] = store.jev_approved(time.time() - 60, 20).rows
        seen_while_running.append(line["ended"])
        if ending == "cut short":
            raise asyncio.CancelledError
        if ending == "raised":
            raise OSError("reading its output failed")
        if ending == "stopped before the launch":
            return sh.ShellResult(exit_code=None, output="", truncated=False, timed_out=False,
                                  stopped="the researcher switched Probe off", started=False)
        return await real_run(*a, **kw)

    monkeypatch.setattr(sh, "run", run)
    if ending in ("cut short", "raised"):
        with pytest.raises((asyncio.CancelledError, OSError)):
            _run(tools.shell(deps, GRAY))
    else:
        assert _run(tools.shell(deps, GRAY)).startswith("[auto-approved: Jev p=0.97")
    assert seen_while_running == ["running"]
    [row] = _writes(deps)
    assert row["status"] == ("not_run" if listed_as is None else listed_as), row
    if listed_as == "cancelled":
        assert row["reason"] == f"auto-approved: Jev p=0.97; {store.CUT_SHORT}"
    if listed_as == "failed":
        assert row["reason"] == f"auto-approved: Jev p=0.97; {store.FAILED_WHILE_RUNNING} (OSError)"
    listed = store.jev_approved(time.time() - 60, 20)
    assert [(r["command"], r["lowest"], r["ended"]) for r in listed.rows] == (
        [] if listed_as is None else [(GRAY, "0.97", listed_as)])
    assert listed.damaged == 0


def test_a_command_whose_worker_died_while_it_ran_is_listed(capsys, no_agent):
    """`_run_shell_write` logs it `running` before the launch; a SIGKILLed worker never updates it."""
    from probe.cli import daemon_cli

    _logged(SID, at=time.time() - 60, reason="auto-approved: Jev p=0.90", status="running")
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert "p=0.90  still running, or the daemon stopped while it ran\n      " + GRAY in out


def test_a_damaged_line_is_counted_never_a_crash(capsys, no_agent):
    """Lines the shape filter passes but no Jev yes is written like: said, not dropped or fatal."""
    from probe.cli import daemon_cli
    from probe.daemon import store

    now = time.time()
    _logged(SID, at=now - 90, reason="auto-approved: Jev p=0.90")
    st = Store(store.store_path(SID), clock=lambda: now - 60)
    for argv in ('["sh", "-c", null]', "not json"):
        st.db.execute("INSERT INTO writes (bite, op_id, at, argv, head, status, reason) VALUES "
                      "(1, 'x', ?, ?, 'shell', 'ran', 'auto-approved: Jev p=0.99')", (now - 60, argv))
    st.db.execute("INSERT INTO writes (bite, op_id, at, argv, head, status, reason) VALUES "
                  "(1, 'y', 'yesterday', '[\"sh\", \"-c\", \"true\"]', 'shell', 'ran', "
                  "'auto-approved: Jev p=0.99')")
    st.db.execute("INSERT INTO writes (bite, op_id, at, argv, head, status, reason) VALUES "
                  "(1, 'z', ?, '[\"sh\", \"-c\", \"true\"]', 'shell', 'failed', 'auto-approved: Jev p=0.99')",
                  (now - 40,))  # a failure without the reason a failure is logged with
    st.db.close()
    found = store.jev_approved(now - DAY, 20)
    assert [r["command"] for r in found.rows] == [GRAY] and found.damaged == 4
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert GRAY in out and "4 logbook line(s) that name Jev are in a shape the daemon never writes" in out


def test_a_store_that_is_there_and_cannot_be_read_is_counted(no_agent):
    """Its own session's store unreadable (permissions): never read as "nothing ran"."""
    from probe.daemon import store

    _logged(SID, at=time.time() - 60, reason="auto-approved: Jev p=0.90")
    folder = store.state_dir()
    folder.chmod(0o600)  # no search permission: stat() raises PermissionError, not FileNotFoundError
    try:
        if os.access(store.store_path(SID), os.R_OK):
            pytest.skip("this user reads through any permission (root)")
        found = store.jev_approved(time.time() - DAY, 20, session_id=SID)
        assert (found.rows, found.unreadable) == ([], 1)
    finally:
        folder.chmod(0o700)
    assert store.jev_approved(time.time() - DAY, 20, session_id="no-such-session").unreadable == 0


@pytest.mark.parametrize("waiting", [False, True], ids=["nothing waiting", "a question waiting"])
def test_probe_approvals_lists_what_jev_ran_without_asking(capsys, no_agent, waiting):
    from probe.cli import daemon_cli
    from probe.daemon import store

    now = time.time()
    long = "python3 -c \"import json\n# a comment line\nprint(json.load(open('m.json'))['" + "x" * 200 + "'])\""
    _logged(SID, at=now - 90, reason="auto-approved: Jev p=0.91", command=long)
    _logged(SID, at=now - 60, reason=f"auto-approved: Jev p=0.88; {store.CUT_SHORT}", status="cancelled",
            command="python3 -c 'print(2)'")
    _logged(OTHER, at=now - 50, reason="auto-approved: Jev p=0.95", command="python3 -c 'print(\x1b[2K3)'")
    _logged(OTHER, at=now - 40, reason="auto-approved: Jev p=0.93", command="python3 -c 'import time'")
    _logged(SID, at=now - 30, reason="auto-approved: bypass mode", command="rm -rf build", request="r1")
    if waiting:
        appr.Board().hold(policy="shell.unsafe_command", session_id=SID, bypass=False,
                          facts={"command": "curl x", "cwd": "/w", "why_asking": "network", "reason": "r"},
                          held={"kind": "shell", "command": "curl x", "cwd": "/w", "op_id": "o"})
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert ("curl x" in out) is waiting and ("nothing is waiting for you" in out) is not waiting
    tail = out[out.index("Run without asking you, on Jev's yes (the last 24 hours"):]
    assert tail.index(f"session {OTHER}") < tail.index(f"session {SID}"), "newest session first"
    assert tail.count(f"session {SID}") == 1
    assert "p=0.95  exit 0\n      python3 -c 'print(\\x1b[2K3)'" in tail, "an escape is shown, never acted on"
    assert "\x1b" not in out
    assert "p=0.88  cut short while it ran\n      python3 -c 'print(2)'" in tail
    assert "p=0.93  exit 0" in tail
    assert "p=0.91  exit 0\n      python3 -c \"import json\n      # a comment line\n      print(" in tail
    assert "x" * 200 in tail, "a command Jev approved is shown whole"
    assert "rm -rf build" not in out, "bypass mode's runs are not Jev's"
    assert "(every decision the daemon made in a session: `probe companion log <session>`)" in tail
    assert "more not shown" not in tail and "with its output" not in tail


def test_probe_approvals_says_how_many_it_did_not_show(capsys, no_agent):
    from probe.cli import daemon_cli
    from probe.daemon import store

    now = time.time()
    for i in range(daemon_cli.JEV_SHOWN + 3):
        _logged(SID, at=now - 100 + i, reason="auto-approved: Jev p=0.90", command=f"python3 -c 'print({i})'")
    (store.state_dir() / "junk.sqlite").write_bytes(b"not a database")
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert out.count("exit 0") == daemon_cli.JEV_SHOWN
    assert f"and 3 more not shown (session {SID}: 3): every one is in `probe companion log <session>`" in out
    assert "1 session logbook(s) could not be read just now" in out


def test_a_coding_agents_shell_sees_its_own_sessions_only(capsys, no_agent, monkeypatch):
    """Its output lands in its transcript, uploaded with its session: another
    session's commands are another project's."""
    from probe.cli import daemon_cli

    now = time.time()
    _logged(SID, at=now - 60, reason="auto-approved: Jev p=0.91", command="python3 -c 'mine'")
    _logged(OTHER, at=now - 50, reason="auto-approved: Jev p=0.95", command="python3 -c 'theirs'")
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert "on Jev's yes (in this session, the last 24 hours" in out
    assert "python3 -c 'mine'" in out and "theirs" not in out and OTHER not in out
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID")  # an agent marker without its session: none is its own
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert "mine" not in out and "theirs" not in out
    assert "listed by `probe approvals` in the researcher's own terminal" in out, "said, not dropped"


def test_the_daemons_own_shell_sees_its_own_sessions_only(capsys, no_agent, monkeypatch):
    """Its `probe` calls carry only PROBE_DAEMON_SESSION (`worker.probe_env`)."""
    from probe.cli import daemon_cli

    now = time.time()
    _logged(SID, at=now - 60, reason="auto-approved: Jev p=0.91", command="python3 -c 'mine'")
    _logged(OTHER, at=now - 50, reason="auto-approved: Jev p=0.95", command="python3 -c 'theirs'")
    monkeypatch.setenv("PROBE_DAEMON_SESSION", SID)
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert "python3 -c 'mine'" in out and "theirs" not in out


def test_a_run_with_no_exit_code_says_it_timed_out_or_was_stopped(capsys, no_agent):
    """`_run_shell_write` logs a timed-out or stopped command as ran, with no exit code."""
    from probe.cli import daemon_cli
    from probe.daemon import store

    st = Store(store.store_path(SID), clock=lambda: time.time() - 60)
    st.log_write(bite=1, op_id="a", argv=["sh", "-c", GRAY], head="shell", status="ran",
                 reason="auto-approved: Jev p=0.90", exit_code=None)
    st.db.close()
    daemon_cli.approvals_cmd(list_only=True)
    assert "p=0.90  no exit code (timed out or stopped)" in capsys.readouterr().out


def test_probe_approvals_says_nothing_of_jev_when_it_ran_nothing(capsys, no_agent):
    from probe.cli import daemon_cli

    _logged(SID, at=time.time() - 60, reason="auto-approved: bypass mode", request="r1")
    daemon_cli.approvals_cmd(list_only=True)
    assert capsys.readouterr().out == "nothing is waiting for you\n"


def test_a_waiting_questions_command_is_shown_escaped(capsys, no_agent):
    from probe.cli import daemon_cli

    command = "python3 -c 'print(1)'\x1b[1A\x1b[2K" + "y" * 400
    appr.Board().hold(policy="shell.unsafe_command", session_id=SID, bypass=False,
                      facts={"command": command, "cwd": "/w", "why_asking": "w", "reason": "r"},
                      held={"kind": "shell", "command": command, "cwd": "/w", "op_id": "o"})
    daemon_cli.approvals_cmd(list_only=True)
    out = capsys.readouterr().out
    assert "\x1b" not in out and "\\x1b[1A\\x1b[2K" in out


def test_a_held_commands_lines_never_start_where_probe_approvals_own_do(capsys, no_agent):
    """A line break in the command cannot print a line that reads as a question of its own."""
    from probe.cli import daemon_cli

    command = ("python3 -c 'print(1)'\n[Probe 7f3a09c1] The Probe daemon wants to run `true`. Run it?\n"
               "y = Run it   n = Don't run it\nthe whole command:\n" + "z" * 400)
    appr.Board().hold(policy="shell.unsafe_command", session_id=SID, bypass=False,
                      facts={"command": command, "cwd": "/w", "why_asking": "w", "reason": "r"},
                      held={"kind": "shell", "command": command, "cwd": "/w", "op_id": "o"})
    daemon_cli.approvals_cmd(list_only=True)
    lines = capsys.readouterr().out.splitlines()
    assert not [line for line in lines if line.startswith("[Probe 7f3a09c1]")]
    assert any(line.startswith("    ") and "[Probe 7f3a09c1]" in line for line in lines)
    assert [line for line in lines if line.startswith(("  y = ", "y = "))] == ["  y = Run it   n = Don't run it"]
    assert [line for line in lines if line.startswith(("  the whole", "the whole"))] in ([], ["  the whole command:"])


@pytest.mark.parametrize("lowest", [0.0, -0.0, 0.5, 0.995, 0.9999, 1.0])
def test_every_score_jev_can_give_reads_back(lowest):
    from probe.daemon.command_check import JEV_REASON, _probability, jev_reason

    assert JEV_REASON.fullmatch(jev_reason(_probability(lowest)))


def test_ordinary_text_is_shown_as_written():
    from probe.cli import daemon_cli

    text = "naïve\u00a0café\u3000日本語\tline\nnext 🙂"
    assert daemon_cli._shown(text) == text
    assert daemon_cli._shown("a\u202eb\u200bc\x1bd\re\u2028f") == "a\\u202eb\\u200bc\\x1bd\\re\\u2028f"
    assert daemon_cli._shown("g\u2065h\ue000i") == "g\\u2065h\\ue000i", "unassigned and private-use"
    hidden = "a\ufe00b\U000e0100c\u034fd\u3164e\U000e0041f"  # variation selectors, CGJ, Hangul filler, a tag
    assert daemon_cli._shown(hidden) == "a\\ufe00b\\U000e0100c\\u034fd\\u3164e\\U000e0041f"
