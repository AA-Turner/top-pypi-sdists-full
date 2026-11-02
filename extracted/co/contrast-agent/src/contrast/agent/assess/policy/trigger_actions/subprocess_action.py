# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.utils.string_utils import ensure_string

COMMON_SHELLS = [
    "sh",
    "csh",
    "tcsh",
    "scsh",
    "ksh",
    "dash",
    "bash",
    "zsh",
    "fish",
    # windows shells
    "cmd",
    "pwsh",
    "powershell",
]


class SubprocessAction(DefaultAction):
    """
    Some functions in the subprocess module behave differently (from a security
    perspective) depending on several factors:
    - the value of the `shell` argument
    - whether arguments are passed as a string or as a list
    - if the command being executed is particularly dangerous (ie invokes a shell)

    If `shell` is explicitly set to True, all arguments are potentially vulnerable,
    whether they appear as a string or list.

    If `shell` is False (the default) and arguments are passed as a string, the entire
    string is potentially vulnerable. If arguments are passed as a list, only the first
    element is potentially vulnerable - unless the first element (or the `executable`
    argument, which takes precedence over the first element as the program that is
    actually run on POSIX) is a common shell command or a Windows batch file, in which
    case all arguments are potentially vulnerable.
    """

    unwind_source = False

    def extract_source(self, source, args, kwargs):
        if (
            kwargs.get("shell") is not True
            and isinstance(source, (list, tuple))
            and len(source) > 0
        ):
            executable = kwargs.get("executable") or source[0]
            command = ensure_string(executable)
            base_command = os.path.basename(command).lower()
            is_shell_command = base_command.removesuffix(".exe") in COMMON_SHELLS
            # Windows may invoke batch files in a system shell, per https://github.com/python/cpython/issues/114539
            is_windows_batch_file = os.name == "nt" and base_command.endswith(
                (".bat", ".cmd")
            )
            if not is_shell_command and not is_windows_batch_file:
                # Not using the shell, so only the command is potentially unsafe.
                # The rest of the arguments cannot exploit cmdi.
                return command
        return source
