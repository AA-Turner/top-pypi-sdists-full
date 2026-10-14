from enum import Enum


class OfferingMergeEffectEnum(str, Enum):
    DEDUPLICATED = "deduplicated"
    KEPT_ON_SOURCE = "kept_on_source"
    MOVED = "moved"
    RECOMPUTED = "recomputed"
    REWRITTEN = "rewritten"

    def __str__(self) -> str:
        return str(self.value)
