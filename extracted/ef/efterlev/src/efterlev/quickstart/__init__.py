"""`efterlev quickstart` — one-command activation demo (Tier 1 #1, v0.1.18).

Lays down a bundled synthetic Terraform + Evidence Manifest fixture in
a temp workspace under the platform-appropriate cache dir, runs
init → scan → agent gap → agent document end-to-end against it, prints
a 5-line summary, and points the user at their own repo for the next
step. Designed for the ICP A day-one experience: install via pipx, run
one command, see real evidence + (with API key) AI-driven KSI
classification + draft attestation in 60-180 seconds.

The bundled fixture is the same one `scripts/e2e_smoke.py` uses for
CI smoke testing — `scripts/e2e_smoke.py` imports `FIXTURE` and
`REMEDIATE_KSI` from this module so both consumers share the same
source. If the fixture grows for new detector coverage in CI,
quickstart benefits automatically.

Graceful no-key degradation: if `ANTHROPIC_API_KEY` is unset, the
deterministic phases (init + scan) still run and produce real evidence;
the agent stages skip with a clear "set the key and re-run" hint. The
user gets actionable output on the no-key path rather than a stack
trace asking for credentials they don't have a console.anthropic.com
account for yet.

See DECISIONS 2026-05-06 "Tier 1 #1 design: efterlev quickstart" for
the design rationale and alternatives considered.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import platformdirs

# ---------- bundled fixture ----------
# Source of truth for both `efterlev quickstart` and CI's
# `scripts/e2e_smoke.py`. If you grow this for new detector coverage,
# both consumers pick it up automatically.

FIXTURE: dict[str, str] = {
    # Encrypted S3 bucket — should match encryption_s3_at_rest detector.
    "infra/s3_encrypted.tf": """\
resource "aws_s3_bucket" "reports" {
  bucket = "quarterly-reports"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
""",
    # Plain S3 bucket — should NOT match, exercising the negative path.
    "infra/s3_plain.tf": """\
resource "aws_s3_bucket" "public_assets" {
  bucket = "public-assets"
}
""",
    # TLS 1.2+ listener — should match tls_on_lb_listeners AND
    # fips_ssl_policies_on_lb_listeners.
    "infra/lb_tls.tf": """\
resource "aws_lb_listener" "https" {
  load_balancer_arn = "arn:aws:elasticloadbalancing:us-east-1:123:loadbalancer/app/x"
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = "arn:aws:acm:us-east-1:123:certificate/abc-123"

  default_action {
    type             = "forward"
    target_group_arn = "arn:aws:elasticloadbalancing:us-east-1:123:targetgroup/app/x"
  }
}
""",
    # Plain HTTP listener — should NOT match (gives the remediation step
    # something real to propose a diff for).
    "infra/lb_http.tf": """\
resource "aws_lb_listener" "http" {
  load_balancer_arn = "arn:aws:elasticloadbalancing:us-east-1:123:loadbalancer/app/x"
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = "arn:aws:elasticloadbalancing:us-east-1:123:targetgroup/app/x"
  }
}
""",
    # Multi-region CloudTrail with validation enabled — should match.
    "infra/cloudtrail.tf": """\
resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name                = "audit-logs-bucket"
  is_multi_region_trail         = true
  include_global_service_events = true
  enable_log_file_validation    = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
}
""",
    # RDS with backup retention AND storage encryption — should match
    # backup_retention_configured and rds_encryption_at_rest.
    "infra/rds.tf": """\
resource "aws_db_instance" "primary" {
  identifier              = "app-primary"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  backup_retention_period = 14
  skip_final_snapshot     = false
  storage_encrypted       = true
  kms_key_id              = "arn:aws:kms:us-east-1:123:key/abc-123"
}
""",
    # IAM policy WITH MFA gate — heredoc-style literal JSON, per the
    # existing fixture convention. `jsonencode(...)` wrapping becomes
    # unparseable by python-hcl2's follow-through; a heredoc with literal
    # JSON is what the mfa_required_on_iam_policies detector expects.
    "infra/iam_mfa.tf": """\
resource "aws_iam_policy" "admin_with_mfa" {
  name = "admin-with-mfa"
  policy = <<-EOT
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "*",
          "Resource": "*",
          "Condition": {
            "Bool": {"aws:MultiFactorAuthPresent": "true"}
          }
        }
      ]
    }
  EOT
}
""",
    # IAM policy WITHOUT MFA gate — also heredoc-style literal JSON.
    "infra/iam_no_mfa.tf": """\
resource "aws_iam_policy" "admin_no_mfa" {
  name = "admin-no-mfa"
  policy = <<-EOT
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "*",
          "Resource": "*"
        }
      ]
    }
  EOT
}
""",
    # S3 public-access-block covering reports bucket — all four flags true.
    # Exercises aws.s3_public_access_block.
    "infra/s3_pab.tf": """\
resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}
""",
    # Symmetric KMS CMK with rotation enabled. Exercises aws.kms_key_rotation.
    "infra/kms.tf": """\
resource "aws_kms_key" "app_data" {
  description             = "Application-data encryption key"
  enable_key_rotation     = true
  deletion_window_in_days = 30
}
""",
    # VPC flow log capturing ALL traffic to S3. Exercises
    # aws.vpc_flow_logs_enabled.
    "infra/flow_log.tf": """\
resource "aws_flow_log" "main" {
  vpc_id               = "vpc-0abc123"
  traffic_type         = "ALL"
  log_destination_type = "s3"
  log_destination      = "arn:aws:s3:::flow-logs-bucket"
}
""",
    # Account-level IAM password policy meeting the FedRAMP Moderate
    # baseline. Exercises aws.iam_password_policy.
    "infra/password_policy.tf": """\
resource "aws_iam_account_password_policy" "strict" {
  minimum_password_length      = 14
  require_uppercase_characters = true
  require_lowercase_characters = true
  require_numbers              = true
  require_symbols              = true
  max_password_age             = 60
  password_reuse_prevention    = 24
}
""",
    # Evidence Manifest for KSI-AFR-FSI (FedRAMP Security Inbox) — a
    # KSI with no Terraform-detectable surface, covered purely by a
    # human-signed procedural attestation. next_review is set well in
    # the future relative to today (2026-04-22) so the "staleness" axis
    # does not interfere with the quality checks.
    ".efterlev/manifests/security-inbox.yml": """\
ksi: KSI-AFR-FSI
name: FedRAMP Security Inbox
evidence:
  - type: attestation
    statement: >
      security@example.com is monitored by the SOC team 24/7. The inbox is
      configured in Google Workspace with a 15-minute acknowledgment SLA
      documented in runbooks/security-inbox.md, and auto-forwards
      high-severity reports to the on-call PagerDuty rotation. Incoming
      messages are triaged into our incident management system within the
      SLA window, and a weekly audit of acknowledgment timings is reviewed
      by the security lead.
    attested_by: vp-security@example.com
    attested_at: 2026-04-15
    reviewed_at: 2026-04-15
    next_review: 2026-10-15
    supporting_docs:
      - ./policies/security-inbox-sop.pdf
      - https://wiki.example.com/soc/security-inbox
""",
}

# KSI picked for `agent remediate` — one whose v0 detector can see a gap
# (the HTTP listener) so the agent has a real Terraform surface to
# propose a diff for. KSI-SVC-SNT (Securing Network Traffic) maps to the
# `tls_on_lb_listeners` detector.
REMEDIATE_KSI = "KSI-SVC-SNT"


def write_terraform_fixture(workspace: Path) -> None:
    """Lay down the Terraform fixture files under `workspace/`.

    Writes everything EXCEPT the manifest YAML. The manifest lives under
    `.efterlev/manifests/` which `efterlev init` refuses to overwrite, so
    the manifest is laid down *after* init via `write_manifest_fixture`.
    """
    for rel, content in FIXTURE.items():
        if rel.startswith(".efterlev/"):
            continue
        dest = workspace / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")


def write_manifest_fixture(workspace: Path) -> None:
    """Lay down Evidence Manifests under `.efterlev/manifests/` post-init."""
    for rel, content in FIXTURE.items():
        if not rel.startswith(".efterlev/"):
            continue
        dest = workspace / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")


# ---------- the quickstart command ----------


def cache_root() -> Path:
    """Per-platform cache dir for quickstart workspaces.

    Linux: `~/.cache/efterlev/quickstart/`. macOS: `~/Library/Caches/
    efterlev/quickstart/`. Windows: `%LOCALAPPDATA%\\efterlev\\efterlev\\
    Cache\\quickstart\\`. Uses `platformdirs` for the right base path on
    each OS — same convention many CLIs follow (pip, uv, ruff).
    """
    return Path(platformdirs.user_cache_dir("efterlev", "efterlev")) / "quickstart"


def fresh_workspace() -> Path:
    """Create a fresh timestamped workspace under the cache dir."""
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    workspace = cache_root() / ts
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


_RESOURCE_COUNT_RE = re.compile(r"resources parsed:\s+(\d+)")
_DETECTOR_COUNT_RE = re.compile(r"^    ([a-z0-9_.]+)@[\d.]+\s+\+(\d+)", re.MULTILINE)
_EVIDENCE_COUNT_RE = re.compile(r"evidence records:\s+(\d+)")


def _parse_scan_summary(stdout: str) -> tuple[int, int, int]:
    """Extract (resources_parsed, detectors_fired, evidence_records) from scan stdout.

    Returns (0, 0, 0) on parse failure rather than raising — the
    quickstart should still complete and surface what it can. The
    real check-docs gate that catches scan-output drift is independent
    of this best-effort parser.
    """
    res = _RESOURCE_COUNT_RE.search(stdout)
    ev = _EVIDENCE_COUNT_RE.search(stdout)
    fired = sum(1 for m in _DETECTOR_COUNT_RE.finditer(stdout) if int(m.group(2)) > 0)
    return (
        int(res.group(1)) if res else 0,
        fired,
        int(ev.group(1)) if ev else 0,
    )


def _parse_gap_summary(workspace: Path) -> str | None:
    """Read the latest gap-report JSON sidecar and summarize.

    Returns a short string like "22 implemented / 18 partial / 14
    not_implemented / 6 evidence_layer_inapplicable / 0 not_applicable",
    or None if no gap report is found.
    """
    # v0.1.160 / #365: glob across new + legacy reports dirs so the
    # quickstart's gap-summary blurb works on workspaces that pre-date
    # the visible-output split.
    from efterlev.paths import iter_report_dirs

    gaps: list[Path] = []
    for d in iter_report_dirs(workspace):
        if d.is_dir():
            gaps.extend(d.glob("gap-*.json"))
    if not gaps:
        return None
    # Sort by mtime ascending so gaps[-1] is the newest.
    gaps.sort(key=lambda p: p.stat().st_mtime)
    try:
        data = json.loads(gaps[-1].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    counts: dict[str, int] = {}
    for cls in data.get("classifications", []):
        status = cls.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    if not counts:
        return None
    # Print in a stable order so the summary doesn't jitter.
    order = [
        "implemented",
        "partial",
        "not_implemented",
        "evidence_layer_inapplicable",
        "not_applicable",
    ]
    parts = [f"{counts.get(s, 0)} {s}" for s in order if s in counts]
    return " / ".join(parts)


def _stage(label: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run one stage as a subprocess; print a progress line; return the result.

    `args` is constructed from in-script literals at the call sites in
    `run_quickstart` (sys.executable + the static argv lists). No shell
    is invoked (subprocess.run with a list argv does not use shell=True),
    and no external/user/network input flows in. The semgrep audit rule
    `python.lang.security.audit.dangerous-subprocess-use-audit` is
    conservative about dynamic-args call shapes; verified safe by
    construction here. Bare `# nosemgrep` (per CLAUDE.md gotcha:
    registry-resolved rule_ids don't match short-form annotations).
    """
    print(f"  {label}", flush=True)
    return subprocess.run(args, capture_output=True, text=True, check=False)  # nosemgrep


def run_quickstart() -> int:
    """Implementation of `efterlev quickstart`. Returns exit code."""
    api_key_present = bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())
    model = os.environ.get("EFTERLEV_E2E_MODEL", "claude-sonnet-4-6").strip() or (
        "claude-sonnet-4-6"
    )

    # v0.1.84: capture run start so the end-of-quickstart cost rollup
    # only sums spend from THIS invocation. Receipts.log is append-only
    # across all efterlev invocations against the same workspace.
    quickstart_started_at = datetime.now(UTC)

    workspace = fresh_workspace()
    python = sys.executable

    # Preamble — set expectations BEFORE the user has to wait.
    print(f"Quickstart workspace: {workspace}")
    if api_key_present:
        print(f"  expected wall: ~3 min, expected cost: ~$0.30 on {model}")
    else:
        print("  ANTHROPIC_API_KEY unset — running init + scan only (no LLM cost)")
    print()

    write_terraform_fixture(workspace)

    init_args = [
        python, "-m", "efterlev", "init",
        "--target", str(workspace),
        "--baseline", "fedramp-20x-moderate",
        "--llm-backend", "anthropic",
        "--llm-model", model,
    ]  # fmt: skip
    init_proc = _stage("[1/4] efterlev init", init_args)
    if init_proc.returncode != 0:
        print(
            f"\nerror: init failed with exit code {init_proc.returncode}\n"
            f"--- stderr ---\n{init_proc.stderr}",
            file=sys.stderr,
        )
        return 1

    write_manifest_fixture(workspace)

    scan_proc = _stage(
        "[2/4] efterlev scan",
        [python, "-m", "efterlev", "scan", "--target", str(workspace)],
    )
    if scan_proc.returncode != 0:
        print(
            f"\nerror: scan failed with exit code {scan_proc.returncode}\n"
            f"--- stderr ---\n{scan_proc.stderr}",
            file=sys.stderr,
        )
        return 1
    resources, detectors_fired, evidence = _parse_scan_summary(scan_proc.stdout)

    gap_summary: str | None = None
    if api_key_present:
        gap_proc = _stage(
            "[3/4] efterlev agent gap (this is the slow one — ~2 min)",
            [python, "-m", "efterlev", "agent", "gap", "--target", str(workspace)],
        )
        if gap_proc.returncode != 0:
            print(
                f"\nerror: agent gap failed with exit code {gap_proc.returncode}\n"
                f"--- stderr ---\n{gap_proc.stderr}",
                file=sys.stderr,
            )
            return 1
        gap_summary = _parse_gap_summary(workspace)

        doc_proc = _stage(
            "[4/4] efterlev agent document",
            [python, "-m", "efterlev", "agent", "document", "--target", str(workspace)],
        )
        if doc_proc.returncode != 0:
            print(
                f"\nerror: agent document failed with exit code {doc_proc.returncode}\n"
                f"--- stderr ---\n{doc_proc.stderr}",
                file=sys.stderr,
            )
            return 1

    # 5-6 line summary.
    print()
    print("=" * 60)
    print(f"Workspace: {workspace}")
    print(
        f"Scanned: {resources} resources / {evidence} evidence records / "
        f"{detectors_fired} detectors fired"
    )
    if gap_summary is not None:
        print(f"Classified: {gap_summary} (gap report under {workspace}/efterlev-out/reports/)")
    elif api_key_present:
        print("Classified: (gap report ran but no JSON sidecar found — see logs)")
    else:
        print()
        print("Set ANTHROPIC_API_KEY and re-run to also generate:")
        print("  - KSI classifications  (Gap Agent → efterlev-out/reports/gap-<ts>.{html,json})")
        print("  - FRMR attestation drafts  (Documentation Agent → efterlev-out/reports/)")
        print(
            "  - POA&M markdown for open KSIs  "
            "(Remediation Agent → efterlev-out/reports/poam/poam-<ts>.md)"
        )
    # v0.1.84: cost rollup. Surfaces total LLM spend on the AI-on path;
    # silently skipped on the keyless path (nothing to sum).
    if api_key_present:
        from efterlev.agents.cost_summary import summarize_run_cost

        cost_line = summarize_run_cost(workspace, quickstart_started_at)
        if cost_line:
            print(f"Total: {cost_line.removeprefix('cost: ')}")

    print(
        "Try this on your own code: "
        "cd <your-repo> && efterlev init --target . && efterlev report run"
    )
    return 0
