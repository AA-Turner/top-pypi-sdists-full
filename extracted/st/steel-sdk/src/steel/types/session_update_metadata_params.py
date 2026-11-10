# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypedDict

__all__ = ["SessionUpdateMetadataParams"]


class SessionUpdateMetadataParams(TypedDict, total=False):
    metadata: Required[Dict[str, Union[str, float, bool, None]]]
    """Metadata keys to change, up to 100 per update.

    Keys follow the same rules as metadata keys. Send a string, finite number or
    boolean to set a key, or null to remove it; keys you leave out are kept. The
    merged metadata must stay within 50 keys and 8192 UTF-8 JSON bytes.
    """
