from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.agentic.recursive_hijacking import (
    RecursiveHijackingType,
)
from deepteam.vulnerabilities.utils import validate_vulnerability_types

RecursiveHijackingLiteralType = Literal[
    "self_modifying_goals",
    "recursive_objective_chaining",
    "goal_propagation_attacks",
]


class RecursiveHijacking(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[RecursiveHijackingLiteralType]] = [
            type.value for type in RecursiveHijackingType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=RecursiveHijackingType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "Recursive Hijacking"
