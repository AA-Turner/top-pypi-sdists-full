"""`efterlev start` — pre-scan strategic walkthrough for FedRAMP 20x.

The lowest-friction Day-0 tool. Runs BEFORE a workspace exists (no
`.efterlev/` directory): it asks a handful of questions about the
customer's cloud, impact level, architecture, and existing posture,
then writes a personalized "your FedRAMP 20x path" markdown report.

This is **Stage 0** of the ISV journey (see `docs/isv-journey.md`):
"should we do this, and how?" Efterlev's core has always served
Stage 1 (engineering readiness) onward; `start` opens the front door.

## Deliberate scope

- **Orientation, not advice.** The report frames the path and points
  to the right next commands. It does not estimate timelines, quote
  costs, or guarantee outcomes — that's advisory work a tool
  shouldn't fake.
- **Qualitative, not quantitative, on KSI scope.** The report says
  *which KSI families* matter for an architecture and which are
  *often* not-applicable. It does NOT claim precise per-KSI counts —
  that's the job of `efterlev agent gap` (which classifies every KSI
  against real evidence, including not-applicable) once a workspace
  exists. Precise bulk applicability marking is a planned `efterlev
  scope` command; `start` deliberately stays qualitative so it never
  over-promises.
- **Only cites shipped commands** in its actionable next-steps. A
  Day-0 user following the report must not hit a command that doesn't
  exist yet.

## Interactive vs flag-driven

`start` works three ways:
  - `efterlev start` on a TTY → interactive prompts (override defaults)
  - `efterlev start --architecture serverless ...` → flag-driven
  - `efterlev start` in CI / non-TTY → uses defaults, prints assumptions

Every input has a sensible default, so the command always produces a
report — it never hard-errors for lack of input. The report echoes
the inputs it used so any assumed default is visible to the reader.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import typer

from efterlev.cli.first_run_wizard import is_interactive

# Marker key on the machine-readable sidecar `efterlev start --out` writes
# next to its .md report, so `efterlev init`'s wizard can pre-fill from a
# prior `start` run. The wizard scans for *.json carrying this marker.
START_SIDECAR_MARKER = "start-answers"
START_SIDECAR_VERSION = 1

CloudProvider = Literal["aws", "azure", "gcp", "other"]
AwsPartition = Literal["commercial", "govcloud"]
ImpactLevel = Literal["low", "moderate", "high"]
Architecture = Literal["serverless", "containers", "vms", "hybrid"]
ExistingPosture = Literal["none", "soc2", "iso27001", "fedramp-rev5", "other"]

# Defaults — chosen so the most common first-time ISV (AWS commercial,
# Moderate, serverless, no prior FedRAMP) gets a sensible report with
# zero flags. Every default is echoed in the report so it's never silent.
DEFAULT_CLOUD: CloudProvider = "aws"
DEFAULT_PARTITION: AwsPartition = "commercial"
DEFAULT_IMPACT: ImpactLevel = "moderate"
DEFAULT_ARCHITECTURE: Architecture = "serverless"
DEFAULT_POSTURE: ExistingPosture = "none"

DEFAULT_OUTPUT_FILENAME = "fedramp-20x-path.md"


@dataclass(frozen=True)
class StartAnswers:
    """The customer's answers — drives the personalized report."""

    cloud: CloudProvider = DEFAULT_CLOUD
    partition: AwsPartition = DEFAULT_PARTITION
    impact_level: ImpactLevel = DEFAULT_IMPACT
    architecture: Architecture = DEFAULT_ARCHITECTURE
    posture: ExistingPosture = DEFAULT_POSTURE


# Human-readable labels.
_CLOUD_LABELS: dict[str, str] = {
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "Google Cloud",
    "other": "Other / on-prem",
}
_PARTITION_LABELS: dict[str, str] = {
    "commercial": "Commercial",
    "govcloud": "GovCloud",
}
_IMPACT_LABELS: dict[str, str] = {
    "low": "Low",
    "moderate": "Moderate",
    "high": "High",
}
_ARCH_LABELS: dict[str, str] = {
    "serverless": "Serverless (Lambda / API Gateway / managed data stores)",
    "containers": "Containers (ECS / EKS / Fargate)",
    "vms": "Virtual machines (EC2 / self-managed hosts)",
    "hybrid": "Hybrid (mix of serverless, containers, and VMs)",
}
_POSTURE_LABELS: dict[str, str] = {
    "none": "None — this is our first formal compliance program",
    "soc2": "SOC 2",
    "iso27001": "ISO 27001",
    "fedramp-rev5": "FedRAMP Rev 5 (traditional process)",
    "other": "Other",
}

# Per-architecture qualitative guidance. Which KSI *families* matter
# most, and which are *often* not-applicable. Intentionally qualitative
# — `efterlev agent gap` does the real per-KSI classification.
_ARCH_GUIDANCE: dict[str, dict[str, list[str]]] = {
    "serverless": {
        "focus": [
            "IAM (least privilege, MFA, key management) — the dominant control surface",
            "Data protection (encryption at rest + in transit on managed stores)",
            "Monitoring + logging (CloudTrail, structured app logs, alerting)",
            "Network (API-level controls, WAF, private endpoints)",
            "Configuration + change management (IaC review, drift detection)",
        ],
        "often_na": [
            "Host / OS hardening — there are no servers you patch",
            "Host-based intrusion detection — managed runtime",
            "VM image / golden-AMI controls — not applicable",
        ],
    },
    "containers": {
        "focus": [
            "Container image scanning + a trusted registry",
            "Orchestration security (RBAC, network policies, pod security)",
            "IAM + workload identity (IRSA / workload identity federation)",
            "Data protection + secrets management",
            "Monitoring + logging across the cluster",
        ],
        "often_na": [
            "Full golden-AMI / VM-image controls — usually node-pool managed",
            "Some host-IDS controls — depends on whether you manage nodes",
        ],
    },
    "vms": {
        "focus": [
            "Host / OS hardening + a documented patching cadence",
            "Host-based intrusion detection + endpoint controls",
            "IAM + key management",
            "Network segmentation (security groups, NACLs, private subnets)",
            "Data protection + monitoring",
        ],
        "often_na": [
            "Few — VM-based architectures exercise most KSI families",
        ],
    },
    "hybrid": {
        "focus": [
            "Most KSI families apply across the mix",
            "Pay special attention to consistency: the same control",
            "  must hold across serverless, container, and VM tiers",
            "IAM + data protection + monitoring span all three",
        ],
        "often_na": [
            "Few — hybrid architectures exercise most KSI families",
        ],
    },
}


def render_start_report(answers: StartAnswers, *, generated_at: datetime) -> str:
    """Build the personalized 'your FedRAMP 20x path' markdown.

    Pure + deterministic given (answers, generated_at). No IO.
    """
    lines: list[str] = []
    lines.append("# Your FedRAMP 20x path")
    lines.append("")
    lines.append(
        f"Generated by `efterlev start` on {generated_at.date().isoformat()}. "
        "This is orientation, not advice — see "
        "[the ISV journey](https://github.com/efterlev/efterlev/blob/main/docs/isv-journey.md) "
        "for the full picture."
    )
    lines.append("")

    lines.extend(_render_situation(answers))
    lines.extend(_render_recommended_path(answers))
    lines.extend(_render_architecture_scope(answers))
    lines.extend(_render_journey_overview())
    lines.extend(_render_next_commands(answers))
    lines.extend(_render_caveats())

    return "\n".join(lines)


def _render_situation(answers: StartAnswers) -> list[str]:
    lines = ["## Your situation", ""]
    cloud_line = _CLOUD_LABELS[answers.cloud]
    if answers.cloud == "aws":
        cloud_line += f" ({_PARTITION_LABELS[answers.partition]})"
    lines.append(f"- **Cloud:** {cloud_line}")
    lines.append(f"- **Target impact level:** FedRAMP 20x {_IMPACT_LABELS[answers.impact_level]}")
    lines.append(f"- **Architecture:** {_ARCH_LABELS[answers.architecture]}")
    lines.append(f"- **Existing posture:** {_POSTURE_LABELS[answers.posture]}")
    lines.append("")
    return lines


def _render_recommended_path(answers: StartAnswers) -> list[str]:
    lines = ["## Recommended path", ""]

    # 20x vs Rev 5 framing.
    if answers.posture == "fedramp-rev5":
        lines.append(
            "You indicated an existing FedRAMP Rev 5 effort. FedRAMP 20x is a "
            "distinct, KSI-based path — not a migration of a Rev 5 package. If "
            "you're early in Rev 5, 20x may be a faster route for a cloud-native "
            "system; if you're far along in Rev 5, finish that. Efterlev produces "
            "20x artifacts (KSI attestations) and, as a bonus, OSCAL output that "
            "Rev 5 consumers can use."
        )
    else:
        lines.append(
            "FedRAMP 20x is the right fit for a cloud-native SaaS pursuing its "
            "first authorization — it's KSI-based and built for "
            "infrastructure-as-code shops. Efterlev is built for this path."
        )
    lines.append("")

    # Cloud-specific note.
    if answers.cloud == "aws" and answers.partition == "govcloud":
        lines.append(
            "**GovCloud note:** running in AWS GovCloud keeps your workloads "
            "inside the boundary many agencies expect. Efterlev's Bedrock "
            "backend lets you run the tool's own LLM calls inside GovCloud "
            "with no egress to anthropic.com — relevant if your build/CI must "
            "stay in-boundary."
        )
        lines.append("")
    elif answers.cloud != "aws":
        lines.append(
            "**Heads-up:** Efterlev's deepest evidence coverage today is for "
            "AWS (Terraform, CloudFormation, CDK, plus AWS-native runtime "
            "imports). It still classifies every KSI and accepts "
            "human-authored Evidence Manifests for anything the scanners can't "
            "reach, but expect to lean more on manifests on non-AWS clouds."
        )
        lines.append("")

    # Impact-level note.
    if answers.impact_level == "high":
        lines.append(
            "**High baseline:** the High impact level is the most demanding. "
            "Efterlev defaults to the Moderate baseline; confirm your agency "
            "actually requires High before scoping to it — most first-time "
            "ISVs target Moderate."
        )
        lines.append("")

    return lines


def _render_architecture_scope(answers: StartAnswers) -> list[str]:
    guidance = _ARCH_GUIDANCE[answers.architecture]
    lines = ["## What's in scope for your architecture", ""]
    lines.append(
        "FedRAMP 20x evaluates 60 Key Security Indicators (KSIs) across 11 "
        "themes. Which ones carry weight depends on how you're built. For your "
        f"**{answers.architecture}** architecture:"
    )
    lines.append("")
    lines.append("**Focus your effort here:**")
    lines.append("")
    for item in guidance["focus"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("**Often not-applicable (Efterlev will confirm per-KSI):**")
    lines.append("")
    for item in guidance["often_na"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(
        "This is a qualitative sketch. `efterlev agent gap` classifies every "
        "KSI against your real evidence — including the ones that come back "
        "*not-applicable* — so you get the precise picture once you scan."
    )
    lines.append("")
    return lines


def _render_journey_overview() -> list[str]:
    lines = ["## The journey ahead", ""]
    lines.append("FedRAMP 20x has seven stages. **You are at Stage 0.**")
    lines.append("")
    lines.append("| Stage | What happens | Where Efterlev helps |")
    lines.append("| --- | --- | --- |")
    lines.append(
        "| 0. Strategic | Decide to pursue 20x, scope the boundary | "
        "You're here — `efterlev start` |"
    )
    lines.append("| 1. Engineering | Meet the KSIs; gather evidence | Strong — the core loop |")
    lines.append(
        "| 2. 3PAO assessment | Independent assessor validates | Hands them the inspector report |"
    )
    lines.append("| 3. Submission | Assemble + submit the package | One-command package |")
    lines.append("| 4. Authorization | Agency grants the ATO | Agency-only |")
    lines.append("| 5. ConMon | Continuously re-validate | Meets the machine cadence |")
    lines.append("| 6. Incident | Follow the comms playbook | Attest the playbook exists |")
    lines.append("")
    lines.append(
        "Full detail: "
        "[the ISV journey](https://github.com/efterlev/efterlev/blob/main/docs/isv-journey.md)."
    )
    lines.append("")
    return lines


def _render_next_commands(answers: StartAnswers) -> list[str]:
    lines = ["## Your next three commands", ""]
    lines.append("Move from Stage 0 to Stage 1 — get a real picture of where you stand:")
    lines.append("")
    lines.append("```bash")
    lines.append("# 1. Install (if you haven't)")
    lines.append("pipx install efterlev")
    lines.append("")
    lines.append("# 2. Initialize a workspace for your baseline")
    init_cmd = f"efterlev init --baseline fedramp-20x-{answers.impact_level}"
    if answers.cloud == "aws" and answers.partition == "govcloud":
        init_cmd += " --llm-backend bedrock --llm-region us-gov-west-1"
    lines.append(init_cmd)
    lines.append("")
    lines.append("# 3. Run the full pipeline (scan → classify → draft → report)")
    lines.append("efterlev report run")
    lines.append("```")
    lines.append("")
    lines.append(
        "After that, `efterlev readiness --strict` gives you a per-KSI "
        "RFC-0017 pass/fail gate, and `efterlev report inspector` produces the "
        "single-page view you'll eventually hand your 3PAO."
    )
    lines.append("")
    return lines


def _render_caveats() -> list[str]:
    lines = ["## Honest caveats", ""]
    lines.append(
        "- **Efterlev is an engineering-readiness tool, not an authorization.** "
        "It produces drafts; every artifact requires human review. It does not "
        "grant ATOs and is not a 3PAO."
    )
    lines.append(
        "- **Procedural KSIs need you.** Personnel security, training, and "
        "incident-response KSIs can't be scanned from infrastructure — you'll "
        "author short Evidence Manifests for those."
    )
    lines.append(
        "- **This report is a starting sketch.** Your real posture comes from "
        "scanning your actual infrastructure, not from these answers."
    )
    lines.append("")
    return lines


# --- Interactive resolution + IO --------------------------------------


def _prompt_choice(label: str, choices: dict[str, str], default: str) -> str:
    """Prompt for one choice from a labeled set; return the chosen key.

    Re-prompts on invalid input. Empty input accepts the default.
    """
    typer.echo("")
    typer.echo(f"{label}")
    keys = list(choices.keys())
    for key in keys:
        marker = " (default)" if key == default else ""
        typer.echo(f"  {key}: {choices[key]}{marker}")
    while True:
        raw = typer.prompt("  >", default=default, show_default=False).strip().lower()
        if raw in choices:
            return raw
        typer.echo(f"  '{raw}' is not one of: {', '.join(keys)}. Try again.")


def _resolve_interactive() -> StartAnswers:
    """Walk the prompts interactively. Each prompt defaults to the
    most-common answer so a user can press Enter through the whole thing."""
    typer.echo("FedRAMP 20x readiness — pre-scan walkthrough")
    typer.echo("Press Enter to accept the default for any question.")

    cloud = _prompt_choice("Cloud provider?", _CLOUD_LABELS, DEFAULT_CLOUD)
    partition: str = DEFAULT_PARTITION
    if cloud == "aws":
        partition = _prompt_choice("AWS partition?", _PARTITION_LABELS, DEFAULT_PARTITION)
    impact = _prompt_choice("Target impact level?", _IMPACT_LABELS, DEFAULT_IMPACT)
    architecture = _prompt_choice("Architecture pattern?", _ARCH_LABELS, DEFAULT_ARCHITECTURE)
    posture = _prompt_choice("Existing compliance posture?", _POSTURE_LABELS, DEFAULT_POSTURE)
    return StartAnswers(
        cloud=cloud,  # type: ignore[arg-type]
        partition=partition,  # type: ignore[arg-type]
        impact_level=impact,  # type: ignore[arg-type]
        architecture=architecture,  # type: ignore[arg-type]
        posture=posture,  # type: ignore[arg-type]
    )


def _validate_flag(name: str, value: str | None, choices: dict[str, str], default: str) -> str:
    """Validate a flag value against its choice set; default when None."""
    if value is None:
        return default
    v = value.strip().lower()
    if v not in choices:
        valid = ", ".join(choices.keys())
        typer.echo(f"error: --{name} must be one of: {valid} (got {value!r})", err=True)
        raise typer.Exit(code=2)
    return v


def run_start(
    *,
    interactive: bool = False,
    cloud: str | None = None,
    partition: str | None = None,
    impact_level: str | None = None,
    architecture: str | None = None,
    posture: str | None = None,
    out: Path | None = None,
) -> int:
    """Resolve answers, render the report, print it, optionally write it.

    Returns the process exit code (0 = success).

    Resolution: explicit `--interactive` OR (no answer flags + a TTY) →
    interactive prompts. Otherwise flags are validated and defaults fill
    the rest. Non-TTY with no flags is fine — defaults produce a report
    (CI/test friendly); the report echoes the inputs it used.
    """
    any_flag = any(v is not None for v in (cloud, partition, impact_level, architecture, posture))
    use_interactive = interactive or (not any_flag and is_interactive())

    if use_interactive:
        answers = _resolve_interactive()
    else:
        answers = StartAnswers(
            cloud=_validate_flag("cloud", cloud, _CLOUD_LABELS, DEFAULT_CLOUD),  # type: ignore[arg-type]
            partition=_validate_flag("partition", partition, _PARTITION_LABELS, DEFAULT_PARTITION),  # type: ignore[arg-type]
            impact_level=_validate_flag(
                "impact-level", impact_level, _IMPACT_LABELS, DEFAULT_IMPACT
            ),  # type: ignore[arg-type]
            architecture=_validate_flag(
                "architecture", architecture, _ARCH_LABELS, DEFAULT_ARCHITECTURE
            ),  # type: ignore[arg-type]
            posture=_validate_flag("posture", posture, _POSTURE_LABELS, DEFAULT_POSTURE),  # type: ignore[arg-type]
        )

    report = render_start_report(answers, generated_at=datetime.now(UTC))

    if out is not None:
        out_path = out.resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        typer.echo(f"Wrote your FedRAMP 20x path to: {out_path}")
        # Machine-readable sidecar (same stem, .json) so `efterlev init`'s
        # wizard can pre-fill your cloud / impact-level / architecture.
        sidecar = out_path.with_suffix(".json")
        sidecar.write_text(_sidecar_json(answers), encoding="utf-8")
        typer.echo(f"  (settings saved to {sidecar.name} for `efterlev init`)")
        typer.echo("")

    typer.echo(report)
    return 0


def _sidecar_json(answers: StartAnswers) -> str:
    payload = {
        "_efterlev": START_SIDECAR_MARKER,
        "version": START_SIDECAR_VERSION,
        **asdict(answers),
    }
    return json.dumps(payload, indent=2)


def load_start_sidecar(search_dirs: list[Path]) -> StartAnswers | None:
    """Find the most-recent `efterlev start` sidecar across `search_dirs`.

    Scans each directory (non-recursively) for `*.json` carrying the
    start-answers marker, returns the newest by mtime parsed into
    `StartAnswers`, or None if none found / all unparseable. Used by the
    `efterlev init` wizard to pre-fill from a prior `start` run.
    """
    candidates: list[tuple[float, StartAnswers]] = []
    seen: set[Path] = set()
    for d in search_dirs:
        if not d.is_dir():
            continue
        for path in d.glob("*.json"):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            answers = _parse_sidecar(path)
            if answers is not None:
                try:
                    mtime = path.stat().st_mtime
                except OSError:
                    continue
                candidates.append((mtime, answers))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0], reverse=True)
    return candidates[0][1]


def _parse_sidecar(path: Path) -> StartAnswers | None:
    """Parse one sidecar file into StartAnswers; None if not a valid sidecar."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("_efterlev") != START_SIDECAR_MARKER:
        return None
    # Pull only the known fields; validate each against its choice set so a
    # hand-edited or future-version sidecar can't smuggle a bad value through.
    try:
        return StartAnswers(
            cloud=_coerce(data.get("cloud"), _CLOUD_LABELS, DEFAULT_CLOUD),  # type: ignore[arg-type]
            partition=_coerce(data.get("partition"), _PARTITION_LABELS, DEFAULT_PARTITION),  # type: ignore[arg-type]
            impact_level=_coerce(data.get("impact_level"), _IMPACT_LABELS, DEFAULT_IMPACT),  # type: ignore[arg-type]
            architecture=_coerce(data.get("architecture"), _ARCH_LABELS, DEFAULT_ARCHITECTURE),  # type: ignore[arg-type]
            posture=_coerce(data.get("posture"), _POSTURE_LABELS, DEFAULT_POSTURE),  # type: ignore[arg-type]
        )
    except (TypeError, ValueError):
        return None


def _coerce(value: object, choices: dict[str, str], default: str) -> str:
    """Return value if it's a valid choice key, else the default."""
    if isinstance(value, str) and value in choices:
        return value
    return default
