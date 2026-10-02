from __future__ import annotations

import io
import mimetypes
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image


class UploadMixin:
    @staticmethod
    def guess_mime_type(path: os.PathLike) -> str:
        mime_type, _ = mimetypes.guess_type(path)

        if mime_type is None:
            return 'application/octet-stream'

        return mime_type

    @staticmethod
    def ensure_bytes(data: bytes | str) -> bytes:
        if isinstance(data, str):
            return data.encode('utf-8')

        return data

    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = 'jpeg') -> bytes:
        with io.BytesIO() as buffer:
            image.save(buffer, format=format)
            return buffer.getvalue()
