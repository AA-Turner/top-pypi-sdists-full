from enum import StrEnum

class TranscriptDtoSourceType(StrEnum):
    AGENT_TURN = "agent_turn"
    GRADING_RUN = "grading_run"
    PROBLEM_RUN = "problem_run"
    QA_JOB = "qa_job"
    RUBRIC_SCORE = "rubric_score"
    SYNTHESIZER_RUN = "synthesizer_run"

    def __str__(self) -> str:
        return str(self.value)
