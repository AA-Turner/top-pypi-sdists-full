import random

from deepteam.attacks import BaseAttack
from deepteam.attacks.single_turn.permission_escalation.template import (
    PermissionEscalationTemplate,
)


class PermissionEscalation(BaseAttack):
    def __init__(self, weight: int = 2, max_retries: int = 3):
        self.weight = (
            weight  # Higher weight since this is a sophisticated attack
        )
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with role manipulation techniques.
        Uses max_retries to attempt different manipulation methods if enhancement fails.
        """
        enhancement_methods = [
            PermissionEscalationTemplate.enhance_identity_shift,
            PermissionEscalationTemplate.enhance_capability_expansion,
            PermissionEscalationTemplate.enhance_contextual_adaptation,
            PermissionEscalationTemplate.enhance_authority_elevation,
            PermissionEscalationTemplate.enhance_functional_transformation,
            PermissionEscalationTemplate.enhance_universal_persona,
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
        return "Permission Escalation"
