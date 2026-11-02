"""Tests for fires_t0 in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive, unit

ENTRY_POINTS = frozenset({"agdt-add-jira-comment"})


def test_canonical_wrapper_fires() -> None:
    """The four-line wrapper shape is what T0's parenthetical measures."""
    assert derive.fires_t0(unit(), ENTRY_POINTS) is True


def test_unit_without_an_entry_point_never_fires() -> None:
    """T0's first limb is the entry-point match; without it the test cannot fire."""
    assert derive.fires_t0(unit(slug="agdt.analyze-workflow"), ENTRY_POINTS) is False


def test_long_body_of_agdt_commands_still_fires() -> None:
    """A body naming nothing but `agdt-*` commands adds no capability."""
    body = (
        "## Actions\n\n1. Run it:\n\n   ```bash\n   agdt-add-jira-comment\n   ```\n\n"
        "2. Then wait:\n\n   ```bash\n   agdt-task-wait\n   ```\n"
    )
    assert derive.fires_t0(unit(body=body), ENTRY_POINTS) is True


def test_body_reaching_for_another_tool_does_not_fire() -> None:
    """A unit that reaches past the command family adds something."""
    body = (
        "## Actions\n\n1. Run it:\n\n   ```bash\n   agdt-add-jira-comment\n   ```\n\n"
        '2. Then sleep:\n\n   ```bash\n   python3 -c "import time; time.sleep(4)"\n   ```\n'
    )
    assert derive.fires_t0(unit(body=body), ENTRY_POINTS) is False


def test_long_actions_section_with_no_command_does_not_fire() -> None:
    """With no command to compare against, nothing establishes that it adds nothing."""
    body = "## Actions\n\n" + "\n".join(f"- Consider point {n}." for n in range(10)) + "\n"
    assert derive.fires_t0(unit(body=body), ENTRY_POINTS) is False
