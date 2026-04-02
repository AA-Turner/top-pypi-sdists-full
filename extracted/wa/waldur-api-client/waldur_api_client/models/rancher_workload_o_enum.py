from enum import Enum


class RancherWorkloadOEnum(str, Enum):
    CLUSTER_NAME = "cluster_name"
    NAME = "name"
    NAMESPACE_NAME = "namespace_name"
    PROJECT_NAME = "project_name"
    VALUE_0 = "-cluster_name"
    VALUE_1 = "-name"
    VALUE_2 = "-namespace_name"
    VALUE_3 = "-project_name"

    def __str__(self) -> str:
        return str(self.value)
