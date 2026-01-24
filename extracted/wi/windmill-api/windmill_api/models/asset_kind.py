from enum import Enum


class AssetKind(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"
    RESOURCE = "resource"
    S3OBJECT = "s3object"

    def __str__(self) -> str:
        return str(self.value)
