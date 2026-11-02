from enum import Enum


class TokenSavingMethodMethod(str, Enum):
    GIT_DIFF = "git_diff"
    JSON_ARRAY = "json_array"
    LOG = "log"
    SEARCH_RESULTS = "search_results"

    def __str__(self) -> str:
        return str(self.value)
