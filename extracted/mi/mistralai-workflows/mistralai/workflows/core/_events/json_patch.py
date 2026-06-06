from typing import Any

import jsonpatch  # type: ignore[import-untyped]
from mistralai.extra.workflows.encoding.models import EncryptableFieldTypes
from pydantic import TypeAdapter

from mistralai.workflows.protocol.v1.events import JSONPatch, json_patch

_ENCRYPTED_FIELD_TYPES = {e.value for e in EncryptableFieldTypes}


def _escape_json_pointer(key: str) -> str:
    """Escape a key for JSON Pointer (RFC6901): ~ -> ~0, / -> ~1."""
    return key.replace("~", "~0").replace("/", "~1")


def find_encrypted_paths(obj: Any, current_path: str = "") -> list[str]:
    """Find all paths containing encrypted field markers.

    Scans the object recursively to find paths where encrypted field types are used.
    Returns paths like ["/api_key", "/credentials"] that should have their patches encrypted.
    """
    paths = []
    if isinstance(obj, dict):
        if obj.get("field_type") in _ENCRYPTED_FIELD_TYPES:
            return [current_path]
        for key, value in obj.items():
            paths.extend(find_encrypted_paths(value, f"{current_path}/{_escape_json_pointer(key)}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            paths.extend(find_encrypted_paths(item, f"{current_path}/{i}"))
    return paths


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
    Convert "replace" to "append" when the new string extends the old string.
    """
    op = patch["op"]
    path = patch["path"]
    value = patch.get("value")

    if op == "replace" and isinstance(value, str):
        old_value = _get_value_at_path(path, previous_payload)
        if isinstance(old_value, str) and value.startswith(old_value):
            return json_patch(op="append", path=path, value=value[len(old_value) :])

    return json_patch(op=op, path=path, value=value)


def _should_encrypt_path(patch_path: str, encrypted_paths: list[str]) -> bool:
    """Check if a patch path targets or contains an encrypted field.

    Returns True if:
    - patch_path equals an encrypted path (direct match)
    - patch_path is a child of an encrypted path (e.g., /secret/data under /secret)
    - patch_path is a parent of an encrypted path (e.g., /credentials containing /credentials/api_key)
    """
    for ep in encrypted_paths:
        if patch_path == ep or patch_path.startswith(ep + "/") or ep.startswith(patch_path + "/"):
            return True
    return False


def make_json_patch(previous_payload: Any, new_payload: Any) -> tuple[list[JSONPatch], set[str]]:
    """
    Generate JSON patch operations between two payloads with "append" optimization.

    Uses the standard jsonpatch library to compute differences, then post-processes
    the patches to convert eligible "replace" operations to "append" operations
    for more efficient streaming of incrementally growing strings.

    Returns:
        Tuple of (list of JSONPatch models, set of paths that should be encrypted)
    """
    json_previous = _to_json(previous_payload)
    json_new = _to_json(new_payload)
    patch = jsonpatch.make_patch(json_previous, json_new)

    # Find paths containing encrypted fields in the new payload
    encrypted_field_paths = find_encrypted_paths(json_new)

    patches: list[JSONPatch] = []
    encrypted_paths: set[str] = set()
    for p in patch.patch:
        patch_obj = _convert_to_append_patch(p, json_previous)
        patches.append(patch_obj)
        if encrypted_field_paths and _should_encrypt_path(patch_obj.path, encrypted_field_paths):
            encrypted_paths.add(patch_obj.path)

    return patches, encrypted_paths


def patches_to_json_patch(patches: list[dict[str, Any]]) -> list[JSONPatch]:
    """Convert patch dicts (from Temporal deserialization) to JSONPatch models."""
    return [json_patch(op=p["op"], path=p["path"], value=p.get("value")) for p in patches]
