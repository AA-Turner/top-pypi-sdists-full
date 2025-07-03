import random

from deepteam.attacks import BaseAttack
from deepteam.attacks.single_turn.input_bypass.template import (
    InputBypassTemplate,
)


class InputBypass(BaseAttack):
    def __init__(self, weight: int = 2, max_retries: int = 3):
        self.weight = weight  # Higher weight since this targets validation vulnerabilities
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with validation bypass techniques.
        Uses max_retries to attempt different bypass methods if enhancement fails.
        """
        enhancement_methods = [
            InputBypassTemplate.enhance_exception_handling,
            InputBypassTemplate.enhance_compliance_circumvention,
            InputBypassTemplate.enhance_operational_necessity,
            InputBypassTemplate.enhance_security_override,
            InputBypassTemplate.enhance_process_acceleration,
            InputBypassTemplate.enhance_universal_bypass_bridge,
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
        return "Input Bypass"
