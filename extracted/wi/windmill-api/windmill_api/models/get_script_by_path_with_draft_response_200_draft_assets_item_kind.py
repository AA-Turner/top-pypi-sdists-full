from enum import Enum


class GetScriptByPathWithDraftResponse200DraftAssetsItemKind(str, Enum):
    DATATABLE = "datatable"
    DUCKLAKE = "ducklake"
    RESOURCE = "resource"
    S3OBJECT = "s3object"

    def __str__(self) -> str:
        return str(self.value)
