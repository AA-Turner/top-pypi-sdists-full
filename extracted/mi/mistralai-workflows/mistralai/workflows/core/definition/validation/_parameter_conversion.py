from typing import Any, Type, cast

import structlog
from pydantic import BaseModel, RootModel, ValidationError

from mistralai.workflows.core.definition.validation._schema_generator import (
    _is_bare_union_of_basemodels,
    _is_basemodel_subclass,
)

logger = structlog.get_logger(__name__)


def _normalize_params(
    params: Any,
    user_params_dict: dict[str, Type],
    input_model: Type[BaseModel],
) -> Any:
    """Normalize raw Temporal input into a value suitable for model_validate.

    Temporal's start_workflow(name, arg) passes ``arg`` as-is to the workflow
    wrapper whose signature is always ``run(self, params: dict | None = None)``.
    So ``params`` can be a dict, None, or a raw primitive (int, str, bool, ...).

    Returns a value that ``input_model.model_validate(...)`` can accept:
    - dict inputs are passed through unchanged.
    - RootModel inputs (bare unions) are passed through unchanged, including None.
    - None for a regular model becomes {} so all-default workflows work.
    - A raw primitive for a single-param model is wrapped as {param_name: value}.
    - A raw primitive for a zero- or multi-param model becomes {} (fall back to defaults).
    """
    if isinstance(params, (dict, BaseModel)):
        return params

    if issubclass(input_model, RootModel):
        return params

    if params is not None and len(user_params_dict) == 1:
        param_name = next(iter(user_params_dict.keys()))
        return {param_name: params}

    return {}


def convert_params_dict_to_user_args(
    params_dict: Any,
    user_params_dict: dict[str, Type],
    input_model: Type[BaseModel],
) -> tuple[Any, ...]:
    """Convert Temporal's parameter dict to user function arguments."""
    params_dict = _normalize_params(params_dict, user_params_dict, input_model)
    validated_params = input_model.model_validate(params_dict)

    if not user_params_dict:
        return ()

    if len(user_params_dict) == 1:
        param_name = next(iter(user_params_dict.keys()))
        param_type = user_params_dict[param_name]

        if _is_basemodel_subclass(param_type):
            return (validated_params,)
        if _is_bare_union_of_basemodels(param_type):
            return (cast(RootModel, validated_params).root,)
        return (getattr(validated_params, param_name),)
    else:
        return tuple(getattr(validated_params, name) for name in user_params_dict.keys())


def convert_result_to_temporal_format(
    result: Any,
    output_model: Type[BaseModel] | None,
) -> Any:
    """Convert handler result to Temporal's dict format.

    If conversion fails (e.g., result doesn't match expected type), this logs
    an error and returns the raw result as a fallback. This prevents workflow
    task failures that would cause the workflow to hang forever.
    """
    if result is None:
        return None

    try:
        if isinstance(result, BaseModel):
            return result.model_dump()

        if output_model:
            if hasattr(output_model, "model_fields") and "result" in output_model.model_fields:
                return output_model(result=result).model_dump()
            return output_model.model_validate(result).model_dump()

        return result
    except Exception as e:
        reason = "type mismatch" if isinstance(e, ValidationError) else "non-serializable object"
        logger.error(
            "Failed to convert workflow result to temporal format, returning raw result as fallback",
            reason=reason,
            result_type=type(result).__name__,
            output_model=output_model.__name__ if output_model else None,
            error=str(e),
        )
        return result


def convert_params_dict_to_user_args_and_kwargs(
    params_dict: Any,
    user_params_dict: dict[str, Type],
    input_model: Type[BaseModel],
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Convert Temporal's parameter dict to user function args and extra kwargs.

    Used for handlers that accept **kwargs. Returns explicit params as positional
    args and any extra fields in params_dict as keyword arguments.
    """
    params_dict = _normalize_params(params_dict, user_params_dict, input_model)
    validated_params = input_model.model_validate(params_dict)

    extra_kwargs = (
        {k: v for k, v in params_dict.items() if k not in user_params_dict} if isinstance(params_dict, dict) else {}
    )

    if not user_params_dict:
        return (), extra_kwargs

    if len(user_params_dict) == 1:
        param_name = next(iter(user_params_dict.keys()))
        param_type = user_params_dict[param_name]

        if _is_basemodel_subclass(param_type):
            # The wrapper model has the BaseModel as a named field (e.g. "data")
            model_instance = getattr(validated_params, param_name)
            if not isinstance(model_instance, param_type):
                model_instance = param_type.model_validate(model_instance)
            return (model_instance,), extra_kwargs
        if _is_bare_union_of_basemodels(param_type):
            # When allow_extra=True, the model is a regular model with a params field
            # When allow_extra=False, the model is a RootModel with the union as root
            if issubclass(input_model, RootModel):
                return (cast(RootModel, validated_params).root,), extra_kwargs
            else:
                return (getattr(validated_params, param_name),), extra_kwargs
        return (getattr(validated_params, param_name),), extra_kwargs
    else:
        args = tuple(getattr(validated_params, name) for name in user_params_dict.keys())
        return args, extra_kwargs


def resolve_handler_args(
    params: dict | None,
    handler_meta_user_params_dict: dict[str, type],
    handler_meta_input_model: type[BaseModel],
    handler_meta_has_kwargs: bool,
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Resolve handler params dict into positional args and extra kwargs.

    Dispatches to the appropriate conversion function based on whether
    the handler accepts **kwargs.
    """
    if handler_meta_has_kwargs:
        return convert_params_dict_to_user_args_and_kwargs(
            params, handler_meta_user_params_dict, handler_meta_input_model
        )
    else:
        actual_args = convert_params_dict_to_user_args(params, handler_meta_user_params_dict, handler_meta_input_model)
        return actual_args, {}


def convert_query_update_result_to_temporal_format(
    result: Any,
    output_model: Type[BaseModel] | None,
) -> Any:
    """Convert query/update handler result to Temporal's format.

    Unlike workflows, queries and updates return primitive values directly
    without wrapping them in a dict when called via Temporal's native client.
    """
    if result is None:
        return None

    if isinstance(result, BaseModel):
        return result.model_dump()

    return result
