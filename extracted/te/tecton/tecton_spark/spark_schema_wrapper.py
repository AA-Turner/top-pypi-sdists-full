import json
import logging
from typing import List

from pyspark.sql.types import DataType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType

from tecton_proto.common.spark_schema__client_pb2 import SparkSchema


logger = logging.getLogger(__name__)


class SparkSchemaWrapper:
    """
    Wrapper around Spark schema (StructType).
    """

    def __init__(self, schema: StructType) -> None:
        """
        Creates a new SparkSchemaWrapper.

        :param schema: DataFrame schema.
        """
        self._schema = schema

    def to_proto(self) -> SparkSchema:
        return self.from_spark_schema(self._schema)

    @classmethod
    def from_spark_schema(cls, schema: StructType) -> SparkSchema:
        proto = SparkSchema()
        spark_dict = schema.jsonValue()
        for field in spark_dict["fields"]:
            proto_field = proto.fields.add()
            proto_field.name = field["name"]
            proto_field.structfield_json = json.dumps(field)
        return proto

    @classmethod
    def from_proto(cls, proto: SparkSchema) -> "SparkSchemaWrapper":
        s = StructType()
        for field in proto.fields:
            field_schema = StructField.fromJson(json.loads(field.structfield_json))
            s.add(field_schema)
        return SparkSchemaWrapper(s)

    def unwrap(self) -> StructType:
        return self._schema

    def column_names(self) -> List[str]:
        return [f["name"] for f in self._schema.jsonValue()["fields"]]

    def spark_type(self, column: str) -> DataType:
        return self._schema[column].dataType

    def column_name_types(self):
        return [(c, self.spark_type(c)) for c in self.column_names()]
