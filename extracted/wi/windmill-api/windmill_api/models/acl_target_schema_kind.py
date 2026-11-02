from enum import Enum


class AclTargetSchemaKind(str, Enum):
    SCHEMA = "schema"

    def __str__(self) -> str:
        return str(self.value)
