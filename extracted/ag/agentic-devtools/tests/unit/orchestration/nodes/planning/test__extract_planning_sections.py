"""Tests for _extract_planning_sections."""

from agentic_devtools.orchestration.nodes.planning import _extract_planning_sections


class TestExtractPlanningSections:
    """Tests for structured plan section extraction."""

    def test_extracts_tasks_files_and_risks_from_mixed_payload(self) -> None:
        tasks, affected_files, risks = _extract_planning_sections(
            {
                "tasks": [
                    "Task A",
                    "   ",
                    {"description": "Task B", "affected_files": ["src/a.py", "src/a.py", "", 1]},
                    {"description": "Task C", "affected_files": "not-a-list"},
                    {"description": "   ", "affected_files": ["src/ignored.py"]},
                    42,
                ],
                "affected_files": ["src/b.py", "src/a.py", None, "   "],
                "risks": [
                    "Risk A",
                    "   ",
                    {"description": "Risk B", "mitigation": "Add tests"},
                    {"description": "Risk C", "mitigation": "   "},
                    {"description": "   ", "mitigation": "ignored"},
                    False,
                ],
            }
        )

        assert tasks == ["Task A", "Task B", "Task C"]
        assert affected_files == ["src/a.py", "src/ignored.py", "src/b.py"]
        assert risks == ["Risk A", "Risk B (Mitigation: Add tests)", "Risk C"]

    def test_non_list_sections_return_empty_lists(self) -> None:
        tasks, affected_files, risks = _extract_planning_sections(
            {"tasks": "not-a-list", "affected_files": "not-a-list", "risks": "not-a-list"}
        )

        assert tasks == []
        assert affected_files == []
        assert risks == []

    def test_whitespace_padded_path_duplicate_is_deduplicated(self) -> None:
        """' src/a.py' and 'src/a.py' should produce only one entry."""
        tasks, affected_files, risks = _extract_planning_sections(
            {
                "tasks": [
                    {"description": "Task", "affected_files": [" src/a.py", "src/a.py"]},
                ],
                "affected_files": ["  src/a.py  ", "src/b.py"],
            }
        )

        assert affected_files.count("src/a.py") == 1
        assert "src/b.py" in affected_files
