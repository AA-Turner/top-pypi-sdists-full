# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from contrast_fireball import OtelAttributes, SpanType

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

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


def _str_mode_permissions(flags: str, is_dbm: bool) -> tuple[str, ...]:
    if is_dbm:
        # https://docs.python.org/3/library/dbm.html#dbm.open
        flags = flags[:1]
        if flags == "r":
            return ("file-read",)
        if flags == "w":
            return ("file-read", "file-write")
        if flags in ("c", "n"):
            return ("file-read", "file-create", "file-write")
        return ()
    permissions: list[str] = []
    if "r" in flags or "+" in flags:
        permissions.append("file-read")
    if "w" in flags or "a" in flags or "x" in flags:
        # w, a and x may all create the file. We can't know whether it already exists
        # without an extra syscall, so we report create for any mode that can.
        permissions.append("file-create")
        permissions.append("file-write")
    elif "+" in flags:
        permissions.append("file-write")
    return tuple(permissions)


def _int_flags_permissions(flags: int) -> tuple[str, ...]:
    permissions: list[str] = []
    access_mode = flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)
    if access_mode in (os.O_RDONLY, os.O_RDWR):
        permissions.append("file-read")
    if flags & os.O_CREAT:
        permissions.append("file-create")
    if access_mode in (os.O_WRONLY, os.O_RDWR) or flags & os.O_TRUNC:
        permissions.append("file-write")
    return tuple(permissions)


def shield_permissions_builder(
    event_dict: EventDict,
) -> Callable[[Mapping[str, object]], tuple[str, ...]]:
    """
    Builds a function that maps the arguments of an open call to the CVE shield
    permissions (capabilities) it uses: file-create, file-read and/or file-write,
    depending on the open mode/flags.
    """
    file_param_location = event_dict.get("file", "")
    flags_param_location = event_dict.get("flags", "")
    is_dbm = event_dict.get("dbm", False)

    if not file_param_location or not flags_param_location:
        raise ValueError(
            "Event must specify both 'file' and 'flags' parameter locations."
        )

    def shield_permissions(args: Mapping[str, object]) -> tuple[str, ...]:
        file_path = args.get(file_param_location, "")
        # opening a file descriptor doesn't access any new file
        if not file_path or isinstance(file_path, int):
            return ()
        flags = args.get(flags_param_location, "")
        if isinstance(flags, int):
            return _int_flags_permissions(flags)
        if isinstance(flags, str):
            return _str_mode_permissions(flags, is_dbm)
        return ()

    return shield_permissions
