from enum import Enum


class ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase(str, Enum):
    FAIL = "FAIL"
    OK = "OK"
    SKIP = "SKIP"

    def __str__(self) -> str:
        return str(self.value)
