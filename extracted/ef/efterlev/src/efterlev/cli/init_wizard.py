"""Interactive `efterlev init` wizard — the Stage 0 → Stage 1 bridge.

`efterlev start` (Stage 0) produces orientation; `efterlev init` creates
the workspace (Stage 1). This wizard connects them: on a TTY it walks the
user through cloud / partition / LLM backend / boundary scope instead of
requiring flags, and pre-fills from a prior `efterlev start --out` run if
its sidecar is present.

## Backward compatibility

The wizard is **opt-in**. `efterlev init` runs it only when:
  - `--interactive` / `-i` is passed, OR
  - stdin+stdout are a TTY AND the user passed no config-determining flags
    (so a bare `efterlev init` at a terminal is guided, but any scripted
    invocation — flags, or piped/CI — keeps the exact pre-v0.1.172
    behavior).

`--no-interactive` forces the old behavior even on a bare TTY.

## What it collects

  - **Cloud + partition** — drives the LLM-backend default (GovCloud →
    Bedrock, to keep the tool's own LLM calls in-boundary).
  - **LLM backend** (+ region for Bedrock).
  - **Boundary scope** (optional) — reuses the `boundary set --interactive`
    prompt so the user can scope at init time.

Baseline is fixed to `fedramp-20x-moderate` (the only supported baseline
today); if the `start` sidecar indicated a different impact level the
wizard says so and proceeds with Moderate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import typer

from efterlev.cli.start_cli import (
    _CLOUD_LABELS,
    _PARTITION_LABELS,
    _prompt_choice,
    load_start_sidecar,
)

# Only baseline supported today; the wizard never offers an unsupported one.
SUPPORTED_BASELINE = "fedramp-20x-moderate"

_BACKEND_LABELS = {
    "anthropic": "Anthropic API (direct; needs ANTHROPIC_API_KEY)",
    "bedrock": "AWS Bedrock (in-boundary; needs AWS creds + a region)",
    "claude_code": "Claude Code subscription (local `claude` CLI; no per-call billing)",
    "openai": "OpenAI API (needs OPENAI_API_KEY; gpt-5.4-mini recommended)",
    "bedrock_openai": "OpenAI on AWS Bedrock (gpt-5.5 via Mantle; needs a region "
    "+ AWS_BEARER_TOKEN_BEDROCK; commercial only at launch)",
}

_DEFAULT_GOVCLOUD_REGION = "us-gov-west-1"


@dataclass(frozen=True)
class InitWizardResult:
    """The wizard's collected choices, applied by the `init` command."""

    baseline: str = SUPPORTED_BASELINE
    llm_backend: str = "anthropic"
    llm_region: str | None = None
    boundary_include: list[str] = field(default_factory=list)
    boundary_exclude: list[str] = field(default_factory=list)


def run_init_wizard(target: Path) -> InitWizardResult:
    """Walk the interactive init prompts; return the collected choices.

    Pre-fills cloud/partition from a prior `efterlev start` sidecar (found
    in cwd or `target`) when present.
    """
    typer.echo("Interactive setup. Press Enter to accept the default for any question.")
    typer.echo("")

    sidecar = load_start_sidecar([Path.cwd(), target])
    cloud_default = sidecar.cloud if sidecar else "aws"
    partition_default = sidecar.partition if sidecar else "commercial"
    if sidecar is not None:
        typer.echo(
            "Found settings from a prior `efterlev start`: "
            f"cloud={sidecar.cloud}, partition={sidecar.partition}, "
            f"impact={sidecar.impact_level}, architecture={sidecar.architecture}."
        )
        if sidecar.impact_level != "moderate":
            typer.echo(
                f"  Note: you indicated {sidecar.impact_level.title()} impact, but only "
                "Moderate is supported today — initializing Moderate."
            )

    cloud = _prompt_choice("Cloud provider?", _CLOUD_LABELS, cloud_default)
    partition = "commercial"
    if cloud == "aws":
        partition = _prompt_choice("AWS partition?", _PARTITION_LABELS, partition_default)

    # Backend default: GovCloud → Bedrock (keeps the tool's own LLM calls in
    # the FedRAMP boundary); otherwise Anthropic API.
    backend_default = "bedrock" if (cloud == "aws" and partition == "govcloud") else "anthropic"
    llm_backend = _prompt_choice("LLM backend?", _BACKEND_LABELS, backend_default)

    llm_region: str | None = None
    if llm_backend == "bedrock":
        region_default = _DEFAULT_GOVCLOUD_REGION if partition == "govcloud" else "us-east-1"
        typer.echo("")
        typer.echo("AWS region for Bedrock (e.g. us-gov-west-1, us-east-1):")
        llm_region = typer.prompt("  region", default=region_default).strip()

    # Boundary scope — optional. Reuse the existing interactive prompt.
    include: list[str] = []
    exclude: list[str] = []
    typer.echo("")
    if typer.confirm("Scope your authorization boundary now?", default=False):
        # Imported lazily: the helper lives in main.py, which imports this
        # module — a top-level import would be circular.
        from efterlev.cli.main import _boundary_set_interactive_prompt

        include, exclude = _boundary_set_interactive_prompt(append=False)

    return InitWizardResult(
        baseline=SUPPORTED_BASELINE,
        llm_backend=llm_backend,
        llm_region=llm_region,
        boundary_include=include,
        boundary_exclude=exclude,
    )
