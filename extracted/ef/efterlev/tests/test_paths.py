"""Catalog-path resolution and hash-verification tests."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from efterlev.errors import CatalogLoadError
from efterlev.paths import (
    EXPECTED_HASHES,
    vendored_catalogs_dir,
    verify_catalog_hashes,
)


def test_dev_install_resolves_repo_root_catalogs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EFTERLEV_CATALOGS_DIR", raising=False)
    resolved = vendored_catalogs_dir()
    # In this editable install, expect repo_root/catalogs (not site-packages).
    assert (resolved / "frmr" / "FRMR.documentation.json").is_file()
    assert (resolved / "nist" / "NIST_SP-800-53_rev5_catalog.json").is_file()


def test_env_override_is_honored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Build a minimal candidate dir with the marker file present.
    candidate = tmp_path / "my-catalogs"
    (candidate / "frmr").mkdir(parents=True)
    (candidate / "frmr" / "FRMR.documentation.json").write_text("{}")
    monkeypatch.setenv("EFTERLEV_CATALOGS_DIR", str(candidate))
    assert vendored_catalogs_dir() == candidate.resolve()


def test_env_override_rejects_missing_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("EFTERLEV_CATALOGS_DIR", str(tmp_path))
    with pytest.raises(CatalogLoadError, match="does not contain"):
        vendored_catalogs_dir()


def test_verify_catalog_hashes_passes_on_vendored_files() -> None:
    # The repo-root vendored files MUST match the pinned hashes; any drift is a
    # provenance-chain failure and should surface immediately.
    catalogs = vendored_catalogs_dir()
    verify_catalog_hashes(catalogs)  # should not raise


def test_verify_catalog_hashes_raises_on_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Build a catalog-ish dir missing one of the expected files.
    source = vendored_catalogs_dir()
    shutil.copytree(source, tmp_path / "catalogs")
    (tmp_path / "catalogs" / "frmr" / "FRMR.md").unlink()
    with pytest.raises(CatalogLoadError, match="missing"):
        verify_catalog_hashes(tmp_path / "catalogs")


def test_verify_catalog_hashes_raises_on_content_drift(tmp_path: Path) -> None:
    source = vendored_catalogs_dir()
    shutil.copytree(source, tmp_path / "catalogs")
    (tmp_path / "catalogs" / "frmr" / "FRMR.md").write_text("tampered")
    with pytest.raises(CatalogLoadError, match="SHA-256 mismatch"):
        verify_catalog_hashes(tmp_path / "catalogs")


def test_expected_hashes_cover_vendored_tree() -> None:
    # Sanity: every file EXPECTED_HASHES names actually exists in the vendored
    # catalogs directory. This catches the case where a path string in
    # EXPECTED_HASHES gets stale (different from what we ship).
    catalogs = vendored_catalogs_dir()
    for rel in EXPECTED_HASHES:
        assert (catalogs / rel).is_file(), f"expected file {rel} not in {catalogs}"


# --- Workspace output dirs (v0.1.160 / #365) ------------------------------


def test_output_root_returns_visible_dir(tmp_path: Path) -> None:
    from efterlev.paths import output_root

    assert output_root(tmp_path) == tmp_path / "efterlev-out"


def test_reports_dir_lives_under_visible_output_root(tmp_path: Path) -> None:
    from efterlev.paths import reports_dir

    assert reports_dir(tmp_path) == tmp_path / "efterlev-out" / "reports"


def test_submissions_dir_lives_under_visible_output_root(tmp_path: Path) -> None:
    from efterlev.paths import submissions_dir

    assert submissions_dir(tmp_path) == tmp_path / "efterlev-out" / "submissions"


def test_poam_dir_lives_under_reports_subdir(tmp_path: Path) -> None:
    """v0.1.6 sub-directory convention preserved across the v0.1.160 move."""
    from efterlev.paths import poam_dir

    assert poam_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "poam"


def test_oscal_dir_lives_under_reports_subdir(tmp_path: Path) -> None:
    from efterlev.paths import oscal_dir

    assert oscal_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "oscal"


def test_internal_root_returns_hidden_efterlev_dir(tmp_path: Path) -> None:
    """Internal state (cache, store, config, manifests) stays hidden."""
    from efterlev.paths import internal_root

    assert internal_root(tmp_path) == tmp_path / ".efterlev"


def test_legacy_reports_dir_returns_pre_v0_1_160_location(tmp_path: Path) -> None:
    """The legacy helper exists so READERS can surface pre-v0.1.160
    artifacts on upgraded workspaces. WRITERS always use the new path."""
    from efterlev.paths import legacy_reports_dir

    assert legacy_reports_dir(tmp_path) == tmp_path / ".efterlev" / "reports"


def test_legacy_submissions_dir_returns_pre_v0_1_160_location(tmp_path: Path) -> None:
    from efterlev.paths import legacy_submissions_dir

    assert legacy_submissions_dir(tmp_path) == tmp_path / ".efterlev" / "submissions"


def test_iter_report_dirs_returns_new_first_then_legacy(tmp_path: Path) -> None:
    """Iterator order is load-bearing: callers globbing across both
    locations rank "newest of all" by mtime, so the order needs to be
    deterministic. NEW first matches the visible-output split's intent
    (new writes preferred when both locations have a match)."""
    from efterlev.paths import iter_report_dirs

    assert iter_report_dirs(tmp_path) == [
        tmp_path / "efterlev-out" / "reports",
        tmp_path / ".efterlev" / "reports",
    ]


def test_iter_submission_dirs_returns_new_first_then_legacy(tmp_path: Path) -> None:
    from efterlev.paths import iter_submission_dirs

    assert iter_submission_dirs(tmp_path) == [
        tmp_path / "efterlev-out" / "submissions",
        tmp_path / ".efterlev" / "submissions",
    ]


def test_writer_helpers_compose_with_internal_root_as_siblings(tmp_path: Path) -> None:
    """Sanity: output_root() and internal_root() are siblings under the
    same workspace_root. Nothing in either should accidentally land
    inside the other."""
    from efterlev.paths import internal_root, output_root

    assert output_root(tmp_path).parent == internal_root(tmp_path).parent == tmp_path
    assert output_root(tmp_path).name != internal_root(tmp_path).name


def test_iter_report_dirs_lets_callers_find_legacy_artifacts(tmp_path: Path) -> None:
    """End-to-end pattern: a v0.1.160+ reader globbing across
    iter_report_dirs() finds an artifact in the legacy `.efterlev/`
    location on an upgraded workspace, so customers don't have to
    `mv .efterlev/reports efterlev-out/reports` manually."""
    from efterlev.paths import iter_report_dirs

    legacy = tmp_path / ".efterlev" / "reports"
    legacy.mkdir(parents=True)
    (legacy / "gap-20260101-000000.html").write_text("<html>legacy</html>")

    matches: list[Path] = []
    for d in iter_report_dirs(tmp_path):
        if d.is_dir():
            matches.extend(d.glob("gap-*.html"))

    assert len(matches) == 1
    assert matches[0].name == "gap-20260101-000000.html"
    assert ".efterlev" in matches[0].parts


def test_iter_report_dirs_walks_both_when_both_exist(tmp_path: Path) -> None:
    """When both NEW and LEGACY have an artifact, the iterator walks BOTH
    so downstream callers can rank by mtime themselves. The order of
    iteration is documented (NEW first), but the picking logic is the
    caller's — we don't impose "new wins" semantics, we walk both and
    let mtime decide.
    """
    import os

    from efterlev.paths import iter_report_dirs

    new = tmp_path / "efterlev-out" / "reports"
    legacy = tmp_path / ".efterlev" / "reports"
    new.mkdir(parents=True)
    legacy.mkdir(parents=True)
    new_file = new / "gap-20260518-120000.html"
    legacy_file = legacy / "gap-20260101-000000.html"
    new_file.write_text("<html>new</html>")
    legacy_file.write_text("<html>legacy</html>")
    # Set mtimes explicitly so the test doesn't depend on filesystem
    # write-ordering granularity (some filesystems give same-second
    # timestamps to back-to-back writes).
    os.utime(new_file, (1747570800, 1747570800))  # 2025-05-18T12:00:00Z
    os.utime(legacy_file, (1735689600, 1735689600))  # 2025-01-01T00:00:00Z

    matches: list[Path] = []
    for d in iter_report_dirs(tmp_path):
        if d.is_dir():
            matches.extend(d.glob("gap-*.html"))

    assert len(matches) == 2
    # With explicit mtimes, the NEW-location file is newer.
    newest = max(matches, key=lambda p: p.stat().st_mtime)
    assert "efterlev-out" in newest.parts
