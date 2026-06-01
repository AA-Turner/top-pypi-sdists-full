from typing import Any

import jsonpatch  # type: ignore[import-untyped]
from pydantic import TypeAdapter

from mistralai.workflows.protocol.v1.events import JSONPatch, JSONPatchAppend, json_patch

adapter: TypeAdapter[Any] = TypeAdapter(Any)


def _to_json(obj: Any) -> Any:
    """Convert an object to JSON-serializable form."""
    return adapter.dump_python(obj, mode="json")


def _get_value_at_path(path: str, obj: Any) -> Any:
    """Get value at a JSON pointer path."""
    if not path or path == "/":
        return obj
    parts = path.split("/")[1:]  # Skip empty string before first /
    current = obj
    for part in parts:
        if current is None:
            return None
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def _convert_to_append_patch(patch: dict[str, Any], previous_payload: Any) -> JSONPatch:
    """
    Convert a "replace" patch to an "append" patch when applicable.

    The conversion happens when:
    1. The operation is "replace"
    2. The new value is a string
    3. The previous value at the same path is also a string
    4. The new value starts with the previous value (i.e., text was appended)

    This optimization is particularly useful for LLM streaming where tokens
    are appended to a response string incrementally.

    Args:
        patch: A raw JSON patch operation dict from jsonpatch library.
        previous_payload: The original payload to look up the old value.

    Returns:
        A JSONPatch with "append" op if conditions are met, otherwise the original op.
    """
    op = patch["op"]
    path = patch["path"]
    value = patch.get("value")

    # Only convert "replace" operations on strings
    if op != "replace" or not isinstance(value, str):
        return json_patch(op=op, path=path, value=value)

    old_value = _get_value_at_path(path, previous_payload)

    # Convert to "append" if the new string extends the old string
    if isinstance(old_value, str) and value.startswith(old_value):
        appended_text = value[len(old_value) :]
        return JSONPatchAppend(op="append", path=path, value=appended_text)

    return json_patch(op=op, path=path, value=value)


def make_json_patch(previous_payload: Any, new_payload: Any) -> list[JSONPatch]:
    """
    Generate JSON patch operations between two payloads with "append" optimization.

    Uses the standard jsonpatch library to compute differences, then post-processes
    the patches to convert eligible "replace" operations to "append" operations
    for more efficient streaming of incrementally growing strings.

    Args:
        previous_payload: The original payload state.
        new_payload: The new payload state.

    Returns:
        A list of JSONPatch operations to transform previous_payload into new_payload.
        String replacements that extend the original value will use "append" instead.

    Example:
        >>> make_json_patch({"text": "Hello"}, {"text": "Hello, world!"})
        [JSONPatch(op="append", path="/text", value=", world!")]
    """
    json_previous = _to_json(previous_payload)
    json_new = _to_json(new_payload)
    patch = jsonpatch.make_patch(json_previous, json_new)
    return [_convert_to_append_patch(p, json_previous) for p in patch.patch]
