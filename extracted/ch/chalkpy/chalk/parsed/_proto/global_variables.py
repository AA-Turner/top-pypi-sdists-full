import importlib
import os
from typing import Any, Iterable, Mapping

import pyarrow as pa

from chalk._gen.chalk.artifacts.v1 import export_pb2 as export_pb
from chalk._gen.chalk.python.v1 import types_pb2 as types_pb
from chalk.features._encoding.converter import pa_scalar_to_proto
from chalk.utils.tracing import safe_trace


def get_envvars(envvars: set[str]) -> Mapping[str, str | None]:
    return {k: os.getenv(k) for k in envvars}


_any_proto_ty = types_pb.Ty(any=types_pb.EmptyMessage(), nullable=True)


class _HashableTy:
    def __init__(self, msg: types_pb.Ty):
        super().__init__()
        self.msg = msg
        self._serialized = self.msg.SerializeToString(deterministic=True)

    def __eq__(self, other: Any):
        if not isinstance(other, _HashableTy):
            return NotImplemented
        return self._serialized == other._serialized

    def __hash__(self):
        return hash(self._serialized)


def _homogeneous_python_type(values: Iterable[object]) -> types_pb.Ty:
    unique_items = {_HashableTy(_parse_python_type(v)) for v in values}
    if len(unique_items) != 1:
        return _any_proto_ty
    return next(iter(unique_items)).msg


def _parse_python_type(value: object) -> types_pb.Ty:
    value_type = type(value)
    if value_type is str:
        return types_pb.Ty(str=types_pb.EmptyMessage(), nullable=False)
    elif value_type is int:
        return types_pb.Ty(int=types_pb.EmptyMessage(), nullable=False)
    elif value_type is float:
        return types_pb.Ty(float=types_pb.EmptyMessage(), nullable=False)
    elif value_type is bool:
        return types_pb.Ty(bool=types_pb.EmptyMessage(), nullable=False)
    elif value is None:
        return types_pb.Ty(none=types_pb.EmptyMessage(), nullable=False)
    elif value_type is set or value_type is list:
        assert isinstance(value, (set, list))
        items = _homogeneous_python_type(value)
        return (
            types_pb.Ty(set=types_pb.TySet(items=items), nullable=False)
            if value_type is set
            else types_pb.Ty(list=types_pb.TyList(items=items), nullable=False)
        )
    elif value_type is dict:
        assert isinstance(value, dict)
        return types_pb.Ty(
            dict=types_pb.TyDict(
                key=_homogeneous_python_type(value.keys()),
                value=_homogeneous_python_type(value.values()),
            ),
            nullable=False,
        )
    return _any_proto_ty


_missing = object()


def get_variables(variables: Iterable[types_pb.CodeVariable]) -> Iterable[types_pb.CodeVariableValue]:
    for variable in variables:
        try:
            module = importlib.import_module(variable.module)
        except ImportError:
            continue
        if (value := getattr(module, variable.name, _missing)) is not _missing:
            ty = _parse_python_type(value)
            try:
                proto_scalar = pa_scalar_to_proto(pa.scalar(value))
            except Exception:
                continue

            yield types_pb.CodeVariableValue(
                variable=variable,
                value=types_pb.SymbolicConst(value=proto_scalar, ty=ty),
            )


def get_function_capture_global_variable_values(
    proto_export: export_pb.Export,
) -> list[types_pb.CodeVariableValue]:
    with safe_trace("get_function_capture_global_variable_values"):
        resolver_captured_global_variables: dict[bytes, types_pb.CodeVariable] = {}
        globals_to_visit = [
            glbl for resolver in proto_export.graph.resolvers for glbl in resolver.function.captured_globals
        ]
        while globals_to_visit:
            glbl = globals_to_visit.pop()
            if glbl.HasField("variable"):
                variable = types_pb.CodeVariable(name=glbl.variable.name, module=glbl.variable.module)
                resolver_captured_global_variables.setdefault(
                    variable.SerializeToString(deterministic=True),
                    variable,
                )
            elif glbl.HasField("function"):
                globals_to_visit.extend(glbl.function.captured_globals)
        return list(get_variables(resolver_captured_global_variables.values()))


def get_global_variables_info_from_export(proto_export: export_pb.Export) -> types_pb.GlobalVariablesInfo:
    return types_pb.GlobalVariablesInfo(
        code_variables=get_function_capture_global_variable_values(proto_export),
        environment_variables={},
    )
