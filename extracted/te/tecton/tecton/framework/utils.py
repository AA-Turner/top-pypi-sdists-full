from typing import Tuple
from typing import Union

from tecton._internals import errors
from tecton._internals.secret_resolver import set_local_secret
from tecton._internals.tecton_pydantic import StrictModel
from tecton.framework import base_tecton_object
from tecton_core.id_helper import IdHelper
from tecton_proto.args import transformation__client_pb2 as transformation__args_proto
from tecton_proto.common.secret__client_pb2 import SecretReference


SPARK_SQL_MODE = "spark_sql"
PYSPARK_MODE = "pyspark"
SNOWFLAKE_SQL_MODE = "snowflake_sql"
PANDAS_MODE = "pandas"
PYTHON_MODE = "python"
BIGQUERY_SQL_MODE = "bigquery_sql"

mode_str_to_proto_enum = {
    SPARK_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL,
    PYSPARK_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK,
    SNOWFLAKE_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SNOWFLAKE_SQL,
    PANDAS_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS,
    PYTHON_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYTHON,
    BIGQUERY_SQL_MODE: transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_BIGQUERY_SQL,
}


class Secret(StrictModel):
    """A reference to a secret for use in Tecton object definitions.

    :param scope: The scope of the secret, specifying its domain or category.
    :param key: The key of the secret, uniquely identifying within its scope.
    """

    scope: str
    key: str

    def __init__(self, scope: str, key: str, **kwargs):
        super().__init__(scope=scope, key=key, **kwargs)

    def to_proto(self) -> SecretReference:
        return SecretReference(scope=self.scope, key=self.key)


def convert_secret_to_sanitized_reference(secret: Union[str, Secret]) -> SecretReference:
    """Convert a secret config to a secret reference proto. Store local secrets in the local secret store."""
    if isinstance(secret, str):
        generated_key = IdHelper.generate_string_id()
        set_local_secret(scope="LOCAL_SECRET", key=generated_key, value=secret)
        return SecretReference(scope="LOCAL_SECRET", key=generated_key, is_local=True)
    elif isinstance(secret, Secret):
        return SecretReference(scope=secret.scope, key=secret.key, is_local=False)
    else:
        msg = f"Invalid secret type: {type(secret)}"
        raise TypeError(msg)


def short_tecton_objects_repr(tecton_objects: Tuple[base_tecton_object.BaseTectonObject]) -> str:
    """Returns a shortened printable representation for a tuple of Tecton objects. Used for printing summaries."""
    short_strings = tuple(short_tecton_object_repr(obj) for obj in tecton_objects)
    return repr(short_strings)


def short_tecton_object_repr(tecton_object: base_tecton_object.BaseTectonObject) -> str:
    """Returns a shortened printable representation for a Tecton object. Used for printing summaries."""
    return f"{type(tecton_object).__name__}('{tecton_object.info.name}')"


def get_transformation_mode_name(mode_proto_enum: mode_str_to_proto_enum) -> str:
    mode_proto_enum_to_str = dict(map(reversed, mode_str_to_proto_enum.items()))
    return mode_proto_enum_to_str.get(mode_proto_enum)


def get_transformation_mode_enum(mode: str, name: str) -> transformation__args_proto.TransformationMode.ValueType:
    """Returns the TransformationMode type from string"""
    mode_enum = mode_str_to_proto_enum.get(mode)
    if mode_enum is None:
        raise errors.InvalidTransformationMode(
            name,
            mode,
            [SPARK_SQL_MODE, PYSPARK_MODE, SNOWFLAKE_SQL_MODE, PANDAS_MODE, PYTHON_MODE],
        )
    else:
        return mode_enum
