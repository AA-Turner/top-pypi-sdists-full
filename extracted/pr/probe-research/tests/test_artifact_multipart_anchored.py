"""Multipart uploads at a project, experiment, workspace or Shared (0333, D5).

The client's half that needs no server: the queued op names its anchor (and
rides no run's lane), every anchor reaches its own doors -- an op queued by
an earlier release, which only ever named a run, reaches the run's -- and a
server that does not declare ``artifact_multipart_anchored`` keeps today's
`probe artifact add --project` path. The whole lifecycle against the real app
and object storage is `tests/integration/test_artifact_multipart_anchored_s3.py`.
"""

from __future__ import annotations

import os

import pytest

from probe import cli
from probe.sdk import multipart
from probe.sdk.anchors import Anchor
from tests.conftest import make_client

MiB = 1024 * 1024
UPLOAD = "11111111-1111-1111-1111-111111111111"


def _sparse(path, size=70 * MiB):
    with open(path, "wb") as fh:
        fh.write(b"head")
        fh.truncate(size)
    return path


class _Journal:
    """What `build_op` reads of a journal: its directory and its op stamp."""

    def __init__(self, directory) -> None:
        self.dir = directory
        self.context = {"name": None, "base_url": "http://test"}

    def _base_op(self, kind, run_ref):
        return {"op_id": "op" + os.urandom(4).hex(), "kind": kind, "run_ref": run_ref}

    def _free_floor(self) -> int:
        return 0


def _op(tmp_path, anchor: str, anchor_id: str | None, **kw) -> dict:
    src = _sparse(tmp_path / f"{anchor}.bin")
    return multipart.build_op(
        _Journal(tmp_path / "outbox"),
        anchor=anchor,
        anchor_id=anchor_id,
        name=f"{anchor}.bin",
        src=str(src),
        kind=None,
        content_type=None,
        meta=None,
        notes="what it is",
        span_id=None,
        step_index=None,
        **kw,
    )


@pytest.mark.parametrize(
    ("anchor", "anchor_id"),
    [("project", "p-1"), ("experiment", "e-1"), ("workspace", "w-1"), ("shared", None)],
)
def test_an_anchored_op_names_its_anchor_and_rides_no_run(tmp_path, anchor, anchor_id) -> None:
    op = _op(tmp_path, anchor, anchor_id)
    assert (op["upload"]["anchor"], op["upload"]["anchor_id"]) == (anchor, anchor_id)
    assert op["run_ref"] is None, "no run's barrier waits on it"
    assert op["lane"] == f"multipart:{op['op_id']}" and op["blocking"] is False
    upload, state = multipart._fields(op)
    assert state["stage_mode"] == "hardlink" and upload["notes"] == "what it is"


def test_a_run_op_is_built_exactly_as_before(tmp_path) -> None:
    op = multipart.build_op(
        _Journal(tmp_path / "outbox"),
        run_id="r-1",
        name="ckpt.pt",
        src=str(_sparse(tmp_path / "ckpt.pt")),
        kind=None,
        content_type=None,
        meta={"step": 1},
        notes=None,
        span_id=None,
        step_index=7,
    )
    assert (op["run_ref"], op["upload"]["anchor"], op["upload"]["anchor_id"]) == ("r-1", "run", "r-1")
    assert op["upload"]["step_index"] == 7 and op["upload"]["meta"] == {"step": 1}


def test_an_anchor_without_its_id_is_refused_before_staging(tmp_path) -> None:
    with pytest.raises(ValueError):
        _op(tmp_path, "project", None)
    assert not (tmp_path / "outbox" / "multipart" / "staged").exists() or not os.listdir(
        tmp_path / "outbox" / "multipart" / "staged"
    )


class _Recorder:
    """Records the (method, path) each door takes; an experiment is placed
    under project `P`, as `Client._on_experiment` places it."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.transport = self

    def post(self, path, body=None, **_kw):
        self.calls.append(("POST", path))
        return {}

    def get(self, path, **_kw):
        self.calls.append(("GET", path))
        return {}

    def delete(self, path, **_kw):
        self.calls.append(("DELETE", path))
        return None

    def _on_experiment(self, call, experiment_id, project_id=None, **_kw):
        return call("P", experiment_id)


@pytest.mark.parametrize(
    ("upload", "door"),
    [
        ({"anchor": "run", "anchor_id": "R"}, "/v1/runs/R/artifacts/multipart"),
        # An op queued before 0333 named a run, and only a run.
        ({"anchor_id": "R"}, "/v1/runs/R/artifacts/multipart"),
        ({"anchor": "project", "anchor_id": "X"}, "/v1/projects/X/artifacts/multipart"),
        (
            {"anchor": "experiment", "anchor_id": "E"},
            "/v1/projects/P/experiments/E/artifacts/multipart",
        ),
        ({"anchor": "workspace", "anchor_id": "W"}, "/v1/workspaces/W/files/multipart"),
        ({"anchor": "shared", "anchor_id": None}, "/v1/shared/files/multipart"),
    ],
)
def test_every_anchor_reaches_its_own_doors(upload, door) -> None:
    client = _Recorder()
    multipart._open(client, upload, {})
    multipart._grant(client, upload, UPLOAD, {"part_numbers": [1]})
    multipart._status(client, upload, UPLOAD)
    multipart._finish(client, upload, UPLOAD)
    multipart._abort(client, upload, UPLOAD)
    assert client.calls == [
        ("POST", door),
        ("POST", f"{door}/{UPLOAD}/parts"),
        ("GET", f"{door}/{UPLOAD}"),
        ("POST", f"{door}/{UPLOAD}/complete"),
        ("DELETE", f"{door}/{UPLOAD}"),
    ]


def test_only_a_run_sends_a_runs_fields() -> None:
    sent: list[dict] = []

    class _Body(_Recorder):
        def post(self, path, body=None, **_kw):
            sent.append(body)
            return {}

    common = {"name": "f.bin", "blob": "a" * 64, "size_bytes": 70 * MiB, "kind": "evaluation",
              "meta": {"k": 1}, "span_id": "s", "step_index": 3, "notes": "n"}
    multipart._create(_Body(), {**common, "anchor": "project", "anchor_id": "X"})
    multipart._create(_Body(), {**common, "anchor": "run", "anchor_id": "R"})
    assert set(sent[0]) == {"name", "content_hash", "size_bytes", "notes"}
    assert {"kind", "meta", "span_id", "step_index"} <= set(sent[1])


def test_the_anchor_vocabulary_is_the_clients() -> None:
    from probe.sdk.client import Anchor as ClientAnchor

    assert ClientAnchor is Anchor


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**kw):
        return make_client(app, tmp_spool=tmp_path / "spool", async_writes=kw.get("async_writes") is not False)

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    return app


def test_a_server_without_the_anchored_doors_keeps_todays_path(wired, tmp_path, capsys) -> None:
    """`artifact_multipart` alone (today's prod) is not enough: a project file
    over 64 MiB goes the way it always did -- the single PUT, which the
    inspection limit refuses -- and nothing is staged or queued."""
    wired.supports_artifact_multipart = True
    big = _sparse(tmp_path / "big.bin")
    assert cli.main(["artifact", "add", str(big), "--project", "p"]) != 0
    assert multipart.pending(make_client(wired, tmp_spool=tmp_path / "spool").journal) == []
    assert not any("/multipart" in r.url.path for r in wired.requests)
    assert "(queued)" not in capsys.readouterr().out


def test_a_big_project_file_queues_in_parts_even_under_probe_async_0(app, tmp_path, monkeypatch, capsys) -> None:
    """The Probe daemon runs `probe` with PROBE_ASYNC=0 and kills a call at
    180 s: a project file over 64 MiB is queued in parts unless --sync says
    otherwise, as a run's is (#2641), when a credential could deliver it."""
    from probe.sdk.client import Client as SdkClient

    def factory(**kw):
        return make_client(app, tmp_spool=tmp_path / "spool", async_writes=kw.get("async_writes") is True)

    monkeypatch.setattr(cli, "Client", factory)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    monkeypatch.setenv("PROBE_BASE_URL", "http://test")
    monkeypatch.setenv("PROBE_ASYNC", "0")
    # A CI runner's outbox disk reads as ephemeral; pin the durable disk.
    monkeypatch.setenv("PROBE_EPHEMERAL", "0")
    monkeypatch.setattr("probe.cli.outbox_worker.maybe_spawn", lambda directory=None: False)
    cli.main(["project", "create", "--kind", "general", "p"])
    real = SdkClient.supports_feature
    monkeypatch.setattr(
        SdkClient,
        "supports_feature",
        lambda self, name: name == multipart.ANCHORED_FEATURE or real(self, name),
    )
    big = _sparse(tmp_path / "big.bin")
    capsys.readouterr()

    assert cli.main(["artifact", "add", str(big), "--project", "p"]) == 0

    assert "(queued)" in capsys.readouterr().out
    [(_, op)] = multipart.pending(make_client(app, tmp_spool=tmp_path / "spool").journal)
    assert op["upload"]["anchor"] == "project"

