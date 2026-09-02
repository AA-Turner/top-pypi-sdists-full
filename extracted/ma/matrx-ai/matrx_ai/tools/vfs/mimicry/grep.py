from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel


class GrepOpts(BaseModel):
    show_filename: bool = False
    show_lineno: bool = False
    count_only: bool = False
    files_with_matches: bool = False
    invert_match: bool = False
    before_context: int = 0
    after_context: int = 0


class GrepMatch(TypedDict):
    path: str
    lineno: int
    line: str
    is_match: bool  # False for context lines


class GrepGroup(TypedDict):
    matches: list[GrepMatch]


def format_grep_match(path: str, lineno: int, line: str, opts: GrepOpts) -> str:
    if opts.show_filename and opts.show_lineno:
        return f"{path}:{lineno}:{line}"
    if opts.show_filename:
        return f"{path}:{line}"
    if opts.show_lineno:
        return f"{lineno}:{line}"
    return line


def format_grep_count(path: str, count: int, opts: GrepOpts) -> str:
    if opts.show_filename:
        return f"{path}:{count}"
    return str(count)


def format_grep_filenames_only(paths: list[str]) -> str:
    if not paths:
        return ""
    return "\n".join(paths) + "\n"


def format_grep_with_context(groups: list[GrepGroup], opts: GrepOpts) -> str:
    if not groups:
        return ""
    rendered: list[str] = []
    for group in groups:
        lines: list[str] = []
        for m in group["matches"]:
            sep = ":" if m["is_match"] else "-"
            if opts.show_filename and opts.show_lineno:
                lines.append(f"{m['path']}{sep}{m['lineno']}{sep}{m['line']}")
            elif opts.show_filename:
                lines.append(f"{m['path']}{sep}{m['line']}")
            elif opts.show_lineno:
                lines.append(f"{m['lineno']}{sep}{m['line']}")
            else:
                lines.append(m["line"])
        rendered.append("\n".join(lines))
    return "\n--\n".join(rendered) + "\n"


def format_grep_binary_warning(path: str) -> str:
    return f"Binary file {path} matches"
