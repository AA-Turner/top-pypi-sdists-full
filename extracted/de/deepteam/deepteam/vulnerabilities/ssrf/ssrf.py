from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.ssrf import SSRFType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

SSRFLiteral = Literal[
    "internal_service_access",
    "cloud_metadata_access",
    "port_scanning",
]


class SSRF(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[SSRFLiteral]] = [type.value for type in SSRFType],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=SSRFType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "SSRF"
