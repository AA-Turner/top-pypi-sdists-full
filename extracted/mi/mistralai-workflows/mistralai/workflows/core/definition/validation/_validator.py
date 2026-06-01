import inspect
from types import NoneType, UnionType
from typing import Any, Callable, Dict, Tuple, Type, TypeVar, Union, get_args, get_origin

from pydantic import BaseModel, TypeAdapter, ValidationError

from mistralai.workflows.core.definition.validation._schema_generator import (
    generate_pydantic_model_from_params,
    generate_pydantic_model_from_return_type,
)
from mistralai.workflows.core.dependencies.dependency_injector import DependsCls
from mistralai.workflows.core.utils.sandbox import is_instance_or_sandboxed_subclass
from mistralai.workflows.core.utils.type_hints import get_type_hints
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

T = TypeVar("T", bound=Callable[..., Any])


def extract_origin_type(type_to_extract: Type) -> Type:
    origin = get_origin(type_to_extract)
    args: Tuple[Type, ...] = get_args(type_to_extract)
    if origin is Union and len(args) == 2 and NoneType in args:
        return next(arg for arg in args if arg is not NoneType)
    elif origin is UnionType and len(args) == 2 and NoneType in args:
        return next(arg for arg in args if arg is not NoneType)
    return type_to_extract


def check_is_valid_type(type_to_check: Type, expected_type: Type, allow_optional: bool = False) -> bool:
    if allow_optional:
        type_to_check = extract_origin_type(type_to_check)

    return (inspect.isclass(type_to_check) and issubclass(type_to_check, expected_type)) or (
        type_to_check is expected_type
    )


def get_function_signature_type_hints(func: Callable, is_method: bool) -> Tuple[Dict[str, Type], Type, bool]:
    """Extract type hints and parameter info from a function signature.

    Returns:
        Tuple of (user_params_dict, return_type, has_kwargs)
    """
    type_hints = get_type_hints(func)
    if "return" not in type_hints:
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=(
                f"'{func.__name__}' must have a return type annotation, use `-> None` if no return type is expected."
            ),
        )

    sig = inspect.signature(func)

    param_names = list(sig.parameters.keys())

    if is_method:
        if not param_names:
            raise WorkflowsException(
                code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
                message=f"Method '{func.__name__}' has no parameters, expected 'self' or 'cls' as the first.",
            )
        type_hints.pop(param_names[0], None)
        param_names = param_names[1:]

    user_params_dict = {}
    has_kwargs = False
    for param_name in param_names:
        param = sig.parameters[param_name]
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            has_kwargs = True
            continue
        if isinstance(param.default, DependsCls):
            continue

        # Only add to user params if it has a type hint
        if param_name in type_hints:
            user_params_dict[param_name] = type_hints[param_name]
        else:
            raise WorkflowsException(
                code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
                message=f"Parameter '{param_name}' in '{func.__name__}' must have a type annotation.",
            )

    return_type = type_hints["return"]
    return user_params_dict, return_type, has_kwargs


def raise_if_function_has_invalid_signature(
    func: Callable, is_method: bool = False, allow_kwargs: bool = False
) -> None:
    """Validate function signature. Raises if invalid."""
    if not inspect.iscoroutinefunction(func):
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=f"'{func.__name__}' must be async function. Use `async def`.",
        )

    user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(func, is_method=is_method)

    if has_kwargs and not allow_kwargs:
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=f"'{func.__name__}' has **kwargs which is not supported for this handler type.",
        )

    try:
        generate_pydantic_model_from_params(func.__name__, user_params_dict, func=func)
    except Exception as e:
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=f"Cannot generate Pydantic model from parameters of '{func.__name__}': {e}",
        ) from e

    try:
        generate_pydantic_model_from_return_type(func.__name__, return_type)
    except Exception as e:
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=f"Cannot generate Pydantic model from return type of '{func.__name__}': {e}",
        ) from e


def raise_if_function_has_invalid_usage(
    func: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any], is_method: bool = False
) -> None:
    user_params_dict, _, has_kwargs = get_function_signature_type_hints(func, is_method=is_method)

    if is_method:
        args = args[1:]

    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())
    if is_method:
        param_names = param_names[1:]

    # Build list of required param names (in order) and total param count
    required_params: list[str] = []
    explicit_params: list[str] = []  # Non-VAR_KEYWORD, non-Depends params
    for param_name in param_names:
        param = sig.parameters[param_name]
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            continue
        if isinstance(param.default, DependsCls):
            continue
        explicit_params.append(param_name)
        if param.default is inspect.Parameter.empty:
            required_params.append(param_name)

    total_param_count = len(explicit_params)
    provided_positional = len(args)

    # Check for unknown kwargs when function doesn't have **kwargs
    if not has_kwargs:
        unknown_kwargs = set(kwargs.keys()) - set(explicit_params)
        if unknown_kwargs:
            raise WorkflowsException(
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                message=(f"'{func.__name__}' got unexpected keyword arguments: {sorted(unknown_kwargs)}."),
            )

    # Check for duplicate args (provided both positionally and as kwarg)
    for i, param_name in enumerate(explicit_params):
        if i < provided_positional and param_name in kwargs:
            raise WorkflowsException(
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                message=(
                    f"'{func.__name__}' got multiple values for parameter '{param_name}': "
                    f"'{args[i]}' and '{kwargs[param_name]}'"
                ),
            )

    # Check too many positional args
    if provided_positional > total_param_count:
        raise WorkflowsException(
            code=ErrorCode.INVALID_ARGUMENTS_ERROR,
            message=(
                f"'{func.__name__}' expects at most {total_param_count} positional parameters. "
                f"Found: {provided_positional} positional arguments."
            ),
        )

    # Check each required param is provided (by position or by name in kwargs)
    for i, param_name in enumerate(required_params):
        param_index = explicit_params.index(param_name)
        provided_by_position = param_index < provided_positional
        provided_by_kwarg = param_name in kwargs
        if not provided_by_position and not provided_by_kwarg:
            raise WorkflowsException(
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                message=f"'{func.__name__}' missing required parameter: '{param_name}'.",
            )

    for i, (param_name, param_type) in enumerate(user_params_dict.items()):
        if i < len(args):
            arg = args[i]
        elif param_name in kwargs:
            arg = kwargs[param_name]
        else:
            continue

        if inspect.isclass(param_type) and issubclass(param_type, BaseModel):
            if not is_instance_or_sandboxed_subclass(arg, param_type):
                raise WorkflowsException(
                    code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                    message=(
                        f"Parameter '{param_name}' in '{func.__name__}' should be of type '{param_type}'. "
                        f"Found: '{type(arg)}'."
                    ),
                )


def raise_if_function_has_invalid_return_type(func: Callable, return_value: Any, is_method: bool = False) -> None:
    _, return_type, _ = get_function_signature_type_hints(func, is_method=is_method)

    try:
        adapter = TypeAdapter(return_type)
        adapter.validate_python(return_value, strict=True)
    except ValidationError as e:
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_DEFINITION_ERROR,
            message=f"'{func.__name__}' return type validation failed: {e}",
        ) from e


def _validate_handler_signature(
    func: Callable,
    is_method: bool,
    error_code: ErrorCode,
    handler_type: str,
    validate_return_type: bool = False,
    require_non_none_return: bool = False,
) -> None:
    user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(func, is_method=is_method)

    try:
        generate_pydantic_model_from_params(func.__name__, user_params_dict, func=func, allow_extra=has_kwargs)
    except Exception as e:
        raise WorkflowsException(
            code=error_code,
            message=f"{handler_type} '{func.__name__}' has invalid parameters for schema generation: {e}",
        ) from e

    if require_non_none_return and (return_type is NoneType or return_type is type(None)):
        raise WorkflowsException(
            code=error_code,
            message=f"{handler_type} '{func.__name__}' must have a return type annotation other than None.",
        )

    if validate_return_type:
        try:
            generate_pydantic_model_from_return_type(func.__name__, return_type)
        except Exception as e:
            raise WorkflowsException(
                code=error_code,
                message=f"{handler_type} '{func.__name__}' has invalid return type for schema generation: {e}",
            ) from e


def validate_signal_handler_signature(func: Callable, is_method: bool = True) -> None:
    _validate_handler_signature(
        func,
        is_method=is_method,
        error_code=ErrorCode.WORKFLOW_SIGNAL_DEFINITION_ERROR,
        handler_type="Signal",
    )


def validate_query_handler_signature(func: Callable, is_method: bool = True) -> None:
    if inspect.iscoroutinefunction(func):
        raise WorkflowsException(
            code=ErrorCode.REJECTED_QUERY_ERROR,
            message=f"Query '{func.__name__}' must be a synchronous function (def), not async def.",
        )

    _validate_handler_signature(
        func,
        is_method=is_method,
        error_code=ErrorCode.REJECTED_QUERY_ERROR,
        handler_type="Query",
        validate_return_type=True,
        require_non_none_return=True,
    )


def validate_update_handler_signature(func: Callable, is_method: bool = True) -> None:
    _validate_handler_signature(
        func,
        is_method=is_method,
        error_code=ErrorCode.WORKFLOW_UPDATE_DEFINITION_ERROR,
        handler_type="Update",
        validate_return_type=True,
        require_non_none_return=True,
    )
