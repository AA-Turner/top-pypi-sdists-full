from enum import Enum


class SoftwareCatalogOEnum(str, Enum):
    CATALOG_TYPE = "catalog_type"
    CREATED = "created"
    MODIFIED = "modified"
    NAME = "name"
    VALUE_0 = "-catalog_type"
    VALUE_1 = "-created"
    VALUE_2 = "-modified"
    VALUE_3 = "-name"
    VALUE_4 = "-version"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
