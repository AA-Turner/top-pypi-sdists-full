from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.sql_injection import SQLInjectionType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

SQLInjectionLiteral = Literal[
    "blind_sql_injection",
    "union_based_injection",
    "error_based_injection",
]


class SQLInjection(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[SQLInjectionLiteral]] = [
            type.value for type in SQLInjectionType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=SQLInjectionType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "SQL Injection"
