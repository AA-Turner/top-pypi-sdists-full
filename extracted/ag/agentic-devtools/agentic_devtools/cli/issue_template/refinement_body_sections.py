"""Pure physical-line section scanning for Markdown and Jira refinement bodies."""

import re

_FENCE = re.compile(r" {0,3}(`{3,}|~{3,})(.*)")
_FENCE_END = re.compile(r" {0,3}(`{3,}|~{3,})[ \t]*")
_ATX = re.compile(r" {0,3}(#{1,2})(?:[ \t]+(.*)|$)")
_JIRA = re.compile(r"h([12])\. (.*)")
# Closing hashes must start the title or follow a space/tab.
_CLOSING_HASHES = re.compile(r"(?<![^ \t])#+[ \t]*\Z")


def find_refinement_section_spans(body: str, section_name: str) -> list[tuple[int, int, str]]:
    """Return heading-inclusive, end-exclusive spans sorted by physical start line.

    Only LF, CRLF and CR split lines. CommonMark fences suppress both syntaxes;
    Markdown ATX and Jira wiki level-1/2 boundaries terminate only their own syntax.
    Titles match the unmodified argument; repeated sections are returned unchanged.
    """
    if not body or not section_name.strip():
        return []
    physical_body = re.sub(r"(?:\r\n|\r|\n)\Z", "", body)
    lines = re.split(r"\r\n|\r|\n", physical_body)
    fence = ""
    headings: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        if fence:
            closing = _FENCE_END.fullmatch(line)
            if closing and closing[1][0] == fence[0] and len(closing[1]) >= len(fence):
                fence = ""
            continue
        opening = _FENCE.fullmatch(line)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = opening[1]
            continue
        markdown = _ATX.fullmatch(line)
        if markdown:
            title = _CLOSING_HASHES.sub("", markdown[2] or "").strip(" \t")
            headings.append((index, len(markdown[1]), title, "markdown"))
        jira = _JIRA.fullmatch(line)
        if jira:
            headings.append((index, int(jira[1]), jira[2].strip(), "jira"))

    spans: list[tuple[int, int, str]] = []
    ends = {"markdown": len(lines), "jira": len(lines)}
    for start, level, title, syntax in reversed(headings):
        if level == 2 and title == section_name:
            spans.append((start, ends[syntax], syntax))
        ends[syntax] = start
    return sorted(spans)
