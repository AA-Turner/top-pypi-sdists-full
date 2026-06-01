from typing import List, Optional
from dataclasses import dataclass

from deepteam.vulnerabilities import (
    BaseVulnerability,
)
from deepteam.attacks import BaseAttack
from deepteam.frameworks.risk_category import RiskCategory


@dataclass
class AISafetyFramework:
    name: str
    description: str
    vulnerabilities: Optional[List[BaseVulnerability]]
    attacks: Optional[List[BaseAttack]]
    risk_categories: Optional[List[RiskCategory]]
    _has_dataset: bool = False

    class Config:
        arbitrary_types_allowed = True
