# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.triggers_type_list_params."""

from __future__ import annotations

from typing import Dict, Optional, Union

from typing_extensions import TypedDict
from .._types import SequenceNotStr


class TriggersTypeListParams(TypedDict, total=False):
    toolkit_slugs: Optional[SequenceNotStr[str]]
    "Array of toolkit slugs to filter triggers by"
    toolkit_versions: Union[str, Dict[str, str]]
    "Toolkit version specification.\n\nUse \"latest\" for latest versions or bracket notation for specific versions per\ntoolkit."
    limit: Optional[float]
    "Number of items per page, max allowed is 1000"
    cursor: str
    "Cursor for pagination.\n\nThe cursor is a base64 encoded string of the page and limit. The page is the\npage number and the limit is the number of items per page. The cursor is used to\npaginate through the items. The cursor is not required for the first page."


__all__ = [
    "TriggersTypeListParams",
]
