import ast
import builtins
import importlib
import inspect
import os
import types
import typing
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


def _captured_variables(proto_export: export_pb.Export) -> list[types_pb.CodeVariable]:
    """Collect referenced module variables, including nested and interned helper captures."""
    with safe_trace("get_function_capture_global_variable_values"):
        resolver_captured_global_variables: dict[bytes, types_pb.CodeVariable] = {}
        captured_global_values = {
            captured_value.id: captured_value.value
            for captured_value in getattr(proto_export.graph, "captured_global_values", ())
        }
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
            elif glbl.HasField("value_ref"):
                if glbl.value_ref.id in captured_global_values:
                    globals_to_visit.append(captured_global_values[glbl.value_ref.id])
        return list(resolver_captured_global_variables.values())


def get_global_variables_info_from_export(proto_export: export_pb.Export) -> types_pb.GlobalVariablesInfo:
    return types_pb.GlobalVariablesInfo(
        code_variables=get_function_capture_global_variable_values(proto_export),
        environment_variables={},
    )


def get_function_capture_global_variable_values(
    proto_export: export_pb.Export,
) -> list[types_pb.CodeVariableValue]:
    """Capture current actor values for globals referenced by the exported graph."""
    return list(get_variables(_captured_variables(proto_export)))


def _annotation_type(annotation: object, namespace: Mapping[str, Any]) -> types_pb.Ty | None:
    """Read primitive or optional primitive annotations without evaluating annotation code."""
    primitive_types = (str, int, float, bool)
    if isinstance(annotation, str):
        try:
            node = ast.parse(annotation, mode="eval").body
        except SyntaxError:
            return None

        def read(node: ast.expr) -> list[object] | None:
            """Accept only builtin names, None, unions, and genuine typing.Optional."""
            if isinstance(node, ast.Name):
                value = namespace.get(node.id, getattr(builtins, node.id, None))
                return [value] if any(value is primitive for primitive in primitive_types) else None
            if isinstance(node, ast.Constant) and node.value is None:
                return [type(None)]
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                left, right = read(node.left), read(node.right)
                return left + right if left is not None and right is not None else None
            if isinstance(node, ast.Subscript):
                optional = (isinstance(node.value, ast.Name) and namespace.get(node.value.id) is typing.Optional) or (
                    isinstance(node.value, ast.Attribute)
                    and isinstance(node.value.value, ast.Name)
                    and namespace.get(node.value.value.id) is typing
                    and node.value.attr == "Optional"
                )
                inner = read(node.slice) if optional else None
                return inner + [type(None)] if inner is not None else None
            return None

        parts = read(node)
    elif typing.get_origin(annotation) in (typing.Union, types.UnionType):
        parts = list(typing.get_args(annotation))
    else:
        parts = [annotation]
    if parts is None:
        return None
    primitives = [part for part in parts if any(part is primitive for primitive in primitive_types)]
    if len(primitives) != 1 or any(part is not primitives[0] and part is not type(None) for part in parts):
        return None
    kind = next(primitive.__name__ for primitive in primitive_types if primitives[0] is primitive)
    result = types_pb.Ty(nullable=type(None) in parts)
    getattr(result, kind).SetInParent()
    return result


def _module_annotations(module: types.ModuleType) -> Mapping[str, object]:
    """Read eager annotations or parse deferred module annotations without executing them."""
    namespace = vars(module)
    annotations = namespace.get("__annotations__")
    if isinstance(annotations, dict):
        return annotations
    # Python 3.14 stores __annotate__ instead of an eager annotation dictionary.
    # Accessing module.__annotations__ would execute annotation expressions.
    if "__annotate__" not in namespace:
        return {}
    try:
        tree = ast.parse(inspect.getsource(module))
    except (OSError, TypeError, SyntaxError):
        return {}
    result: dict[str, object] = {}
    for statement in tree.body:
        if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            annotation = statement.annotation
            result[statement.target.id] = (
                annotation.value
                if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str)
                else ast.unparse(annotation)
            )
    return result


def _environment_initializer_types(module: types.ModuleType) -> dict[str, types_pb.Ty]:
    """Recognize single module assignments from getenv with literal string/None defaults.

    This is provenance for the supported environment pattern, not arbitrary Python
    type inference. Any other binding of the name makes its initializer ambiguous.
    """
    try:
        tree = ast.parse(inspect.getsource(module))
    except (OSError, TypeError, SyntaxError):
        return {}
    bindings: dict[str, int] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            bindings[node.id] = bindings.get(node.id, 0) + 1
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings[node.name] = bindings.get(node.name, 0) + 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                bindings[name] = bindings.get(name, 0) + 1
    namespace = vars(module)
    result: dict[str, types_pb.Ty] = {}
    os_aliases: set[str] = set()
    getenv_aliases: set[str] = set()
    for statement in tree.body:
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                name = alias.asname or alias.name
                if alias.name == "os" and bindings.get(name) == 1 and namespace.get(name) is os:
                    os_aliases.add(name)
            continue
        if isinstance(statement, ast.ImportFrom):
            if statement.module == "os" and statement.level == 0:
                for alias in statement.names:
                    name = alias.asname or alias.name
                    if alias.name == "getenv" and bindings.get(name) == 1 and namespace.get(name) is os.getenv:
                        getenv_aliases.add(name)
            continue
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target, expression = statement.targets[0], statement.value
        elif isinstance(statement, ast.AnnAssign):
            target, expression = statement.target, statement.value
        else:
            continue
        if not isinstance(target, ast.Name) or bindings.get(target.id) != 1 or not isinstance(expression, ast.Call):
            continue
        function = expression.func
        supported = (
            isinstance(function, ast.Attribute)
            and isinstance(function.value, ast.Name)
            and function.value.id in os_aliases
            and function.attr == "getenv"
        ) or (isinstance(function, ast.Name) and function.id in getenv_aliases)
        if not supported or not 1 <= len(expression.args) <= 2:
            continue
        key = expression.args[0]
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            continue
        if expression.keywords:
            if len(expression.args) != 1 or len(expression.keywords) != 1 or expression.keywords[0].arg != "default":
                continue
            default = expression.keywords[0].value
        else:
            default = expression.args[1] if len(expression.args) == 2 else ast.Constant(value=None)
        if not isinstance(default, ast.Constant) or (default.value is not None and not isinstance(default.value, str)):
            continue
        result[target.id] = types_pb.Ty(str=types_pb.EmptyMessage(), nullable=default.value is None)
    return result


def _is_portable_global_type(ty: types_pb.Ty) -> bool:
    """Accept existing concrete scalar/container types, never unresolved Any or Python objects."""
    kind = ty.WhichOneof("ty")
    if kind in {"str", "int", "float", "bool", "bytes", "date", "datetime", "timedelta", "none"}:
        return True
    if kind in {"list", "set"}:
        return _is_portable_global_type(getattr(ty, kind).items)
    if kind == "dict":
        return _is_portable_global_type(ty.dict.key) and _is_portable_global_type(ty.dict.value)
    if kind == "tuple":
        return all(_is_portable_global_type(item) for item in ty.tuple.fixed)
    return False


def get_global_variable_types_from_export(proto_export: export_pb.Export) -> types_pb.GlobalVariablesInfo:
    """Publish concrete global types without reading envvars or serializing their values.

    Simple module annotations preserve optional types when a value is absent.
    A single supported getenv initializer also supplies its optional string type.
    Other unannotated None or unsupported values supply no portable type metadata.
    Actor value snapshots continue to use get_global_variables_info_from_export.
    """
    result = types_pb.GlobalVariablesInfo()
    initializer_types: dict[str, dict[str, types_pb.Ty]] = {}
    annotations: dict[str, Mapping[str, object]] = {}
    for variable in _captured_variables(proto_export):
        try:
            module = importlib.import_module(variable.module)
        except ImportError:
            continue
        namespace = vars(module)
        value = namespace.get(variable.name, _missing)
        if value is _missing:
            continue
        if variable.module not in annotations:
            annotations[variable.module] = _module_annotations(module)
        annotation = annotations[variable.module].get(variable.name)
        declared = _annotation_type(annotation, namespace)
        if declared is None:
            if variable.module not in initializer_types:
                initializer_types[variable.module] = _environment_initializer_types(module)
            declared = initializer_types[variable.module].get(variable.name)
        if declared is not None:
            if value is None:
                if not declared.nullable:
                    continue
            elif type(value) not in (str, int, float, bool) or not declared.HasField(type(value).__name__):
                continue
            ty = declared
        else:
            if value is None:
                continue
            try:
                ty = _parse_python_type(value)
            except RecursionError:
                continue
            if not _is_portable_global_type(ty):
                continue
        result.code_variables.add(variable=variable, value=types_pb.SymbolicConst(ty=ty))
    return result
