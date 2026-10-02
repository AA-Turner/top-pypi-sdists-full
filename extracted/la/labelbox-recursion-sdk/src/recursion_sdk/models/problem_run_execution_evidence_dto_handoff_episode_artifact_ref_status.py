from enum import StrEnum

class ProblemRunExecutionEvidenceDtoHandoffEpisodeArtifactRefStatus(StrEnum):
    MISSING = "missing"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
