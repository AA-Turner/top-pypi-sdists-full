import random

from deepteam.attacks import BaseAttack
from deepteam.attacks.single_turn.objective_reframing.template import (
    GoalRedirectionTemplate,
)


class GoalRedirection(BaseAttack):
    def __init__(self, weight: int = 2, max_retries: int = 3):
        self.weight = (
            weight  # Higher weight since this is a sophisticated attack
        )
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with goal redirection techniques.
        Uses max_retries to attempt different redirection methods if enhancement fails.
        """
        enhancement_methods = [
            GoalRedirectionTemplate.enhance_objective_reframing,
            GoalRedirectionTemplate.enhance_priority_manipulation,
            GoalRedirectionTemplate.enhance_constraint_redefinition,
            GoalRedirectionTemplate.enhance_purpose_alignment,
            GoalRedirectionTemplate.enhance_mission_transformation,
            GoalRedirectionTemplate.enhance_universal_goal_bridge,
        ]

        for attempt in range(self.max_retries):
            try:
                # Randomly select an enhancement method
                method = random.choice(enhancement_methods)
                enhanced_attack = method(attack)

                # Basic validation - ensure the enhancement actually modified the attack
                if enhanced_attack and len(enhanced_attack.strip()) > len(
                    attack.strip()
                ):
                    return enhanced_attack

            except Exception:
                # If enhancement fails, try again with a different method
                continue

        # If all retries fail, return the original attack
        return attack

    def get_name(self) -> str:
        return "Goal Redirection"
