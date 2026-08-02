# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Simple CPU-only UDFs for image processing.

These UDFs have minimal dependencies and can run on any worker.
"""

import io

import pyarrow as pa

import geneva


@geneva.udf(version="0.1")
def file_size(image: bytes) -> int:
    """Compute the byte size of an image."""
    return len(image)


@geneva.udf(
    version="0.1",
    data_type=pa.struct(
        [pa.field("width", pa.int32()), pa.field("height", pa.int32())]
    ),
)
def dimensions(image: bytes) -> tuple[int, int]:
    """Extract image dimensions (width, height)."""
    from PIL import Image

    image_stream = io.BytesIO(image)
    img = Image.open(image_stream)
    return img.size


@geneva.udf(version="0.2", data_type=pa.binary())
def normalize_image(image) -> bytes | None:  # noqa: ANN001
    """Resize to 224x224 and convert to grayscale; return PNG bytes.

    Accepts either raw ``bytes`` (a plain ``binary`` column) or a BlobFile-like
    object exposing ``readall()`` / ``read()`` (top-level or nested blob
    columns). The same UDF object can be bound to ``image`` / ``image_blob`` /
    ``image.image_bytes`` per table via ``add_columns``' tuple form. For a
    nested-blob input, backfill with ``blob_read_strategy="range"`` so the
    nested blob is materialized as bytes (see GEN-517).

    Returns ``None`` for inputs PIL cannot decode. Web-scraped image datasets
    (e.g. laion-1m) routinely contain truncated / corrupt JPEGs; the
    ``ImageFile.LOAD_TRUNCATED_IMAGES`` flag covers the common
    "image file is truncated" case, and the ``except`` covers anything else
    PIL refuses so a single bad row doesn't fail the whole backfill task.
    """
    from PIL import Image, ImageFile

    # Tolerate truncated JPEGs (common in scraped web datasets).
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    if image is None:
        return None
    if isinstance(image, (bytes, bytearray, memoryview)):
        raw = bytes(image)
    elif hasattr(image, "readall"):
        raw = image.readall()
    elif hasattr(image, "read"):
        raw = image.read()
    else:
        raise TypeError(f"unsupported image input type: {type(image)!r}")

    try:
        # PIL mode "L" is 8-bit single-channel luminance, i.e. grayscale.
        img = Image.open(io.BytesIO(raw)).convert("L").resize((224, 224))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except (OSError, ValueError, SyntaxError):
        # Undecodable bytes -> null row in the output column.
        return None
