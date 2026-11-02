"""Tests for implementation_review_node."""

from agentic_devtools.orchestration.nodes.implementation_review import _scan_file


class TestScanFile:
    def test_detects_breakpoint(self):
        content = "x = 1\nbreakpoint()\ny = 2"
        issues = _scan_file("test.py", content)
        assert len(issues) == 1
        assert "Debug statement" in issues[0]

    def test_detects_pdb_set_trace(self):
        content = "import pdb\npdb.set_trace()"
        issues = _scan_file("test.py", content)
        assert any("pdb" in i.lower() for i in issues)

    def test_detects_todo_marker(self):
        content = "# TODO: fix this later"
        issues = _scan_file("test.py", content)
        assert len(issues) == 1
        assert "TODO" in issues[0]

    def test_detects_fixme_marker(self):
        content = "# FIXME: broken"
        issues = _scan_file("test.py", content)
        assert len(issues) == 1

    def test_clean_code_has_no_issues(self):
        content = "def hello():\n    return 'world'"
        issues = _scan_file("test.py", content)
        assert issues == []
