# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
import os
from typing import Callable

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent.policy.handlers import EventDict


def observe_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[
    SpanType,
    Callable[[Mapping[str, object], object], OtelAttributes],
    Callable[[Mapping[str, object]], str | None],
]:
    file_param_location = event_dict.get("file", "")
    flags_param_location = event_dict.get("flags", "")
    is_dbm = event_dict.get("dbm", False)

    if not file_param_location or not flags_param_location:
        raise ValueError(
            "Event must specify both 'file' and 'flags' parameter locations."
        )

    def skip_check(args: Mapping[str, object]) -> str | None:
        file_path = args.get(file_param_location, "")
        if not file_path:
            return "empty file path"
        if isinstance(file_path, int):
            return "path is a file descriptor"
        return None

    OS_FLAG_MASK = os.O_RDONLY | os.O_WRONLY | os.O_RDWR

    def observe_span_attrs(args: Mapping[str, object], result: object):
        file_path = args.get(file_param_location, "")
        fs_path = os.fspath(file_path)
        abs_file_path = os.path.abspath(fs_path)
        if isinstance(abs_file_path, bytes):
            abs_file_path = abs_file_path.decode("utf-8", errors="replace")

        flags = args.get(flags_param_location, "")
        str_flags = ""
        if isinstance(flags, int):
            masked_flags = flags & OS_FLAG_MASK
            if masked_flags == os.O_RDONLY:
                str_flags = "o_rdonly"
            elif masked_flags == os.O_WRONLY:
                str_flags = "o_wronly"
            elif masked_flags == os.O_RDWR:
                str_flags = "o_rdwr"
        if isinstance(flags, str):
            if "+" in flags or flags in ("c", "n"):
                str_flags = "o_rdwr"
            elif "r" in flags:
                str_flags = "o_rdonly"
            elif "w" in flags or "a" in flags or "x" in flags:
                str_flags = "o_wronly"
                # special case: https://docs.python.org/3/library/dbm.html#dbm.open
                if is_dbm and flags == "w":
                    str_flags = "o_rdwr"
        if not str_flags:
            raise ValueError(f"Unsupported file open mode: {flags}.")

        return {"file.open.path": abs_file_path, "file.open.flags": str_flags}

    return SpanType.FileOpenCreate, observe_span_attrs, skip_check
