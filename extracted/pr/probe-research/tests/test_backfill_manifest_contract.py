"""The manifest contract: what backfill's prompt tells an agent to WRITE must be
what `artifact add --from-manifest` READS.

The producer and the consumer were built by different lanes that never saw each
other's code. A textually clean merge does not make them agree, and the first
disagreement was invisible: rows parsed fine and landed with the wrong names.
"""

from __future__ import annotations

import re

from probe.cli import backfill_prompts as bp


def _row_keys_the_import_writes(tmp_path=None) -> set[str]:
    """The JSON keys an agent unit's manifest carries. Code writes the rows now
    (the model only adds notes), so the producer is `_write_unit_manifest`."""
    import json
    import tempfile
    from pathlib import Path

    from probe.cli import backfill_ledger, backfill_run

    root = Path(tempfile.mkdtemp())
    (root / "a.py").write_text("x = 1\n")
    unit = backfill_ledger.Unit("u", "p", ("a.py",))
    manifest = root / "work" / "u.jsonl"
    backfill_run._write_unit_manifest(root, unit, manifest, {}, {"a.py": "the entry point"})
    keys: set[str] = set()
    for line in manifest.read_text().splitlines():
        keys |= set(json.loads(line))
    assert "path" in keys and "notes" in keys, "the writer moved; this test is reading nothing"
    return keys


def test_the_prompt_only_asks_for_keys_the_reader_accepts():
    """An unknown key FAILS the row, so a prompt naming one nobody reads would
    make every unit enqueue nothing while reporting success."""
    from probe.cli.main import _MANIFEST_KEYS  # noqa: PLC0415

    assert _row_keys_the_import_writes() <= set(_MANIFEST_KEYS)


def test_an_artifact_name_defaults_to_the_relative_path_not_the_basename(tmp_path, monkeypatch):
    """`backfill.py` states the contract the dashboard depends on: the name is
    the relative path, because the folder tree is built by splitting it on '/'.
    The prompt never asks the agent for `name`, so the default IS the contract.

    Note the chdir: a manifest row's `path` resolves against the CWD, so the
    enqueue has to run with the imported folder as its working directory. That
    is not incidental -- with the wrong cwd every row fails "is not a regular
    file", which is at least loud.
    """
    from probe.cli.main import _plan_manifest_row  # noqa: PLC0415

    target = tmp_path / "michael" / "odyssey" / "config.yaml"
    target.parent.mkdir(parents=True)
    target.write_text("lr: 3e-4")
    monkeypatch.chdir(tmp_path)

    row = {"path": "michael/odyssey/config.yaml", "notes": "the odyssey config"}
    from probe.sdk.client import Anchor  # noqa: PLC0415

    planned = _plan_manifest_row(row, default_anchor=(Anchor.PROJECT, "p-1"), reference_over=10**9)
    assert planned["name"] == "michael/odyssey/config.yaml", (
        "a manifest name must keep its directories, or every import flattens to "
        "one folder and every config.yaml collides"
    )


def test_the_import_does_not_set_a_name():
    """If it ever starts to, the default above stops being load-bearing and this
    test should be revisited rather than silently kept green."""
    assert "name" not in _row_keys_the_import_writes()


def test_the_prompt_asks_for_notes_only_never_rows():
    """The upload list is code's: the model cannot drop a file by copying its
    path wrong, because it never writes one."""
    text = bp.import_unit(root="/drive", project="p", paths=["a.py"], work_dir="/tmp")
    assert "being\nimported into the project p whatever you do" in text
    assert "probe-backfill-plan note" in text
    assert "Write JSONL to" not in text and "exactly as listed" not in text


def test_an_absolute_path_still_falls_back_to_the_basename(tmp_path, monkeypatch):
    """An absolute path says where a file sits on the machine that wrote the
    manifest. That is not a name anyone wants in a dashboard, and it leaks a
    local layout into shared data."""
    from probe.cli.main import _plan_manifest_row  # noqa: PLC0415
    from probe.sdk.client import Anchor  # noqa: PLC0415

    target = tmp_path / "deep" / "shard.bin"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"x")
    planned = _plan_manifest_row(
        {"path": str(target)},
        default_anchor=(Anchor.PROJECT, "p-1"),
        reference_over=10**9,
    )
    assert planned["name"] == "shard.bin"
