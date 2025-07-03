import random

from deepteam.attacks import BaseAttack
from deepteam.attacks.single_turn.semantic_manipulation.template import (
    LinguisticConfusionTemplate,
)


class LinguisticConfusion(BaseAttack):
    def __init__(self, weight: int = 2, max_retries: int = 3):
        self.weight = (
            weight  # Higher weight since this is a sophisticated attack
        )
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with linguistic confusion techniques.
        Uses max_retries to attempt different confusion methods if enhancement fails.
        """
        enhancement_methods = [
            LinguisticConfusionTemplate.enhance_semantic_ambiguity,
            LinguisticConfusionTemplate.enhance_syntactic_variation,
            LinguisticConfusionTemplate.enhance_contextual_reframing,
            LinguisticConfusionTemplate.enhance_linguistic_obfuscation,
            LinguisticConfusionTemplate.enhance_meaning_distortion,
            LinguisticConfusionTemplate.enhance_universal_confusion_bridge,
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
        return "Linguistic Confusion"
