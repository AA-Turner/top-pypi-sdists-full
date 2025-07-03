from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.shell_injection import ShellInjectionType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

ShellInjectionLiteral = Literal[
    "command_injection",
    "system_command_execution",
    "shell_escape_sequences",
]


class ShellInjection(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[ShellInjectionLiteral]] = [
            type.value for type in ShellInjectionType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=ShellInjectionType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "Shell Injection"
