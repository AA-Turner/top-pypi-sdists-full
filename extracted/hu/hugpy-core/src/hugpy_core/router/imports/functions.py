"""Pure helpers shared across the router."""
from __future__ import annotations

import os
from typing import Optional, Tuple

from hugpy_core.router.imports import constants as C


def split_model(name: str) -> Tuple[str, Optional[str]]:
    """'model@opts' -> ('model', 'opts'); 'model' -> ('model', None). The options are
    the box's own variant syntax (hugpy-wrapper's model@options) and pass through."""
    name = (name or "").strip()
    base, sep, opts = name.partition("@")
    return base, (opts.strip() or None) if sep else None


def config_dir() -> str:
    from hugpy_resources.imports.functions import application_paths as app_dirs
    return os.path.join(app_dirs.config_dir(), C.STORE_SUBDIR)


def data_dir() -> str:
    from hugpy_resources.imports.functions import application_paths as app_dirs
    return os.path.join(app_dirs.data_dir(), C.STORE_SUBDIR)


def boxes_path() -> str:
    return os.environ.get(C.ENV_BOXES, "").strip() or os.path.join(config_dir(), C.BOXES_FILENAME)
