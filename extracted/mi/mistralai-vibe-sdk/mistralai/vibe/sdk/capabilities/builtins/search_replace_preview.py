import re
from collections.abc import Iterator

from pydantic import BaseModel

LINE_BREAK = re.compile(r"\r\n|[\n\r\v\f\x1c-\x1e\x85\u2028\u2029]")


class LinePreview(BaseModel):
    old_start_line: int
    new_start_line: int
    old_lines: list[str]
    new_lines: list[str]


class ReplacementResult(BaseModel):
    content: str
    previews: list[LinePreview]
    lines_changed: int


def replace_with_preview(
    content: str,
    old_str: str,
    new_str: str,
    count: int,
) -> ReplacementResult:
    common_prefix_length = 0
    for old_character, new_character in zip(old_str, new_str, strict=False):
        if old_character != new_character:
            break
        common_prefix_length += 1

    common_suffix_length = 0
    max_common_suffix = min(len(old_str), len(new_str)) - common_prefix_length
    while (
        common_suffix_length < max_common_suffix
        and old_str[-common_suffix_length - 1] == new_str[-common_suffix_length - 1]
    ):
        common_suffix_length += 1

    old_change_end = len(old_str) - common_suffix_length
    new_change_end = len(new_str) - common_suffix_length
    updated = content.replace(old_str, new_str, count)
    windows: list[tuple[int, int, int, int]] = []
    old_spans = _change_spans(
        content,
        old_str,
        count,
        common_prefix_length,
        old_change_end,
        0,
    )
    new_spans = _change_spans(
        content,
        old_str,
        count,
        common_prefix_length,
        new_change_end,
        len(new_str) - len(old_str),
    )
    for (old_start, old_end), (new_start, new_end) in zip(
        _line_windows(content, old_spans),
        _line_windows(updated, new_spans),
        strict=True,
    ):
        if windows and old_start <= windows[-1][1] and new_start <= windows[-1][3]:
            previous = windows[-1]
            windows[-1] = (
                previous[0],
                max(previous[1], old_end),
                previous[2],
                max(previous[3], new_end),
            )
        else:
            windows.append((old_start, old_end, new_start, new_end))

    previews: list[LinePreview] = []
    old_line = 1
    new_line = 1
    old_cursor = 0
    new_cursor = 0
    for old_start, old_end, new_start, new_end in windows:
        old_line += sum(1 for _ in LINE_BREAK.finditer(content, old_cursor, old_start))
        new_line += sum(1 for _ in LINE_BREAK.finditer(updated, new_cursor, new_start))
        old_lines = content[old_start:old_end].splitlines(keepends=True)
        new_lines = updated[new_start:new_end].splitlines(keepends=True)
        common_line_prefix = 0
        while (
            common_line_prefix < len(old_lines)
            and common_line_prefix < len(new_lines)
            and old_lines[common_line_prefix] == new_lines[common_line_prefix]
        ):
            common_line_prefix += 1
        common_line_suffix = 0
        while (
            common_line_suffix < len(old_lines) - common_line_prefix
            and common_line_suffix < len(new_lines) - common_line_prefix
            and old_lines[-common_line_suffix - 1] == new_lines[-common_line_suffix - 1]
        ):
            common_line_suffix += 1
        old_stop = len(old_lines) - common_line_suffix
        new_stop = len(new_lines) - common_line_suffix
        changed_old_lines = old_lines[common_line_prefix:old_stop]
        changed_new_lines = new_lines[common_line_prefix:new_stop]
        previews.append(
            LinePreview(
                old_start_line=(
                    old_line + common_line_prefix
                    if changed_old_lines
                    else max(1, old_line + common_line_prefix - 1)
                ),
                new_start_line=(
                    new_line + common_line_prefix
                    if changed_new_lines
                    else max(1, new_line + common_line_prefix - 1)
                ),
                old_lines=changed_old_lines,
                new_lines=changed_new_lines,
            )
        )
        old_line += sum(1 for _ in LINE_BREAK.finditer(content, old_start, old_end))
        new_line += sum(1 for _ in LINE_BREAK.finditer(updated, new_start, new_end))
        old_cursor = old_end
        new_cursor = new_end

    return ReplacementResult(
        content=updated,
        previews=previews,
        lines_changed=sum(
            max(len(preview.old_lines), len(preview.new_lines)) for preview in previews
        ),
    )


def _change_spans(
    content: str,
    old_str: str,
    count: int,
    change_start: int,
    change_end: int,
    length_delta: int,
) -> Iterator[tuple[int, int]]:
    search_start = 0
    accumulated_delta = 0
    for _ in range(count):
        match_start = content.find(old_str, search_start)
        mapped_start = match_start + accumulated_delta
        yield mapped_start + change_start, mapped_start + change_end
        search_start = match_start + len(old_str)
        accumulated_delta += length_delta


def _line_windows(
    content: str,
    spans: Iterator[tuple[int, int]],
) -> Iterator[tuple[int, int]]:
    breaks = iter(LINE_BREAK.finditer(content))
    previous_line_start = 0
    line_start = 0
    next_break = next(breaks, None)
    line_end = next_break.end() if next_break is not None else len(content)

    for span_start, span_end in spans:
        if (
            span_start == span_end == len(content)
            and next_break is not None
            and next_break.end() == len(content)
            and (not content or content[-1] != "\r")
        ):
            yield len(content), len(content)
            continue
        while line_end <= span_start and line_end < len(content):
            previous_line_start = line_start
            line_start = line_end
            next_break = next(breaks, None)
            line_end = next_break.end() if next_break is not None else len(content)
        window_start = (
            previous_line_start
            if span_start > 0 and content[span_start - 1] == "\r"
            else line_start
        )
        while line_end <= span_end and line_end < len(content):
            previous_line_start = line_start
            line_start = line_end
            next_break = next(breaks, None)
            line_end = next_break.end() if next_break is not None else len(content)
        yield window_start, line_end
