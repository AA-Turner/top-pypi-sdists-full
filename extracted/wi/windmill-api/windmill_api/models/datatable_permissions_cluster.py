from enum import Enum


class DatatablePermissionsCluster(str, Enum):
    EXTERNAL_INSTANCE = "external_instance"
    INSTANCE = "instance"

    def __str__(self) -> str:
        return str(self.value)
