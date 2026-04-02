from enum import Enum


class RancherNamespaceOEnum(str, Enum):
    CLUSTER_NAME = "cluster_name"
    NAME = "name"
    PROJECT_NAME = "project_name"
    VALUE_0 = "-cluster_name"
    VALUE_1 = "-name"
    VALUE_2 = "-project_name"

    def __str__(self) -> str:
        return str(self.value)
