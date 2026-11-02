from enum import Enum


class GetFilesTreeResponse200Status(str, Enum):
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
