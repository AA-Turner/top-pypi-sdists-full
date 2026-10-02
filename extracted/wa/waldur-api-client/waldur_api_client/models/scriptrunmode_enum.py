from enum import Enum


class SCRIPTRUNMODEEnum(str, Enum):
    DOCKER = "docker"
    K8S = "k8s"

    def __str__(self) -> str:
        return str(self.value)
