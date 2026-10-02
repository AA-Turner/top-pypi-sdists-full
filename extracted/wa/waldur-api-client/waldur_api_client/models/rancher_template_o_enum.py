from enum import Enum


class RancherTemplateOEnum(str, Enum):
    CATALOG_NAME = "catalog_name"
    NAME = "name"
    VALUE_0 = "-catalog_name"
    VALUE_1 = "-name"

    def __str__(self) -> str:
        return str(self.value)
