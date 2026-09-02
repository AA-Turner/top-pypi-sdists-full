from __future__ import annotations

from typing import TypedDict


class Frame(TypedDict):
    file: str
    lineno: int
    funcname: str
    source_line: str


def format_traceback(exc_class: str, exc_message: str, frames: list[Frame]) -> str:
    out = ["Traceback (most recent call last):"]
    for f in frames:
        out.append(f'  File "{f["file"]}", line {f["lineno"]}, in {f["funcname"]}')
        if f["source_line"]:
            out.append(f"    {f['source_line']}")
    out.append(f"{exc_class}: {exc_message}")
    return "\n".join(out) + "\n"


def _single_frame(file: str, lineno: int, funcname: str, source_line: str) -> list[Frame]:
    return [
        Frame(file=file, lineno=lineno, funcname=funcname, source_line=source_line),
    ]


def file_not_found(
    path: str,
    source_line: str = "open('...')",
    file: str = "<stdin>",
    lineno: int = 1,
    funcname: str = "<module>",
) -> str:
    msg = f"[Errno 2] No such file or directory: '{path}'"
    return format_traceback(
        "FileNotFoundError",
        msg,
        _single_frame(file, lineno, funcname, source_line),
    )


def is_a_directory(
    path: str,
    source_line: str = "open('...')",
    file: str = "<stdin>",
    lineno: int = 1,
    funcname: str = "<module>",
) -> str:
    msg = f"[Errno 21] Is a directory: '{path}'"
    return format_traceback(
        "IsADirectoryError",
        msg,
        _single_frame(file, lineno, funcname, source_line),
    )


def not_a_directory(
    path: str,
    source_line: str = "open('...')",
    file: str = "<stdin>",
    lineno: int = 1,
    funcname: str = "<module>",
) -> str:
    msg = f"[Errno 20] Not a directory: '{path}'"
    return format_traceback(
        "NotADirectoryError",
        msg,
        _single_frame(file, lineno, funcname, source_line),
    )


def permission_denied(
    path: str,
    source_line: str = "open('...')",
    file: str = "<stdin>",
    lineno: int = 1,
    funcname: str = "<module>",
) -> str:
    msg = f"[Errno 13] Permission denied: '{path}'"
    return format_traceback(
        "PermissionError",
        msg,
        _single_frame(file, lineno, funcname, source_line),
    )


def file_exists(
    path: str,
    source_line: str = "open('...')",
    file: str = "<stdin>",
    lineno: int = 1,
    funcname: str = "<module>",
) -> str:
    msg = f"[Errno 17] File exists: '{path}'"
    return format_traceback(
        "FileExistsError",
        msg,
        _single_frame(file, lineno, funcname, source_line),
    )
