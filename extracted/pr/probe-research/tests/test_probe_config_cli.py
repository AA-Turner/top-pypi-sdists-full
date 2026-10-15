"""`.probe.config` on the CLI: the write gate, `probe exec`, `probe ignore check`,
`probe session parent`, the retired `--folder`, and doctor's conversion.

Every test runs in an isolated home with no server: these paths decide BEFORE
anything is sent, and a refusal that reached the network would be a bug.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.cli import probe_config_cli, write_gate
from probe.sdk import agent_session, probe_config as pc, session_marker

SID = "11111111-aaaa-bbbb-cccc-222222222222"


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    for agent in agent_session.AGENTS:
        if agent.session_env:
            monkeypatch.delenv(agent.session_env, raising=False)
    for name in ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID", "KIMI_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "home").mkdir()
    pc._CACHE.clear()
    return tmp_path


def _in_session(monkeypatch, state="full"):
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    session_marker.set_session_state(SID, state)


# ---------------------------------------------------------------------------
# The write gate
# ---------------------------------------------------------------------------


def test_a_write_from_an_excluded_folder_is_refused(home, monkeypatch, capsys):
    repo = home / "repo"
    repo.mkdir()
    (repo / pc.CONFIG_NAME).write_text("*\n")
    monkeypatch.chdir(repo)
    assert cli.main(["notes", "push", "x.md"]) == write_gate.EXIT_REFUSED
    err = capsys.readouterr().err
    assert "is excluded by" in err and ".probe.config:1 (*)" in err and "do not route around it" in err


def test_a_write_naming_an_excluded_path_is_refused(home, monkeypatch, capsys):
    (home / pc.CONFIG_NAME).write_text("/secret/\n")
    (home / "secret").mkdir()
    (home / "secret" / "w.pt").write_text("x")
    monkeypatch.chdir(home)
    refused = write_gate.excluded_refusal(["artifact", "add", "run-1", "secret/w.pt"])
    assert refused is not None and refused[1] is None
    assert "secret/w.pt" in refused[0]


def test_a_bare_word_that_is_a_folder_name_is_not_a_path(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("/data/\n")
    (home / "data").mkdir()
    monkeypatch.chdir(home)
    assert write_gate.excluded_refusal(["run", "create", "--name", "data"]) is None


def test_reads_and_help_are_never_refused(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("*\n")
    sub = home / "x"
    sub.mkdir()
    monkeypatch.chdir(sub)
    assert write_gate.excluded_refusal(["run", "list"]) is None
    assert write_gate.excluded_refusal(["notes", "push", "--help"]) is None


def test_exec_runs_the_command_unrecorded(home, monkeypatch, tmp_path):
    repo = home / "repo"
    repo.mkdir()
    (repo / pc.CONFIG_NAME).write_text("*\n")
    monkeypatch.chdir(repo)
    message, child = write_gate.excluded_refusal(["exec", "--", "python", "train.py"])
    assert child == ["python", "train.py"]
    assert "`probe exec` opens no run; running the command directly" in message


def test_exec_of_an_excluded_script_from_elsewhere(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("/secret/\n")
    (home / "secret").mkdir()
    (home / "secret" / "t.py").write_text("print(1)")
    monkeypatch.chdir(home)
    message, child = write_gate.excluded_refusal(["exec", "--", "python", "secret/t.py"])
    assert child == ["python", "secret/t.py"]


def test_session_answer_sets_parent_files_aside(home, monkeypatch, capsys):
    code = home / "code"
    launch = code / "repo-a"
    launch.mkdir(parents=True)
    (code / pc.CONFIG_NAME).write_text("/*\n")
    _in_session(monkeypatch)
    session_marker.record_launch_dir(SID, str(launch))
    monkeypatch.chdir(launch)
    assert write_gate.excluded_refusal(["notes", "push", "x.md"]) is not None

    # The agent may record the researcher's answer only with --directed.
    assert cli.main(["session", "parent", "ignore"]) == write_gate.EXIT_REFUSED
    assert "runs only with `--directed`" in capsys.readouterr().err
    assert cli.main(["session", "parent", "ignore", "--directed"]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert out["parent"] == "ignore" and out["parent_files"]
    assert write_gate.excluded_refusal(["notes", "push", "x.md"]) is None

    assert cli.main(["session", "parent", "follow", "--directed"]) in (0, None)
    capsys.readouterr()
    assert write_gate.excluded_refusal(["notes", "push", "x.md"]) is not None


def test_session_parent_rejects_other_words(home, monkeypatch, capsys):
    _in_session(monkeypatch)
    assert cli.main(["session", "parent", "maybe", "--directed"]) == 1


def test_status_carries_the_probe_config_block(home, monkeypatch, capsys):
    code = home / "code"
    launch = code / "repo-a"
    launch.mkdir(parents=True)
    (code / pc.CONFIG_NAME).write_text("*.ckpt\n")
    _in_session(monkeypatch)
    session_marker.record_launch_dir(SID, str(launch))
    import importlib

    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_unfiled_runs_block", lambda: None)
    assert cli.main(["session", "status"]) in (0, None)
    block = json.loads(capsys.readouterr().out)["probe_config"]
    assert block["parent"] == "unasked"
    assert block["launch_dir"] == str(launch)


# ---------------------------------------------------------------------------
# probe ignore check
# ---------------------------------------------------------------------------


def test_ignore_check(home, monkeypatch, capsys):
    (home / pc.CONFIG_NAME).write_text("# models\n*.ckpt\n")
    monkeypatch.chdir(home)
    assert cli.main(["ignore", "check", "m.ckpt", "train.py"]) in (0, None)
    rows = json.loads(capsys.readouterr().out)
    assert rows[0]["excluded"] is True and rows[0]["source"].endswith(".probe.config:2 (*.ckpt)")
    assert rows[0]["level"] == "off"
    assert rows[1] == {
        "path": rows[1]["path"], "level": "on", "excluded": False, "identity_only": False, "source": None, "at": None,
    }


def test_ignore_check_prints_each_level_and_its_line(home, monkeypatch, capsys):
    (home / pc.CONFIG_NAME).write_text("@probe read\nnotebooks/\nnotebooks/public.md @probe on\n")
    (home / "notebooks").mkdir()
    monkeypatch.chdir(home)
    assert cli.main(["ignore", "check", "notebooks/a.ipynb", "notebooks/public.md"]) in (0, None)
    nb, public = json.loads(capsys.readouterr().out)
    assert (nb["level"], nb["excluded"]) == ("read", True) and nb["source"].endswith(".probe.config:2 (notebooks/)")
    assert (public["level"], public["excluded"]) == ("on", False)
    assert public["source"].endswith(".probe.config:3 (notebooks/public.md @probe on)")


def test_ignore_check_is_allowed_in_the_daemon_profile():
    assert "ignore check" in session_marker.DAEMON_PROFILE_ALLOWED
    assert "session parent" in session_marker.DAEMON_PROFILE_ALLOWED


# ---------------------------------------------------------------------------
# Folder defaults retired
# ---------------------------------------------------------------------------


def test_session_default_folder_is_retired(home, capsys):
    assert cli.main(["session", "default", "off", "--folder", str(home)]) == 1
    assert "Folder defaults are retired" in capsys.readouterr().err
    assert not (home / ".probe" / "config.json").exists()


def test_new_sessions_no_longer_read_folder_defaults(home, monkeypatch):
    repo = home / "repo"
    (repo / ".probe").mkdir(parents=True)
    (repo / ".probe" / "config.json").write_text(json.dumps({"defaults": {"session_state": "off"}}))
    state, source = session_marker.resolve_state_default(str(repo))
    assert source in ("shipped", str(session_marker.config_path()))
    # ...but in an agent session the retired `off` still keeps the folder out
    # of Probe; outside one (a training node) it never applied.
    assert pc.check(repo / "x.py", legacy=True).excluded
    assert not pc.check(repo / "x.py").excluded


def test_doctor_finds_and_converts_retired_defaults(home, monkeypatch):
    off = home / "home" / "a"
    on = home / "home" / "b"
    for folder, word in ((off, "off"), (on, "full")):
        (folder / ".probe").mkdir(parents=True)
        (folder / ".probe" / "config.json").write_text(json.dumps({"defaults": {"session_state": word}}))
    monkeypatch.chdir(home / "home")
    rows = probe_config_cli.doctor_rows()
    assert any("retired folder default (`off`)" in r for r in rows)
    assert any("does nothing now" in r for r in rows)

    rows = probe_config_cli.doctor_rows(fix=True)
    assert len(rows) == 2
    assert (off / pc.CONFIG_NAME).read_text() == "*\n"
    assert not (off / ".probe").exists() and not (on / ".probe").exists()
    assert not (on / pc.CONFIG_NAME).exists()
    assert pc.check(off / "x.py").excluded
    assert probe_config_cli.doctor_rows() == []


def test_doctor_fix_keeps_an_existing_probe_config(home, monkeypatch):
    folder = home / "home" / "c"
    (folder / ".probe").mkdir(parents=True)
    (folder / ".probe" / "config.json").write_text(json.dumps({"defaults": {"session_state": "read-only"}}))
    (folder / ".probe" / "other").write_text("keep")
    (folder / pc.CONFIG_NAME).write_text("!keep.py\n")
    probe_config_cli.convert(str(folder))
    assert (folder / pc.CONFIG_NAME).read_text() == "*\n!keep.py\n"
    assert (folder / ".probe" / "other").exists()  # the folder holds more: left


def test_missing_paths_and_file_uris_are_checked(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("/secret/\n")
    monkeypatch.chdir(home)
    assert write_gate.excluded_refusal(["artifact", "add", "r1", "secret/not-yet.pt", "--reference", "--allow-missing"])
    assert write_gate.excluded_refusal(["artifact", "add", "r1", "--uri", f"file://{home}/secret/w.pt"])


def test_manifest_rows_are_checked(home, monkeypatch):
    import importlib

    import typer

    main_mod = importlib.import_module("probe.cli.main")
    (home / pc.CONFIG_NAME).write_text("/secret/\n")
    (home / "secret").mkdir()
    (home / "secret" / "w.pt").write_text("x")
    monkeypatch.chdir(home)
    with pytest.raises(typer.BadParameter, match="excluded by"):
        main_mod._plan_manifest_row({"path": "secret/w.pt", "run": "r1"}, default_anchor=None, reference_over=0)


def test_only_unmistakable_paths_count_when_missing(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("data\nsecret*\n")
    monkeypatch.chdir(home)
    assert write_gate.excluded_refusal(["run", "create", "--name=eval/data"]) is None
    assert write_gate.excluded_refusal(["run", "create", "exp/secret-sauce"]) is None
    assert write_gate.excluded_refusal(["exec", "--", "python", "train.py", "--model", "meta-llama/Llama-3-8B"]) is None
    assert write_gate.excluded_refusal(["artifact", "add", "r1", "out/data", "--allow-missing", "--reference"])
    assert write_gate.excluded_refusal(["notes", "push", "./secret-notes.md"])


def test_output_paths_into_an_existing_folder_count(home, monkeypatch):
    (home / pc.CONFIG_NAME).write_text("out/\n")
    (home / "out").mkdir()
    monkeypatch.chdir(home)
    assert write_gate.excluded_refusal(["exec", "--", "python", "t.py", "--out", "out/run1"])
    assert write_gate.excluded_refusal(["artifact", "add", "r1", "m.pt", "--name", "x/out/y"]) is None
