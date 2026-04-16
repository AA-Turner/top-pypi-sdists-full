"""Shared multipart/form-data parser used by hook and page SDKs.

The SDK transport delivers multipart bodies as base64-encoded strings (see
``HookSDKController.get_raw_request``). This helper decodes them and yields a
list of parts with the raw bytes preserved — callers that need base64 (e.g.
the public hooks contract) can re-encode after the fact.
"""

import base64
from io import BytesIO
from typing import Dict, List, Union

from abstra_internals.utils.insensitive_dict import CaseInsensitiveDict

FilePart = Dict[str, Union[str, bytes]]
TextPart = Dict[str, str]
Part = Union[FilePart, TextPart]


def parse_multipart(body: str, headers: CaseInsensitiveDict) -> List[Part]:
    """Parse a base64-encoded multipart/form-data body into a list of parts.

    File parts are returned as::

        {"name": str, "filename": str, "content_type": str, "content": bytes}

    Text parts are returned as::

        {"name": str, "value": str}
    """
    from multipart import MultipartParser, MultipartPart, parse_options_header

    raw_bytes = base64.b64decode(body, validate=True)
    _, options = parse_options_header(headers["Content-Type"])
    boundary = options["boundary"].encode("utf-8")
    parser = MultipartParser(BytesIO(raw_bytes), boundary)
    parts: List[Part] = []
    for i in parser:
        if not isinstance(i, MultipartPart):
            continue
        filename = getattr(i, "filename", None)
        if filename:
            raw = getattr(i, "raw", b"")
            parts.append(
                {
                    "name": i.name,
                    "filename": filename,
                    "content_type": getattr(
                        i, "content_type", "application/octet-stream"
                    ),
                    "content": raw,
                }
            )
        else:
            parts.append({"name": i.name, "value": i.value})
    return parts
