"""Regression: FileSearchMatch must accept the sandbox/ripgrep branch shape.

Bug: ``fs_search`` with ``content_search=True`` crashed on the sandbox
(``_proxy_fs_search``) branch because ripgrep rows carry ``line_number``,
``lines`` and ``submatches`` keys that were not declared on the
``extra="forbid"`` ``FileSearchMatch`` model. Every match therefore raised
``Extra inputs are not permitted``. Per the model's own documented
"declare every key any branch returns" rule, those fields are now declared.
"""

from matrx_ai.tools.kinds.filesystem import FileSearchMatch, FileSearchResults


def test_content_search_ripgrep_row_is_accepted():
    row = {
        "path": "aidream/podcast.py",
        "line_number": 39,
        "lines": "podcast generation / GSC-ingest lane (driving",
        "submatches": [{"match": {"text": "Master"}, "start": 39, "end": 49}],
    }
    result = FileSearchResults(
        results=[FileSearchMatch(**row)], count=1, content_search=True
    )
    assert result.results[0].line_number == 39
    assert result.results[0].submatches[0]["start"] == 39


def test_name_search_row_still_valid():
    m = FileSearchMatch(path="b.py", size=10)
    assert m.size == 10
    assert m.line_number is None


def test_local_content_row_still_valid():
    m = FileSearchMatch(path="c.py", matches=["a hit"])
    assert m.matches == ["a hit"]
