import gc
from importlib.metadata import version
import re
import sys
from typing import Any, List

from vellum import (
    ArrayInput,
    ArrayVellumValue,
    ChatHistoryInput,
    ErrorInput,
    FunctionCallInput,
    SearchResultsInput,
    VellumAudio,
    VellumDocument,
    VellumImage,
    VellumValue,
    VellumVideo,
)
from workflow_server.config import CONTAINER_IMAGE, is_development


def unwrap_vellum_value(item: VellumValue) -> Any:
    """Recursively unwrap VellumValue objects to their primitive values.

    This is needed because ArrayInput.value returns List[VellumValue] objects,
    but workflows expect primitive Python values (str, int, etc.).
    """
    if isinstance(item, ArrayVellumValue):
        if item.value is None:
            return None
        return [unwrap_vellum_value(nested_item) for nested_item in item.value]
    else:
        return item.value


def convert_json_inputs_to_vellum(inputs: List[dict]) -> dict:
    vellum_inputs: dict[str, Any] = {}

    for input in inputs:
        value = input["value"]
        # sync with vellum-python-sdks/ee/codegen/src/context/input-variable-context.ts
        name = to_valid_python_identifier(input["name"], "input")

        # If a value is null, we don't need to bother with any validation or deserialization
        if value is None:
            vellum_inputs[name] = None
            continue

        type = input["type"]
        if type == "CHAT_HISTORY":
            vellum_inputs[name] = ChatHistoryInput.model_validate(input).value
        elif type == "FUNCTION_CALL":
            vellum_inputs[name] = FunctionCallInput.model_validate(input).value
        elif type == "SEARCH_RESULTS":
            vellum_inputs[name] = SearchResultsInput.model_validate(input).value
        elif type == "ERROR":
            vellum_inputs[name] = ErrorInput.model_validate(input).value
        elif type == "ARRAY":
            array_value = ArrayInput.model_validate(input).value
            vellum_inputs[name] = [unwrap_vellum_value(item) for item in array_value]
        # Once we export *Input classes for these two cases, we can add the union to the WorkflowExecutorContext
        # model and simplify this method to just a {to_python_safe_snake_case(input.name): input.value} mapping
        elif type == "IMAGE":
            vellum_inputs[name] = VellumImage.model_validate(value)
        elif type == "AUDIO":
            vellum_inputs[name] = VellumAudio.model_validate(value)
        elif type == "VIDEO":
            vellum_inputs[name] = VellumVideo.model_validate(value)
        elif type == "DOCUMENT":
            vellum_inputs[name] = VellumDocument.model_validate(value)
        else:
            vellum_inputs[name] = value

    return vellum_inputs


def get_version() -> dict:
    # Return hotswappable lock file so we can save it and reuse it
    lock_file = None
    try:
        with open("/app/uv.lock", "r") as f:
            lock_file = f.read()
    except Exception:
        pass

    return {
        "sdk_version": version("vellum-ai"),
        "server_version": "local" if is_development() else version("vellum-workflow-server"),
        "container_image": CONTAINER_IMAGE,
        "lock_file": lock_file,
    }


def to_python_safe_snake_case(string: str, safety_prefix: str = "_") -> str:
    # Strip special characters from start of string
    cleaned_str = re.sub(r"^[^a-zA-Z0-9_]+", "", string)

    # Check if cleaned string starts with a number or an underscore
    starts_with_unsafe = bool(re.match(r"^[\d_]", cleaned_str))

    # Convert to snake case
    snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", cleaned_str)  # Insert underscore between lower and upper case
    snake_case = re.sub(r"[^a-zA-Z0-9]+", "_", snake_case)  # Replace any non-alphanumeric chars with underscore
    snake_case = re.sub(r"^_+|_+$", "", snake_case)  # Remove leading/trailing underscores
    snake_case = snake_case.lower()

    # Add safety prefix if needed
    cleaned_safety_prefix = (
        "_" if safety_prefix == "_" else f"{safety_prefix}{'_' if not safety_prefix.endswith('_') else ''}"
    )
    return f"{cleaned_safety_prefix}{snake_case}" if starts_with_unsafe else snake_case


def to_valid_python_identifier(string: str, safety_prefix: str = "_") -> str:
    # Strip special characters from start of string
    cleaned_str = re.sub(r"^[^a-zA-Z0-9_]+", "", string)

    # Check if cleaned string starts with a number or an underscore
    starts_with_unsafe = bool(re.match(r"^[\d_]", cleaned_str))

    # Check if the string is already a valid Python identifier (preserve case)
    is_valid_python_identifier = bool(re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", cleaned_str))

    if is_valid_python_identifier and not starts_with_unsafe:
        return cleaned_str

    return to_python_safe_snake_case(string, safety_prefix)


def get_obj_size(obj: Any) -> int:
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()  # type: ignore
        marked.update(new_refr.keys())

    return sz
