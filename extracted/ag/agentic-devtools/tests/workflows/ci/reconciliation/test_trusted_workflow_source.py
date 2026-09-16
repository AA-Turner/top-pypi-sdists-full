"""Static checks for trusted workflow source protections."""

from __future__ import annotations

from pathlib import Path


def test_scheduled_reconciliation_checks_out_default_branch() -> None:
    workflow = Path(".github/workflows/ai-pr-loop.yml").read_text(encoding="utf-8")
    assert "ref: '${{ github.event.repository.default_branch }}'" in workflow


def test_scheduled_reconciliation_uses_reconcile_command() -> None:
    workflow = Path(".github/workflows/ai-pr-loop.yml").read_text(encoding="utf-8")
    assert "agdt-ci-reconcile" in workflow
