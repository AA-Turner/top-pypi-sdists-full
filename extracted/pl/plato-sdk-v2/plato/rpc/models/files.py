"""Files service models.

Raw-byte push/pull over ``PUT``/``GET /v1/files/content`` — replaces
``scp_content_to_vm`` and the ``cat``-spool reads. Metadata (path, mode) rides
query params and headers; the body is the raw octet stream (no base64
inflation). This module holds only the JSON metadata responses; the bytes
themselves never pass through a pydantic model.
"""

from __future__ import annotations

from pydantic import BaseModel


class FileWriteResponse(BaseModel):
    path: str
    bytes_written: int
    sha256: str


class FileStatResponse(BaseModel):
    path: str
    exists: bool
    size: int = 0
    is_dir: bool = False
