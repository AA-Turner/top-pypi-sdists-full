# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections.abc import Mapping
import shlex
from typing import Callable

from contrast_fireball import OtelAttributes, SpanType

from contrast.agent.policy.handlers import EventDict


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
        shell = args.get(shell_param_location, False)
        command = args.get(cmd_param_location) or ""
        arguments = args.get(args_param_location)
        # The logic here comes from subprocess.Popen._execute_child, specifically
        # https://github.com/python/cpython/blob/c489934/Lib/subprocess.py#L1819-L1838
        if shell:
            if not command:
                command = "/bin/sh"
            command += " -c"
        if isinstance(arguments, str):
            arguments = shlex.quote(arguments)
        if isinstance(arguments, (list, tuple)):
            arguments = shlex.join(arguments)
        if command_string := f"{command} {arguments or ''}".strip():
            return {"cmd": command_string}
        return {}

    return SpanType.HostCommandExec, observe_span_attrs, None
