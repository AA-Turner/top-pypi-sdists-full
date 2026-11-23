from enum import Enum


class ContainerV2ChangeAction(str, Enum):
    DELETE = "delete"
    PAUSE = "pause"
    RENAME = "rename"
    RESUME = "resume"
    START = "start"
    STOP = "stop"
    UPDATE_RESOURCES = "update_resources"
    UPDATE_TIMEOUT_POLICIES = "update_timeout_policies"

    def __str__(self) -> str:
        return str(self.value)
