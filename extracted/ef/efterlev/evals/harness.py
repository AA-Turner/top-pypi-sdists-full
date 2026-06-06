"""Harness driver: runs the efterlev pipeline against a fixture and
collects the agent outputs needed for metric calculation.

Generalizes `scripts/e2e_smoke.py` (the existing pipeline driver) so
fixture-laydown is parameterized rather than hardcoded. The fixture
directory must follow the layout under `evals/fixtures/<id>/`:

    fixture/
      infra/                       # Terraform source (.tf files)
      .github/workflows/           # optional, for github_workflows detectors
      .efterlev/manifests/         # optional, manifest fixtures
      GROUND_TRUTH.yaml

The harness:
  1. Wipes any prior `<run-results>/<ts>/workspace/.efterlev/`.
  2. Copies the fixture's `infra/` + `.github/` to the workspace.
  3. Runs `efterlev init → scan → agent gap → agent document → poam`.
  4. Drops the fixture's `.efterlev/manifests/` into the workspace
     post-init (init refuses to overwrite -- same dance as e2e_smoke).
  5. Returns the path to the workspace so callers can read the
     emitted reports for metric computation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class RunResult:
    """Output of one harness run against one fixture."""

    workspace: Path
    timestamp: str
    init_exit: int
    scan_exit: int
    gap_exit: int
    document_exit: int
    poam_exit: int

    @property
    def all_stages_succeeded(self) -> bool:
        """True iff every pipeline stage exited 0. Metric calculation
        requires this -- partial-pipeline runs don't produce the report
        files the metrics read."""
        return all(
            code == 0
            for code in (
                self.init_exit,
                self.scan_exit,
                self.gap_exit,
                self.document_exit,
                self.poam_exit,
            )
        )


def _run_efterlev(args: list[str], cwd: Path) -> int:
    """Invoke `efterlev <args>` as a subprocess; return exit code.

    Uses `sys.executable -m efterlev` so the harness picks up the
    editable install rather than whatever `efterlev` happens to be on
    PATH. Stderr/stdout pass through to the caller's terminal so a
    failed harness run leaves diagnostic output visible.

    `args` is built from in-script literals at every caller site in
    `run_fixture()` (literal stage names + str(Path) values derived
    from the harness's own params). No shell is invoked
    (subprocess.run with a list argv does not use shell=True), no
    external/user/network input flows in. Same posture as
    `scripts/e2e_smoke.py:_stage()`. The semgrep audit rule
    `python.lang.security.audit.dangerous-subprocess-use-audit` is
    conservative about dynamic-args call shapes; verified safe by
    construction here. Bare `# nosemgrep` (per CLAUDE.md gotcha:
    registry-resolved rule_ids don't match short-form annotations).
    """
    proc = subprocess.run(  # nosemgrep
        [sys.executable, "-m", "efterlev", *args],
        cwd=str(cwd),
        check=False,
    )
    return proc.returncode


def _run_gap_with_retry(workspace: Path) -> int:
    """Run `agent gap` with one retry on failure. Returns final exit code.

    Per DECISIONS 2026-05-09 ("Per-metric noise-floor calibration;
    pipeline-reliability ceiling on Haiku 4.5 surfaces"): the gap agent
    on Haiku 4.5 hits ~21% validator-rejection rate (prompt-injection
    guard catching fabricated `sha256:...` evidence IDs, OR model-layer
    validator catching positive classifications without evidence
    citations). The validators are working as designed — fail-loud,
    fail-safe, no bad data leaks — but the wasted runs erode multi-run
    aggregates by undersampling.

    A single retry converts most stochastic Haiku rejections into
    successful runs while still catching deterministic prompt/fixture
    issues on the second failure. Doc and poam stages aren't retried
    because they don't run when gap fails (the cascade in `run_fixture`
    short-circuits them), so there are no stale reports to clean up
    between attempts.

    `max_attempts` is intentionally hardcoded at 2: the failures
    captured in the DECISIONS entry are stochastic, not infrastructural,
    so unbounded retry would mask deterministic issues without
    additional benefit.
    """
    args = ["agent", "gap", "--target", str(workspace)]
    first_exit = _run_efterlev(args, workspace)
    if first_exit == 0:
        return 0
    print(
        f"[harness] agent gap exited {first_exit}; retrying once "
        f"(typical cause: Haiku-side validator rejection -- "
        f"DECISIONS 2026-05-09)",
        file=sys.stderr,
    )
    return _run_efterlev(args, workspace)


def run_fixture(
    fixture_dir: Path,
    results_root: Path,
    *,
    llm_backend: str = "bedrock",
    llm_region: str = "us-east-1",
    llm_model: str | None = None,
) -> RunResult:
    """Run the efterlev pipeline against one fixture.

    Args:
      fixture_dir: path to `evals/fixtures/<id>/`. Must contain at
        least an `infra/` subdirectory; `.github/workflows/` and
        `.efterlev/manifests/` are optional.
      results_root: directory under which a per-run timestamped
        workspace is created. Caller (CLI / pytest) chooses this
        -- typically `evals/results/<fixture_id>/` for repeatable
        local runs or a tmp dir under pytest control for tests.
      llm_backend: "bedrock" (default), "anthropic", or "openai". The
        maintainer policy is bedrock + Haiku 4.5 (DECISIONS 2026-05-08);
        the other backends are for graduation-validation dispatches.
      llm_model: explicit model ID. None defers to a per-backend default
        (env-var indirection for bedrock; in-tree literals for the others).

    Returns:
      RunResult with the workspace path and per-stage exit codes.
    """
    if not (fixture_dir / "infra").is_dir():
        raise FileNotFoundError(f"{fixture_dir}: missing required 'infra/' subdirectory")

    # Per-backend default: literal ARN belongs to the maintainer's local env
    # for bedrock (v0.1.42-style env-var indirection); the other backends use
    # in-tree-safe public model IDs.
    if llm_model is None:
        if llm_backend == "bedrock":
            llm_model = os.environ.get(
                "EFTERLEV_TEST_BEDROCK_MODEL",
                "us.anthropic.claude-haiku-4-5-20251001-v1:0",
            )
        elif llm_backend == "openai":
            llm_model = os.environ.get("EFTERLEV_TEST_OPENAI_MODEL", "gpt-5.4")
        elif llm_backend == "bedrock_openai":
            llm_model = os.environ.get("EFTERLEV_TEST_BEDROCK_OPENAI_MODEL", "openai.gpt-5.4")
        else:  # anthropic
            llm_model = "claude-haiku-4-5"

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    workspace = results_root / timestamp / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    # Copy infra/ + (optional) .github/workflows/ into the workspace.
    # Skip .efterlev/manifests/ here -- init refuses to overwrite, so
    # the manifest copy happens post-init.
    for subdir in ("infra", ".github"):
        src = fixture_dir / subdir
        if src.is_dir():
            shutil.copytree(src, workspace / subdir)

    # Stage 1: init.
    init_args = [
        "init",
        "--target",
        str(workspace),
        "--baseline",
        "fedramp-20x-moderate",
        "--llm-backend",
        llm_backend,
        "--llm-model",
        llm_model,
    ]
    if llm_backend in ("bedrock", "bedrock_openai"):
        init_args.extend(["--llm-region", llm_region])
    init_exit = _run_efterlev(init_args, workspace)

    # Drop any manifest fixtures into place post-init.
    manifests_src = fixture_dir / ".efterlev" / "manifests"
    if init_exit == 0 and manifests_src.is_dir():
        manifests_dst = workspace / ".efterlev" / "manifests"
        manifests_dst.mkdir(parents=True, exist_ok=True)
        for item in manifests_src.iterdir():
            if item.is_file():
                shutil.copy2(item, manifests_dst / item.name)

    # Stage 2: scan. `--allow-subdir-target` because the eval harness
    # workspace lives at `evals/results/<fixture>/<ts>/workspace/`,
    # below the repo root's `.github/workflows/`. Per v0.1.59 scan
    # hard-errors on that situation by default; the harness is the
    # legitimate "deliberately fixture-only Terraform scope" case the
    # flag is for. Missed in v0.1.59's CI-compat sweep (only e2e_smoke +
    # release-smoke got the flag); fixed inline as part of v0.1.64.
    #
    # CFN scanning is default-on as of v0.1.99 (CFN graduation arc step
    # 3); no per-fixture flag dispatch needed. Pre-v0.1.99 the harness
    # appended `--allow-cfn` here for fixtures with CFN templates;
    # `_fixture_has_cfn_templates` was removed in v0.1.100 along with
    # this branching.
    scan_args = ["scan", "--target", str(workspace), "--allow-subdir-target"]
    scan_exit = _run_efterlev(scan_args, workspace) if init_exit == 0 else 1

    # Stage 3: agent gap (with one retry — see _run_gap_with_retry).
    gap_exit = _run_gap_with_retry(workspace) if scan_exit == 0 else 1

    # Stage 4: agent document.
    document_exit = (
        _run_efterlev(["agent", "document", "--target", str(workspace)], workspace)
        if gap_exit == 0
        else 1
    )

    # Stage 5: poam (skipped if document failed; metric M5 needs the
    # poam output).
    poam_exit = (
        _run_efterlev(["poam", "--target", str(workspace)], workspace) if document_exit == 0 else 1
    )

    return RunResult(
        workspace=workspace,
        timestamp=timestamp,
        init_exit=init_exit,
        scan_exit=scan_exit,
        gap_exit=gap_exit,
        document_exit=document_exit,
        poam_exit=poam_exit,
    )
