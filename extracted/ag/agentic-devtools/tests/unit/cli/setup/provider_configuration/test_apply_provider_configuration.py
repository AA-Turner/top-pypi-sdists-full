"""Unit tests for apply_provider_configuration."""

from pathlib import Path

from agentic_devtools.cli.setup.provider_configuration import apply_provider_configuration, plan_provider_configuration


def test_apply_provider_configuration_writes_only_mutating_plans(tmp_path: Path) -> None:
    created = plan_provider_configuration(
        tmp_path,
        available_models=["gpt-4.1"],
        readiness=lambda _document: ("ready", "ready"),
    )
    assert apply_provider_configuration(created)

    preserved = plan_provider_configuration(tmp_path, existing_model="gpt-4.1")
    assert preserved.status == "preserved"
    assert not apply_provider_configuration(preserved)

    dry = plan_provider_configuration(
        tmp_path,
        available_models=["gpt-4.1"],
        dry_run=True,
        readiness=lambda _document: ("ready", "ready"),
    )
    assert not apply_provider_configuration(dry)
