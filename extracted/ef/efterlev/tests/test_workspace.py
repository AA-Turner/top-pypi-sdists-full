"""`init_workspace` end-to-end tests.

These load the real vendored catalogs (one trestle parse per test file, since
`init_workspace` doesn't currently accept a pre-loaded catalog). Kept to two
tests that exercise the happy path + the exists/force flow; CLI-level
integration tests live in `test_cli.py`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from efterlev.config import load_config
from efterlev.errors import ConfigError
from efterlev.provenance import ProvenanceStore, walk_chain
from efterlev.workspace import init_workspace


def test_init_workspace_creates_everything_a_scan_needs(tmp_path: Path) -> None:
    result = init_workspace(tmp_path, "fedramp-20x-moderate")

    assert result.efterlev_dir == tmp_path / ".efterlev"
    assert (tmp_path / ".efterlev").is_dir()
    assert (tmp_path / ".efterlev" / "config.toml").is_file()
    assert (tmp_path / ".efterlev" / "cache" / "frmr_document.json").is_file()
    assert (tmp_path / ".efterlev" / "cache" / "oscal_catalog.json").is_file()
    assert (tmp_path / ".efterlev" / "store.db").is_file()
    assert (tmp_path / ".efterlev" / "receipts.log").is_file()

    # Config round-trips to the expected baseline.
    cfg = load_config(tmp_path / ".efterlev" / "config.toml")
    assert cfg.baseline.id == "fedramp-20x-moderate"

    # Known FRMR and 800-53 shape.
    assert result.frmr_version == "0.9.43-beta"
    assert result.num_indicators == 60
    assert result.num_themes == 11
    assert result.num_controls == 324

    # The init writes a provenance load-receipt walkable via the existing
    # `efterlev provenance show` plumbing.
    with ProvenanceStore(tmp_path) as store:
        chain = walk_chain(store, result.receipt_record_id)
    assert chain.record.record_type == "evidence"
    assert chain.record.primitive == "efterlev.init@0.1.0"
    assert chain.parents == []  # raw evidence, no parents


def test_init_refuses_when_efterlev_already_exists(tmp_path: Path) -> None:
    init_workspace(tmp_path, "fedramp-20x-moderate")
    with pytest.raises(ConfigError, match="already exists"):
        init_workspace(tmp_path, "fedramp-20x-moderate")


def test_v0_1_39_init_allows_manifests_only_directory(tmp_path: Path) -> None:
    """v0.1.39 fix for S3b: a `.efterlev/manifests/` that's been committed
    to git WITHOUT cache/ or config.toml (because cache/ is gitignored)
    should not block init. Pre-v0.1.39 a fresh clone of a repo that ships
    Evidence Manifests forced the user to pass --force just to bootstrap.
    """
    efterlev_dir = tmp_path / ".efterlev"
    manifests_dir = efterlev_dir / "manifests"
    manifests_dir.mkdir(parents=True)
    (manifests_dir / "ksi-foo.yml").write_text("# evidence manifest", encoding="utf-8")
    (manifests_dir / "README.md").write_text("# manifests dir", encoding="utf-8")

    # Should NOT raise — only manifests/ is present, no init outputs.
    result = init_workspace(tmp_path, "fedramp-20x-moderate")
    assert result.efterlev_dir == efterlev_dir
    # User content under manifests/ is preserved through init.
    assert (manifests_dir / "ksi-foo.yml").read_text(encoding="utf-8") == "# evidence manifest"


def test_v0_1_39_init_still_refuses_when_cache_present(tmp_path: Path) -> None:
    """The v0.1.39 fix narrows when init refuses — but if cache/ exists
    (a real prior init), it must still refuse without --force. Lock that
    the loosening doesn't accidentally break the destructive-overwrite
    safety check.
    """
    efterlev_dir = tmp_path / ".efterlev"
    (efterlev_dir / "cache").mkdir(parents=True)
    (efterlev_dir / "manifests").mkdir(parents=True)

    with pytest.raises(ConfigError, match="already exists"):
        init_workspace(tmp_path, "fedramp-20x-moderate")


def test_init_with_force_overwrites(tmp_path: Path) -> None:
    first = init_workspace(tmp_path, "fedramp-20x-moderate")
    second = init_workspace(tmp_path, "fedramp-20x-moderate", force=True)
    # Same workspace; the two receipts are distinct records in the same store.
    assert first.receipt_record_id != second.receipt_record_id


def test_init_rejects_unsupported_baseline(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not supported at v0"):
        init_workspace(tmp_path, "fedramp-high")
