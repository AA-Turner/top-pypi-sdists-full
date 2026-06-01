"""Smoke tests that every `evals/fixtures/<id>/` parses cleanly.

Catches the regression class "vendored upstream Terraform updated
and now efterlev's HCL parser chokes on a new syntax form". Cheap
(no LLM calls) — runs on every PR alongside the rest of pytest.
Only the parse + GROUND_TRUTH-shape contracts are checked; the
quality-evaluation work happens via `python -m evals run`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from efterlev.cloudformation import parse_cfn_file
from efterlev.terraform import parse_terraform_file

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "evals" / "fixtures"


def _fixture_dirs() -> list[Path]:
    """Every directory under `evals/fixtures/` that has both an
    `infra/` subdir and a `GROUND_TRUTH.yaml`."""
    if not FIXTURES_DIR.is_dir():
        return []
    return [
        d
        for d in sorted(FIXTURES_DIR.iterdir())
        if d.is_dir() and (d / "infra").is_dir() and (d / "GROUND_TRUTH.yaml").is_file()
    ]


def _terraform_fixture_dirs() -> list[Path]:
    """Fixtures that contain `.tf` files (Terraform-shaped)."""
    return [d for d in _fixture_dirs() if any((d / "infra").rglob("*.tf"))]


def _cfn_fixture_dirs() -> list[Path]:
    """Fixtures that contain CFN templates (`.yaml`/`.yml`/`.json` with
    `Resources:` or `AWSTemplateFormatVersion`)."""
    out: list[Path] = []
    for d in _fixture_dirs():
        candidates = (
            list((d / "infra").rglob("*.yaml"))
            + list((d / "infra").rglob("*.yml"))
            + list((d / "infra").rglob("*.json"))
        )
        for c in candidates:
            try:
                # Cheap content-sniff via the parser itself — empty list
                # means non-CFN. Catches all the LICENSE.txt-style files
                # that should NOT be classified as CFN.
                if parse_cfn_file(c):
                    out.append(d)
                    break
            except Exception:
                continue
    return out


@pytest.mark.parametrize("fixture_dir", _terraform_fixture_dirs(), ids=lambda d: d.name)
def test_fixture_terraform_parses(fixture_dir: Path) -> None:
    """Every `.tf` file under the fixture's `infra/` parses without error.

    A parse failure means efterlev's HCL parser can't read the file —
    which means a real-customer scan against a similar-shape repo would
    silently lose detector coverage. v0.1.5+ surfaces parse failures via
    the post-scan note; this test catches them at PR time.

    Parametrized only over Terraform-shaped fixtures (CFN fixtures get
    their own test below).
    """
    tf_files = sorted((fixture_dir / "infra").rglob("*.tf"))
    assert tf_files, f"{fixture_dir.name}: no .tf files under infra/ — fixture is malformed"
    for tf in tf_files:
        # Don't assert on the contents; just that the parser doesn't
        # raise. Detectors run separately and are tested per-detector.
        # Each fixture's scan-output snapshot lives under evals/results/.
        parse_terraform_file(tf)


@pytest.mark.parametrize("fixture_dir", _cfn_fixture_dirs(), ids=lambda d: d.name)
def test_fixture_cloudformation_parses(fixture_dir: Path) -> None:
    """Every CFN-shaped `.yaml`/`.yml`/`.json` file parses without error.

    Tier 5 #1 PR β v0.1.72 — companion to the Terraform parse test for
    CFN fixtures. Catches the regression class "vendored upstream CFN
    template updated and now efterlev's CFN parser chokes on a new
    intrinsic function or syntax form".
    """
    candidates = (
        list((fixture_dir / "infra").rglob("*.yaml"))
        + list((fixture_dir / "infra").rglob("*.yml"))
        + list((fixture_dir / "infra").rglob("*.json"))
    )
    cfn_files = []
    for c in candidates:
        # Round-trip through the parser; empty list means content-sniff
        # found no `Resources:` (e.g. a LICENSE in YAML form, or a
        # non-template config). The parser raises on actual broken YAML.
        if parse_cfn_file(c):
            cfn_files.append(c)
    assert cfn_files, (
        f"{fixture_dir.name}: no CFN templates under infra/ — fixture is malformed "
        f"(scanned {len(candidates)} YAML/JSON files)"
    )


@pytest.mark.parametrize("fixture_dir", _fixture_dirs(), ids=lambda d: d.name)
def test_fixture_ground_truth_yaml_well_formed(fixture_dir: Path) -> None:
    """`GROUND_TRUTH.yaml` carries the required scaffolding fields.

    Per `GROUND_TRUTH_FORMAT.md`: `fixture_id`, `description`,
    `authored_by`, `authored_at`, `revision`, `frmr_version`,
    `expected_classifications` (may be empty in Phase 2 lite stubs).
    """
    gt_path = fixture_dir / "GROUND_TRUTH.yaml"
    data = yaml.safe_load(gt_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{gt_path}: top level must be a YAML mapping"

    required = {
        "fixture_id",
        "description",
        "authored_by",
        "authored_at",
        "revision",
        "frmr_version",
        "expected_classifications",
    }
    missing = required - data.keys()
    assert not missing, f"{gt_path}: missing required fields: {sorted(missing)}"

    assert data["fixture_id"] == fixture_dir.name, (
        f"{gt_path}: fixture_id `{data['fixture_id']}` must match directory name "
        f"`{fixture_dir.name}`"
    )

    # Phase 2 lite stubs are allowed to ship with empty
    # expected_classifications — the harness's "skip unlabeled" discipline
    # handles that. But the field MUST exist as a mapping.
    ec = data["expected_classifications"]
    assert ec is None or isinstance(ec, dict), (
        f"{gt_path}: expected_classifications must be a mapping (or null)"
    )
