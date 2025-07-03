from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.agentic.validation_bypass import (
    ValidationBypassType,
)
from deepteam.vulnerabilities.utils import validate_vulnerability_types

ValidationBypassLiteralType = Literal[
    "unverified_claims", "false_confidence", "misleading_responses"
]


class ValidationBypass(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[ValidationBypassLiteralType]] = [
            type.value for type in ValidationBypassType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=ValidationBypassType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "Validation Bypass"
