# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
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
    element is potentially vulnerable - unless the first element is a common shell
    command, in which case all arguments are potentially vulnerable.
    """

    unwind_source = False

    def extract_source(self, source, args, kwargs):
        return (
            source[0]
            if kwargs.get("shell") is not True
            and isinstance(source, (list, tuple))
            and len(source) > 0
            and ensure_string(source[0]) not in COMMON_SHELLS
            else source
        )
