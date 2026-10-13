"""Saved model state (`.ckpt`, `.safetensors`, `.pt`, `.pth`) is filed as a
`checkpoint` when the caller names no kind, by the SDK (`Run.log_artifact`) and
by `probe artifact add` alike; every other file, an image included, is `other`.
Output capture keeps `checkpoint` out (`checkpoints=False`): a captured
checkpoint FOLDER's small files must not each become "the last checkpoint".

`plot` was the image default until `artifacts.kind` became a fixed vocabulary
(`probe.sdk.artifact_kinds`): a figure is not a kind, and the server files the
word `plot` as `other` with the word kept as its label.

The kind is read from the extension only when the caller passed none: an
explicit kind always wins. The wire contract is unchanged: the default kind
(`other`, or `file` as it was spelled before) travels as NO kind (`None` keeps an
existing row's kind when the same name is restaged), and anything else travels
as itself. The in-memory API stores a missing kind as `file`, its old default.
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
        ("loss.png", None, "other"),
        ("loss.PNG", None, "other"),
        ("sample.jpg", None, "other"),
        ("attention.svg", None, "other"),
        ("rollout.gif", None, "other"),
        ("report.pdf", None, "other"),
        ("outputs/plots/fig.png", None, "other"),
        ("loss-curve", "figs/loss.png", "other"),
        ("ckpt.pt", None, "checkpoint"),
        ("last.ckpt", None, "checkpoint"),
        ("model.safetensors", None, "checkpoint"),
        ("resnet.PTH", None, "checkpoint"),
        ("checkpoint-500/optimizer.pt", None, "checkpoint"),
        # Any binary, or an exported model: not a checkpoint by extension alone.
        ("pytorch_model.bin", None, "other"),
        ("model.gguf", None, "other"),
        ("model.onnx", None, "other"),
        ("notes.md", None, "other"),
        ("metrics.json", None, "other"),
        ("weights", None, "other"),
        # The name has no extension; the path supplies it.
        ("ckpt", "runs/ckpt-4000.pt", "checkpoint"),
        # A name's own extension beats the path's.
        ("table.csv", "figs/ckpt.pt", "other"),
    ],
)
def test_artifact_kind_for(name, path, expected):
    assert artifact_kind_for(name, path) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [("ckpt.pt", "other"), ("model.safetensors", "other"), ("rng_state.pth", "other"), ("curve.png", "other")],
)
def test_output_capture_never_infers_a_checkpoint(name, expected):
    assert artifact_kind_for(name, checkpoints=False) == expected


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
        # The default travels as no kind, so the fake's own default lands.
        ("loss.png", {}, "file", None),
        ("report.pdf", {}, "file", None),
        ("ckpt.pt", {}, "checkpoint", "checkpoint"),
        ("model.safetensors", {}, "checkpoint", "checkpoint"),
        # Explicit always wins, and an explicit default (either spelling)
        # still travels as no kind.
        ("ckpt.pt", {"kind": "file"}, "file", None),
        ("ckpt.pt", {"kind": "other"}, "file", None),
        ("loss.png", {"kind": "Other"}, "file", None),
        # Any other word travels as itself: the server keeps it as the label.
        ("loss.png", {"kind": "eval_curve"}, "eval_curve", "eval_curve"),
        ("loss.png", {"kind": "evaluation"}, "evaluation", "evaluation"),
        ("ckpt.pt", {"kind": "checkpoint"}, "checkpoint", "checkpoint"),
    ],
)
def test_log_artifact_upload_infers_the_kind_only_when_none_was_passed(
    app, tmp_path, monkeypatch, name, kw, stored, on_the_wire
):
    row, sent = _log(app, tmp_path, monkeypatch, name, path=_file(tmp_path, name), **kw)
    assert row["kind"] == stored
    assert sent and sent[-1].get("kind") == on_the_wire


def test_a_uri_reference_to_an_image_is_other(app, tmp_path, monkeypatch):
    row, _sent = _log(app, tmp_path, monkeypatch, "loss.svg", uri="s3://bucket/loss.svg")
    assert row["kind"] == "other"


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
        ("loss.png", [], "file"),
        ("attention.svg", [], "file"),
        ("report.pdf", [], "file"),
        ("notes.md", [], "file"),
        ("ckpt.pt", [], "checkpoint"),
        ("loss.png", ["--kind", "file"], "file"),
        ("loss.png", ["--kind", "other"], "file"),
        ("ckpt.pt", ["--kind", "checkpoint"], "checkpoint"),
        ("results.json", ["--kind", "evaluation"], "evaluation"),
        # The name has no extension; the path supplies it.
        ("ckpt.pt", ["--name", "last"], "checkpoint"),
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
    """Only a run artifact has a kind: a file filed on a project must not trip
    the run-only `--kind` check because the default it is given is `other`."""
    assert cli.main(["artifact", "add", _file(tmp_path, "loss.png"), "--project", "p"]) == 0


@pytest.mark.parametrize("default", ["other", "file"])
def test_cli_artifact_add_on_a_project_accepts_the_default_kind_spelled_out(
    wired, tmp_path, capsys, default
):
    assert cli.main(
        ["artifact", "add", _file(tmp_path, "loss.png"), "--project", "p", "--kind", default]
    ) == 0


def test_cli_artifact_add_on_a_project_refuses_a_chosen_kind(wired, tmp_path, capsys):
    assert cli.main(
        ["artifact", "add", _file(tmp_path, "loss.png"), "--project", "p", "--kind", "evaluation"]
    ) != 0
    assert "run-only" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# A word the vocabulary does not list is filed under a listed kind, and the
# CLI says where, once, on stderr: the listing will show a different kind than
# the one typed.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "line"),
    [
        ("report", "kind: filed as other (label: report)"),
        ("Benchmark", "kind: filed as evaluation (label: benchmark)"),
        ("script", "kind: filed as code (label: script)"),
    ],
)
def test_cli_says_where_an_unlisted_kind_was_filed(wired, tmp_path, capsys, word, line):
    run_id = _cli_run(capsys)
    assert cli.main(["artifact", "add", run_id, _file(tmp_path, "r.md"), "--sync", "--kind", word]) == 0
    captured = capsys.readouterr()
    assert "recorded on" in captured.out
    assert [ln for ln in captured.err.splitlines() if ln.startswith("kind:")] == [line]
    # The client sends the word itself; the server's trigger does the filing
    # (the in-memory API only lowercases it).
    assert [row["kind"] for row in wired.artifacts[run_id]] == [word.lower()]


@pytest.mark.parametrize("flags", [[], ["--kind", "evaluation"], ["--kind", "file"], ["--kind", "Code-Snapshot"]])
def test_cli_says_nothing_for_a_listed_kind_or_the_default(wired, tmp_path, capsys, flags):
    run_id = _cli_run(capsys)
    assert cli.main(["artifact", "add", run_id, _file(tmp_path, "r.md"), "--sync", *flags]) == 0
    assert "kind:" not in capsys.readouterr().err
