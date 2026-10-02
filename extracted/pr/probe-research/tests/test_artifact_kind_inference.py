"""An image is filed as a `plot` when the caller names no kind, by the SDK
(`Run.log_artifact`) and by `probe artifact add` alike.

A training script's `run.log_artifact("loss", path="loss.png")` used to land as
kind `file`, the same as a checkpoint or a config, so nothing downstream could
tell a result's picture from its inputs without re-deriving it from the name.
The kind is read from the extension only when the caller passed none: an
explicit kind always wins, `"file"` included. A PDF stays a `file`: a paper or a
report is a PDF far more often than a figure is.

The wire contract is unchanged: `file` still travels as NO kind (`None` keeps an
existing row's kind when the same name is restaged), and anything else travels
as itself.
"""

from __future__ import annotations

import pytest

from probe import cli
from probe.sdk.filetype import artifact_kind_for
from probe.sdk.run import Run
from tests.conftest import make_client
from tests.test_outbox import seeded_run


@pytest.mark.parametrize(
    ("name", "path", "expected"),
    [
        ("loss.png", None, "plot"),
        ("loss.PNG", None, "plot"),
        ("sample.jpg", None, "plot"),
        ("sample.jpeg", None, "plot"),
        ("attention.svg", None, "plot"),
        ("report.pdf", None, "file"),
        ("paper.PDF", None, "file"),
        ("rollout.gif", None, "plot"),
        ("frame.webp", None, "plot"),
        ("outputs/plots/fig.png", None, "plot"),
        # The name has no extension; the path supplies it.
        ("loss-curve", "figs/loss.png", "plot"),
        ("ckpt.pt", None, "file"),
        ("notes.md", None, "file"),
        ("metrics.json", None, "file"),
        ("weights", None, "file"),
        ("ckpt", "runs/ckpt-4000.pt", "file"),
        # A name's own extension beats the path's.
        ("table.csv", "figs/table.png", "file"),
    ],
)
def test_artifact_kind_for(name, path, expected):
    assert artifact_kind_for(name, path) == expected


def _file(tmp_path, name: str) -> str:
    p = tmp_path / name
    p.write_bytes(b"\x89PNG not really")
    return str(p)


def _log(app, tmp_path, monkeypatch, name: str, **kw) -> tuple[dict, list[dict]]:
    """Log one artifact; return the stored row and every upload body sent."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    sent: list[dict] = []
    post = client.transport.post

    def _recording_post(path, body=None, *args, **kwargs):
        if path.endswith("/artifacts/uploads") or path.endswith("/artifacts"):
            sent.append(dict(body or {}))
        return post(path, body, *args, **kwargs)

    monkeypatch.setattr(client.transport, "post", _recording_post)
    Run(client, {"id": run_id}).log_artifact(name, **kw)
    client.close()
    rows = [row for row in app.artifacts.get(run_id, []) if row["name"].startswith(name.split(".")[0])]
    assert rows, app.artifacts
    return rows[-1], sent


@pytest.mark.parametrize(
    ("name", "kw", "stored", "on_the_wire"),
    [
        ("loss.png", {}, "plot", "plot"),
        ("report.pdf", {}, "file", None),
        ("ckpt.pt", {}, "file", None),
        # Explicit always wins, and an explicit `file` still travels as no kind.
        ("loss.png", {"kind": "file"}, "file", None),
        ("loss.png", {"kind": "eval_curve"}, "eval_curve", "eval_curve"),
        ("ckpt.pt", {"kind": "checkpoint"}, "checkpoint", "checkpoint"),
    ],
)
def test_log_artifact_upload_infers_the_kind_only_when_none_was_passed(
    app, tmp_path, monkeypatch, name, kw, stored, on_the_wire
):
    row, sent = _log(app, tmp_path, monkeypatch, name, path=_file(tmp_path, name), **kw)
    assert row["kind"] == stored
    assert sent and sent[-1].get("kind") == on_the_wire


def test_a_uri_reference_to_a_plot_is_a_plot(app, tmp_path, monkeypatch):
    row, _sent = _log(app, tmp_path, monkeypatch, "loss.svg", uri="s3://bucket/loss.svg")
    assert row["kind"] == "plot"


# ---------------------------------------------------------------------------
# `probe artifact add`: the same default as the SDK when --kind is not given.
# ---------------------------------------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


def _cli_run(capsys) -> str:
    cli.main(["run", "start", "--experiment", "e", "--name", "r"])
    return capsys.readouterr().out.strip()


@pytest.mark.parametrize(
    ("filename", "flags", "stored"),
    [
        ("loss.png", [], "plot"),
        ("attention.svg", [], "plot"),
        ("report.pdf", [], "file"),
        ("notes.md", [], "file"),
        ("loss.png", ["--kind", "file"], "file"),
        ("ckpt.pt", ["--kind", "checkpoint"], "checkpoint"),
        # The name has no extension; the path supplies it.
        ("loss.png", ["--name", "loss-curve"], "plot"),
    ],
)
def test_cli_artifact_add_defaults_the_kind_like_the_sdk(
    wired, tmp_path, capsys, filename, flags, stored
):
    run_id = _cli_run(capsys)
    path = _file(tmp_path, filename)
    assert cli.main(["artifact", "add", run_id, path, "--sync", *flags]) == 0
    rows = wired.artifacts.get(run_id, [])
    assert [row["kind"] for row in rows] == [stored], rows


def test_cli_artifact_add_on_a_project_still_takes_no_kind(wired, tmp_path, capsys):
    """Only a run artifact has a kind: an image filed on a project must not trip
    the run-only `--kind` check just because its default is now inferred."""
    assert cli.main(["artifact", "add", _file(tmp_path, "loss.png"), "--project", "p"]) == 0
