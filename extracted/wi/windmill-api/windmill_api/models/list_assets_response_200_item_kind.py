from enum import Enum


class ListAssetsResponse200ItemKind(str, Enum):
    DUCKLAKE = "ducklake"
    RESOURCE = "resource"
    S3OBJECT = "s3object"

    def __str__(self) -> str:
        return str(self.value)
