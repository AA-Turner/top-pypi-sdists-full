import inspect
import json
from collections.abc import Awaitable, Callable
from typing import Any, Literal, cast

from pydantic import BaseModel, ValidationError

import mistralai.extra.run.tools as mistralai_extra_tools
from mistralai.client import models as mistralai_models
from mistralai.workflows.core.activity import check_is_activity, get_wrapped_activity
from mistralai.workflows.core.definition.validation._schema_generator import generate_pydantic_model_from_params
from mistralai.workflows.core.definition.validation._validator import get_function_signature_type_hints
from mistralai.workflows.exceptions import ActivityError, ErrorCode, WorkflowsException

CustomTool = Callable[..., Awaitable[Any]]

Tool = (
    mistralai_models.CodeInterpreterTool
    | mistralai_models.DocumentLibraryTool
    | mistralai_models.FunctionTool
    | mistralai_models.ImageGenerationTool
    | mistralai_models.WebSearchTool
    | mistralai_models.WebSearchPremiumTool
    | CustomTool
)


_local_function_registry: dict[str, Callable] = {}


class ToolArgumentErrorResult(BaseModel):
    error: str
    success: Literal[False] = False


def raise_or_return_tool_call_error(
    message: str, raise_on_tool_fail: bool, code: ErrorCode, cause: Exception | None = None
) -> str:
    if raise_on_tool_fail:
        error = WorkflowsException(message, code=code)
        if cause:
            raise error from cause
        raise error
    return ToolArgumentErrorResult(error=message).model_dump_json()


def format_validation_error_for_llm(error: ValidationError, tool_name: str) -> str:
    """Format Pydantic validation errors in a clear way for LLMs."""
    errors = error.errors()

    error_lines = [f"Invalid arguments for tool {tool_name} with the following issues:\n"]

    for err in errors:
        location = " -> ".join(str(loc) for loc in err["loc"])
        error_type = err["type"]
        message = err["msg"]

        # Make it more readable
        if error_type == "missing":
            if location:
                error_lines.append(f"- Missing required field: '{location}'")
            else:
                error_lines.append("- Missing required field")
        elif "type" in error_type:
            if location:
                error_lines.append(f"- Wrong type for '{location}': {message}")
            else:
                error_lines.append(f"- Wrong type: {message}")
        else:
            if location:
                error_lines.append(f"- Error in '{location}': {message}")
            else:
                error_lines.append(f"- Error: {message}")

    return "\n".join(error_lines)


def unwrap_activity_error_message(error: BaseException) -> str:
    """Surface the underlying error message from Temporal's exception wrappers.

    Inside a workflow, ``await activity(...)`` raises a Temporal ``ActivityError``
    whose ``str()`` is a generic wrapper (e.g. "Activity task failed"); the real
    error lives in ``__cause__`` (e.g. ActivityError -> ApplicationError). Walk the
    cause chain so the message we report reflects the actual failure.
    """
    current = error
    while isinstance(current, ActivityError) and current.__cause__ is not None:
        current = current.__cause__
    return str(current)


def check_is_custom_tool(tool: Tool) -> bool:
    return callable(tool)


def get_tool_name(tool: Tool) -> str | None:
    if callable(tool):
        return tool.__name__
    else:
        return tool.type


def convert_tool_to_mistral_tool(tool: Tool) -> mistralai_models.CreateAgentRequestToolTypedDict:
    if callable(tool):
        if not check_is_activity(tool):
            _local_function_registry[tool.__name__] = tool
        mistral_tool_obj = mistralai_extra_tools.create_tool_call(tool)
        mistral_tool_obj.function.strict = None
        mistral_tool = mistral_tool_obj.model_dump()
    else:
        mistral_tool = tool.model_dump()
    return cast(mistralai_models.CreateAgentRequestToolTypedDict, mistral_tool)


def _is_single_basemodel_param(user_params_dict: dict[str, type]) -> bool:
    if len(user_params_dict) != 1:
        return False
    param_type = next(iter(user_params_dict.values()))
    return inspect.isclass(param_type) and issubclass(param_type, BaseModel)


async def execute_activity_tool(
    activity_tool_name: str, activity_tool_kwargs: str | dict, raise_on_tool_fail: bool
) -> str:
    """
    Execute an activity tool with support for three parameter styles:

    1. Explicit params + **kwargs: async def tool(name: str, **kwargs)
    2. Only **kwargs: async def tool(**kwargs)
    3. Single BaseModel with extra="allow": async def tool(params: MyModel)
    """
    activity = get_wrapped_activity(activity_tool_name)
    if not activity:
        if activity_tool_name in _local_function_registry:
            activity = _local_function_registry[activity_tool_name]
        else:
            return raise_or_return_tool_call_error(
                f"Invalid tool name {activity_tool_name}.\nCould not find it in the declared agent tools.",
                raise_on_tool_fail,
                code=ErrorCode.ACTIVITY_NOT_FOUND_ERROR,
            )

    user_params_dict, _, activity_has_kwargs = get_function_signature_type_hints(activity, is_method=False)

    param_type = None
    if user_params_dict:
        param_type = generate_pydantic_model_from_params(
            activity.__name__,
            user_params_dict,
            func=activity,
            allow_extra=activity_has_kwargs,
        )

    # Parse JSON params
    if isinstance(activity_tool_kwargs, dict):
        json_params = activity_tool_kwargs
    elif isinstance(activity_tool_kwargs, str):
        try:
            json_params = json.loads(activity_tool_kwargs)
        except json.JSONDecodeError as e:
            return raise_or_return_tool_call_error(
                f"Invalid arguments for tool {activity_tool_name}.\n"
                f"Could not parse JSON provided to tool {activity_tool_kwargs}\nError: {e}",
                raise_on_tool_fail,
                code=ErrorCode.TOOL_ARGUMENT_ERROR,
                cause=e,
            )
    else:
        raise WorkflowsException(
            message=(
                f"Invalid arguments for tool {activity_tool_name}, "
                f"expected a string or dict. Got {type(activity_tool_kwargs)}"
            ),
            code=ErrorCode.TOOL_ARGUMENT_ERROR,
        )

    # Extract nested kwargs if present (LLM sends {"query": "...", "kwargs": {...}})
    kwargs_params: dict[str, Any] = {}
    if activity_has_kwargs and "kwargs" in json_params:
        kwargs_params = json_params.pop("kwargs") or {}

    try:
        if param_type is not None:
            is_single_basemodel = _is_single_basemodel_param(user_params_dict) and not activity_has_kwargs

            if is_single_basemodel:
                # Case 3: Single BaseModel param - use existing wrapped format
                if len(json_params) != 1:
                    return raise_or_return_tool_call_error(
                        f"Invalid arguments for tool {activity_tool_name}, "
                        f"expected a single argument in the form of : {param_type.model_json_schema()}",
                        raise_on_tool_fail,
                        code=ErrorCode.TOOL_ARGUMENT_ERROR,
                    )
                json_param_key = next(iter(json_params))
                params = param_type.model_validate(json_params[json_param_key])
                result = await activity(params)
            else:
                params = param_type.model_validate(json_params)

                if activity_has_kwargs:
                    # Case 1: Explicit params + **kwargs - unpack all as kwargs
                    # Activity wrapper handles packing for Temporal
                    explicit_values = {k: getattr(params, k) for k in user_params_dict}
                    extra_values = params.model_extra or {}
                    all_kwargs = {**extra_values, **kwargs_params}
                    # Filter out duplicates - explicit params take precedence
                    all_kwargs = {k: v for k, v in all_kwargs.items() if k not in explicit_values}
                    result = await activity(**explicit_values, **all_kwargs)
                else:
                    # Non-kwargs activity with primitive params - pass as positional args
                    positional_args = tuple(getattr(params, k) for k in user_params_dict)
                    result = await activity(*positional_args)
        else:
            # Case 2 with no explicit params: only **kwargs
            if activity_has_kwargs:
                # Activity wrapper handles packing for Temporal
                # Merge json_params with nested kwargs (json_params takes precedence for flat format)
                all_kwargs = {**kwargs_params, **json_params}
                result = await activity(**all_kwargs)
            else:
                result = await activity()

    except ValidationError as e:
        validation_error_message = (
            f"Invalid arguments for tool {activity_tool_name}: {e}"
            if raise_on_tool_fail
            else format_validation_error_for_llm(e, activity_tool_name)
        )
        return raise_or_return_tool_call_error(
            validation_error_message,
            raise_on_tool_fail,
            code=ErrorCode.TOOL_ARGUMENT_ERROR,
            cause=e,
        )
    except WorkflowsException:
        # Framework errors raised by the activity wrapper itself (e.g. a missing
        # sticky worker session) already carry a meaningful ErrorCode. Let them
        # propagate unchanged instead of masking the code with EXECUTION_ERROR.
        raise
    except Exception as e:
        return raise_or_return_tool_call_error(
            f"Tool {activity_tool_name} raised an error during execution: {unwrap_activity_error_message(e)}",
            raise_on_tool_fail,
            code=ErrorCode.EXECUTION_ERROR,
            cause=e,
        )

    if result is None:
        return "None"
    if isinstance(result, BaseModel):
        return result.model_dump_json()
    if isinstance(result, str):
        # we suppose the string is already JSON-serialized
        return result
    # This should never be raised: non-serializable results are already caught by
    # Temporal's payload serialization when running `await activity(...)` above.
    try:
        return json.dumps(result)
    except (TypeError, ValueError) as e:
        return raise_or_return_tool_call_error(
            f"Tool {activity_tool_name} returned a non-serializable result of type {type(result).__name__}. ",
            raise_on_tool_fail,
            ErrorCode.TOOL_ARGUMENT_ERROR,
            e,
        )
