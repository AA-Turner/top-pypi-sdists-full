from enum import Enum


class AnonymousChatFeedbackOEnum(str, Enum):
    LLM_RESOLUTION_SCORE = "llm_resolution_score"
    SCORE = "score"
    SUBMITTED_AT = "submitted_at"
    VALUE_0 = "-llm_resolution_score"
    VALUE_1 = "-score"
    VALUE_2 = "-submitted_at"

    def __str__(self) -> str:
        return str(self.value)
