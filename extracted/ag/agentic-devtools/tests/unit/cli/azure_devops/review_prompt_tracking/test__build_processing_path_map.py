"""Tests for _build_processing_path_map."""

from agentic_devtools.cli.azure_devops.review_prompt_tracking import _build_processing_path_map


def test_maps_valid_entries_and_normalizes_fallback_paths() -> None:
    result = _build_processing_path_map(
        [
            {"normalizedPath": "/src/a.py", "processingPath": "reviewed"},
            {"path": "src/b.py", "processingPath": "inherited"},
            {"path": "src/ignored.py", "processingPath": ""},
            "invalid",
        ],
        lambda path: f"/{path}" if path else None,
    )

    assert result == {"/src/a.py": "reviewed", "/src/b.py": "inherited"}
