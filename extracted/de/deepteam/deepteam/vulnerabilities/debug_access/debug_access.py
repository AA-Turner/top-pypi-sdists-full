from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.debug_access import DebugAccessType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

DebugAccessLiteral = Literal[
    "debug_mode_bypass",
    "development_endpoint_access",
    "administrative_interface_exposure",
]


class DebugAccess(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[DebugAccessLiteral]] = [
            type.value for type in DebugAccessType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=DebugAccessType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "Debug Access"
