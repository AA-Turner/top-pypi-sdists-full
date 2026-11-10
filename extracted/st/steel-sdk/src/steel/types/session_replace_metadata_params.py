# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypedDict

__all__ = ["SessionReplaceMetadataParams"]


class SessionReplaceMetadataParams(TypedDict, total=False):
    metadata: Required[Dict[str, Union[str, float, bool]]]
    """Customer-defined flat metadata: up to 50 keys and 8192 UTF-8 JSON bytes.

    Keys must start with a letter, use only letters, digits, underscores, dots or
    hyphens, and be at most 64 characters; steel\\__ is reserved. Values are strings
    (up to 1024 characters, valid Unicode without NUL), finite numbers or booleans.
    Numbers and booleans are stored as strings, so 3 and "3" are the same value.
    """
