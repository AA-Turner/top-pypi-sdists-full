"""Atomic file-write helper.

Writes content to a temporary file in the same directory as the target,
then renames it into place.  This ensures readers never see a partially
written file.
"""

import os
import stat
import tempfile
from pathlib import Path


def atomic_write(path: Path, content: str) -> None:
    """Write *content* to *path* atomically.

    Creates a temporary file in the same directory, encodes *content* as
    UTF-8, writes the bytes in binary mode (so line endings are emitted
    verbatim with no platform-specific translation), flushes to disk, and
    renames the temporary file over the target.  On Windows ``os.replace``
    is used which is atomic on NTFS.

    Args:
        path: Destination file path.
        content: Text content to write (must be a ``str``; encoded as UTF-8).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(content.encode("utf-8"))
            fh.flush()
            os.fsync(fh.fileno())
            if existing_mode is not None:
                try:
                    os.fchmod(fh.fileno(), existing_mode)
                except (AttributeError, OSError):
                    os.chmod(tmp_path, existing_mode)
        os.replace(tmp_path, str(path))
    except BaseException:
        # Clean up the temporary file on any error.
        try:
            os.unlink(tmp_path)
        except OSError:  # pragma: no cover
            pass
        raise
