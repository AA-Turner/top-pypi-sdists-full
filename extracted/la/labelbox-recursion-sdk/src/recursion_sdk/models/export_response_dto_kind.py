from enum import StrEnum

class ExportResponseDtoKind(StrEnum):
    EVALUATION_RESULTS = "evaluation_results"
    PROBLEM_ARCHIVE = "problem_archive"

    def __str__(self) -> str:
        return str(self.value)
