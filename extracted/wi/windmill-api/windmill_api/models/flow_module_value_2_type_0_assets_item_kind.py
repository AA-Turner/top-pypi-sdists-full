from enum import Enum


class FlowModuleValue2Type0AssetsItemKind(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"
    RESOURCE = "resource"
    S3OBJECT = "s3object"

    def __str__(self) -> str:
        return str(self.value)
