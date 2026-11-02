from enum import Enum


class ListRunAssetsResponse200AssetsItemKind(str, Enum):
    DATATABLE = "datatable"
    DBT = "dbt"
    DUCKLAKE = "ducklake"
    RESOURCE = "resource"
    S3OBJECT = "s3object"
    VOLUME = "volume"

    def __str__(self) -> str:
        return str(self.value)
