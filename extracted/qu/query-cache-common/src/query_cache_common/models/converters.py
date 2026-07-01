from __future__ import annotations

import typing as t
from datetime import timedelta

from query_cache_protobuf.query_cache.struct_pb2 import ListValue, Struct, Value, NULL_VALUE
from google.protobuf.duration_pb2 import Duration

if t.TYPE_CHECKING:
    from google.protobuf.internal.containers import MessageMap
    from query_cache_protobuf.query_cache import shared_pb2


def transformed_nodes_by_query_from_proto(
    m: MessageMap[str, shared_pb2.NodeFuncMapping],
) -> t.Dict[str, t.Dict[str, str]]:
    result: t.Dict[str, t.Dict[str, str]] = {}
    for outer_key, node_mapping in m.items():
        result[outer_key] = dict(node_mapping.node_to_func)
    return result


def transformed_nodes_by_query_to_proto(
    d: t.Dict[str, t.Dict[str, str]],
) -> MessageMap[str, shared_pb2.NodeFuncMapping]:
    from query_cache_protobuf.query_cache import shared_pb2

    result: MessageMap[str, shared_pb2.NodeFuncMapping] = {}  # type: ignore
    for outer_key, inner_dict in d.items():
        node_func_mapping = shared_pb2.NodeFuncMapping()
        node_func_mapping.node_to_func.update(inner_dict)
        result[outer_key] = node_func_mapping
    return result


def _struct_value_to_python(value: Value) -> t.Any:
    kind = value.WhichOneof("kind")
    if kind == "null_value":
        return None
    if kind == "double_value":
        return value.double_value
    if kind == "int_value":
        return value.int_value
    if kind == "string_value":
        return value.string_value
    if kind == "bool_value":
        return value.bool_value
    if kind == "struct_value":
        return struct_to_dict(value.struct_value)
    if kind == "list_value":
        return [_struct_value_to_python(v) for v in value.list_value.values]
    raise ValueError(f"Unexpected Value.kind: {kind}")


def _python_to_struct_value(obj: t.Any) -> Value:
    if obj is None:
        return Value(null_value=NULL_VALUE)
    if isinstance(obj, bool):
        return Value(bool_value=obj)
    if isinstance(obj, int):
        return Value(int_value=obj)
    if isinstance(obj, float):
        return Value(double_value=obj)
    if isinstance(obj, str):
        return Value(string_value=obj)
    if isinstance(obj, dict):
        return Value(struct_value=dict_to_struct(obj))
    if isinstance(obj, (list, tuple)):
        return Value(list_value=ListValue(values=[_python_to_struct_value(v) for v in obj]))
    raise TypeError(f"Unsupported type: {type(obj)}")


def struct_to_dict(struct_value: Struct) -> t.Dict[str, t.Any]:
    return {key: _struct_value_to_python(value) for key, value in struct_value.fields.items()}


def dict_to_struct(d: t.Dict[str, t.Any]) -> Struct:
    return Struct(fields={key: _python_to_struct_value(value) for key, value in d.items()})


def duration_to_timedelta(duration: Duration) -> timedelta:
    return duration.ToTimedelta()


def timedelta_to_duration(value: timedelta) -> Duration:
    d = Duration()
    d.FromTimedelta(value)
    return d
