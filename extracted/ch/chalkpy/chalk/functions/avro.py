import json
from typing import Type, Union

import pyarrow as pa

from chalk.features._encoding.pyarrow import rich_to_pyarrow
from chalk.features.underscore import Underscore, UnderscoreFunction


def avro_deserialize(body: Union[Underscore, bytes], schema: Union[dict, str], target_type: Type):
    """
    Deserialize an Avro message from a bytes feature.

    Parameters
    ----------
    body
        The bytes feature to deserialize.
    schema
        The Avro schema as a dictionary or JSON string.
    target_type
        The target dataclass type to deserialize into.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> from dataclasses import dataclass
    >>> from typing import Optional
    >>> USER_SCHEMA = {
    ...     "type": "record",
    ...     "name": "User",
    ...     "fields": [
    ...         {"name": "name", "type": "string"},
    ...         {"name": "age", "type": "long"},
    ...         {"name": "email", "type": ["null", "string"], "default": None},
    ...     ],
    ... }
    >>> @dataclass
    ... class UserStruct:
    ...     name: str
    ...     age: int
    ...     email: Optional[str]
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     user_avro_bytes: bytes
    ...     user: UserStruct = F.avro_deserialize(
    ...         _.user_avro_bytes,
    ...         USER_SCHEMA,
    ...         UserStruct,
    ...     )
    """
    if not isinstance(body, (bytes, Underscore)):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"F.avro_deserialize(): body must be bytes or Underscore, got {type(body)}")
    if not isinstance(schema, (dict, str)):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"F.avro_deserialize(): schema must be a dict or str, got {type(schema)}")
    if not isinstance(target_type, type):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"F.avro_deserialize(): target_type must be a type, got {type(target_type)}")

    schema_json = schema if isinstance(schema, str) else json.dumps(schema)
    pa_type = rich_to_pyarrow(target_type, name=target_type.__name__)
    pa_scalar = pa.scalar(None, pa_type)
    repr_override = f"F.{avro_deserialize.__name__}({body!r}, {schema!r}, {target_type.__name__})"
    return UnderscoreFunction("avro_to_struct", schema_json, pa_scalar, body, _chalk__repr_override=repr_override)


__all__ = ["avro_deserialize"]
