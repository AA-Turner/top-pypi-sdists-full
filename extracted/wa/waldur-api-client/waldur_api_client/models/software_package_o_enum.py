from enum import Enum


class SoftwarePackageOEnum(str, Enum):
    CATALOG_NAME = "catalog_name"
    CATALOG_VERSION = "catalog_version"
    CREATED = "created"
    MODIFIED = "modified"
    NAME = "name"
    VALUE_0 = "-catalog_name"
    VALUE_1 = "-catalog_version"
    VALUE_2 = "-created"
    VALUE_3 = "-modified"
    VALUE_4 = "-name"

    def __str__(self) -> str:
        return str(self.value)
