"""Static checks for trusted workflow source protections."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import yaml


def test_scheduled_reconciliation_checks_out_default_branch() -> None:
    workflow = Path(".github/workflows/ai-pr-loop.yml").read_text(encoding="utf-8")
    assert "ref: '${{ github.event.repository.default_branch }}'" in workflow


def test_scheduled_reconciliation_uses_reconcile_command() -> None:
    workflow = Path(".github/workflows/ai-pr-loop.yml").read_text(encoding="utf-8")
    assert "agdt-ci-reconcile" in workflow


def test_watchdog_checkout_uses_default_branch() -> None:
    workflow_path = Path(__file__).resolve().parents[4] / ".github/workflows/ai-pr-loop-watchdog.yml"
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    triggers = workflow[True]  # PyYAML's YAML 1.1 loader parses the unquoted "on" key as True.
    assert triggers == {
        "workflow_dispatch": {},
        "repository_dispatch": {"types": ["ai-pr-loop-due-probe"]},
        "schedule": [{"cron": "*/20 * * * *"}, {"cron": "*/5 * * * *"}],
    }

    job = workflow["jobs"]["watchdog"]
    checkout = next(step for step in job["steps"] if step.get("uses") == "actions/checkout@v4")
    assert checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
    assert "if" not in checkout
    probe_step = next(
        step for step in job["steps"] if step.get("name") == "Restart stalled ai-pr-loop when eligible PRs exist"
    )
    assert probe_step["run"] == dedent(
        r"""
        MODE="watchdog"
        if [ "${{ github.event_name }}" = "repository_dispatch" ] ||
          { [ "${{ github.event_name }}" = "schedule" ] && [ "${{ github.event.schedule }}" = "*/5 * * * *" ]; }; then
          MODE="due-probe-only"
        fi
        if [ "$MODE" = "due-probe-only" ] &&
           [ "${{ github.event_name }}" = "schedule" ] &&
           [ "${{ github.event.schedule }}" = "*/5 * * * *" ]; then
          for iteration in 1 2 3 4 5; do
            started_at=$(date +%s)
            agdt-ai-pr-loop-watchdog \
              --mode "$MODE" \
              --repo "${{ github.repository }}" \
              --default-branch "${{ github.event.repository.default_branch }}"
            elapsed=$(( $(date +%s) - started_at ))
            delay=$(( 60 - elapsed ))
            if [ "$iteration" -lt 5 ] && [ "$delay" -gt 0 ]; then
              sleep "$delay"
            fi
          done
        else
          agdt-ai-pr-loop-watchdog \
            --mode "$MODE" \
            --repo "${{ github.repository }}" \
            --default-branch "${{ github.event.repository.default_branch }}"
        fi
        """
    ).lstrip("\n")
