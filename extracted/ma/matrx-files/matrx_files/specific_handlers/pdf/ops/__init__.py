"""PDF page operations: extract, crop, rotate, delete, merge, split, compress,
reorder, insert, duplicate, render.

Every public function in this subpackage exposes two surfaces:

- a sync function that operates on bytes — safe to call from non-async code
- an ``_async`` variant that pushes the work to the matrx-pdf CPU executor

Per the PyMuPDF FAQ, ``Document`` objects are not thread-safe — each function
opens its own Document inside its execution context and closes it before
returning via ``with pymupdf.open(...) as doc:``.
"""

from .compose import (
    merge_pdfs_from_bytes,
    merge_pdfs_from_bytes_async,
    split_pdf_bytes,
    split_pdf_bytes_async,
)
from .compress import compress_pdf_bytes, compress_pdf_bytes_async
from .pages import (
    crop_pages_in_bytes,
    crop_pages_in_bytes_async,
    delete_pages_from_bytes,
    delete_pages_from_bytes_async,
    duplicate_pages_in_bytes,
    duplicate_pages_in_bytes_async,
    extract_pages_from_bytes,
    extract_pages_from_bytes_async,
    insert_pages_in_bytes,
    insert_pages_in_bytes_async,
    reorder_pages_in_bytes,
    reorder_pages_in_bytes_async,
    rotate_pages_in_bytes,
    rotate_pages_in_bytes_async,
)
from .render import (
    PdfPageRender,
    RenderColorspace,
    RenderFormat,
    iter_render_pages_to_image_bytes,
    render_all_pages_to_image_bytes,
    render_all_pages_to_image_bytes_async,
    render_page_to_image_bytes,
    render_page_to_image_bytes_async,
    render_thumbnail_bytes,
    render_thumbnail_bytes_async,
)


__all__ = [
    # Page selection / manipulation
    "extract_pages_from_bytes",
    "extract_pages_from_bytes_async",
    "crop_pages_in_bytes",
    "crop_pages_in_bytes_async",
    "rotate_pages_in_bytes",
    "rotate_pages_in_bytes_async",
    "delete_pages_from_bytes",
    "delete_pages_from_bytes_async",
    "reorder_pages_in_bytes",
    "reorder_pages_in_bytes_async",
    "insert_pages_in_bytes",
    "insert_pages_in_bytes_async",
    "duplicate_pages_in_bytes",
    "duplicate_pages_in_bytes_async",
    # Multi-doc composition
    "merge_pdfs_from_bytes",
    "merge_pdfs_from_bytes_async",
    "split_pdf_bytes",
    "split_pdf_bytes_async",
    # Compression
    "compress_pdf_bytes",
    "compress_pdf_bytes_async",
    # Render
    "PdfPageRender",
    "RenderFormat",
    "RenderColorspace",
    "render_page_to_image_bytes",
    "render_page_to_image_bytes_async",
    "iter_render_pages_to_image_bytes",
    "render_all_pages_to_image_bytes",
    "render_all_pages_to_image_bytes_async",
    "render_thumbnail_bytes",
    "render_thumbnail_bytes_async",
]
