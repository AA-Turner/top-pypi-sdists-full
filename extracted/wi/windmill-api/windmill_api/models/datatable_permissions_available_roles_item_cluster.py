from enum import Enum


class DatatablePermissionsAvailableRolesItemCluster(str, Enum):
    EXTERNAL_INSTANCE = "external_instance"
    INSTANCE = "instance"

    def __str__(self) -> str:
        return str(self.value)
