import dataclasses
import inspect
from types import NoneType, UnionType
from typing import Any, Callable, Dict, Literal, Type, TypeGuard, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict, Field, RootModel, create_model


def _is_basemodel_subclass(tp: Any) -> TypeGuard[Type[BaseModel]]:
    return inspect.isclass(tp) and issubclass(tp, BaseModel)


def _is_bare_union_of_basemodels(tp: Any) -> bool:
    origin = get_origin(tp)
    if origin not in (Union, UnionType):
        return False
    args = get_args(tp)
    non_none_args = [a for a in args if a is not NoneType and a is not type(None)]
    return bool(non_none_args) and all(_is_basemodel_subclass(a) for a in non_none_args)


def _validate_union_param_type(tp: Any, param_name: str, func_name: str) -> None:
    """Raise TypeError at definition time if a union mixes BaseModel with non-BaseModel types.

    Pure primitive unions (str | int, str | None) are allowed through to the general
    field-creation path. Mixed unions (SchemaA | str) are rejected because the RootModel
    path won't apply and the resulting wrapper-model behaviour would be confusing.
    """
    origin = get_origin(tp)
    if origin not in (Union, UnionType):
        return
    args = get_args(tp)
    non_none_args = [a for a in args if a is not NoneType and a is not type(None)]
    has_basemodel = any(_is_basemodel_subclass(a) for a in non_none_args)
    if not has_basemodel:
        return
    bad_args = [a for a in non_none_args if not _is_basemodel_subclass(a)]
    if not bad_args:
        return
    bad_names = ", ".join(getattr(a, "__name__", repr(a)) for a in bad_args)
    raise TypeError(
        f"Parameter '{param_name}' of '{func_name}' has unsupported union members: {bad_names}. "
        "Union inputs only support Pydantic BaseModel subclasses and None. "
        "Use a dedicated BaseModel instead."
    )


def _transform_type(annotation: Any, processing: set[type]) -> Any:
    origin = get_origin(annotation)
    if origin is not None:
        return _recurse_into_generic(annotation, processing)

    if dataclasses.is_dataclass(annotation) and isinstance(annotation, type):
        return _dataclass_to_forbid_extra(annotation, processing)

    return annotation


def _recurse_into_generic(annotation: Any, processing: set[type]) -> Any:
    origin = get_origin(annotation)
    args = get_args(annotation)
    transformed_args = tuple(_transform_type(arg, processing) for arg in args)

    if origin is Union or origin is UnionType:
        return Union[transformed_args]

    try:
        return origin[transformed_args]
    except TypeError:
        return annotation


def _dataclass_to_forbid_extra(dc: type, processing: set[type]) -> Type[BaseModel]:
    if dc in processing:
        return dc

    processing.add(dc)
    try:
        fields: dict[str, Any] = {}
        for field in dataclasses.fields(dc):
            transformed = _transform_type(field.type, processing)

            if field.default is not dataclasses.MISSING:
                fields[field.name] = (transformed, Field(default=field.default))
            elif field.default_factory is not dataclasses.MISSING:
                fields[field.name] = (transformed, Field(default_factory=field.default_factory))
            else:
                fields[field.name] = (transformed, ...)

        return create_model(
            f"{dc.__name__}_ForbidExtra",
            __config__=ConfigDict(extra="forbid"),
            **fields,
        )
    finally:
        processing.discard(dc)


def generate_pydantic_model_from_params(
    func_name: str,
    user_params_dict: Dict[str, Type],
    model_suffix: str = "Input",
    func: Callable | None = None,
    allow_extra: bool = False,
) -> Type[BaseModel]:
    extra_mode: Literal["allow", "forbid"] = "allow" if allow_extra else "forbid"

    if not user_params_dict:
        model_name = f"{func_name}_{model_suffix}"
        return create_model(model_name, __config__=ConfigDict(extra=extra_mode))

    if len(user_params_dict) == 1 and not allow_extra:
        param_name = next(iter(user_params_dict.keys()))
        param_type = user_params_dict[param_name]
        if _is_basemodel_subclass(param_type):
            return param_type
        _validate_union_param_type(param_type, param_name, func_name)
        if _is_bare_union_of_basemodels(param_type):
            model_name = f"{func_name}_{model_suffix}"
            # Dynamically create a named RootModel subclass — equivalent to
            # `class <name>(RootModel[param_type]): pass` but with a runtime type.
            return create_model(model_name, __base__=RootModel[param_type])  # type: ignore[valid-type]

    fields = {}
    sig = inspect.signature(func) if func else None
    processing: set[type] = set()

    for param_name, param_type in user_params_dict.items():
        transformed = _transform_type(param_type, processing)

        if sig and param_name in sig.parameters:
            param = sig.parameters[param_name]
            if param.default is not inspect.Parameter.empty:
                fields[param_name] = (transformed, Field(default=param.default))
            else:
                fields[param_name] = (transformed, ...)
        else:
            fields[param_name] = (transformed, ...)

    model_name = f"{func_name}_{model_suffix}"
    return create_model(model_name, __config__=ConfigDict(extra=extra_mode), **fields)  # type: ignore[call-overload, no-any-return]


def generate_pydantic_model_from_return_type(
    func_name: str, return_type: Type, model_suffix: str = "Output"
) -> Type[BaseModel] | None:
    if return_type is NoneType or return_type is type(None):
        return None

    if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
        return return_type

    origin = get_origin(return_type)
    if origin in (Union, UnionType):
        args = get_args(return_type)
        non_none_types = [arg for arg in args if arg is not NoneType and arg is not type(None)]
        if len(non_none_types) == 1:
            actual_type = non_none_types[0]
            if inspect.isclass(actual_type) and issubclass(actual_type, BaseModel):
                return actual_type
            return_type = actual_type
        elif len(non_none_types) > 1:
            return_type = Union[tuple(non_none_types)]  # type: ignore[assignment]

    model_name = f"{func_name}_{model_suffix}"
    return create_model(model_name, result=(return_type, ...))
