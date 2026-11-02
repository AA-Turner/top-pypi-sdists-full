"""Capture caller-relative path declarations without reading their contents."""

import inspect
import os
from pathlib import Path


class LocalPath:
    """Anchor a local input at the authored call site rather than the launcher's cwd."""

    @staticmethod
    def capture(path: Path | str) -> Path:
        """Retain an absolute lexical path; publication later verifies every component."""
        origin = Path(inspect.stack(context=0)[2].filename).parent
        return Path(os.path.abspath(origin / path))
