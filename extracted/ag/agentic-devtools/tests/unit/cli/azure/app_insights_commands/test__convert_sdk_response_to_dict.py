"""Tests for _convert_sdk_response_to_dict."""

from types import SimpleNamespace

from agentic_devtools.cli.azure.app_insights_commands import _convert_sdk_response_to_dict


def test_converts_sdk_tables_to_cli_response_shape():
    tables = [
        SimpleNamespace(columns=["timestamp", "message"], rows=[("now", "failed")]),
        SimpleNamespace(columns=["severity"], rows=[]),
    ]

    result = _convert_sdk_response_to_dict(tables)

    assert result == {
        "tables": [
            {
                "columns": [
                    {"name": "timestamp", "type": "string"},
                    {"name": "message", "type": "string"},
                ],
                "rows": [["now", "failed"]],
            },
            {
                "columns": [{"name": "severity", "type": "string"}],
                "rows": [],
            },
        ]
    }
