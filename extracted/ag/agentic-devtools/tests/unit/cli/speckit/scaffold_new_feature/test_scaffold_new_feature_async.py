"""Tests for ``scaffold_new_feature_async``."""

from unittest.mock import patch

from agentic_devtools.cli.speckit import scaffold_new_feature


def test_scaffold_new_feature_async_calls_background() -> None:
    with (
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.run_function_in_background") as mock_bg,
        patch("agentic_devtools.cli.speckit.scaffold_new_feature.print_task_tracking_info") as mock_print,
    ):
        scaffold_new_feature.scaffold_new_feature_async(["--json", "Add x"])
    mock_bg.assert_called_once()
    mock_print.assert_called_once()
