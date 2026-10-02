from enum import StrEnum

class ManagedAgentsApiErrorSlackConnectionMalformedCode(StrEnum):
    SLACK_CONNECTION_MALFORMED = "slack_connection_malformed"

    def __str__(self) -> str:
        return str(self.value)
