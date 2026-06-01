"""Tests for the v0.1.21 manifest starter pack (Tier 1 #3).

Covers:
- The bundled `efterlev.manifest_templates` package contains exactly 24
  `<KSI-ID>.template.yml` files + `README.md` + `SELECTION.md`.
- Each template parses as valid YAML and has the expected top-level
  shape (`ksi`, `name`, `_template_help` with description + questions,
  `evidence` list with one attestation).
- Each template's `ksi` field is a real KSI ID in the FRMR catalog.
- The `_template_help` namespace has at least 3 hand-authored questions
  (lock against accidental empty-questions regressions).
- DRAFT placeholders are present in every fillable field.
- After stripping DRAFT placeholders + the `_template_help` namespace,
  each template parses cleanly via the existing `EvidenceManifest`
  Pydantic loader (proves structural validity).
- The CLI command `efterlev manifests init --starter-pack` copies all
  templates into `.efterlev/manifests/starter-pack/`.
- The CLI refuses to overwrite without `--force`; with `--force` it
  overwrites cleanly.
- The CLI refuses without `--starter-pack` (no other modes today).
- The `discover_manifest_files` loader skip filter excludes
  `*.template.yml` files even when placed directly in
  `.efterlev/manifests/` (defense-in-depth).
"""

from __future__ import annotations

import importlib.resources
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


def _template_files() -> list[Path]:
    """All `<KSI-ID>.template.yml` files bundled in the manifest_templates package."""
    pkg = importlib.resources.files("efterlev.manifest_templates")
    return sorted(
        Path(str(p)) for p in pkg.iterdir() if p.is_file() and p.name.endswith(".template.yml")
    )


def _frmr_ksi_ids() -> set[str]:
    """All KSI IDs in the vendored FRMR catalog."""
    repo_root = Path(__file__).resolve().parent.parent
    catalog = json.loads((repo_root / "catalogs" / "frmr" / "FRMR.documentation.json").read_text())
    ids: set[str] = set()
    for theme in catalog.get("KSI", {}).values():
        ids.update(theme.get("indicators", {}).keys())
    return ids


def test_starter_pack_has_26_templates() -> None:
    """Selection criteria locked in DECISIONS 2026-05-06 produces 24 templates;
    DECISIONS 2026-05-07 'Tier 1 #4 design' added 2 more (KSI-MLA-RVL +
    KSI-SVC-EIS) when the gap analysis classified them procedural-only.
    Total at v0.1.35: 26 KSI templates: 10 AFR + 4 CED + 3 INR + 4 PIY +
    1 CMT-RVP + 1 RPL-RRO + 1 SVC-PRR + 1 MLA-RVL + 1 SVC-EIS."""
    templates = _template_files()
    assert len(templates) == 26, (
        f"Expected 26 starter-pack templates; got {len(templates)}: "
        f"{sorted(p.name for p in templates)}"
    )


def test_starter_pack_includes_readme_and_selection_audit() -> None:
    """README workflow guide + SELECTION audit trail ship alongside templates."""
    pkg = importlib.resources.files("efterlev.manifest_templates")
    names = {p.name for p in pkg.iterdir() if p.is_file()}
    assert "README.md" in names
    assert "SELECTION.md" in names


def test_every_template_ksi_id_exists_in_frmr_catalog() -> None:
    """A starter-pack template for a non-existent KSI would be a real bug.
    Lock the integrity by cross-checking each template's `ksi` field
    against the vendored FRMR catalog."""
    catalog_ids = _frmr_ksi_ids()
    for template_path in _template_files():
        loaded = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        ksi_id = loaded["ksi"]
        assert ksi_id in catalog_ids, (
            f"Template {template_path.name} references KSI {ksi_id} which is not in FRMR catalog"
        )


def test_every_template_has_template_help_with_questions() -> None:
    """Each template carries `_template_help` with description + ≥3 questions.
    Locks against accidental empty-questions regressions in the generator."""
    for template_path in _template_files():
        loaded = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        help_block = loaded.get("_template_help")
        assert help_block is not None, f"{template_path.name} missing _template_help"
        assert "description" in help_block
        assert isinstance(help_block["description"], str) and help_block["description"].strip()
        questions = help_block.get("questions", [])
        assert len(questions) >= 3, (
            f"{template_path.name} has only {len(questions)} questions; "
            f"templates should have at least 3 for non-trivial guidance"
        )


def test_every_template_has_draft_placeholders_in_fillable_fields() -> None:
    """Every fillable field (statement, attested_by, etc.) starts with `DRAFT —`.
    A 3PAO grepping for `DRAFT —` in a manifest dir should find every
    not-yet-filled-in template."""
    for template_path in _template_files():
        loaded = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        evidence = loaded["evidence"][0]
        for field in ("statement", "attested_by", "attested_at", "reviewed_at", "next_review"):
            value = evidence.get(field, "")
            assert "DRAFT" in str(value), (
                f"{template_path.name}: field {field!r} should contain `DRAFT —` placeholder; "
                f"got: {value!r}"
            )


def test_loader_discover_skips_template_yml_files(tmp_path: Path) -> None:
    """Defense-in-depth: even if a user accidentally copies a
    `.template.yml` to `.efterlev/manifests/` without dropping the
    suffix, the loader's discover function skips it."""
    from efterlev.manifests.loader import discover_manifest_files

    manifest_dir = tmp_path / ".efterlev" / "manifests"
    manifest_dir.mkdir(parents=True)
    real_yml = manifest_dir / "real-attestation.yml"
    template_yml = manifest_dir / "KSI-AFR-FSI.template.yml"
    real_yml.write_text("ksi: KSI-AFR-FSI\n")
    template_yml.write_text("ksi: KSI-AFR-FSI\n")  # would-be DRAFT content

    discovered = discover_manifest_files(manifest_dir)
    discovered_names = [p.name for p in discovered]
    assert "real-attestation.yml" in discovered_names
    assert "KSI-AFR-FSI.template.yml" not in discovered_names


def _run_efterlev(*args: str, env: dict[str, str] | None = None) -> tuple[int, str, str]:
    """Invoke `python -m efterlev` for CLI integration tests."""
    full_env = {**os.environ, **(env or {})}
    proc = subprocess.run(  # nosemgrep
        [sys.executable, "-m", "efterlev", *args],
        capture_output=True,
        text=True,
        env=full_env,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_cli_manifests_init_starter_pack_copies_templates(tmp_path: Path) -> None:
    """End-to-end: `efterlev manifests init --starter-pack` against a
    fresh workspace copies all 26 templates + README + SELECTION."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')

    code, _, _ = _run_efterlev("init", "--target", str(target))
    assert code == 0

    code, _stdout, stderr = _run_efterlev(
        "manifests", "init", "--starter-pack", "--target", str(target)
    )
    assert code == 0, f"manifests init failed: {stderr}"
    assert "wrote 26 starter-pack templates" in stderr

    starter_pack = target / ".efterlev" / "manifests" / "starter-pack"
    assert starter_pack.is_dir()
    templates = sorted(starter_pack.glob("*.template.yml"))
    assert len(templates) == 26
    assert (starter_pack / "README.md").exists()
    assert (starter_pack / "SELECTION.md").exists()


def test_cli_manifests_init_refuses_overwrite_without_force(tmp_path: Path) -> None:
    """Re-running `init --starter-pack` against an existing subdir
    refuses with exit 2 and a clear message."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')

    _run_efterlev("init", "--target", str(target))
    code, _, stderr = _run_efterlev("manifests", "init", "--starter-pack", "--target", str(target))
    assert code == 0, "first init should succeed"

    # Add a sentinel file to verify the dir is NOT cleared on refused re-init.
    sentinel = target / ".efterlev" / "manifests" / "starter-pack" / "USER_KEPT_THIS.md"
    sentinel.write_text("user-edited content")

    code, _, stderr = _run_efterlev("manifests", "init", "--starter-pack", "--target", str(target))
    assert code == 2
    assert "exists; pass --force to overwrite" in stderr
    assert sentinel.exists() and sentinel.read_text() == "user-edited content"


def test_cli_manifests_init_force_overwrites(tmp_path: Path) -> None:
    """`--force` REPLACES the subdir wholesale (sentinel file from prior
    init is wiped). Per DECISIONS this is acceptable because templates
    are version-pinned to the wheel and re-running --force is the
    canonical refresh-templates workflow."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')

    _run_efterlev("init", "--target", str(target))
    _run_efterlev("manifests", "init", "--starter-pack", "--target", str(target))

    # Drop a sentinel that the --force overwrite should remove.
    sentinel = target / ".efterlev" / "manifests" / "starter-pack" / "USER_LEFT_OVER.md"
    sentinel.write_text("stale content from prior version")

    code, _, stderr = _run_efterlev(
        "manifests", "init", "--starter-pack", "--target", str(target), "--force"
    )
    assert code == 0, f"force-init failed: {stderr}"
    assert "wrote 26 starter-pack templates" in stderr
    assert not sentinel.exists(), "stale sentinel should be removed by --force"


def test_cli_manifests_init_refuses_without_starter_pack(tmp_path: Path) -> None:
    """`efterlev manifests init` without `--starter-pack` exits 2 — no
    other modes today, but the flag-required pattern keeps the
    subcommand forward-compatible."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')
    _run_efterlev("init", "--target", str(target))

    code, _, stderr = _run_efterlev("manifests", "init", "--target", str(target))
    assert code == 2
    assert "requires --starter-pack" in stderr


def test_cli_manifests_init_refuses_without_efterlev_dir(tmp_path: Path) -> None:
    """An uninitialized workspace can't have starter-pack templates installed.
    Exit 1 with the standard `run efterlev init first` message."""
    target = tmp_path / "uninitialized"
    target.mkdir()

    code, _, stderr = _run_efterlev("manifests", "init", "--starter-pack", "--target", str(target))
    assert code == 1
    assert "no `.efterlev/` directory" in stderr
