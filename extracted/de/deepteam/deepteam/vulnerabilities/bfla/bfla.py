from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.bfla import BFLAType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

BFLALiteral = Literal[
    "privilege_escalation",
    "function_bypass",
    "authorization_bypass",
]


class BFLA(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[BFLALiteral]] = [type.value for type in BFLAType],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=BFLAType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "BFLA"
