"""Three small defects found while verifying the 2026-08-05 dev deploy.

Each test is written so it fails against the pre-fix code, not merely passes
against the fixed code.
"""

from __future__ import annotations

import argparse

import pytest
from sqlmodel import SQLModel

from src.cli.commands.boards import format_sync_status
from src.cli.utils.formatters import describe_exception
from src.domain.board_credential import BoardCredential
from src.domain.cli_token import CLIToken


class TestDescribeException:
    """`✗ Error:` with nothing after it -- observed from `board sync-status`.

    The CLI's top-level handler interpolates the exception into an error
    template. `str(exc)` is empty for anything raised without arguments, so the
    user saw a blank error and the only detail was behind `--verbose`.
    """

    def test_exception_with_no_message_still_says_something(self):
        class SomethingBroke(Exception):
            pass

        described = describe_exception(SomethingBroke())
        assert described.strip(), "an empty description is the bug being fixed"
        assert "SomethingBroke" in described

    def test_whitespace_only_message_is_treated_as_empty(self):
        assert "ValueError" in describe_exception(ValueError("   "))

    def test_real_message_is_preserved_verbatim(self):
        assert describe_exception(ValueError("board not found")) == "board not found"

    def test_status_code_is_surfaced_when_present(self):
        """An APIError's HTTP status is often the most actionable part."""
        from src.cli.client import APIError

        described = describe_exception(APIError("Unauthorized: bad token", 401))
        assert "401" in described
        assert "Unauthorized: bad token" in described


class TestSyncStatusCasing:
    """`SyncStatus` values are lowercase; the CLI compared against uppercase.

    The database stores the enum *name* (`COMPLETED`) while the API serialises
    the enum *value* (`completed`), so the same status appears in either case
    depending on where it is read. The handler only matched uppercase, so every
    branch fell through to the unstyled `Status: <x>` default -- including
    failures, which lost their error styling entirely.
    """

    @pytest.mark.parametrize(
        "value,expected",
        [
            # What the API actually returns (SyncStatus values are lowercase).
            ("completed", "Last sync completed successfully"),
            ("failed", "Last sync failed"),
            ("in_progress", "Sync in progress"),
            ("pending", "Sync pending"),
            # What the database column holds (the enum names).
            ("COMPLETED", "Last sync completed successfully"),
            ("FAILED", "Last sync failed"),
            ("IN_PROGRESS", "Sync in progress"),
        ],
    )
    def test_both_casings_select_the_right_branch(self, value, expected):
        assert expected in format_sync_status(value)

    def test_failed_sync_is_styled_as_an_error(self):
        """The regression that mattered: failures lost their error styling."""
        assert "[red]" in format_sync_status("failed")
        assert "[green]" in format_sync_status("completed")

    def test_genuinely_unknown_status_falls_through_unchanged(self):
        assert format_sync_status("weird") == "Status: weird"

    def test_missing_status_does_not_crash(self):
        assert "unknown" in format_sync_status(None)

    def test_lowercase_values_come_from_the_enum_itself(self):
        """Pin the premise: if these ever become uppercase, the fix is moot."""
        from src.domain.board import SyncStatus

        assert SyncStatus.COMPLETED.value == "completed"
        assert SyncStatus.FAILED.value == "failed"


class TestExplicitSaColumnNullability:
    """`sa_column=Column(...)` discards the nullability the annotation implies.

    SQLModel infers NOT NULL from a non-Optional annotation only when it builds
    the column itself. Passing an explicit `sa_column` hands control to
    SQLAlchemy, whose own default is `nullable=True` -- so `organization_id: str`
    produced a NULLable column.

    That matters because `SQLModel.metadata.create_all` (used by the test
    fixtures) then builds a *more permissive* schema than migrations do: these
    three columns are NOT NULL on dev, so a row the tests accepted would be
    rejected in deployment. Measured on dev 2026-08-05 -- these were the only
    three columns where the model and the real database actually disagreed.
    """

    @pytest.mark.parametrize(
        "model,field",
        [
            (BoardCredential, "organization_id"),
            (BoardCredential, "board_registration_id"),
            (CLIToken, "scopes"),
        ],
    )
    def test_column_is_not_nullable(self, model, field):
        column = model.__table__.columns[field]
        assert column.nullable is False, (
            f"{model.__tablename__}.{field} is NOT NULL on dev but nullable in the "
            "model -- add nullable=False to its Column(...)"
        )

    def test_create_all_enforces_it(self):
        """The point of the fix: the generated schema must reject the NULL too."""
        from sqlalchemy import create_engine, inspect

        engine = create_engine("sqlite://")
        SQLModel.metadata.create_all(engine)
        columns = {
            c["name"]: c for c in inspect(engine).get_columns("board_credentials")
        }
        assert columns["organization_id"]["nullable"] is False
        assert columns["board_registration_id"]["nullable"] is False


class TestProjectEnumArgs:
    """`innoday projects list --status/--priority` returned 422 for every value.

    Two independent causes: the hardcoded choices were UPPERCASE while
    `GET /projects` validates against the enums' lowercase *values*, and two of
    the offered statuses (`ON_HOLD`, `COMPLETED`) plus one priority (`CRITICAL`)
    do not exist in the enums at all -- argparse accepted them and the server
    rejected them, so the error surfaced as far as possible from its cause.
    """

    def test_choices_are_exactly_the_enum_values(self):
        from src.cli.commands.projects import (
            PROJECT_PRIORITY_CHOICES,
            PROJECT_STATUS_CHOICES,
        )
        from src.domain.project import ProjectPriority, ProjectStatus

        assert PROJECT_STATUS_CHOICES == [s.value for s in ProjectStatus]
        assert PROJECT_PRIORITY_CHOICES == [p.value for p in ProjectPriority]

    def test_phantom_values_are_gone(self):
        """These three were offered but rejected by the API."""
        from src.cli.commands.projects import (
            PROJECT_PRIORITY_CHOICES,
            PROJECT_STATUS_CHOICES,
        )

        assert "on_hold" not in PROJECT_STATUS_CHOICES
        assert "completed" not in PROJECT_STATUS_CHOICES
        assert "critical" not in PROJECT_PRIORITY_CHOICES

    @pytest.mark.parametrize(
        "given,expected",
        [("ACTIVE", "active"), ("active", "active"), ("  Planning ", "planning")],
    )
    def test_either_casing_normalises_to_the_api_value(self, given, expected):
        from src.cli.commands.projects import project_status

        assert project_status(given) == expected

    def test_priority_normalises_too(self):
        from src.cli.commands.projects import project_priority

        assert project_priority("MEDIUM") == "medium"

    def test_nonexistent_value_is_rejected_locally_with_the_real_options(self):
        """Better an argparse error naming the options than a server-side 422."""
        import argparse

        from src.cli.commands.projects import project_status

        with pytest.raises(argparse.ArgumentTypeError) as excinfo:
            project_status("ON_HOLD")
        assert "planning" in str(excinfo.value)

    def test_create_defaults_are_already_canonical(self):
        """argparse `default=` bypasses `type=`, so it must not be UPPERCASE."""
        from src.cli.commands.projects import ProjectCommands
        from src.domain.project import ProjectPriority, ProjectStatus

        parser = argparse.ArgumentParser()
        ProjectCommands.setup_parser(parser)
        args = parser.parse_args(["create", "Demo", "--alias", "DEMO"])
        assert args.status == ProjectStatus.PLANNING.value
        assert args.priority == ProjectPriority.MEDIUM.value


class TestStatusStyleLookups:
    """No enum member may fall through to the default style.

    `TicketStatus.IN_PROGRESS` is literally `"in progress"` -- a space, where the
    enum *name* has an underscore. The lookups upper-cased their input, so
    `"in progress".upper()` gave `"IN PROGRESS"`, matched no key, and silently
    returned the default. `in progress` and `in review` -- the two most common
    working states -- therefore rendered unstyled.

    Written as an invariant over the enums rather than a fixed list, so adding a
    member with a space (or a hyphen) fails here instead of quietly losing its
    colour.
    """

    @staticmethod
    def _formatter():
        from src.cli.utils.formatters import OutputFormatter

        # Bypass __init__: it builds a Rich Console, which these lookups do not need.
        return OutputFormatter.__new__(OutputFormatter)

    def test_every_ticket_status_resolves_a_style(self):
        from src.domain.ticket import TicketStatus

        formatter = self._formatter()
        for member in TicketStatus:
            # Both forms reach the CLI: the API serialises `.value`, the database
            # column stores `.name`.
            for form in (member.value, member.name):
                assert formatter._get_status_style(form) != "white", (
                    f"{member.name} via {form!r} fell through to the default style"
                )

    def test_every_project_status_resolves_a_style(self):
        from src.domain.project import ProjectStatus

        formatter = self._formatter()
        for member in ProjectStatus:
            for form in (member.value, member.name):
                assert formatter._get_project_status_style(form) != "white", (
                    f"{member.name} via {form!r} fell through"
                )

    def test_every_project_priority_resolves_a_style(self):
        from src.domain.project import ProjectPriority

        formatter = self._formatter()
        for member in ProjectPriority:
            for form in (member.value, member.name):
                assert formatter._get_priority_style(form) != "white", (
                    f"{member.name} via {form!r} fell through"
                )

    def test_the_two_that_were_broken(self):
        """Explicit regression pins for the actual reported symptom."""
        formatter = self._formatter()
        assert formatter._get_status_style("in progress") == "yellow"
        assert formatter._get_status_style("in review") == "magenta"

    def test_unknown_status_still_falls_back(self):
        """The default must survive -- this is not a "colour everything" change."""
        assert self._formatter()._get_status_style("nonsense") == "white"

    def test_enum_key_normalises_all_three_shapes(self):
        from src.cli.utils.formatters import enum_key

        assert enum_key("in progress") == "IN_PROGRESS"
        assert enum_key("IN_PROGRESS") == "IN_PROGRESS"
        assert enum_key("  in-progress ") == "IN_PROGRESS"


# --------------------------------------------------------------------------- #
# A dry run is not a sync (#576)
# --------------------------------------------------------------------------- #


def test_a_dry_run_is_never_reported_in_the_past_tense():
    """It used to print "Last sync completed successfully" over counts of tickets
    it had not touched, which is how a stale board came to look freshly synced."""
    from src.cli.commands.boards import format_sync_status

    real = format_sync_status("completed")
    preview = format_sync_status("completed", dry_run=True)

    assert "completed successfully" in real
    assert "completed successfully" not in preview
    assert "DRY RUN" in preview and "nothing was written" in preview
    # Either casing, since the API serialises the value and the column stores the
    # name -- the reason this helper exists at all.
    assert "DRY RUN" in format_sync_status("COMPLETED", dry_run=True)
    assert "Dry run" in format_sync_status("IN_PROGRESS", dry_run=True)
    assert "Sync in progress" in format_sync_status("IN_PROGRESS")


def test_board_sync_exposes_force_so_a_wedged_board_needs_no_sql():
    """An interrupted sync leaves a PENDING row that blocks every later one, and
    `force` was hardcoded False -- so the only way out was editing that row by
    hand, which is what happened on Atomic the night before its release."""
    import argparse

    from src.cli.commands.boards import BoardCommands

    parser = argparse.ArgumentParser()
    BoardCommands.setup_parser(parser)
    assert parser.parse_args(["sync", "--force"]).force is True
    assert parser.parse_args(["sync"]).force is False
