"""The extension survives the trip in, on every door that names an artifact.

`name` IS the artifact's relative posix path server-side, and the dashboard's
preview route decides text-vs-raster-vs-binary from its extension. `--name`
REPLACES the file's basename, though, and the skill documents naming an upload
for what it IS (`--name ckpt`), so the extension was routinely dropped on the way
in. The file arrived whole and unreadable: "Preview unavailable" on ordinary
markdown, measured at 91% of one tenant's artifacts.

These pin the repair at each door independently, because they are reached
independently: the CLI's async branch journals a name without ever entering the
SDK, and an in-process script enters the SDK without ever touching the CLI.
"""

from __future__ import annotations

import pytest

from probe.sdk.client import Anchor
from probe.sdk.filetype import file_extension, name_with_extension
from probe.sdk.run import Run
from tests.conftest import make_client
from tests.test_outbox import seeded_run


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("notes.md", "md"),
        ("data.tar.gz", "gz"),
        ("outputs/plots/fig.png", "png"),
        ("clip.mp4", "mp4"),
        ("shard-0.safetensors", "safetensors"),
        # No dot at all -- the shape agents actually write.
        ("atomworks-study-README", ""),
        ("Ben feedback — three separate product specs", ""),
        # A version suffix is NOT an extension. Reading `3` as one would leave
        # this name unrepaired, and it is the family the repair is for.
        ("atomworks-study-v0.3", ""),
        ("2026.08.28", ""),
        # A dotfile's "extension" is its whole name.
        (".gitignore", ""),
        # A hyphen is not an extension character, and nothing real is this long --
        # both are titles that happen to contain a dot.
        ("model.checkpoint-final", ""),
        ("plan.assignmentmodeling", ""),
    ],
)
def test_file_extension(name: str, expected: str) -> None:
    assert file_extension(name) == expected


@pytest.mark.parametrize(
    ("name", "path", "expected"),
    [
        ("ckpt", "runs/ckpt-4000.pt", "ckpt.pt"),
        ("atomworks-study-README", "/tmp/study.md", "atomworks-study-README.md"),
        ("outputs/fig", "fig.png", "outputs/fig.png"),
        ("atomworks-study-v0.3", "s.md", "atomworks-study-v0.3.md"),
        (r"C:\work\notes", r"C:\work\notes.md", r"C:\work\notes.md"),
        # Additive ONLY: a caller who named the upload keeps what they chose.
        ("report.txt", "source.md", "report.txt"),
        ("data.tar.gz", "data.tar.gz", "data.tar.gz"),
        # Nothing to take an extension from.
        ("ckpt", "weights", "ckpt"),
        ("ckpt", None, "ckpt"),
        # A trailing dot must not become `foo..md`.
        ("foo.", "x.md", "foo.md"),
    ],
)
def test_name_with_extension(name: str, path: str | None, expected: str) -> None:
    assert name_with_extension(name, path) == expected


def test_name_with_extension_is_idempotent() -> None:
    """Both the CLI door and the SDK door apply it, and a CLI upload passes
    through both. Re-applying must not produce `ckpt.pt.pt`."""
    once = name_with_extension("ckpt", "ckpt-4000.pt")
    assert name_with_extension(once, "ckpt-4000.pt") == once == "ckpt.pt"


def _file(tmp_path, name: str, body: bytes = b"# hello\n") -> str:
    p = tmp_path / name
    p.write_bytes(body)
    return str(p)


def test_log_artifact_stores_the_extension(app, tmp_path) -> None:
    """`run.log_artifact("ckpt", path=...)` is the shape the skill documents."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    Run(client, {"id": run_id}).log_artifact("ckpt", path=_file(tmp_path, "ckpt-4000.pt"))
    client.close()

    names = [row["name"] for rows in app.artifacts.values() for row in rows]
    assert "ckpt.pt" in names, names


def test_a_path_reference_keeps_the_extension_too(app, tmp_path) -> None:
    """A reference records WHERE the bytes are, but it still shows up in the file
    tree under `name` -- so it loses the extension the same way."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    Run(client, {"id": run_id}).log_artifact(
        "big-ckpt", path=_file(tmp_path, "shard-0.safetensors"), reference=True
    )
    client.close()

    names = [row["name"] for rows in app.artifacts.values() for row in rows]
    assert "big-ckpt.safetensors" in names, names


def test_upload_file_stores_the_extension(app, tmp_path) -> None:
    """The non-run anchors (project/experiment/workspace/Shared) go through
    `Client.upload_file`, not `Run.log_artifact` -- a survey or spec uploaded to a
    project is exactly the case the dashboard could not preview."""
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    project = client.create_project("p", kind="research")
    client.upload_file(
        Anchor.PROJECT,
        project["id"],
        "atomworks-study-README",
        _file(tmp_path, "study.md"),
    )
    client.close()

    names = [row["name"] for rows in app.artifacts.values() for row in rows]
    assert "atomworks-study-README.md" in names, names


def test_resolve_artifact_finds_the_repaired_name(app, tmp_path) -> None:
    """The other half of the repair: a script that logs `"ckpt"` and later asks for
    `"ckpt"` must still find it, even though it is stored as `ckpt.pt`."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    run = Run(client, {"id": run_id})
    run.log_artifact("ckpt", path=_file(tmp_path, "ckpt-4000.pt"))

    resolved = run.resolve_artifact("ckpt")
    client.close()
    assert resolved is not None, "the stem fallback did not fire"
    assert resolved["name"] == "ckpt.pt"


def test_resolve_artifact_prefers_an_exact_name(app, tmp_path) -> None:
    """The fallback must not shadow a real artifact literally named `ckpt`."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    run = Run(client, {"id": run_id})
    run.log_artifact("ckpt", path=_file(tmp_path, "ckpt-4000.pt"))
    run.log_artifact("ckpt", uri="s3://bucket/ckpt")  # no path -> stored bare

    resolved = run.resolve_artifact("ckpt")
    client.close()
    assert resolved is not None and resolved["name"] == "ckpt"


def test_resolve_artifact_still_misses_an_unrelated_name(app, tmp_path) -> None:
    """`ckpt-4000.pt` is not `ckpt` with an extension -- the fallback matches ONE
    extension appended, not any name that happens to share a prefix."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox")
    run = Run(client, {"id": run_id})
    run.log_artifact("ckpt-4000.pt", path=_file(tmp_path, "ckpt-4000.pt"))

    resolved = run.resolve_artifact("ckpt")
    client.close()
    assert resolved is None
