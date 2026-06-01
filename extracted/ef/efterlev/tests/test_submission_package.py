"""Tests for `efterlev.primitives.submission.package` — submission bundling."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from efterlev.primitives.submission import build_submission


def _seed_artifacts(root: Path, *, include: set[str] | None = None) -> None:
    """Create fake artifacts in the workspace at the expected paths.

    `include` is the subset to create; None = all of them.
    """
    include = (
        include
        if include is not None
        else {
            "attestation",
            "poam_md",
            "oscal_poam",
            "oscal_cd",
            "gap_html",
            "doc_html",
            "manifest",
        }
    )
    reports = root / ".efterlev" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "poam").mkdir(exist_ok=True)
    (reports / "oscal").mkdir(exist_ok=True)
    (root / ".efterlev" / "manifests").mkdir(exist_ok=True)

    if "attestation" in include:
        (reports / "attestation-20260516.json").write_text('{"frmr": "yes"}', encoding="utf-8")
    if "poam_md" in include:
        (reports / "poam" / "poam-20260516.md").write_text("# POA&M\n", encoding="utf-8")
    if "oscal_poam" in include:
        (reports / "oscal" / "poam-20260516.json").write_text('{"oscal": "poam"}', encoding="utf-8")
    if "oscal_cd" in include:
        (reports / "oscal" / "component-definition-20260516.json").write_text(
            '{"oscal": "cd"}', encoding="utf-8"
        )
    if "gap_html" in include:
        (reports / "gap-20260516.html").write_text("<html>gap</html>", encoding="utf-8")
    if "doc_html" in include:
        (reports / "documentation-20260516.html").write_text("<html>doc</html>", encoding="utf-8")
    if "manifest" in include:
        (root / ".efterlev" / "manifests" / "ksi-afr-per.yml").write_text(
            "ksi_id: KSI-AFR-PER\n", encoding="utf-8"
        )


def test_full_artifact_set_produces_archive(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    result = build_submission(tmp_path)
    assert result.is_archive is True
    assert result.output_path.exists()
    assert result.output_path.suffix == ".zip"
    assert len(result.artifacts) == 7  # 6 reports + 1 manifest
    assert result.missing == []


def test_archive_contains_readme_and_index(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    result = build_submission(tmp_path)
    with zipfile.ZipFile(result.output_path) as z:
        names = z.namelist()
        assert "README.md" in names
        assert "index.json" in names
        # index.json is parsable JSON
        idx = json.loads(z.read("index.json"))
        assert idx["tool"] == "efterlev"
        assert len(idx["artifacts"]) == 7


def test_missing_artifacts_listed_not_fatal(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path, include={"poam_md", "manifest"})
    result = build_submission(tmp_path)
    # Should still build the package with what's available.
    assert result.is_archive is True
    assert result.output_path.exists()
    # Missing list should include the 3 things we skipped.
    assert any("FRMR attestation" in m for m in result.missing)
    assert any("OSCAL POA&M" in m for m in result.missing)


def test_no_archive_writes_directory(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    result = build_submission(tmp_path, archive=False)
    assert result.is_archive is False
    assert result.output_path.is_dir()
    assert (result.output_path / "README.md").is_file()
    assert (result.output_path / "index.json").is_file()
    assert (result.output_path / "attestation" / "frmr-attestation.json").is_file()
    assert (result.output_path / "manifests" / "ksi-afr-per.yml").is_file()


def test_output_path_override_honored(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    custom = tmp_path / "custom-name.zip"
    result = build_submission(tmp_path, output=custom)
    assert result.output_path == custom
    assert custom.exists()


def test_archive_picks_latest_when_multiple_versions_exist(tmp_path: Path) -> None:
    """If poam-old.md and poam-new.md both exist, only the latest goes in."""
    _seed_artifacts(tmp_path)
    poam_dir = tmp_path / ".efterlev" / "reports" / "poam"
    # Add an OLDER poam (touch with older mtime).
    older = poam_dir / "poam-20260101.md"
    older.write_text("# old POA&M\n", encoding="utf-8")
    import os

    # Mtime in the past
    os.utime(older, (1_700_000_000, 1_700_000_000))
    result = build_submission(tmp_path)
    with zipfile.ZipFile(result.output_path) as z:
        poam_body = z.read("poam/poam.md").decode("utf-8")
    assert "# POA&M" in poam_body  # the newer one
    assert "old" not in poam_body


def test_sha256_recorded_per_artifact(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    result = build_submission(tmp_path)
    for a in result.artifacts:
        assert len(a.sha256) == 64  # hex sha256
        assert a.size_bytes > 0


def test_package_version_string_in_readme(tmp_path: Path) -> None:
    _seed_artifacts(tmp_path)
    result = build_submission(tmp_path, package_version="v3.14")
    with zipfile.ZipFile(result.output_path) as z:
        readme = z.read("README.md").decode("utf-8")
    assert "v3.14" in readme
    assert result.package_version == "v3.14"


def test_empty_workspace_produces_minimal_package(tmp_path: Path) -> None:
    """Even with NO artifacts, build_submission should produce a (sparse) package."""
    (tmp_path / ".efterlev").mkdir()
    result = build_submission(tmp_path)
    assert result.is_archive is True
    assert result.output_path.exists()
    assert result.artifacts == []
    assert len(result.missing) >= 4  # at least the 4 main artifact types
    # README should still exist.
    with zipfile.ZipFile(result.output_path) as z:
        readme = z.read("README.md").decode("utf-8")
    assert "Missing pieces" in readme


def _seed_artifacts_in_new_location(root: Path) -> None:
    """v0.1.161 / #366: seed artifacts at the NEW v0.1.160+ visible
    location (`efterlev-out/reports/`) instead of the legacy hidden
    `.efterlev/reports/`. Manifests stay at `.efterlev/manifests/` —
    they're customer-authored input, not output.
    """
    new_reports = root / "efterlev-out" / "reports"
    new_reports.mkdir(parents=True, exist_ok=True)
    (new_reports / "poam").mkdir(exist_ok=True)
    (new_reports / "oscal").mkdir(exist_ok=True)
    (root / ".efterlev" / "manifests").mkdir(parents=True, exist_ok=True)

    (new_reports / "attestation-20260516.json").write_text('{"frmr": "yes"}', encoding="utf-8")
    (new_reports / "poam" / "poam-20260516.md").write_text("# POA&M\n", encoding="utf-8")
    (new_reports / "oscal" / "poam-20260516.json").write_text('{"oscal": "poam"}', encoding="utf-8")
    (new_reports / "oscal" / "component-definition-20260516.json").write_text(
        '{"oscal": "cd"}', encoding="utf-8"
    )
    (new_reports / "gap-20260516.html").write_text("<html>gap</html>", encoding="utf-8")
    (new_reports / "documentation-20260516.html").write_text("<html>doc</html>", encoding="utf-8")
    (root / ".efterlev" / "manifests" / "ksi-afr-per.yml").write_text(
        "ksi_id: KSI-AFR-PER\n", encoding="utf-8"
    )


def test_build_submission_reads_artifacts_from_new_location_v0_1_161(tmp_path: Path) -> None:
    """v0.1.161 / #366 SHOWSTOPPER FIX: v0.1.160 moved writes to
    `efterlev-out/reports/` but the submission package collector still
    hardcoded `.efterlev/reports/` on the read side. Fresh-install
    customers (the modal new user) produced an empty 3PAO zip because
    every artifact landed in the new location while the collector
    looked in the old one. This regression test seeds artifacts at the
    NEW location and confirms they all appear in the package.
    """
    _seed_artifacts_in_new_location(tmp_path)
    result = build_submission(tmp_path)
    assert result.missing == [], f"expected no missing artifacts; got {result.missing}"
    # 6 reports + 1 manifest = 7 entries in the package.
    assert len(result.artifacts) == 7
    archive_paths = {a.archive_path for a in result.artifacts}
    assert "attestation/frmr-attestation.json" in archive_paths
    assert "poam/poam.md" in archive_paths
    assert "oscal/poam.json" in archive_paths
    assert "oscal/component-definition.json" in archive_paths
    assert "reports/gap-report.html" in archive_paths
    assert "reports/documentation.html" in archive_paths


def test_build_submission_prefers_newer_artifact_across_new_and_legacy_dirs(
    tmp_path: Path,
) -> None:
    """When BOTH locations have an artifact of the same kind, the
    collector picks the newest by mtime — the v0.1.160 path transition
    is transparent. Customers don't need to `mv .efterlev/reports
    efterlev-out/reports` to get correct submission contents.
    """
    import os

    # Seed both: an OLD attestation in the legacy location and a NEWER
    # attestation in the new location. Newer should win.
    legacy = tmp_path / ".efterlev" / "reports"
    new = tmp_path / "efterlev-out" / "reports"
    legacy.mkdir(parents=True)
    new.mkdir(parents=True)
    (legacy / "attestation-old.json").write_text('{"vintage": "legacy"}', encoding="utf-8")
    (new / "attestation-new.json").write_text('{"vintage": "new"}', encoding="utf-8")
    os.utime(legacy / "attestation-old.json", (1735689600, 1735689600))  # 2025-01-01
    os.utime(new / "attestation-new.json", (1747570800, 1747570800))  # 2025-05-18

    result = build_submission(tmp_path)
    attestations = [a for a in result.artifacts if "attestation/" in a.archive_path]
    assert len(attestations) == 1
    assert "efterlev-out" in str(attestations[0].source_path), (
        f"expected newer attestation from efterlev-out/ to win; "
        f"got source_path={attestations[0].source_path}"
    )


def test_build_submission_falls_back_to_legacy_when_only_legacy_exists(tmp_path: Path) -> None:
    """Upgraded customers who haven't yet run anything on v0.1.160+ have
    artifacts only in `.efterlev/reports/`. The collector must still find
    them so the upgrade doesn't silently degrade the submission package.
    """
    _seed_artifacts(tmp_path)  # this seeds the OLD location
    result = build_submission(tmp_path)
    assert result.missing == [], (
        f"legacy-only workspace should not show missing; got {result.missing}"
    )
    assert len(result.artifacts) == 7
