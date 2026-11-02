"""Tests for _apply_processing_path_map."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.review_prompt_tracking import _apply_processing_path_map


def test_persists_processing_path_values_to_review_state() -> None:
    file_entry = MagicMock()
    state = MagicMock(files={"/src/a.py": file_entry})
    context = MagicMock()
    context.__enter__.return_value = state
    context.__exit__.return_value = False

    with patch(
        "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
        return_value=context,
    ):
        _apply_processing_path_map(42, {"/src/a.py": "inherited"}, lambda *args, **kwargs: None)

    assert file_entry.processingPath == "inherited"
