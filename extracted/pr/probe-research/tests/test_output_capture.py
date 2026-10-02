"""Output capture (D17): what a run wrote to its folder reaches the run when it closes.

End to end against the in-memory API: open a run with capture on, write files,
close it, read back what was stored. The fd-level log tee is off here
(`PROBE_CAPTURE_LOG=0`: pytest owns this process's file descriptors) and is
covered by test_logcapture.py.
"""

from __future__ import annotations

import base64
import gzip
import io
import json
import os
import socket
import sys
import time
import warnings
import zipfile

import pytest

from probe.sdk import ephemeral, inputs, outputs, secret_gate
from tests.conftest import open_run

TOKEN = "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"


@pytest.fixture
def work(monkeypatch, tmp_path):
    folder = tmp_path / "work"
    folder.mkdir()
    monkeypatch.chdir(folder)
    monkeypatch.setenv("PROBE_CAPTURE_LOG", "0")
    monkeypatch.setenv(ephemeral.ENV, "0")  # storage that lasts, unless a test says otherwise
    monkeypatch.setattr(outputs, "_shared_warned", set())
    return folder


@pytest.fixture(autouse=True)
def _close_leaked_windows():
    """A test that opens a window and never closes it would leave it for the
    next test's `_finalize_at_exit`, and in the registry."""
    yield
    with outputs._live_lock:
        leaked = list(outputs._live)
        outputs._live.clear()
    for capture in leaked:
        if capture._tee is not None:
            try:
                capture._tee.stop()
            except Exception:  # noqa: BLE001
                pass
        capture._unregister()


def _rows(app, run):
    """Captured rows by their path in the watched folder; Probe's own files
    (`probe/run.log`, the manifest) keep their full name."""
    rows = {}
    for a in app.artifacts.get(run.id, []):
        name = a["name"]
        rows[name[len("outputs/"):] if name.startswith("outputs/") else name] = a
    return rows


def _bytes(app, row):
    return app.blobs.get(row["id"]) or app.blobs_by_hash.get(row["content_hash"])


def test_new_and_changed_files_are_captured_unchanged_and_deleted_are_not(client, app, work):
    (work / "unchanged.txt").write_text("same")
    (work / "changed.txt").write_text("before")
    (work / "deleted.txt").write_text("gone soon")
    run = open_run(client, experiment="cap-basic", capture_outputs=True)
    (work / "new.txt").write_text("fresh result")
    (work / "changed.txt").write_text("after, and longer")
    (work / "deleted.txt").unlink()
    (work / "sub").mkdir()
    (work / "sub" / "metrics.json").write_text('{"acc": 0.9}')
    run.finish()
    rows = _rows(app, run)
    assert set(rows) == {"new.txt", "changed.txt", "sub/metrics.json"}
    assert {a["name"] for a in app.artifacts[run.id]} == {"outputs/new.txt", "outputs/changed.txt", "outputs/sub/metrics.json"}
    assert _bytes(app, rows["new.txt"]) == b"fresh result"
    assert rows["new.txt"]["meta"]["capture"] == "outputs"
    assert rows["sub/metrics.json"]["kind"] == "file"


def test_the_skip_list_is_honoured(client, app, work):
    run = open_run(client, experiment="cap-skip", capture_outputs=True)
    for rel in (".git/objects/ab", "node_modules/x/index.js", "__pycache__/m.cpython-312.pyc",
                ".venv/lib/site.py", ".cache/hf/model.bin", ".probe/config.json", "mod.pyc"):
        (work / rel).parent.mkdir(parents=True, exist_ok=True)
        (work / rel).write_text("x")
    (work / ".env").write_text("OPENAI_API_KEY=sk-proj-" + "a" * 48)
    (work / "kept.txt").write_text("kept")
    with pytest.warns(UserWarning, match=r"may hold a credential.*\.env"):
        run.finish()
    assert set(_rows(app, run)) == {"kept.txt"}


def test_a_plot_is_filed_as_a_plot(client, app, work):
    run = open_run(client, experiment="cap-plot", capture_outputs=True)
    (work / "curve.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
    run.finish()
    assert _rows(app, run)["curve.png"]["kind"] == "plot"


def test_a_text_credential_is_redacted_and_the_file_still_uploaded(client, app, work):
    run = open_run(client, experiment="cap-redact", capture_outputs=True)
    (work / "notes.txt").write_text(f"token {TOKEN} used\n")
    with pytest.warns(UserWarning, match=r"replaced credentials in 1 output file\(s\).*notes.txt"):
        run.finish()
    stored = _bytes(app, _rows(app, run)["notes.txt"])
    assert TOKEN.encode() not in stored and b"<redacted:" in stored


def test_a_credential_the_gate_cannot_redact_skips_the_file(client, app, work):
    run = open_run(client, experiment="cap-zip", capture_outputs=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("cfg.txt", f"key={TOKEN}")
    (work / "bundle.zip").write_bytes(buf.getvalue())
    (work / "fine.txt").write_text("fine")
    with pytest.warns(UserWarning, match="bundle.zip"):
        run.finish()
    assert set(_rows(app, run)) == {"fine.txt"}


def test_a_field_name_hit_never_skips(client, app, work):
    run = open_run(client, experiment="cap-cookie", capture_outputs=True)
    (work / "preds.jsonl").write_text('{"q": "$0.10/cookie = 10 biscuits"}\n')
    run.finish()
    assert "preds.jsonl" in _rows(app, run)


def test_a_big_file_on_lasting_storage_is_a_pointer(client, app, work, monkeypatch):
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    run = open_run(client, experiment="cap-pointer", capture_outputs=True)
    (work / "ckpt.pt").write_bytes(b"\x01" * 5000)
    run.finish()
    row = _rows(app, run)["ckpt.pt"]
    assert row["is_reference"] and row["uri"].startswith("file://")
    assert row["meta"]["local_path"] == str(work / "ckpt.pt")
    assert row["size_bytes"] == 5000
    assert not app.puts  # no bytes left the machine


def test_a_big_file_on_a_throwaway_box_is_listed_not_pointed_to(client, app, work, monkeypatch):
    """A pointer to a container's own disk names bytes that are gone with it,
    and 64 MB is the most an upload carries (the server's guard refuses more):
    the file is named in the manifest, with a warning, instead."""
    monkeypatch.setenv(ephemeral.ENV, "1")
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    run = open_run(client, experiment="cap-throwaway", capture_outputs=True)
    (work / "huge.bin").write_bytes(b"\x02" * 4096)
    (work / "small.txt").write_text("kept")
    with pytest.warns(UserWarning, match="outputs-manifest.json: huge.bin") as caught:
        run.finish()
    # log_artifact cannot upload it either, so the advice must not send you there.
    listed_warning = next(str(w.message) for w in caught if "outputs-manifest" in str(w.message))
    assert "bucket or a mounted volume" in listed_warning and "log_artifact" not in listed_warning
    rows = _rows(app, run)
    assert "huge.bin" not in rows and "small.txt" in rows
    manifest = json.loads(_bytes(app, rows["probe/outputs-manifest.json"]))
    assert manifest["files"] == [
        {"path": "huge.bin", "size": 4096, "code": outputs.TOO_LARGE, "reason": "over the 64 MB upload limit"}
    ]



def test_on_a_multipart_server_the_advice_names_log_artifact(client, app, work, monkeypatch):
    """Plan (g): on a server that ADVERTISES multipart uploads an explicit
    `log_artifact` does keep a file over 64 MiB, so the advice says so (and
    the test above pins that it does not on any other server)."""
    app.supports_artifact_multipart = True
    monkeypatch.setenv(ephemeral.ENV, "1")
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    run = open_run(client, experiment="cap-throwaway-mp", capture_outputs=True)
    (work / "huge.bin").write_bytes(b"\x02" * 4096)
    with pytest.warns(UserWarning, match="outputs-manifest.json: huge.bin") as caught:
        run.finish()
    listed_warning = next(str(w.message) for w in caught if "outputs-manifest" in str(w.message))
    assert "run.log_artifact(path)" in listed_warning

def test_a_file_the_script_logged_is_not_uploaded_twice(client, app, work):
    run = open_run(client, experiment="cap-dedupe", capture_outputs=True)
    (work / "model.pt").write_bytes(b"weights")
    run.log_artifact("model", path=str(work / "model.pt"), sync=True)
    (work / "other.txt").write_text("other")
    run.finish()
    rows = _rows(app, run)
    assert set(rows) == {"model.pt", "other.txt"}  # model.pt is the logged row
    assert sum(1 for r in app.artifacts[run.id] if r["content_hash"] == rows["model.pt"]["content_hash"]) == 1
    assert "outputs/model.pt" not in {a["name"] for a in app.artifacts[run.id]}


def test_a_logged_file_changed_afterwards_is_captured(client, app, work):
    run = open_run(client, experiment="cap-dedupe-changed", capture_outputs=True)
    (work / "ckpt.pt").write_bytes(b"step 1000")
    run.log_artifact("ckpt", path=str(work / "ckpt.pt"), sync=True)
    (work / "ckpt.pt").write_bytes(b"step 2000, the final one")
    run.finish()
    hashes = {r["content_hash"] for r in app.artifacts[run.id]}
    assert len(hashes) == 2


@pytest.mark.parametrize("how", ["argument", "env"])
def test_opting_out_captures_nothing(client, app, work, monkeypatch, how):
    if how == "env":
        monkeypatch.setenv(outputs.CAPTURE_ENV, "0")
        run = open_run(client, experiment="cap-off-env")
    else:
        run = open_run(client, experiment="cap-off-arg", capture_outputs=False)
    (work / "result.txt").write_text("r")
    run.finish()
    assert _rows(app, run) == {}


def test_outputs_narrows_the_sweep_and_names_are_relative_to_it(client, app, work):
    (work / "results").mkdir()
    run = open_run(client, experiment="cap-narrow", capture_outputs=True, outputs="results")
    (work / "results" / "metrics.json").write_text("{}")
    (work / "elsewhere.txt").write_text("not mine")
    run.finish()
    assert set(_rows(app, run)) == {"metrics.json"}


def test_a_second_close_uploads_nothing_new(client, app, work):
    run = open_run(client, experiment="cap-idem", capture_outputs=True)
    (work / "a.txt").write_text("a")
    run.finish()
    count = len(app.artifacts[run.id])
    run._capture._sweep_done = run._capture._log_done = False  # force a re-sweep
    run._finalize_capture()
    client.flush(run_ref=run.id)
    assert len(app.artifacts[run.id]) == count


def test_the_crash_path_queues_outputs_at_interpreter_exit(client, app, work):
    run = open_run(client, experiment="cap-crash", capture_outputs=True)
    (work / "partial.txt").write_text("written before the crash")
    outputs._finalize_at_exit()  # what atexit runs for a run nobody finished
    queued = [op for _, op in client.journal.pending() if op.get("run_ref") == run.id]
    assert [op["upload"]["name"] for op in queued if op.get("kind") == "upload"] == ["outputs/partial.txt"]
    assert all(op.get("blocking") is False for op in queued)


def test_an_upload_outage_cannot_keep_the_run_open(client, app, work):
    run = open_run(client, experiment="cap-outage", capture_outputs=True)
    (work / "out.txt").write_text("x")
    app.fail_put_names = {"outputs/out.txt"}
    run.finish()  # would raise "not closed" if capture ops were blocking
    assert app.runs[run.id]["status"] == "completed"
    assert any(op.get("run_ref") == run.id for _, op in client.journal.pending())


def test_two_runs_in_one_folder_at_once_skip_the_sweep(client, app, work):
    first = open_run(client, experiment="cap-shared-a", capture_outputs=True)
    second = open_run(client, experiment="cap-shared-b", capture_outputs=True)
    (work / "whose.txt").write_text("?")
    with pytest.warns(UserWarning, match="at the same time"):
        first.finish()
    second.finish()
    assert _rows(app, first) == {} and _rows(app, second) == {}


def test_a_folder_too_big_to_list_keeps_only_the_log(client, app, work, monkeypatch):
    monkeypatch.setattr(outputs, "MAX_BASELINE_ENTRIES", 3)
    for i in range(5):
        (work / f"f{i}").write_text("x")
    with pytest.warns(UserWarning, match="workspace rather than a run folder"):
        run = open_run(client, experiment="cap-huge", capture_outputs=True)
    assert run._capture is not None and not run._capture.sweeps
    (work / "new.txt").write_text("not swept")
    run.finish()
    assert _rows(app, run) == {}


def test_a_listing_cut_short_still_captures_what_it_listed(client, app, work, monkeypatch):
    run = open_run(client, experiment="cap-truncate", capture_outputs=True)
    monkeypatch.setattr(outputs, "MAX_FINAL_ENTRIES", 2)
    for i in range(4):
        (work / f"r{i}.txt").write_text(str(i))
    with pytest.warns(UserWarning, match="listing stopped"):
        run.finish()
    rows = _rows(app, run)
    assert len([n for n in rows if n.startswith("r")]) == 2
    assert json.loads(_bytes(app, rows["probe/outputs-manifest.json"]))["listing_truncated"] is True


def test_a_file_the_gate_cannot_inspect_is_a_pointer_on_lasting_storage(client, app, work, monkeypatch):
    real = secret_gate.read_upload_redacted_sourced

    def refuse_archive(path, **kw):
        if str(path).endswith(".tar"):
            raise secret_gate.CredentialBlocked("Artifact upload refused: archive member count exceeds inspection limit")
        return real(path, **kw)

    monkeypatch.setattr(secret_gate, "read_upload_redacted_sourced", refuse_archive)
    run = open_run(client, experiment="cap-uninspectable", capture_outputs=True)
    (work / "many.tar").write_bytes(b"x" * 100)
    run.finish()
    assert _rows(app, run)["many.tar"]["is_reference"]


def test_a_nested_init_under_exec_on_this_host_does_not_capture_again(client, work, monkeypatch):
    monkeypatch.setenv(outputs.OWNER_ENV, socket.gethostname())
    monkeypatch.setenv(outputs.ROOT_ENV, str(work))
    monkeypatch.setenv(outputs.LOG_OWNER_ENV, socket.gethostname())
    run = open_run(client, experiment="cap-nested", capture_outputs=True)
    assert run._capture is None


def test_a_nested_init_whose_launcher_could_not_tee_keeps_its_own_log(client, work, monkeypatch):
    """Exec sweeps the folder but says nothing about the log (its tee could not
    start): the child's own window keeps the log and leaves the files to exec."""
    monkeypatch.setenv(outputs.OWNER_ENV, socket.gethostname())
    monkeypatch.setenv(outputs.ROOT_ENV, str(work))
    run = open_run(client, experiment="cap-nested-log", capture_outputs=True)
    assert run._capture is not None and not run._capture.sweeps
    assert run._capture._baseline_file is None  # no folder listing either


def test_a_nested_init_writing_outside_the_launchers_folder_captures_it(client, work, tmp_path, monkeypatch):
    elsewhere = tmp_path / "scratch"
    elsewhere.mkdir()
    monkeypatch.setenv(outputs.OWNER_ENV, socket.gethostname())
    monkeypatch.setenv(outputs.ROOT_ENV, str(work))
    run = open_run(client, experiment="cap-nested-out", capture_outputs=True, outputs=str(elsewhere))
    assert run._capture is not None and run._capture.root == str(elsewhere)


def test_a_nested_init_on_another_machine_captures(client, work, monkeypatch):
    monkeypatch.setenv(outputs.OWNER_ENV, "some-other-host")
    monkeypatch.setenv(outputs.ROOT_ENV, str(work))
    run = open_run(client, experiment="cap-remote", capture_outputs=True)
    assert run._capture is not None


def test_a_detached_run_never_captures(client, work):
    run = open_run(client, experiment="cap-detached", capture_outputs=True, heartbeat=False)
    assert run._capture is None


def test_execute_tees_the_child_and_captures_its_outputs(client, app, work, monkeypatch):
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    run = open_run(client, experiment="cap-exec", capture_outputs=False)
    script = work / "job.py"
    script.write_text(
        "import os\n"
        "print('training...', flush=True)\n"
        "open('result.json','w').write('{\"loss\": 0.1}')\n"
        "print(os.environ.get('PROBE_CAPTURE_OWNER') is not None, os.environ.get('PROBE_CAPTURE_ROOT'))\n"
    )
    import sys

    result = run.execute([sys.executable, str(script)], cwd=str(work), capture_outputs=True)
    assert result.returncode == 0
    rows = _rows(app, run)
    assert "result.json" in rows and "probe/run.log" in rows
    log = _bytes(app, rows["probe/run.log"])
    assert b"training..." in log and f"True {work}".encode() in log
    assert rows["probe/run.log"]["meta"]["capture"] == "log"
    assert app.runs[run.id]["status"] == "completed"


def test_recovery_finishes_a_dead_runs_capture_from_disk(client, app, work, tmp_path, monkeypatch):
    """What the log helper starts when the run's process dies mid-run."""
    run = open_run(client, experiment="cap-recover", capture_outputs=True)
    capture = run._capture
    (work / "ckpt-100.txt").write_text("saved before the segfault")
    entry = str(capture._entry)
    record = json.loads(open(entry).read())
    record["pid"] = 999_999_999  # dead
    open(entry, "w").write(json.dumps(record))
    monkeypatch.setattr(outputs, "_recovery_client", lambda record: (client, client.journal))
    outputs.recover(entry)
    assert "ckpt-100.txt" in _rows(app, run)  # swept against the recorded baseline, delivered
    assert not os.path.exists(entry)


def test_a_damaged_registry_record_breaks_nothing(client, app, work, monkeypatch):
    """The registry is a folder of files anything can damage. One record with
    a pid that is not a number used to raise out of every later run's start
    (capture off on this host until it aged out, 30 days) and out of the close
    of `probe exec`, after the child finished and before its status landed."""
    spawned = []
    monkeypatch.setattr(outputs, "_spawn_recovery", spawned.append)
    registry = outputs._registry()
    (registry / "junk.1.json").write_text(json.dumps({"pid": "not-a-pid"}))
    (registry / "junk.2.json").write_text(json.dumps({"root": str(work), "shared_with": 7}))
    (registry / "junk.3.json").write_text("[1, 2]")
    run = open_run(client, experiment="cap-damaged-registry", capture_outputs=True)
    assert len(spawned) == 2  # the two dead records go to recovery; the list is ignored
    assert run._capture is not None
    (work / "kept.txt").write_text("kept")
    run.finish()
    assert "kept.txt" in _rows(app, run)


def test_a_record_whose_pid_was_reused_is_not_alive(monkeypatch):
    me = os.getpid()
    assert outputs._record_alive({"pid": me, "proc_start": outputs._process_started(me)})
    assert not outputs._record_alive({"pid": 0})  # os.kill(0, 0) would say alive
    assert not outputs._record_alive({"pid": None})
    assert not outputs._record_alive({"pid": "not-a-pid"})
    assert not outputs._record_alive({"pid": me, "proc_start": 1.0})  # same pid, other process


def test_a_tee_is_stopped_when_the_window_fails_to_open(client, work, monkeypatch):
    stopped = []

    class FakeTee:
        helper_pid = None

        def __init__(self, *a, **k):
            pass

        def start(self):
            pass

        def stop(self):
            stopped.append(True)

    import probe.sdk.logcapture as logcapture

    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    monkeypatch.setattr(outputs, "in_process_log_supported", lambda: True)
    monkeypatch.setattr(logcapture, "InProcessTee", FakeTee)

    def broken_register(self):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(outputs.OutputCapture, "_register", broken_register)
    with pytest.warns(UserWarning, match="could not start"):
        run = open_run(client, experiment="cap-tee-leak", capture_outputs=True)
    assert run._capture is None and stopped == [True]


# -- review fixes (PR #1959) ------------------------------------------------------------
def _script(work, body: str):
    path = work / "job.py"
    path.write_text(body)
    return path


def _stored_log(app, run, name="probe/run.log"):
    return _bytes(app, _rows(app, run)[name])


def test_a_credential_printed_beside_a_binary_byte_is_redacted_in_the_log(client, app, work, monkeypatch):
    """The uploaded log is made UTF-8 before the gate sees it: next to one 0xFF
    byte the gate could only flag the token, and it would ship as printed."""
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    run = open_run(client, experiment="cap-log-binary", capture_outputs=False)
    job = _script(work, f"import os\nos.write(1, bytes([255]) + b' progress' + bytes([10]))\nprint('token {TOKEN}', flush=True)\n")
    with pytest.warns(UserWarning, match="replaced credentials in probe/run.log"):
        run.execute([sys.executable, str(job)], cwd=str(work), capture_outputs=True)
    stored = _stored_log(app, run)
    assert TOKEN.encode() not in stored and b"<redacted:" in stored


def test_a_log_that_starts_like_a_zip_is_still_redacted(client, app, work, monkeypatch):
    """`PK\\x03\\x04` at byte 0 made the gate treat the log as an archive and
    hand it back untouched. A log is text; it is redacted as text."""
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    run = open_run(client, experiment="cap-log-pk", capture_outputs=False)
    job = _script(work, f"import os\nos.write(1, b'PK' + bytes([3, 4]) + b' header' + bytes([10]))\nprint('GITHUB_TOKEN={TOKEN}', flush=True)\n")
    with pytest.warns(UserWarning, match="replaced credentials"):
        run.execute([sys.executable, str(job)], cwd=str(work), capture_outputs=True)
    assert TOKEN.encode() not in _stored_log(app, run)


def test_an_encoded_credential_in_the_log_never_ships(client, app, work, monkeypatch):
    """base64(gzip(token)) is seen by the gate but cannot be replaced in place:
    the encoded run is blanked, and the rest of the log still uploads."""
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    blob = base64.b64encode(gzip.compress(f"export GH={TOKEN}\n".encode())).decode()
    run = open_run(client, experiment="cap-log-encoded", capture_outputs=False)
    job = _script(work, f"print('epoch 1 done', flush=True)\nprint('{blob}', flush=True)\n")
    with pytest.warns(UserWarning, match="replaced credentials"):
        run.execute([sys.executable, str(job)], cwd=str(work), capture_outputs=True)
    stored = _stored_log(app, run)
    assert b"epoch 1 done" in stored and blob.encode() not in stored
    assert b"<redacted:encoded>" in stored


def test_the_bytes_uploaded_are_the_bytes_inspected(client, app, work, monkeypatch):
    """A writer that swaps the file between the check and the upload cannot
    change what leaves: the sweep uploads its own checked copy."""
    run = open_run(client, experiment="cap-toctou", capture_outputs=True)
    target = work / "report.txt"
    target.write_text("clean report")
    real = secret_gate.read_upload_redacted_sourced

    def swap_after_reading(path, **kw):
        result = real(path, **kw)
        if str(path) == str(target):
            target.write_text(f"swapped in: {TOKEN}")
        return result

    monkeypatch.setattr(secret_gate, "read_upload_redacted_sourced", swap_after_reading)
    run.finish()
    assert _bytes(app, _rows(app, run)["report.txt"]) == b"clean report"


@pytest.mark.parametrize(("ephemeral_value", "pointer"), [("0", True), ("1", False)])
def test_past_the_close_budget_files_are_pointed_to_or_listed(client, app, work, monkeypatch, ephemeral_value, pointer):
    monkeypatch.setenv(ephemeral.ENV, ephemeral_value)
    monkeypatch.setenv(outputs.BUDGET_ENV, "0")
    run = open_run(client, experiment=f"cap-budget-{ephemeral_value}", capture_outputs=True)
    (work / "late.jsonl").write_text('{"a": 1}\n')
    with pytest.warns(UserWarning) if not pointer else _no_warning():
        run.finish()
    rows = _rows(app, run)
    if pointer:
        assert rows["late.jsonl"]["is_reference"]
        assert rows["late.jsonl"]["meta"]["reason"] == outputs._REASONS[outputs.OVER_BUDGET]
    else:
        manifest = json.loads(_bytes(app, rows["probe/outputs-manifest.json"]))
        assert [f["code"] for f in manifest["files"]] == [outputs.OVER_BUDGET]


class _no_warning:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_a_pointer_whose_path_holds_a_credential_is_never_recorded(client, app, work, monkeypatch):
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 16)
    run = open_run(client, experiment="cap-path-secret", capture_outputs=True)
    folder = work / f"runs-{TOKEN}"
    folder.mkdir()
    (folder / "ckpt.pt").write_bytes(b"\x01" * 64)
    with pytest.warns(UserWarning, match="may hold a credential"):
        run.finish()
    assert not any(TOKEN in (r.get("uri") or "") for r in app.artifacts.get(run.id, []))


def test_a_second_close_records_a_pointer_once(client, app, work, monkeypatch):
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 16)
    run = open_run(client, experiment="cap-pointer-once", capture_outputs=True)
    (work / "ckpt.pt").write_bytes(b"\x01" * 64)
    run.finish()
    count = len(app.artifacts[run.id])
    run._capture._sweep_done = run._capture._log_done = False  # force a re-sweep
    run._finalize_capture()
    client.flush(run_ref=run.id)
    assert len(app.artifacts[run.id]) == count


def test_links_are_never_followed_out_of_the_folder(client, app, work, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "id_file").write_text("private")
    run = open_run(client, experiment="cap-links", capture_outputs=True)
    (work / "file-link").symlink_to(outside / "id_file")
    (work / "dir-link").symlink_to(outside, target_is_directory=True)
    (work / "real.txt").write_text("mine")
    run.finish()
    assert set(_rows(app, run)) == {"real.txt"}


def test_in_the_home_folder_dot_entries_are_tool_state(client, app, work, monkeypatch):
    """Modal's working folder IS home (/root): `.kube/config` or
    `.docker/config.json` written during the run are not its outputs."""
    monkeypatch.setenv("HOME", str(work))
    run = open_run(client, experiment="cap-home", capture_outputs=True)
    for rel in (".kube/config", ".docker/config.json", ".config/gcloud/creds.db"):
        (work / rel).parent.mkdir(parents=True, exist_ok=True)
        (work / rel).write_text("tool state")
    (work / "result.txt").write_text("r")
    run.finish()
    assert set(_rows(app, run)) == {"result.txt"}


@pytest.mark.parametrize("name", [".pgpass", ".git-credentials", "prod.env", "kaggle.json"])
def test_home_style_credential_files_are_never_read(client, app, work, name):
    run = open_run(client, experiment=f"cap-secret-name-{name}", capture_outputs=True)
    (work / name).write_text("host:5432:db:user:hunter2")
    with pytest.warns(UserWarning, match="may hold a credential"):
        run.finish()
    assert name not in _rows(app, run)


def test_the_filesystem_root_is_never_swept(client, work):
    with pytest.warns(UserWarning, match="root of the filesystem"):
        capture = outputs.OutputCapture.start(client, "11111111-1111-4111-8111-111111111111", cwd="/", tee=False, launcher=True)
    assert capture is not None and not capture.sweeps and capture.baseline == {}
    capture._unregister()


def test_every_rank_sweeps_and_keeps_its_own_log(client, app, work, monkeypatch):
    """A rank may write its last file after another rank has closed, so every
    rank sweeps; each keeps its log under its own name."""
    run_id = "22222222-2222-4222-8222-222222222222"
    peer = os.getppid()
    (outputs._registry() / f"{run_id}.{peer}.rank0.json").write_text(json.dumps({
        "run_id": run_id, "pid": peer, "proc_start": outputs._process_started(peer), "root": str(work),
    }))
    rank3 = outputs.OutputCapture.start(client, run_id, tee=False)
    assert rank3 is not None and rank3.sweeps and rank3.log_name == f"probe/run.{os.getpid()}.log"
    rank3._unregister()


def test_a_distributed_rank_names_its_log_from_the_environment(client, work, monkeypatch):
    """The registry is per host: the first rank on every host found no peer and
    kept `probe/run.log`, so the hosts' logs overwrote each other."""
    monkeypatch.setenv("WORLD_SIZE", "16")
    monkeypatch.setenv("RANK", "9")
    capture = outputs.OutputCapture.start(client, "44444444-4444-4444-8444-444444444444", tee=False)
    assert capture.log_name == "probe/run.rank9.log"
    capture._unregister()
    monkeypatch.setenv("WORLD_SIZE", "1")
    assert outputs._distributed_log_name() is None


def test_what_another_close_queued_is_not_read_again(client, app, work, monkeypatch):
    """The ledger remembers size and mtime: a second close of the run -- or
    another rank's -- skips an untouched file without inspecting it."""
    run = open_run(client, experiment="cap-ledger-stat", capture_outputs=True)
    (work / "a.jsonl").write_text('{"x": 1}\n')
    run.finish()
    second = outputs.OutputCapture(client, run.id, str(work), tee=False, launcher=False)

    def never(path, **kw):
        raise AssertionError(f"{path} was read again")

    monkeypatch.setattr(secret_gate, "read_upload_redacted_sourced", never)
    summary = second._sweep(time.monotonic() + 60)
    assert summary["uploaded"] == 0 and summary["unchanged_logged"] >= 1


def test_two_windows_of_one_run_in_one_process_keep_separate_records(client, work, tmp_path):
    run = open_run(client, experiment="cap-two-windows", capture_outputs=True)
    other = tmp_path / "other"
    other.mkdir()
    second = outputs.OutputCapture.start(client, run.id, cwd=str(other), tee=False, launcher=True)
    assert second._entry != run._capture._entry
    second.finalize()
    assert run._capture._entry.exists()  # closing one never unregisters the other


def test_execute_finalizes_the_handles_own_window(client, app, work):
    """Client.run opened a window; execute() closing the run must close it
    too -- not leave it open, then sweep later work into a finished run."""
    run = open_run(client, experiment="cap-exec-existing", capture_outputs=True)
    job = _script(work, "open('result.json', 'w').write('{}')\n")
    result = run.execute([sys.executable, str(job)], cwd=str(work))
    assert result.returncode == 0
    assert run._capture._sweep_done and "result.json" in _rows(app, run)
    assert app.runs[run.id]["status"] == "completed"


def test_a_hand_off_captures_nothing(client, app, work, monkeypatch):
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    run = open_run(client, experiment="cap-handoff", capture_outputs=False)
    job = _script(work, "import os\nopen('env.txt', 'w').write(os.environ.get('PROBE_CAPTURE_OWNER') or 'none')\n")
    run.execute([sys.executable, str(job)], cwd=str(work), finalize=False, capture_outputs=True)
    assert (work / "env.txt").read_text() == "none"
    assert _rows(app, run) == {}


def test_a_launch_failure_still_closes_the_window(client, work):
    run = open_run(client, experiment="cap-launch-fail", capture_outputs=False)
    with pytest.raises(FileNotFoundError):
        run.execute(["/nonexistent/binary"], cwd=str(work), capture_outputs=True)
    capture = run._capture
    assert capture is not None and capture._sweep_done
    assert not list(outputs._registry().glob(f"{run.id}.*.json"))


def test_recovery_runs_under_the_runs_own_context(monkeypatch):
    """A crashed run from context A recovered while context B is current must
    never send A's files to B's server."""
    import probe.sdk.config as config

    class Settings:
        base_url = "https://other.example"

    monkeypatch.setattr(config, "resolve", lambda **kw: Settings())
    client, journal = outputs._recovery_client(
        {"context": {"name": "prod", "base_url": "https://api.research.prbe.ai"}, "journal_dir": None}
    )
    assert client is None and journal is not None


def test_a_claim_left_by_a_dead_recoverer_is_taken_over(tmp_path):
    entry = tmp_path / "rec.json"
    entry.write_text("{}")
    claim = outputs._claim_path(entry)
    claim.write_text("")
    assert not outputs._claim(entry)  # fresh: someone is on it
    old = time.time() - outputs.CLAIM_STALE_SECONDS - 5
    os.utime(claim, (old, old))
    assert outputs._claim(entry)


def test_a_record_whose_helper_still_runs_is_left_to_the_helper(monkeypatch, tmp_path):
    """The run died, but its helper is still draining the last output: a new
    run starting on the host must not grab the record and send a log with no
    ending."""
    spawned = []
    monkeypatch.setattr(outputs, "_spawn_recovery", spawned.append)
    registry = outputs._registry()
    me = os.getpid()
    (registry / "dead.1.json").write_text(json.dumps({
        "pid": 999_999_999, "helper_pid": me, "helper_start": outputs._process_started(me),
    }))
    outputs._recover_stale_logs()
    assert spawned == []


def test_a_file_mounted_on_its_own_is_judged_by_its_own_storage(client, app, work, monkeypatch):
    """Kubernetes can bind-mount a single file (subPath) into a throwaway
    folder: a big checkpoint mounted from NFS is still a pointer."""
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 16)
    monkeypatch.delenv(ephemeral.ENV, raising=False)
    run = open_run(client, experiment="cap-file-mount", capture_outputs=True)
    mounted = work / "ckpt.pt"
    mounted.write_bytes(b"\x01" * 64)
    monkeypatch.setattr(ephemeral, "mount_points", lambda: frozenset({str(mounted)}))

    def describe(path):
        durable = str(path) == str(mounted)
        return {"durable": durable, "fstype": "nfs4" if durable else "overlay", "reason": "test"}

    monkeypatch.setattr(ephemeral, "describe", describe)
    run.finish()
    assert _rows(app, run)["ckpt.pt"]["is_reference"]


def test_a_log_only_window_never_claims_the_folder(client, work, monkeypatch):
    """Exec could not list its folder (a workspace): it must not tell the
    child it sweeps it, or a narrower probe.init(outputs=...) there skips too."""
    monkeypatch.setattr(outputs, "MAX_BASELINE_ENTRIES", 0)
    (work / "existing.txt").write_text("x")
    run = open_run(client, experiment="cap-log-only-claim", capture_outputs=False)
    job = _script(work, "import os\nopen('owner.txt', 'w').write(os.environ.get('PROBE_CAPTURE_OWNER') or 'none')\n")
    with pytest.warns(UserWarning, match="workspace rather than a run folder"):
        run.execute([sys.executable, str(job)], cwd=str(work), capture_outputs=True)
    assert (work / "owner.txt").read_text() == "none"


# -- second review round (PR #1959) ------------------------------------------------------
def test_a_log_only_window_blocks_no_other_runs_sweep(client, app, work):
    """A run working in `/` (Docker with no WORKDIR) keeps only its log; it
    must not make every run beneath it skip its files as 'shared'."""
    peer = os.getppid()
    (outputs._registry() / "other.json").write_text(json.dumps({
        "run_id": "33333333-3333-4333-8333-333333333333", "pid": peer,
        "proc_start": outputs._process_started(peer), "root": "/", "sweeps": False,
    }))
    run = open_run(client, experiment="cap-log-only-rival", capture_outputs=True)
    (work / "result.json").write_text("{}")
    run.finish()
    assert "result.json" in _rows(app, run)


def test_a_record_with_no_root_overlaps_nothing():
    assert not outputs._overlap("/work", "")


def test_an_unreaped_zombie_is_not_alive():
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    try:
        assert _wait(lambda: not outputs._alive(pid))
    finally:
        os.waitpid(pid, 0)


def _wait(predicate, timeout=10.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return False


def test_a_file_that_would_outrun_the_budget_is_not_started(client, app, work, monkeypatch):
    """The deadline is checked before each file AND against its predicted
    inspection time (~1 MB/s): a 3 MB file with 1 s left is pointed to, not
    read for three seconds."""
    monkeypatch.setenv(outputs.BUDGET_ENV, "1")
    run = open_run(client, experiment="cap-budget-predict", capture_outputs=True)
    (work / "big.jsonl").write_text('{"x": 1}\n' * 350_000)
    real = secret_gate.read_upload_redacted_sourced
    read = []
    monkeypatch.setattr(secret_gate, "read_upload_redacted_sourced", lambda p, **kw: read.append(p) or real(p, **kw))
    run.finish()
    assert _rows(app, run)["big.jsonl"]["is_reference"] and read == []


def test_the_finish_timeout_caps_the_close_budget(monkeypatch):
    monkeypatch.delenv(outputs.BUDGET_ENV, raising=False)
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "10")
    assert outputs.close_budget() == 10


def test_a_recovery_can_be_stopped_by_sigterm(monkeypatch):
    """The helper that starts a recovery ignores nearly every signal, and
    ignored signals survive exec."""
    import signal

    monkeypatch.setattr(signal, "signal", signal.signal)  # restored after the test
    previous = signal.signal(signal.SIGTERM, signal.SIG_IGN)
    try:
        outputs._default_signals()
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
    finally:
        signal.signal(signal.SIGTERM, previous)


# -- final review round (PR #1959) --------------------------------------------------------
def test_an_encoded_token_beside_a_literal_one_is_never_uploaded(client, app, work):
    """Replacing the literal GitHub token used to count the encoded one as
    replaced too (same rule name): the file shipped with it inside."""
    blob = base64.b64encode(gzip.compress(f"export GH={TOKEN}\n".encode())).decode()
    run = open_run(client, experiment="cap-encoded-beside-literal", capture_outputs=True)
    (work / "notes.txt").write_text(f"token {TOKEN}\nblob {blob}\n")
    (work / "fine.txt").write_text("fine")
    with pytest.warns(UserWarning, match=r"may hold a credential.*notes.txt"):
        run.finish()
    assert set(_rows(app, run)) == {"fine.txt"}


def test_the_gate_reports_what_redaction_left_behind():
    blob = base64.b64encode(gzip.compress(f"export GH={TOKEN}\n".encode())).decode()
    data, result = secret_gate.redact_bytes(f"token {TOKEN}\nblob {blob}\n".encode())
    assert TOKEN.encode() not in data.split(b"blob")[0]  # the literal one is replaced
    assert "github-token" in result.flagged  # and the encoded one is still reported


def test_ranks_closing_together_queue_a_file_once(client, app, work):
    import threading

    run = open_run(client, experiment="cap-concurrent-ranks", capture_outputs=True)
    (work / "shared.jsonl").write_text('{"x": 1}\n' * 1000)
    first = run._capture
    second = outputs.OutputCapture(client, run.id, str(work), tee=False, launcher=False)
    second.baseline = dict(first.baseline)
    deadline = time.monotonic() + 60
    threads = [threading.Thread(target=c._sweep, args=(deadline,)) for c in (first, second)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(60)
    names = [op["upload"]["name"] for _, op in client.journal.pending() if op.get("kind") == "upload"]
    assert names.count("outputs/shared.jsonl") == 1
    first._sweep_done = first._log_done = True
    first._unregister()


def test_execute_delivery_uses_what_is_left_of_the_deadline(client, work, monkeypatch):
    run = open_run(client, experiment="cap-exec-deadline", capture_outputs=False)
    flushed = []
    monkeypatch.setattr(client, "flush", lambda **kw: flushed.append(1) or 0)
    run._deliver_captured(time.monotonic() - 1)  # already spent: no drain, hand off
    assert flushed == []


# -- .probeignore (plan (n)) ------------------------------------------------------


def test_probeignore_keeps_files_out_of_the_sweep(client, app, work):
    (work / ".probeignore").write_text("ckpt/\n*.tmp\n!keep.tmp\n")
    run = open_run(client, experiment="cap-ign", capture_outputs=True)
    for rel in ("ckpt/step-1/model.pt", "scratch.tmp", "keep.tmp", "results.csv"):
        (work / rel).parent.mkdir(parents=True, exist_ok=True)
        (work / rel).write_text("x")
    run.finish()
    assert set(_rows(app, run)) == {"keep.tmp", "results.csv"}


def test_probeignore_never_re_includes_a_credential(client, app, work):
    (work / ".probeignore").write_text("!.env\n!*.pem\n")
    run = open_run(client, experiment="cap-ign-safety", capture_outputs=True)
    (work / ".env").write_text("OPENAI_API_KEY=sk-proj-" + "a" * 48)
    (work / "kept.txt").write_text("kept")
    with pytest.warns(UserWarning, match=r"may hold a credential.*\.env"):
        run.finish()
    assert set(_rows(app, run)) == {"kept.txt"}


def test_an_explicit_log_artifact_wins_over_probeignore(client, app, work):
    (work / ".probeignore").write_text("ckpt/\n")
    run = open_run(client, experiment="cap-ign-explicit", capture_outputs=True)
    (work / "ckpt").mkdir()
    (work / "ckpt" / "model.pt").write_bytes(b"weights")
    run.log_artifact("model", path=str(work / "ckpt" / "model.pt"), sync=True)
    run.finish()
    names = {a["name"] for a in app.artifacts[run.id]}
    assert names == {"model.pt"}, "the explicit upload, and no swept copy under outputs/ckpt"


def test_ignore_argument_applies_to_the_sweep(client, app, work):
    run = open_run(client, experiment="cap-ign-arg", capture_outputs=True, ignore=["*.bin"])
    (work / "shard.bin").write_bytes(b"b")
    (work / "metrics.json").write_text("{}")
    run.finish()
    assert set(_rows(app, run)) == {"metrics.json"}


def test_patterns_apply_to_an_outputs_folder_outside_the_root(client, app, work, tmp_path):
    """review MED-1: `outputs=` in $SCRATCH lies outside the `.probeignore` root.
    Unanchored file patterns and `ignore=` still apply there, relative to that
    folder; an anchored one (`/data`) cannot, and output capture says so once."""
    (work / ".probeignore").write_text("*.jsonl\n/data\n")
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    with pytest.warns(UserWarning, match=r"outside .* 1 anchored \.probeignore pattern.*'/data'"):
        run = open_run(
            client, experiment="cap-ign-out", capture_outputs=True, outputs=str(scratch), ignore=["*.ckpt", "/tmp"]
        )
    for rel in ("customer_rows.jsonl", "model.ckpt", "data/x.csv", "tmp/t.txt", "results.csv"):
        (scratch / rel).parent.mkdir(parents=True, exist_ok=True)
        (scratch / rel).write_text("x")
    run.finish()
    assert set(_rows(app, run)) == {"data/x.csv", "results.csv"}


def test_patterns_apply_to_an_outputs_folder_inside_the_root(client, app, work):
    """Control: inside the root every pattern reads as git reads it, `/data`
    included (the root's `data/`, not `out/data/`), and nothing is said."""
    (work / ".probeignore").write_text("*.jsonl\n/data\n")
    out = work / "out"
    out.mkdir()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run = open_run(client, experiment="cap-ign-in", capture_outputs=True, outputs=str(out), ignore=["*.ckpt"])
    assert not [w for w in caught if "anchored" in str(w.message)]
    for rel in ("customer_rows.jsonl", "model.ckpt", "data/x.csv", "results.csv"):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / rel).write_text("x")
    run.finish()
    assert set(_rows(app, run)) == {"data/x.csv", "results.csv"}


def test_a_recovered_window_keeps_the_runs_rules(client, work):
    from probe.sdk import ignore

    rules = ignore.load(str(work), extra=["ckpt/"])
    capture = outputs.OutputCapture(client, "run-rec", str(work), tee=False, launcher=False, ignore=rules)
    record = capture._record(shared_with=[])
    rebuilt = ignore.from_record(json.loads(json.dumps(record))["ignore"])
    assert rebuilt is not None and rebuilt.ignored(str(work / "ckpt" / "a.pt"))
    assert outputs.OutputCapture(client, "run-rec", str(work), tee=False, launcher=False)._record(
        shared_with=[]
    )["ignore"] is None


@pytest.mark.parametrize("shared", [True, False])
def test_a_childs_own_ignore_reaches_the_launchers_sweep(client, app, work, shared):
    """#2045 re-review MED: the launcher sweeps its child's folder after the
    child exits, with the rules the launcher loaded; a child's own
    `probe.init(ignore=['*.ckpt'])` never reached it and `model.ckpt` was
    queued. The child hands its rules to the launcher's window record
    (`share_ignore`), which the sweep re-reads. Control: not shared, swept."""
    run = open_run(client, experiment="cap-ign-child", capture_outputs=False)
    share = (
        "from probe.sdk import ignore, outputs\n"
        "assert outputs.share_ignore(os.environ['PROBE_RUN_ID'], ignore.load(os.getcwd(), extra=['*.ckpt'])) == 1\n"
        if shared
        else ""
    )
    (work / "job.py").write_text(
        "import os\n" + share + "open('model.ckpt', 'w').write('w')\nopen('metrics.json', 'w').write('{}')\n"
    )
    result = run.execute([sys.executable, str(work / "job.py")], cwd=str(work), capture_outputs=True)
    assert result.returncode == 0
    swept = set(_rows(app, run)) - {"probe/run.log"}
    assert swept == ({"metrics.json"} if shared else {"metrics.json", "model.ckpt"}), swept


def test_share_ignore_skips_its_own_windows_and_other_runs(client, work):
    from probe.sdk import ignore

    rules = ignore.load(str(work), extra=["*.ckpt"])
    run = open_run(client, experiment="cap-ign-share", capture_outputs=True)
    assert outputs.share_ignore(run.id, rules) == 0, "a window of this very process already has them"
    assert outputs.share_ignore("some-other-run", rules) == 0
    assert outputs.share_ignore(run.id, None) == 0
    run.finish()


# -- what a reader can match (lineage plan 3, F1) -------------------------------------


def _sha256(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def test_the_sourced_reader_takes_both_hashes_from_one_read(tmp_path, monkeypatch) -> None:
    path = tmp_path / "notes.txt"
    path.write_bytes(f"token {TOKEN} used\n".encode())
    reads = []
    real = secret_gate._read_source
    monkeypatch.setattr(secret_gate, "_read_source", lambda p, **k: reads.append(p) or real(p, **k))
    data, result, source = secret_gate.read_upload_redacted_sourced(path, full_scan=True)
    assert len(reads) == 1
    assert source == _sha256(path.read_bytes()) and TOKEN.encode() not in data and result.rewritten
    assert (data, result.rewritten) == (lambda d, r: (d, r.rewritten))(*secret_gate.read_upload_redacted(path, full_scan=True))


def test_a_redacted_capture_carries_the_originals_hash(client, app, work, monkeypatch) -> None:
    """The stored hash names bytes no reader opened; `meta.source_sha256` is
    what a later run READING the original hashes -- the server's
    `pre_redaction` basis."""
    original = f"token {TOKEN} used\n".encode()
    run = open_run(client, experiment="f1-source", capture_outputs=True)
    (work / "notes.txt").write_bytes(original)
    (work / "clean.txt").write_text("nothing secret")
    with pytest.warns(UserWarning, match="replaced credentials"):
        run.finish()
    rows = {a["name"]: a for a in app.artifacts[run.id]}
    redacted = rows["outputs/notes.txt"]
    assert TOKEN.encode() not in _bytes(app, redacted)
    assert redacted["meta"]["source_sha256"] == _sha256(original) != redacted["content_hash"]
    assert "source_sha256" not in rows["outputs/clean.txt"]["meta"]
    # What the read recorder of a later run hashes for that file.
    ident = inputs._ident(os.stat(work / "notes.txt"))
    assert inputs.hash_file(str(work / "notes.txt"), ident, cache=None, budget=[1 << 40])[0] == _sha256(original)
