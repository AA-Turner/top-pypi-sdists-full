from enum import Enum


class ApplyDatatableAclJsonBodyChangeType0Type(str, Enum):
    SET_OWNER = "set_owner"

    def __str__(self) -> str:
        return str(self.value)
