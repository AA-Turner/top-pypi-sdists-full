from agentic_devtools.adapters.pull_request_details import _parse_github_patch


def test_parse_github_patch_extracts_added_and_removed_lines() -> None:
    patch = "@@ -1,3 +1,4 @@\n context\n-removed\n+added one\n+added two\n context"
    added, removed = _parse_github_patch(patch)
    assert added == [
        {"line": 2, "content": "added one"},
        {"line": 3, "content": "added two"},
    ]
    assert removed == [{"line": 2, "content": "removed"}]


def test_parse_github_patch_handles_multiple_hunks() -> None:
    patch = "@@ -1,2 +1,2 @@\n context\n-old\n+new\n@@ -10,1 +10,2 @@\n context\n+extra"
    added, removed = _parse_github_patch(patch)
    assert added == [{"line": 2, "content": "new"}, {"line": 11, "content": "extra"}]
    assert removed == [{"line": 2, "content": "old"}]


def test_parse_github_patch_ignores_no_newline_marker() -> None:
    patch = "@@ -1,1 +1,1 @@\n-old\n+new\n\\ No newline at end of file"
    added, removed = _parse_github_patch(patch)
    assert added == [{"line": 1, "content": "new"}]
    assert removed == [{"line": 1, "content": "old"}]


def test_parse_github_patch_returns_empty_for_unrecognized_text() -> None:
    added, removed = _parse_github_patch("@@")
    assert added == []
    assert removed == []
