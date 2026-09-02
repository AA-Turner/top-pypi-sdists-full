"""Loud-degrade guards for parser vocabulary drift.

Both cases below used to fail SILENTLY (crash swallowed -> block finalized
with ``data=None``, or hollow cells with no trace). The fixes degrade
gracefully but must SCREAM — these tests pin the warning, not just the value.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks.parsers import comparison_parser, diagram_parser
from matrx_ai.processing.blocks.parsers.comparison_parser import parse_comparison
from matrx_ai.processing.blocks.parsers.diagram_parser import parse_diagram


@pytest.fixture(autouse=True)
def _reset_log_once() -> None:
    """_log_once is once-per-process; isolate each test's warning assertion."""
    diagram_parser._logged_causes.clear()
    comparison_parser._logged_causes.clear()


def _diagram_source(diagram_type: str) -> str:
    return json.dumps(
        {
            "diagram": {
                "title": "T",
                "type": diagram_type,
                "nodes": [{"id": "a", "label": "A"}],
            }
        }
    )


def _comparison_source(values: dict[str, str]) -> str:
    return json.dumps(
        {
            "comparison": {
                "title": "T",
                "items": ["React", "Vue"],
                "criteria": [{"name": "Size", "values": values}],
            }
        }
    )


def test_unknown_diagram_type_degrades_loudly_and_preserves_original(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING", logger=diagram_parser.__name__):
        result = parse_diagram(_diagram_source("architecture"))
    assert result is not None
    assert result.type == "flowchart"
    assert result.requested_type == "architecture"  # zero data loss
    assert any("architecture" in r.message and "flowchart" in r.message for r in caplog.records)
    # The dumped payload carries the original type for the envelope residue.
    assert result.model_dump(by_alias=True)["requested_type"] == "architecture"


def test_known_diagram_type_is_quiet_and_dump_shape_unchanged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING", logger=diagram_parser.__name__):
        result = parse_diagram(_diagram_source("system"))
    assert result is not None
    assert result.type == "system"
    assert not caplog.records
    # Ordinary diagrams keep their established payload — no new key appears.
    assert "requested_type" not in result.model_dump(by_alias=True)


def test_comparison_dict_values_missing_key_warns_and_still_parses(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING", logger=comparison_parser.__name__):
        result = parse_comparison(_comparison_source({"React": "40kb"}))  # Vue missing
    assert result is not None
    assert result.criteria[0].values == ["40kb", ""]
    assert any("missing=['Vue']" in r.message for r in caplog.records)


def test_comparison_dict_values_extra_key_warns_and_still_parses(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING", logger=comparison_parser.__name__):
        result = parse_comparison(
            _comparison_source({"React": "40kb", "Vue": "33kb", "Svelte": "5kb"})
        )
    assert result is not None
    assert result.criteria[0].values == ["40kb", "33kb"]
    assert any("extra=['Svelte']" in r.message for r in caplog.records)


def test_comparison_dict_values_exact_match_is_quiet(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level("WARNING", logger=comparison_parser.__name__):
        result = parse_comparison(_comparison_source({"React": "40kb", "Vue": "33kb"}))
    assert result is not None
    assert result.criteria[0].values == ["40kb", "33kb"]
    assert not caplog.records
