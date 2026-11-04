# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.triggers_type_retrieve_params."""

from __future__ import annotations

from typing import Dict, Union

from typing_extensions import TypedDict


class TriggersTypeRetrieveParams(TypedDict, total=False):
    toolkit_versions: Union[str, Dict[str, str]]
    "Toolkit version specification.\n\nUse \"latest\" for latest versions or bracket notation for specific versions per\ntoolkit."


__all__ = [
    "TriggersTypeRetrieveParams",
]
