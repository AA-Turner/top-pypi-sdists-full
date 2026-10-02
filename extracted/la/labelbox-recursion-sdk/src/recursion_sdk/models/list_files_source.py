from enum import StrEnum

class ListFilesSource(StrEnum):
    SESSION_OUTPUT = "session_output"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
