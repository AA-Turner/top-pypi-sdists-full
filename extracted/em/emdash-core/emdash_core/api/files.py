"""File serving endpoint for generated artifacts."""

import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/files", tags=["files"])

# Allowed directories for serving files
ALLOWED_DIRS = ["/app", "/tmp"]


@router.get("/{file_path:path}")
async def serve_file(file_path: str):
    """Serve a generated file (image, PDF, doc, etc.)."""
    # Reconstruct full path
    full_path = Path("/") / file_path

    # Security: ensure path is in allowed directories
    resolved = full_path.resolve()
    if not any(str(resolved).startswith(d) for d in ALLOWED_DIRS):
        raise HTTPException(status_code=403, detail="Access denied")

    if not resolved.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not resolved.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    # Get content type
    content_type, _ = mimetypes.guess_type(str(resolved))

    return FileResponse(
        path=resolved,
        media_type=content_type,
        filename=resolved.name
    )
