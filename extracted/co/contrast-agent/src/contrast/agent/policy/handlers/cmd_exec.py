# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
import shlex
from subprocess import list2cmdline
from typing import TYPE_CHECKING

from contrast_fireball import OtelAttributes, SpanType

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contrast.agent.policy.handlers import EventDict


def windows_default_command() -> str:
    """Returns the default 'executable' for subprocess.Popen on Windows.

    Logic from https://github.com/python/cpython/blob/c489934/Lib/subprocess.py#L1535-L1537
    """
    comspec = os.environ.get("COMSPEC")
    if not comspec:
        system_root = os.environ.get("SYSTEMROOT", "")
        comspec = os.path.join(system_root, "System32", "cmd.exe")
    return comspec


def posix_arguments_printer(args) -> str:
    if isinstance(args, str):
        return shlex.quote(args)
    elif isinstance(args, (list, tuple)):
        return shlex.join(args)
    elif args is None:
        return ""
    else:
        raise TypeError("unexpected arguments type", type(args))


def windows_arguments_printer(args) -> str:
    if isinstance(args, str):
        return args
    elif isinstance(args, (bytes, os.PathLike)):
        return list2cmdline([args])
    elif args is None:
        return ""
    else:
        return list2cmdline(args)


IS_POSIX = os.name == "posix"


def observe_span_attrs_builder(
    event_dict: EventDict,
) -> tuple[SpanType, Callable[[Mapping[str, object], object], OtelAttributes], None]:
    cmd_param_location = event_dict.get("cmd", "")
    args_param_location = event_dict.get("args", "")
    shell_param_location = event_dict.get("shell", "")

    if not cmd_param_location and not args_param_location:
        raise ValueError(
            "Event must specify either 'cmd' or 'args' parameter location."
        )

    def observe_span_attrs(args: Mapping[str, object], result: object):
        default_shell_cmd = "/bin/sh" if IS_POSIX else windows_default_command()
        shell_cmd_separator = "-c" if IS_POSIX else "/c"
        arguments_printer = (
            posix_arguments_printer if IS_POSIX else windows_arguments_printer
        )

        shell = args.get(shell_param_location, False)
        command = args.get(cmd_param_location) or ""
        arguments = args.get(args_param_location)
        # The logic here comes from subprocess.Popen._execute_child, specifically
        # https://github.com/python/cpython/blob/c489934/Lib/subprocess.py#L1819-L1838 for posix
        # and
        # https://github.com/python/cpython/blob/c489934/Lib/subprocess.py#L1525-L1554 for windows
        if shell:
            if not command:
                command = default_shell_cmd
            command += f" {shell_cmd_separator}"
        arguments = arguments_printer(arguments)
        if command_string := f"{command} {arguments}".strip():
            return {"cmd": command_string}
        return {}

    return SpanType.HostCommandExec, observe_span_attrs, None
