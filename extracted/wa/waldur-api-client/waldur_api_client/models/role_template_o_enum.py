from enum import Enum


class RoleTemplateOEnum(str, Enum):
    NAME = "name"
    SCOPE_TYPE = "scope_type"
    VALUE_0 = "-name"
    VALUE_1 = "-scope_type"

    def __str__(self) -> str:
        return str(self.value)
