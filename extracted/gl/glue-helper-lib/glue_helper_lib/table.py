import dataclasses
import typing
import pyspark.sql


class S3Uri:
    def __init__(self, path: str) -> None:
        self._path = path
        if not path.startswith("s3://"):
            raise ValueError("path should start with 's3://'")

    def __str__(self) -> str:
        return self._path


class GlueTable(typing.Protocol):
    def write(self, df: pyspark.sql.DataFrame):
        ...

    def read(
        self, spark_session: pyspark.sql.SparkSession
    ) -> pyspark.sql.DataFrame:
        ...


@dataclasses.dataclass
class GlueCatalogArguments:
    database: str
    table: str


class StorageLocation:
    def __init__(self, path: S3Uri):
        self._path = path

    def __str__(self) -> str:
        return str(self._path)


class ParquetTable:
    def __init__(
        self,
        storage_location: StorageLocation,
        partition_columns: typing.Optional[typing.List[str]] = None,
        compression: typing.Optional[str] = None,
    ) -> None:
        super().__init__()
        self._storage_location = storage_location
        self._partition_columns = partition_columns
        self._compression = compression

    def write(self, df: pyspark.sql.DataFrame):
        df.write.parquet(
            str(self._storage_location),
            mode="overwrite",
            partitionBy=self._partition_columns,
            compression=self._compression,
        )

    def read(
        self, spark_session: pyspark.sql.SparkSession
    ) -> pyspark.sql.DataFrame:
        return spark_session.read.parquet(str(self._storage_location))
