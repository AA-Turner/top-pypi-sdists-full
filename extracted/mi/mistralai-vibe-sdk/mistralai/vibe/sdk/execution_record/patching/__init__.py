"""Execution Record patching exports."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "AddOp",
    "AppendOp",
    "CopyOp",
    "JsonPointer",
    "JsonTestOp",
    "MoveOp",
    "Op",
    "Patch",
    "RemoveOp",
    "ReplaceOp",
    "apply_patches",
    "reroute_patches",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.execution_record.patching.json_patch import (
        apply_patches,
        reroute_patches,
    )
    from mistralai.vibe.sdk.execution_record.patching.types import (
        AddOp,
        AppendOp,
        CopyOp,
        JsonPointer,
        JsonTestOp,
        MoveOp,
        Op,
        Patch,
        RemoveOp,
        ReplaceOp,
    )

_LAZY_EXPORTS = {
    "AddOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "AppendOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "CopyOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "JsonPointer": "mistralai.vibe.sdk.execution_record.patching.types",
    "JsonTestOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "MoveOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "Op": "mistralai.vibe.sdk.execution_record.patching.types",
    "Patch": "mistralai.vibe.sdk.execution_record.patching.types",
    "RemoveOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "ReplaceOp": "mistralai.vibe.sdk.execution_record.patching.types",
    "apply_patches": "mistralai.vibe.sdk.execution_record.patching.json_patch",
    "reroute_patches": "mistralai.vibe.sdk.execution_record.patching.json_patch",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
