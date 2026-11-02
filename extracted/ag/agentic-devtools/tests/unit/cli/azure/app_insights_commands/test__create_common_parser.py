"""Tests for _create_common_parser."""

from agentic_devtools.cli.azure.app_insights_commands import _create_common_parser


def test_creates_parser_with_common_options():
    parser = _create_common_parser("Query logs")

    args = parser.parse_args(
        [
            "--environment",
            "INT",
            "--timespan",
            "3h",
            "--limit",
            "12",
            "--dataproduct",
            "dp-42",
            "--workbench",
            "STND",
        ]
    )

    assert parser.description == "Query logs"
    assert args.environment == "INT"
    assert args.timespan == "3h"
    assert args.limit == 12
    assert args.dataproduct == "dp-42"
    assert args.workbench == "STND"
    assert args.include_mgmt is None
    assert args.output_to_file is None
    assert args.auto_switch is None
