"""Regression tests for `efterlev quickstart` (Tier 1 #1, v0.1.18).

Covers:
- The no-key path runs init + scan and exits 0 with a clear hint pointing
  at ANTHROPIC_API_KEY (the deterministic activation funnel that gives
  ICP A users real value before they have a Claude account).
- The 5-line summary structure: workspace path, scan stats, no-key hint
  (or classification stats with a key — covered by the existing E2E smoke
  gate, not duplicated here), next-steps line.
- The bundled fixture's structural integrity: 13 entries, the manifest
  YAML lives under `.efterlev/manifests/`, the rest under `infra/`.
- The cache-root helper resolves to a writable, platform-appropriate path.
- The scan-output parser extracts the right summary fields.
- The shared-fixture import path: `scripts.e2e_smoke` re-exports FIXTURE
  via `efterlev.quickstart`, so a fixture grow lands in both consumers.

The with-key path is covered by `tests/test_e2e_smoke.py` against the same
fixture. Quickstart is essentially a thinner wrapper around the same CLI
stages, so duplicating the with-key test surface here would burn ~$0.30/PR
without measurable additional signal.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


def test_fixture_has_expected_shape() -> None:
    """The bundled fixture covers 12 .tf files + 1 manifest. Hardcoded
    count locks the fixture surface against accidental shrinkage; if a
    contributor grows the fixture for new detector coverage, this test
    is the sentinel that prompts updating the count + the README claim."""
    from efterlev.quickstart import FIXTURE, REMEDIATE_KSI

    tf_files = [k for k in FIXTURE if k.endswith(".tf")]
    manifest_files = [k for k in FIXTURE if k.startswith(".efterlev/manifests/")]
    assert len(tf_files) == 12, (
        f"Expected 12 .tf fixture files; got {len(tf_files)}: {sorted(tf_files)}"
    )
    assert len(manifest_files) == 1, (
        f"Expected 1 manifest fixture file; got {len(manifest_files)}: {manifest_files}"
    )
    assert REMEDIATE_KSI == "KSI-SVC-SNT", (
        "REMEDIATE_KSI should target a KSI whose detector can see a real "
        "gap in the fixture (KSI-SVC-SNT maps to tls_on_lb_listeners, which "
        "fires on infra/lb_http.tf)."
    )


def test_write_terraform_fixture_skips_manifests(tmp_path: Path) -> None:
    """Terraform fixture writer must NOT write the manifest YAML — that's
    the manifest writer's job, run after `efterlev init` carves the
    `.efterlev/manifests/` directory."""
    from efterlev.quickstart import write_terraform_fixture

    write_terraform_fixture(tmp_path)
    tf_files = list(tmp_path.rglob("*.tf"))
    assert len(tf_files) == 12, f"Expected 12 .tf files written; got {len(tf_files)}"
    assert not (tmp_path / ".efterlev").exists(), (
        "Terraform writer should not create .efterlev/ — that's `efterlev init`'s job"
    )


def test_write_manifest_fixture_only_writes_manifests(tmp_path: Path) -> None:
    """Manifest writer is a no-op for .tf files — it only writes the
    Evidence Manifest YAML under `.efterlev/manifests/`."""
    from efterlev.quickstart import write_manifest_fixture

    write_manifest_fixture(tmp_path)
    tf_files = list(tmp_path.rglob("*.tf"))
    assert tf_files == [], "Manifest writer should not write any .tf files; got " + str(tf_files)
    manifests = list((tmp_path / ".efterlev" / "manifests").glob("*.yml"))
    assert len(manifests) == 1, f"Expected 1 manifest YAML; got {len(manifests)}"


def test_cache_root_is_under_user_cache_dir() -> None:
    """`cache_root()` should resolve to the platform-appropriate user
    cache directory + `efterlev/quickstart/`. On macOS that's
    `~/Library/Caches/efterlev/quickstart/`; on Linux,
    `~/.cache/efterlev/quickstart/`. Either is acceptable; what we
    assert is the suffix and that it's a subpath of the user's HOME."""
    from efterlev.quickstart import cache_root

    root = cache_root()
    assert root.name == "quickstart"
    assert root.parent.name == "efterlev"
    home = Path.home().resolve()
    assert root.resolve().is_relative_to(home), (
        f"cache_root() {root} should be under user home {home}, not a system path"
    )


def test_parse_scan_summary_extracts_fields() -> None:
    """Smoke test for the scan-output parser. If `efterlev scan`'s stdout
    shape changes, this test is the canary."""
    from efterlev.quickstart import _parse_scan_summary

    sample = """\
Scanned /tmp/foo
  resources parsed:    12
  detectors run:       45
  manifest files:      1
  manifests loaded:    1
  evidence records:    20
    from detectors:    19
    from manifests:    1
    aws.encryption_s3_at_rest@0.1.0    +2
    aws.tls_on_lb_listeners@0.1.0    +2
    aws.kms_key_rotation@0.1.0    +1
    aws.iam_password_policy@0.1.0    +0
"""
    resources, fired, evidence = _parse_scan_summary(sample)
    assert resources == 12
    assert evidence == 20
    # Three detectors with non-zero contributions.
    assert fired == 3


def test_parse_gap_summary_returns_none_when_no_report(tmp_path: Path) -> None:
    """Quickstart's no-key path skips the agent gap stage, so
    `_parse_gap_summary` must return None (which the summary printer
    then turns into the "set ANTHROPIC_API_KEY" hint instead of
    inventing a fake count)."""
    from efterlev.quickstart import _parse_gap_summary

    assert _parse_gap_summary(tmp_path) is None


def test_e2e_smoke_imports_fixture_from_quickstart() -> None:
    """The shared-fixture refactor lands in this same v0.1.18 PR.
    `scripts/e2e_smoke.py` re-imports FIXTURE + REMEDIATE_KSI from
    `efterlev.quickstart`; this test asserts the import path holds and
    the values are object-identical (so a fixture grow lands in both
    consumers without forking)."""
    import importlib.util
    import sys as _sys

    from efterlev.quickstart import FIXTURE as Q_FIXTURE
    from efterlev.quickstart import REMEDIATE_KSI as Q_REMEDIATE_KSI

    repo_root = Path(__file__).resolve().parent.parent
    module_name = "_e2e_smoke_for_test"
    spec = importlib.util.spec_from_file_location(
        module_name, repo_root / "scripts" / "e2e_smoke.py"
    )
    assert spec is not None and spec.loader is not None
    e2e_smoke = importlib.util.module_from_spec(spec)
    # Register in sys.modules BEFORE exec_module — dataclass field
    # resolution does sys.modules lookups against the module name, which
    # would otherwise return None and crash. (Standard importlib pattern
    # per https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly)
    _sys.modules[module_name] = e2e_smoke
    try:
        spec.loader.exec_module(e2e_smoke)
        assert e2e_smoke.FIXTURE is Q_FIXTURE, (
            "scripts/e2e_smoke.py should re-export the same FIXTURE object as "
            "efterlev.quickstart, so a fixture grow lands in both consumers"
        )
        assert e2e_smoke.REMEDIATE_KSI == Q_REMEDIATE_KSI
    finally:
        del _sys.modules[module_name]


def test_quickstart_no_key_path_runs_clean(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The dominant ICP A activation case: a user runs `efterlev quickstart`
    cold, before they have a Claude account. The deterministic phases
    (init + scan) must complete and produce real evidence; the agent
    stages must skip with a clear hint.

    Pinning HOME to tmp_path keeps the test isolated from the user's
    real `~/Library/Caches/efterlev/quickstart/` so a flaky test run
    can't pollute it."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")  # also handle the empty-string case

    proc = subprocess.run(
        [sys.executable, "-m", "efterlev", "quickstart"],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "HOME": str(tmp_path), "ANTHROPIC_API_KEY": ""},
    )
    assert proc.returncode == 0, (
        f"quickstart no-key path exited {proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n"
        f"--- stderr ---\n{proc.stderr}"
    )
    # No-key preamble.
    assert "ANTHROPIC_API_KEY unset" in proc.stdout
    # Init + scan ran; agent stages did NOT.
    assert "[1/4] efterlev init" in proc.stdout
    assert "[2/4] efterlev scan" in proc.stdout
    assert "[3/4]" not in proc.stdout
    # Summary block.
    assert "Workspace:" in proc.stdout
    assert "Scanned:" in proc.stdout
    # v0.1.79: footer names the three concrete artifacts the user is
    # missing (Gap classifications, FRMR attestation drafts, POA&M
    # markdown) so the upgrade path is concrete, not vague.
    assert "Set ANTHROPIC_API_KEY" in proc.stdout
    assert "Gap Agent" in proc.stdout
    assert "POA&M" in proc.stdout
    assert "Try this on your own code" in proc.stdout
    # Workspace lives under the test-pinned HOME, not the real user cache.
    assert str(tmp_path) in proc.stdout
