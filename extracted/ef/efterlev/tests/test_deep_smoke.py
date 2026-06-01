"""Deterministic deep-test smoke — user-flow integration suite.

Replaces the deterministic-tier portion of the human deep-test prompt
(the section we hand to a fresh Claude Code session for an end-to-end
shakedown). The human deep-test of a v0.1.x release used to take ~30
minutes and ~$3 of LLM tokens; about 80% of what it covered is
deterministic and doesn't need an LLM tester. This module captures
that 80% as a structured pytest suite that runs in under a minute with
zero LLM cost.

What's IN scope here:
  - User flows that span multiple primitives via the CLI (init → scan
    → manifests, init refusal vs --force, broken-HCL handling, etc.).
  - Friendly-error and shadow-warning paths the human tester catches
    that unit tests can miss.
  - End-to-end shape of doctor / detectors-list / manifests-init.

What's OUT of scope (deferred to a separate `deep-agent` tier):
  - Anything that needs a real LLM call (gap, document, remediate
    agent runs against actual prompts). Those are covered by the
    existing `e2e` mark and live in `test_e2e_smoke.py`.
  - Container-level smoke (S9). Covered by `release-smoke.yml` matrix.
  - Verify-release.sh (S7). Post-tag-only; covered by triage.sh.

Why pytest instead of a bash script: pytest gives parametrize, clean
assertion failures, parallelism, and one consistent runner across both
unit and integration tiers. The bash wrapper at `scripts/deep-test.sh`
is just a one-liner so the entry point is discoverable from the repo
root.

Run via:
  pytest -m deep                  # the suite
  scripts/deep-test.sh            # convenience wrapper
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.deep

REPO_ROOT = Path(__file__).resolve().parent.parent
EFTERLEV_CMD = [sys.executable, "-m", "efterlev"]


def _run(
    args: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    expect_success: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Invoke `efterlev <args>` as a subprocess. Returns the completed
    process. On unexpected failure, raises with full stdout+stderr in
    the assertion message so a CI failure is debuggable from the log
    alone (no need to re-run locally).
    """
    proc = subprocess.run(
        EFTERLEV_CMD + args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    if expect_success and proc.returncode != 0:
        raise AssertionError(
            f"`efterlev {' '.join(args)}` exited {proc.returncode}\n"
            f"--- stdout ---\n{proc.stdout}\n"
            f"--- stderr ---\n{proc.stderr}"
        )
    return proc


def _write_terraform_fixture(target: Path) -> None:
    """Drop a minimal but realistic Terraform file in `target` so scan has
    something to chew on. Hits a couple of common detectors (S3 bucket,
    IAM policy) without depending on huge fixtures.
    """
    (target / "main.tf").write_text(
        """
terraform {
  required_version = ">= 1.5.0"
}

resource "aws_s3_bucket" "example" {
  bucket = "example-bucket-deep-smoke"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket                  = aws_s3_bucket.example.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_policy" "example" {
  name = "example-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject"]
      Resource = "arn:aws:s3:::example-bucket-deep-smoke/*"
    }]
  })
}
""".strip(),
        encoding="utf-8",
    )


# --- S1: install + version basics ----------------------------------------


def test_s1_version_flag_emits_version_line() -> None:
    """`efterlev --version` prints the package version and exits 0."""
    proc = _run(["--version"])
    from efterlev import __version__

    assert __version__ in proc.stdout, f"expected {__version__} in stdout: {proc.stdout!r}"


def test_s1_help_lists_v0_subcommands() -> None:
    """Top-level --help advertises every v0 subcommand the user is told
    to run from the README quickstart. A regression here means a docs
    example breaks for new users.
    """
    proc = _run(["--help"])
    for cmd in ("init", "scan", "agent", "doctor", "manifests", "detectors", "report"):
        assert cmd in proc.stdout, f"`{cmd}` missing from `efterlev --help`"


# --- S2: doctor end-to-end shape -----------------------------------------


def test_s2_doctor_against_uninitialized_dir_runs_clean(tmp_path: Path) -> None:
    """Doctor against an uninitialized directory must NOT crash — it's
    the first thing a confused user runs when something's off, so it
    has to be robust against the no-`.efterlev/` case. v0.1.x has hit
    this footgun more than once.
    """
    proc = _run(["doctor", "--target", str(tmp_path)], expect_success=False)
    # Doctor exits 0 (warnings, no errors) or 1 (one or more checks
    # warned/failed) — both are acceptable. What we forbid is exit 2
    # (CLI error) or a Python traceback in stderr.
    assert proc.returncode in (0, 1), f"unexpected exit {proc.returncode}: {proc.stderr}"
    assert "Traceback" not in proc.stderr, f"traceback in doctor stderr: {proc.stderr}"
    # All 7 checks must be present in the output regardless of pass/warn.
    for check in (
        "python_version",
        "install_uniqueness",
        "efterlev_dir",
        "frmr_cache",
        "anthropic_api_key",
        "bedrock_credentials",
        "boundary_declared",
    ):
        assert check in proc.stdout, f"doctor output missing check `{check}`"


# --- S3: init flow + force semantics + v0.1.39 manifests-only fix --------


def test_s3_init_against_fresh_directory(tmp_path: Path) -> None:
    """The simplest happy path: empty dir → init → expected files exist."""
    _run(["init", "--target", str(tmp_path)])
    efterlev_dir = tmp_path / ".efterlev"
    assert efterlev_dir.is_dir()
    assert (efterlev_dir / "config.toml").is_file()
    assert (efterlev_dir / "cache" / "frmr_document.json").is_file()
    assert (efterlev_dir / "manifests").is_dir()  # auto-created with README


def test_s3_init_refuses_already_initialized_without_force(tmp_path: Path) -> None:
    """Re-running init on an already-initialized workspace MUST refuse
    without `--force`. Locks the safety check that prevents accidental
    config/cache obliteration when a user types `efterlev init` twice.
    """
    _run(["init", "--target", str(tmp_path)])  # initialize once
    proc = _run(["init", "--target", str(tmp_path)], expect_success=False)
    assert proc.returncode != 0
    assert "already exists" in proc.stderr or "already exists" in proc.stdout


def test_s3_init_with_force_overwrites(tmp_path: Path) -> None:
    """`--force` must work on an already-initialized workspace."""
    _run(["init", "--target", str(tmp_path)])
    _run(["init", "--target", str(tmp_path), "--force"])  # would raise on failure


def test_s3_v0_1_39_init_succeeds_on_manifests_only_directory(tmp_path: Path) -> None:
    """The v0.1.39 fix for S3b (deep-test finding): a `.efterlev/manifests/`
    directory committed to git WITHOUT `cache/` or `config.toml` (the
    canonical pattern: manifests committed, cache gitignored) must NOT
    block init. Pre-v0.1.39 a fresh clone of a manifest-shipping repo
    forced the user to pass `--force` to bootstrap.
    """
    manifests_dir = tmp_path / ".efterlev" / "manifests"
    manifests_dir.mkdir(parents=True)
    (manifests_dir / "ksi-example.yml").write_text(
        "# customer-authored evidence manifest\n", encoding="utf-8"
    )

    _run(["init", "--target", str(tmp_path)])  # would fail pre-v0.1.39

    # User-authored content under manifests/ is preserved through init.
    preserved = (manifests_dir / "ksi-example.yml").read_text(encoding="utf-8")
    assert "customer-authored" in preserved


# --- S4: scan idempotency + broken HCL handling --------------------------


def test_s4_scan_against_real_terraform(tmp_path: Path) -> None:
    """Init + drop a tf file + scan → exit 0, evidence emitted."""
    _write_terraform_fixture(tmp_path)
    _run(["init", "--target", str(tmp_path)])
    proc = _run(["scan", "--target", str(tmp_path)])
    # Scan output is human-readable; the fixture should fire at least
    # one detector (s3 public access block is well-covered).
    assert "evidence" in proc.stdout.lower() or "detector" in proc.stdout.lower()


def test_s4_scan_is_idempotent(tmp_path: Path) -> None:
    """Running scan twice must produce equivalent evidence and not
    double-emit. A non-idempotent scan would mean each save-and-rerun
    cycle in a developer's edit loop produces a different report.
    """
    _write_terraform_fixture(tmp_path)
    _run(["init", "--target", str(tmp_path)])
    first = _run(["scan", "--target", str(tmp_path)])
    second = _run(["scan", "--target", str(tmp_path)])

    # Allow header/timing variation but require the evidence-counts line
    # (and any deterministic "N detectors fired" line) to match.
    # v0.1.155 / #360: filter out the "X re-emitted... deduped" summary
    # — it's the user-visible signal that write-time dedupe fired; the
    # detector-by-detector breakdown is what must match between runs.
    def _evidence_lines(out: str) -> list[str]:
        return [
            line.strip()
            for line in out.splitlines()
            if ("detector" in line.lower() or "evidence" in line.lower())
            and "re-emitted" not in line
            and "deduped" not in line
            and "written to" not in line
        ]

    assert _evidence_lines(first.stdout) == _evidence_lines(second.stdout), (
        f"scan output diverges on rerun:\n--- first ---\n{first.stdout}\n"
        f"--- second ---\n{second.stdout}"
    )


def test_s4_broken_hcl_emits_clean_error(tmp_path: Path) -> None:
    """Malformed Terraform should surface a helpful message — NOT a
    Python traceback. v0.1.x has had multiple HCL-error-handling
    regressions where a parse failure leaked the underlying exception
    type to stderr instead of a friendly explanation.
    """
    (tmp_path / "broken.tf").write_text(
        'resource "aws_s3_bucket" "x" { bucket = "missing-quote }', encoding="utf-8"
    )
    _run(["init", "--target", str(tmp_path)])
    proc = _run(["scan", "--target", str(tmp_path)], expect_success=False)
    # Either the scan exits non-zero with a clean error, or it skips the
    # broken file and exits 0 with a warning. Both are reasonable. What
    # we forbid is a Python traceback.
    assert "Traceback" not in proc.stderr, f"traceback in scan stderr: {proc.stderr}"


# --- S5: friendly errors at the LLM boundary (v0.1.38 fix) ---------------


def test_s5_v0_1_38_quickstart_with_invalid_api_key_friendly_error(tmp_path: Path) -> None:
    """The v0.1.38 deep-test S2 fix: a set-but-invalid `ANTHROPIC_API_KEY`
    must produce a one-line friendly message + hint, not a 600-line
    Python traceback ending in `anthropic.AuthenticationError`. Locks
    the friendly-handler chain-walk that v0.1.38 introduced.
    """
    env = {
        **os.environ,
        "HOME": str(tmp_path),  # isolate quickstart cache
        "ANTHROPIC_API_KEY": "sk-ant-not-a-real-key-deep-smoke-fixture",
    }
    proc = _run(["quickstart"], env=env, expect_success=False)
    assert proc.returncode != 0, "quickstart should fail on invalid key"
    # Friendly message present.
    assert "ANTHROPIC_API_KEY" in proc.stderr, "friendly error message missing"
    assert "401" in proc.stderr or "invalid" in proc.stderr.lower()
    # No raw SDK traceback leak.
    assert "anthropic.AuthenticationError" not in proc.stderr, (
        f"raw SDK traceback leaked:\n{proc.stderr}"
    )
    assert "Traceback (most recent call last):" not in proc.stderr, (
        f"Python traceback leaked:\n{proc.stderr}"
    )


# --- S6: manifests starter pack flow -------------------------------------


def test_s6_manifests_starter_pack_full_flow(tmp_path: Path) -> None:
    """Init → manifests init --starter-pack → 26 templates appear.

    Locks the manifest pack count + the CLI flow that ships them.
    Surfaced by the v0.1.21 + v0.1.35 manifest expansions.
    """
    _run(["init", "--target", str(tmp_path)])
    _run(["manifests", "init", "--target", str(tmp_path), "--starter-pack"])
    starter_dir = tmp_path / ".efterlev" / "manifests" / "starter-pack"
    assert starter_dir.is_dir()
    templates = sorted(p.name for p in starter_dir.glob("*.yml"))
    assert len(templates) == 26, (
        f"expected 26 starter-pack templates, found {len(templates)}: {templates}"
    )


# --- S7: detector registry shape -----------------------------------------


def test_s7_detectors_list_reports_66(tmp_path: Path) -> None:
    """`efterlev detectors list` must report exactly 66 detectors. This
    constant is also pinned at the source level by
    `tests/test_triage_constant_alignment.py`; the deep-smoke version
    locks the CLI surface end-to-end (different abstraction layer, same
    invariant).
    """
    proc = _run(["detectors", "list"])
    # The CLI surface renders the count as a literal "66" somewhere in the
    # output (header, total line, etc.). A future format change that hides
    # the count would still pass this if it's unchanged anywhere — we
    # ALSO sanity-check a few well-known detector names below.
    assert "66" in proc.stdout, (
        f"expected 66-detector count in `detectors list` output:\n{proc.stdout}"
    )
    # Sanity-check a few well-known detector names land in the output.
    for name in ("cloudtrail_audit_logging", "rpl_backup_configured"):
        assert name in proc.stdout, f"expected detector `{name}` missing from list"


# --- S8: cross-flow regression — manifests survive --force ---------------


def test_s8_force_init_preserves_manifests_directory(tmp_path: Path) -> None:
    """`init --force` must not destroy customer-authored manifests. The
    canonical workflow has the user committing `manifests/*.yml` to
    git; an `init --force` that wiped them would silently delete
    months of authored content.
    """
    _run(["init", "--target", str(tmp_path)])
    manifests_dir = tmp_path / ".efterlev" / "manifests"
    user_manifest = manifests_dir / "ksi-customer.yml"
    user_manifest.write_text("# precious customer content\n", encoding="utf-8")

    _run(["init", "--target", str(tmp_path), "--force"])

    assert user_manifest.is_file(), "init --force destroyed manifests/"
    assert "precious customer content" in user_manifest.read_text(encoding="utf-8")
