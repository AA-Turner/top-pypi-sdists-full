# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re
from contrast.agent.protect.rule.deserialization.custom_searcher import CustomSearcher


_MODULES = [
    "os",
    "system",
    "sys",
    "subprocess",
    "__builtin__",
    "builtins",
    "globals",
    "open",
    "popen",
]

# we only need to know if the command begins with a module we care about (or "c" and
# then the module)
MODULE_REGEXES = [re.compile(rf"^c?{module}") for module in _MODULES]


class PickleSearcher(CustomSearcher):
    ID = "UD-PICKLE-1"

    NEW_LINE = "\n"
    ESCAPED_NEW_LINE = "\\n"

    def __init__(self):
        CustomSearcher.__init__(self, self.ID)

    def impact_of(self, value: str) -> int:
        impact = self.IMPACT_NONE

        split_char = (
            self.ESCAPED_NEW_LINE if self.ESCAPED_NEW_LINE in value else self.NEW_LINE
        )
        stack_commands = value.split(split_char)
        count = 0

        for command in stack_commands:
            contains_command = any(
                re.search(regex, command) for regex in MODULE_REGEXES
            )

            if contains_command:
                count += 1

                # pushing module only the stack
                if command.startswith("c"):
                    count += 1

        if count >= 3:
            impact = self.IMPACT_CRITICAL
        elif count >= 2:
            impact = self.IMPACT_HIGH

        return impact
