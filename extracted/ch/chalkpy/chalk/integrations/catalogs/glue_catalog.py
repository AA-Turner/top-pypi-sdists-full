from __future__ import annotations

from typing import TYPE_CHECKING, Any

from chalk.integrations.catalogs.base_catalog import BaseCatalog

if TYPE_CHECKING:
    import pyarrow

    from chalk.client import DatasetRevision


def _pyarrow_type_to_hive_type_or_throw(pyarrow_type: pyarrow.DataType) -> str:
    import pyarrow

    if pyarrow_type == pyarrow.utf8():
        return "string"
    elif pyarrow_type == pyarrow.large_utf8():
        return "string"
    elif pyarrow_type == pyarrow.int32():
        return "int"
    elif pyarrow_type == pyarrow.int64():
        return "bigint"
    elif pyarrow_type == pyarrow.uint32():
        return "int"
    elif pyarrow_type == pyarrow.uint64():
        return "bigint"
    elif pyarrow_type == pyarrow.float32():
        return "float"
    elif pyarrow_type == pyarrow.float64():
        return "double"
    elif isinstance(pyarrow_type, pyarrow.TimestampType):
        return "timestamp"
    elif pyarrow_type == pyarrow.date32():
        return "date"
    elif pyarrow_type == pyarrow.bool_():
        return "boolean"
    elif pyarrow_type == pyarrow.Decimal128Type:
        return "decimal"
    elif pyarrow_type == pyarrow.ListType:
        return "array"
    elif pyarrow_type == pyarrow.StructType:
        return "struct"
    elif pyarrow_type == pyarrow.MapType:
        return "map"
    else:
        raise ValueError(f"Unsupported Arrow type '{pyarrow_type}' for conversion to Hive type")


def _convert_arrow_schema_to_athena_schema(arrow_schema: pyarrow.Schema) -> list[dict]:
    athena_schema = []
    for field in list(arrow_schema):
        try:
            type = _pyarrow_type_to_hive_type_or_throw(field.type)
            athena_schema.append(
                {
                    "Name": field.name,
                    "Type": type,
                }
            )
        except ValueError as e:
            raise ValueError(f"Error converting field {field.name} to Athena schema") from e

    return athena_schema


class GlueCatalog(BaseCatalog):
    """
    A class to represent an AWS Glue Catalog.

    Attributes:
        name (str): The name of the Glue Catalog.
        skip_default_database (bool): Whether to skip the default database. Defaults to True.
        aws_role_arn (str | None): The AWS role ARN to assume for accessing the Glue Catalog.
        aws_region (str | None): The AWS region where the Glue Catalog is located.
        aws_profile (str | None): The AWS profile to use for accessing the Glue Catalog.
        aws_secret_key_id (str | None): The AWS secret key ID for accessing the Glue Catalog.
        aws_secret_access_key (str | None): The AWS secret access key for accessing the Glue Catalog.
        aws_session_token (str | None): The AWS session token for accessing the Glue Catalog.
        endpoint_url (str | None): The endpoint URL for the Glue Catalog.
        catalog_id (str | None): The catalog ID for the Glue Catalog.
        cache_ttl (int): The cache time-to-live in seconds. Defaults to 600.

    Methods:
        __init__: Initializes the GlueCatalog with the provided parameters.
    """

    def __init__(
        self,
        name: str,
        skip_default_database: bool = True,
        aws_role_arn: str | None = None,
        aws_region: str | None = None,
        aws_profile: str | None = None,
        aws_secret_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        endpoint_url: str | None = None,
        catalog_id: str | None = None,
        cache_ttl: int = 600,
        glue_client: Any | None = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.cache_ttl = cache_ttl
        self.skip_default_database = skip_default_database
        self.aws_role_arn = aws_role_arn
        self.aws_region = aws_region
        self.aws_profile = aws_profile
        self.aws_secret_key_id = aws_secret_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.endpoint_url = endpoint_url
        self.catalog_id = catalog_id
        self.glue_client = glue_client

    def to_scan_options(self):
        return {
            "catalog_type": "glue",
            "name": self.name,
            "aws_role_arn": self.aws_role_arn,
            "aws_region": self.aws_region,
            "aws_profile": self.aws_profile,
            "endpoint_url": self.endpoint_url,
            "catalog_id": self.catalog_id,
        }

    def write_to_catalog(
        self,
        revision: DatasetRevision,
        destination: str,
    ):
        import boto3

        # Destination must of the form 'database_name.table_name'
        database_name, table_name = destination.split(".")

        glue_client = self.glue_client or boto3.client("glue")

        glue_client.create_table(
            DatabaseName=database_name,
            TableInput={
                "Name": table_name,
                "StorageDescriptor": {
                    "Columns": _convert_arrow_schema_to_athena_schema(revision.arrow_schema()),
                    "Location": revision.output_uris,
                    "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
