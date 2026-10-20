"""Section parser edge cases (adversarial review L8 findings 2 and 3).

Every section must be reachable by id AND by number; headings the way CommonMark reads them.
"""

from __future__ import annotations

from matrx_ai.skills.sections import find_section, parse_sections


def _titles(body: str) -> list[str]:
    return [s.title for s in parse_sections(body) if s.level > 0]


def test_duplicate_headings_get_unique_ids_each_reachable():
    body = "# Dup\n\na\n\n## Dup\n\nb\n\n# Dup\n\nc\n\n# Dup 1\n\nd\n"
    secs = parse_sections(body)
    ids = [s.id for s in secs]
    assert len(ids) == len(set(ids)), ids
    for s in secs:
        assert find_section(secs, s.id) is s


def test_a_a_a1_ids_are_unique():
    secs = parse_sections("# a\n\nx\n\n# a\n\ny\n\n# a 1\n\nz\n")
    ids = [s.id for s in secs]
    assert len(ids) == len(set(ids)), ids


def test_skipped_level_never_gives_two_sections_one_number():
    secs = parse_sections("# T\n\n### deep\n\nx\n\n## mid\n\ny\n")
    numbers = [s.number for s in secs]
    assert len(numbers) == len(set(numbers)), numbers
    for s in secs:
        assert find_section(secs, s.number) is s


def test_setext_headings_are_sections():
    body = "Title\n=====\n\nintro text\n\nSub\n---\n\nmore\n"
    assert _titles(body) == ["Title", "Sub"]
    secs = parse_sections(body)
    assert [s.level for s in secs if s.level] == [1, 2]


def test_list_item_followed_by_rule_is_not_setext():
    assert _titles("- item\n---\n\nbody\n") == []


def test_headings_inside_html_comments_and_pre_are_ignored():
    body = "# Real\n\n<!--\n# hidden\n-->\n\n<pre>\n# also hidden\n</pre>\n\n## Next\n"
    assert _titles(body) == ["Real", "Next"]


def test_longer_fence_is_not_closed_by_a_shorter_one():
    body = "# A\n\n````md\n```\n# still in\n```\n````\n\n# B\n"
    assert _titles(body) == ["A", "B"]


def test_fence_with_info_string_does_not_close():
    body = "# A\n\n```\n```python\n# inside\n```\n\n# B\n"
    assert _titles(body) == ["A", "B"]


def test_indented_atx_heading_counts():
    assert _titles("   # Indented\n\nbody\n") == ["Indented"]


def test_closing_hashes_need_whitespace():
    assert _titles("# C#\n\nx\n") == ["C#"]
    assert _titles("# Title ##\n\nx\n") == ["Title"]
