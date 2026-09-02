"""`output.format` in the profile decides the format when no flag is given.

The field was persisted, shown by `config show` and settable by
`config set format`, and could never take effect: the global `--format`
carried `default="table"`, so every consumer saw an explicit choice on the
namespace and had nothing to fall back from. #729 makes the flag default to
`None` and the two consumers that know about the profile fall back to it.

Nothing detected any of that -- reverting the whole change left the suite
green -- so these tests exist to fail when it is reverted, one per part:

- ``--format`` carries no default            (`main.py`)
- ``tickets`` falls back to the profile      (`tickets.py`)
- ``status`` falls back to the profile       (`utils.py`)
- an absent choice still renders a table     (`utils/formatters.py`)

They drive the real parser and the real `CLIConfig`, so a profile value has
to survive the same path it does in a real invocation rather than being
handed to the code under test directly.
"""

import csv
import io
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.tickets import TicketCommands
from src.cli.commands.utils import UtilityCommands
from src.cli.config import CLIConfig
from src.cli.main import create_parser
from src.cli.utils.formatters import OutputFormatter

TICKETS = [
    {
        "id": 1380,
        "title": "A ticket",
        "status": "TODO",
        "priority": "MEDIUM",
        "assignee": "someone",
    }
]


def _config(tmp_path, output_format):
    """A real config file whose profile asks for `output_format`."""
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "profiles": {
                    "default": {
                        "output": {"format": output_format, "color": False},
                        "organizations": {"hs": {"id": "org-1"}},
                    }
                }
            }
        )
    )
    config = CLIConfig(config_path=str(path))
    # Resolved per-invocation from cwd in real use; `tickets` refuses to run
    # without one, and which org it is has no bearing on the format.
    config.set_current_organization("hs")
    return config


def _fake_client():
    client = MagicMock()
    client.list_tickets = AsyncMock(return_value=TICKETS)
    client.ping_api = AsyncMock(return_value={"message": "ok"})
    client.project_id = None
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=False)
    return client


async def _run_tickets_list(argv, config):
    args = create_parser().parse_args(argv)
    with patch(
        "src.cli.commands.tickets.InnoDayAPIClient", return_value=_fake_client()
    ):
        assert await TicketCommands.execute(args, config) == 0


class TestTheGlobalFormatFlagHasNoDefault:
    """The distinction the rest of this rests on: "no format asked for" has to
    be tellable from "table asked for"."""

    def test_an_absent_flag_leaves_format_unset(self):
        args = create_parser().parse_args(["tickets", "list"])
        assert args.format is None

    def test_an_explicit_flag_is_still_recorded(self):
        args = create_parser().parse_args(["--format", "json", "tickets", "list"])
        assert args.format == "json"


class TestTicketsFollowsTheProfile:
    @pytest.mark.asyncio
    async def test_a_json_profile_produces_json(self, tmp_path, capsys):
        await _run_tickets_list(["tickets", "list"], _config(tmp_path, "json"))

        payload = json.loads(capsys.readouterr().out)
        assert payload[0]["title"] == "A ticket"

    @pytest.mark.asyncio
    async def test_a_csv_profile_produces_csv(self, tmp_path, capsys):
        await _run_tickets_list(["tickets", "list"], _config(tmp_path, "csv"))

        rows = list(csv.reader(io.StringIO(capsys.readouterr().out)))
        assert rows[0] == ["id", "summary", "status", "assignee", "created_at"]
        assert rows[1][0] == "1380"

    @pytest.mark.asyncio
    async def test_an_explicit_flag_beats_the_profile(self, tmp_path, capsys):
        """Both directions, so this cannot pass by the profile being ignored."""
        await _run_tickets_list(
            ["--format", "table", "tickets", "list"], _config(tmp_path, "json")
        )

        out = capsys.readouterr().out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)
        assert "Total: 1 tickets" in out  # the table renderer, not JSON or CSV

    @pytest.mark.asyncio
    async def test_an_explicit_json_flag_wins_over_a_table_profile(
        self, tmp_path, capsys
    ):
        await _run_tickets_list(
            ["--format", "json", "tickets", "list"], _config(tmp_path, "table")
        )

        assert json.loads(capsys.readouterr().out)[0]["title"] == "A ticket"


class TestStatusFollowsTheProfile:
    """The second consumer, and a separate revert: `utils.py` has its own copy
    of the fallback."""

    @pytest.mark.asyncio
    async def test_a_json_profile_produces_json(self, tmp_path, capsys):
        config = _config(tmp_path, "json")
        args = create_parser().parse_args(["status"])

        with patch(
            "src.cli.commands.utils.InnoDayAPIClient", return_value=_fake_client()
        ):
            assert await UtilityCommands._handle_status(args, config) == 0

        assert json.loads(capsys.readouterr().out)["api_status"] == "healthy"

    @pytest.mark.asyncio
    async def test_an_explicit_flag_beats_the_profile(self, tmp_path, capsys):
        config = _config(tmp_path, "json")
        args = create_parser().parse_args(["--format", "table", "status"])

        with patch(
            "src.cli.commands.utils.InnoDayAPIClient", return_value=_fake_client()
        ):
            assert await UtilityCommands._handle_status(args, config) == 0

        with pytest.raises(json.JSONDecodeError):
            json.loads(capsys.readouterr().out)


class TestACommandThatPassesTheFlagStraightThroughStillGetsATable:
    """The commands that do not consult the profile (`projects`, `orgs`,
    `scopes`) hand `args.format` to the formatter unchanged, so with no flag
    they now hand it `None`. Every branch inside compares against `"json"` or
    `"csv"` and falls through to a table anyway, which is why this is asserted
    on the attribute: it is the contract, and it is the only thing that goes
    red when the coercion is dropped.
    """

    def test_no_choice_means_table(self):
        assert OutputFormatter(format_type=None).format_type == "table"

    def test_the_old_default_is_unchanged(self):
        assert OutputFormatter().format_type == "table"

    def test_an_explicit_choice_survives(self):
        assert OutputFormatter(format_type="csv").format_type == "csv"


class TestAProfileValueIsWhatArrives:
    """Guards the fixture itself: if the profile value never reached
    `get_output_format`, every test above would pass for the wrong reason."""

    def test_the_config_reports_the_profiles_format(self, tmp_path):
        assert _config(tmp_path, "csv").get_output_format() == "csv"


def test_no_subcommand_format_flag_was_disturbed():
    """The five subcommand-level `--format` arguments shadow the global one and
    carry their own defaults, so they are unaffected -- asserted rather than
    assumed, because a `None` reaching one of them would be a real break."""
    parser = create_parser()
    for argv in (
        ["board", "list"],
        ["repos", "issues", "--repository-id", "r-1"],
    ):
        assert parser.parse_args(argv).format == "table", argv
