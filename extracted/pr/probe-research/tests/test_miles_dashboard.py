from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest

from probe.integrations.miles_dashboard import DashboardPublisher, start_capture


class UploadRun:
    def __init__(self):
        self.files = {}
        self.fail = False
        self.reference = False

    def log_artifact(self, name, *, path, strict, sync, **kwargs):
        assert strict is True and sync is True
        if self.fail:
            raise ConnectionError("offline")
        self.files[name] = (Path(path).read_bytes(), kwargs)
        return {"id": "uploaded", "is_reference": self.reference}


def test_stream_uploads_only_complete_lines_and_resumes_at_the_confirmed_offset(tmp_path):
    dump = tmp_path / "dump"
    (dump / "dashboard").mkdir(parents=True)
    source = dump / "dashboard" / "metrics.jsonl"
    first = b'{"ts":1,"step":1,"metrics":{"reward":0}}\n'
    partial = b'{"ts":2'
    source.write_bytes(first + partial)
    run = UploadRun()
    publisher = DashboardPublisher(run, dump, tmp_path / "state")
    publisher.sync_once()
    assert len(run.files) == 1
    assert next(iter(run.files.values()))[0] == first
    state = json.loads((tmp_path / "state/state.json").read_text())
    assert state["files"]["metrics.jsonl"]["offset"] == len(first)
    source.write_bytes(first + partial + b',"step":2,"metrics":{"reward":1}}\n')
    publisher.sync_once()
    assert len(run.files) == 2
    assert sum(len(raw.splitlines()) for raw, _ in run.files.values()) == 2
    publisher.sync_once()
    assert len(run.files) == 2  # no repeated whole-file upload


def test_failed_upload_does_not_advance_the_durable_cursor(tmp_path):
    dump = tmp_path / "dump"
    (dump / "dashboard").mkdir(parents=True)
    (dump / "dashboard/gpu_util.jsonl").write_text('{"ts":1,"node":"n","gpu":0,"util":90}\n')
    run = UploadRun()
    publisher = DashboardPublisher(run, dump, tmp_path / "state")
    run.fail = True
    with pytest.raises(ConnectionError):
        publisher.sync_once()
    assert not (tmp_path / "state/state.json").exists()
    run.fail = False
    publisher.sync_once()
    assert len(run.files) == 1
    assert json.loads((tmp_path / "state/state.json").read_text())["files"]["gpu_util.jsonl"]["offset"] > 0


def test_reference_refusal_is_not_acknowledged_as_uploaded(tmp_path):
    dump = tmp_path / "dump"
    (dump / "dashboard").mkdir(parents=True)
    (dump / "dashboard/phases.jsonl").write_text('{"t0":1,"t1":-1}\n')
    run = UploadRun()
    run.reference = True
    publisher = DashboardPublisher(run, dump, tmp_path / "state")
    with pytest.raises(RuntimeError, match="not uploaded"):
        publisher.sync_once()
    assert not (tmp_path / "state/state.json").exists()


def test_open_phase_remains_visible_in_later_viewports(tmp_path):
    dump = tmp_path / "dump"
    (dump / "dashboard").mkdir(parents=True)
    (dump / "dashboard/phases.jsonl").write_text('{"t0":1,"t1":-1}\n')
    run = UploadRun()
    DashboardPublisher(run, dump, tmp_path / "state").sync_once()
    _, options = next(iter(run.files.values()))
    assert options["meta"]["rl_dashboard"]["t1"] is None


def test_capture_is_optional_without_native_dumps(tmp_path):
    assert start_capture(Namespace(), "run", tmp_path) is None
    assert start_capture(Namespace(dump_details="/dump", probe_dashboard=False), "run", tmp_path) is None
