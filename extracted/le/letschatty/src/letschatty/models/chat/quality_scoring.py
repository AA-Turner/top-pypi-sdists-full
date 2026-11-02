
from enum import StrEnum
from typing import List, Dict

class QualityScore(StrEnum):
    BAD = "bad"
    GOOD = "good"
    NEUTRAL = "neutral"

    @classmethod
    def get_all_values(cls) -> List[str]:
        return [QualityScore.BAD.value, QualityScore.GOOD.value, QualityScore.NEUTRAL.value]

    @classmethod
    def get_all_values_with_name_for_attributes(cls) -> List[Dict[str, str]]:
        return [{"name": "Mala calidad", "id": QualityScore.BAD.value}, {"name": "Buena calidad", "id": QualityScore.GOOD.value}, {"name": "Neutral", "id": QualityScore.NEUTRAL.value}]
