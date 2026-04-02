from enum import Enum


class CatalogTypeEnum(str, Enum):
    BINARY_RUNTIME = "binary_runtime"
    PACKAGE_MANAGER = "package_manager"
    SOURCE_PACKAGE = "source_package"

    def __str__(self) -> str:
        return str(self.value)
