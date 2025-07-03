from typing import List, Literal, Optional

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.vulnerabilities.agentic.goal_theft import GoalTheftType
from deepteam.vulnerabilities.utils import validate_vulnerability_types

GoalTheftLiteralType = Literal[
    "escalating_probing", "cooperative_dialogue", "social_engineering"
]


class GoalTheft(BaseVulnerability):
    def __init__(
        self,
        types: Optional[List[GoalTheftLiteralType]] = [
            type.value for type in GoalTheftType
        ],
    ):
        enum_types = validate_vulnerability_types(
            self.get_name(), types=types, allowed_type=GoalTheftType
        )
        super().__init__(types=enum_types)

    def get_name(self) -> str:
        return "Goal Theft"
