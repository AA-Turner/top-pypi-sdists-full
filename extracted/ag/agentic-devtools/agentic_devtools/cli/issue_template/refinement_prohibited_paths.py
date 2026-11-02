"""Pure parsing of explicit prohibited paths in refinement candidates."""

import re as _re

from .refinement_body_sections import find_refinement_section_spans as _spans
from .refinement_paths import normalize_refinement_path as _normalize


def parse_prohibited_refinement_paths(body: str) -> dict[str, list[str] | list[dict[str, str | None]]]:
    """Return sorted unique paths and per-line diagnostics, without authorizing paths."""
    messages = {
        "repeated_prohibited_section": "Out of Scope must appear at most once.",
        "malformed_prohibited_entry": "Out of Scope lines must be Path or Note entries in the section syntax.",
        "invalid_prohibited_path": "Prohibited path is not a valid repository-relative path.",
    }

    def _fence_after(line: str, fence: str) -> str:
        closing = _re.fullmatch(r" {0,3}(`{3,}|~{3,})[ \t]*", line)
        opening = _re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
        closed = closing and closing[1][0] == fence[:1] and len(closing[1]) >= len(fence)
        opened = opening[1] if opening and not (opening[1][0] == "`" and "`" in opening[2]) else ""
        return ("" if closed else fence) if fence else opened

    sections = _spans(body, "Out of Scope")
    paths: set[str] = set()
    errors: list[tuple[str, str | None]] = []
    if len(sections) > 1:
        errors.append(("repeated_prohibited_section", None))
    elif sections:
        start, end, syntax = sections[0]
        lines = _re.split(r"\r\n|\r|\n", _re.sub(r"(?:\r\n|\r|\n)\Z", "", body))
        path_pattern, note_prefix, delimiters = (
            (r"- Path: `([^`]+)`", "- Note: ", ("`",))
            if syntax == "markdown"
            else (r"\* Path: \{\{([^{}]+)\}\}", "* Note: ", ("{{", "}}"))
        )
        fence = ""
        for line in lines[start + 1 : end]:
            previous_fence, fence = fence, _fence_after(line, fence)
            line = line.rstrip(" \t")
            if previous_fence or fence or not line.strip():
                continue
            path = _re.fullmatch(path_pattern, line)
            if path:
                normalized, error = _normalize(path[1])
                if error is not None:
                    errors.append(("invalid_prohibited_path", path[1]))
                else:
                    assert normalized is not None
                    paths.add(normalized)
            elif not (
                line.startswith(note_prefix)
                and line[len(note_prefix) :].strip()
                and not any(delimiter in line for delimiter in delimiters)
            ):
                errors.append(("malformed_prohibited_entry", None))
    return {
        "paths": sorted(paths),
        "errors": [
            {"code": code, "path": path, "message": messages[code]}
            for code, path in sorted(errors, key=lambda error: (error[0], error[1] or "", messages[error[0]]))
        ],
    }
