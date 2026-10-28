"""`probe/_shared/finisher.py`: frozen, stdlib-only, generation-bound, resumable (clean-uninstall U-T9).

The finisher is what deletes the CLI once `probe uninstall` has done
everything else: the CLI execs a copy of it (`S/uninstall/finisher.py`) with
the base interpreter, and a person with no CLI left runs that copy by hand. A
change that slipped into it would reach every machine mid-uninstall, so its
bytes are pinned here like the hand-off's.

TO CHANGE IT, DELIBERATELY: raise `FINISHER_VERSION` in finisher.py, then set
`FROZEN_FINISHER` below to `(<the new version>, "<sha256 of the new file>")`
(`sha256sum agent/src/probe/_shared/finisher.py`). Say in the PR what an older
copy (one an interrupted uninstall left on a machine) does with a new plan.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from probe._shared import finisher

#: (FINISHER_VERSION, sha256 of finisher.py): see the module docstring.
FROZEN_FINISHER = (1, "6700673557e42a5020bb6b03164694df29351e650fa99a052613d675281c2155")

SOURCE = Path(finisher.__file__)


def test_the_finisher_changes_only_with_its_version():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert (finisher.FINISHER_VERSION, digest) == FROZEN_FINISHER, (
        f"{SOURCE} changed (sha256 {digest}, FINISHER_VERSION {finisher.FINISHER_VERSION}). It is frozen: an "
        "interrupted uninstall's copy of it is what finishes the job once the CLI is gone. If the change is "
        "deliberate, raise FINISHER_VERSION and set FROZEN_FINISHER in this file to (<new version>, <new sha256>)."
    )


def test_it_imports_only_the_standard_library_and_nothing_of_probe():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, "no relative imports: it runs as a script"
            imported.add((node.module or "").split(".")[0])
    imported.discard("__future__")
    assert imported <= set(sys.stdlib_module_names), imported - set(sys.stdlib_module_names)


def _entry(path: Path, *, empty_only: bool = False) -> dict:
    st = os.lstat(path)
    kind = "link" if path.is_symlink() else "dir" if path.is_dir() else "file"
    record = {"path": str(path), "kind": kind, "inode": st.st_ino, "mtime": st.st_mtime, "owner": "probe",
              "stage": "finish"}
    if empty_only:
        record["empty_only"] = True
    return record


def _witnessed(record: dict, witness: Path) -> dict:
    st = os.lstat(witness)
    return {**record, "witness": {"path": str(witness), "inode": st.st_ino, "mtime": st.st_mtime}}


def _layout(home: Path) -> dict:
    """A CLI the way uv and the side-by-side installer leave it, plus the uninstall's folder."""
    share = home / ".local" / "share" / "uv"
    env = share / "probe-versions" / "0.900.0" / "probe-research"
    (env / "bin").mkdir(parents=True)
    (env / "bin" / "probe").write_text("#!/bin/sh\n")
    (env / "pyvenv.cfg").write_text("home = /usr/bin\n")
    tools = share / "tools"
    tools.mkdir(parents=True)
    (tools / ".lock").write_text("")  # uv's own: never touched
    link = tools / "probe-research"
    link.symlink_to(env)
    (share / "probe-versions" / "active.json").write_text("{}")
    bins = home / ".local" / "bin"
    bins.mkdir(parents=True)
    shim = bins / "probe"
    shim.symlink_to(link / "bin" / "probe")
    (bins / "probe-foo").write_text("not probe's\n")
    folder = home / ".local" / "state" / "probe" / "uninstall"
    folder.mkdir(parents=True)
    (folder / "barrier.json").write_text("{}")
    paths = [
        _entry(shim), _entry(link), _witnessed(_entry(env.parent), env / "pyvenv.cfg"),
        _entry(share / "probe-versions" / "active.json"),
        _entry(share / "probe-versions", empty_only=True),
    ]
    plan = {"v": 1, "paths": paths, "env_generations": [str(env)], "shims": [str(shim)]}
    plan_path = folder / "plan.json"
    plan_path.write_text(json.dumps(plan))
    return {"plan": plan_path, "share": share, "bins": bins, "env": env, "folder": folder, "tools": tools}


def test_it_deletes_the_plan_then_its_own_folder_and_nothing_else(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path))
    laid = _layout(tmp_path)
    assert finisher.run(str(laid["plan"])) == 0
    assert not (laid["share"] / "probe-versions").exists()
    assert not (laid["tools"] / "probe-research").exists() and (laid["tools"] / ".lock").exists()
    assert not (laid["bins"] / "probe").exists() and (laid["bins"] / "probe-foo").exists()
    assert not laid["folder"].exists() and not (tmp_path / ".local" / "state" / "probe").exists()
    assert "uninstalled" in capsys.readouterr().out


def test_a_path_another_install_made_since_is_kept(tmp_path, monkeypatch, capsys):
    """Generation-bound: a version env made again after the plan (a new inode)
    is another install's now."""
    monkeypatch.setenv("HOME", str(tmp_path))
    laid = _layout(tmp_path)
    version = laid["env"].parent
    import shutil

    shutil.rmtree(version)
    (version / "probe-research").mkdir(parents=True)  # the folder may well get its old inode back
    (version / "probe-research" / "pyvenv.cfg").write_text("home = /usr/bin\n")
    assert finisher.run(str(laid["plan"])) == 0
    assert version.is_dir()
    assert "Kept 1 item(s)" in capsys.readouterr().out


def test_partial_keeps_the_plan_and_names_the_resume_command(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("HOME", str(tmp_path))
    laid = _layout(tmp_path)
    real = finisher.remove
    calls = {"n": 0}

    def failing(entry):
        calls["n"] += 1
        return finisher.FAILED if entry["kind"] == "dir" and not entry.get("empty_only") else real(entry)

    monkeypatch.setattr(finisher, "remove", failing)
    assert finisher.run(str(laid["plan"])) == 1
    out = capsys.readouterr().out
    assert "partly uninstalled" in out and f"--plan {laid['plan']}" in out
    assert laid["plan"].exists()
    monkeypatch.setattr(finisher, "remove", real)
    # The resume, as a person runs it: a plain python3 on the copy.
    assert finisher.run(str(laid["plan"])) == 0
    assert not laid["env"].exists() and not laid["folder"].exists()


def test_it_runs_as_a_script_with_minus_I_minus_S_and_ends_the_event_stream(tmp_path):
    laid = _layout(tmp_path)
    copy = laid["folder"] / "finisher.py"
    copy.write_bytes(SOURCE.read_bytes())
    (laid["folder"] / "tail.json").write_text(json.dumps({
        "action": "uninstall", "rows": [{"agent": None, "requested": {}, "actual": {}, "ok": True, "message": ""}],
        "steps": [{"name": "uninstall_state", "status": "done", "message": "", "agent": None}],
    }))
    done = subprocess.run([sys.executable, "-I", "-S", str(copy), "--plan", str(laid["plan"]), "--json"],
                          capture_output=True, text=True, timeout=60, env={**os.environ, "HOME": str(tmp_path)})
    assert done.returncode == 0, done.stderr
    events = [json.loads(line) for line in done.stdout.splitlines()]
    assert [e["event"] for e in events] == ["step", "result", "done"]
    assert events[-1]["ok"] and events[-1]["complete"] and events[-1]["exit_code"] == 0
    assert [s["name"] for s in events[-1]["steps"]] == ["uninstall_state", "uninstall_finish"]
    assert not laid["folder"].exists()


def test_a_retry_never_changes_what_a_symlink_names(tmp_path):
    """A folder it cannot empty (read-only) holding a link to a file outside:
    the retry opens folders up, never chmods through the link."""
    outside = tmp_path / "outside.txt"
    outside.write_text("someone else's\n")
    outside.chmod(0o444)
    folder = tmp_path / "doomed"
    folder.mkdir()
    (folder / "link").symlink_to(outside)
    folder.chmod(0o555)
    try:
        if os.access(folder, os.W_OK):
            import pytest

            pytest.skip("this user can write anywhere (root)")
        try:
            finisher._rmtree(str(folder))
        except OSError:
            pass
        assert outside.stat().st_mode & 0o777 == 0o444
    finally:
        folder.chmod(0o755)
        outside.chmod(0o644)


def test_it_never_removes_home_or_a_top_level_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    for path in (tmp_path, Path("/"), Path("/usr")):
        st = os.lstat(path)
        assert finisher.remove({"path": str(path), "kind": "dir", "inode": st.st_ino, "owner": "probe"}) == \
            finisher.CHANGED


def test_its_exit_1_says_why_as_data_partial_or_busy(tmp_path, monkeypatch, capsys):
    """With `--json`, the finisher's exit 1 ends the stream with the CLI's
    `reason` shape: `partial` (the command that finishes it) or `busy`."""
    import fcntl

    monkeypatch.setenv("HOME", str(tmp_path))
    laid = _layout(tmp_path)
    tail = {"action": "uninstall", "rows": [{"agent": None, "ok": True}], "steps": [], "resumed": True}
    (laid["folder"] / finisher.TAIL_NAME).write_text(json.dumps(tail))
    real = finisher.remove
    monkeypatch.setattr(finisher, "remove",
                        lambda entry: finisher.FAILED if entry["path"].endswith("probe") else real(entry))
    capsys.readouterr()
    assert finisher.run(str(laid["plan"]), json_mode=True) == 1
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines() if line.strip()]
    result = next(e for e in events if e["event"] == "result")
    assert result["reason"] == {"code": "partial", "resumed": True, "phase": "finishing",
                                "resume": finisher.resume_command(str(laid["plan"]))}
    # Another install holds the lock (no fd inherited): `busy`.
    monkeypatch.setattr(finisher, "remove", real)
    monkeypatch.delenv(finisher.LOCK_FD_ENV, raising=False)
    monkeypatch.setattr(finisher, "LOCK_WAIT_S", 0.1)
    lock = tmp_path / "install.lock"
    lock.write_text("")
    plan = json.loads(laid["plan"].read_text())
    laid["plan"].write_text(json.dumps({**plan, "install_lock": str(lock)}))
    held = os.open(lock, os.O_RDWR)
    try:
        fcntl.flock(held, fcntl.LOCK_EX)
        assert finisher.run(str(laid["plan"]), json_mode=True) == 1
    finally:
        os.close(held)
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines() if line.strip()]
    assert next(e for e in events if e["event"] == "result")["reason"] == {"code": "busy", "resumed": True}
