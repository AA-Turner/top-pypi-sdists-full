import io
import os
import pathlib
import shutil
from typing import TYPE_CHECKING, Optional, Union
from urllib.parse import urlparse

import requests

if TYPE_CHECKING:
    from PIL.Image import Image

from abstra_internals.constants import get_uploads_dir
from abstra_internals.utils.file import (
    get_tmp_upload_dir,
    make_random_tmp_path,
    upload_file,
)

FILE_CHUNK_SIZE = 8192


def _local_uploads_path(url: str) -> Optional[pathlib.Path]:
    """When a ``/_files/`` reference points at a file the player (cloud-api)
    already wrote to the shared persistent uploads dir on EFS, return its local
    path so the worker reads it directly instead of round-tripping over HTTP.

    Else, returns ``None`` (caller falls back to HTTP / legacy handling).
    """
    path = urlparse(url).path
    prefix = "/_files/"
    if not path.startswith(prefix):
        return None
    base = get_uploads_dir().resolve()
    candidate = (base / path[len(prefix) :]).resolve()
    try:
        if os.path.commonpath([str(base), str(candidate)]) != str(base):
            return None
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def upload_widget_file(
    file: Union[str, io.IOBase, pathlib.Path, "Image"],
    custom_name: Optional[str] = None,
) -> str:
    if not file:
        return ""

    if isinstance(file, (io.IOBase, pathlib.Path, str)):
        return upload_file(file, custom_name)

    from PIL.Image import Image

    if isinstance(file, Image):
        path = make_random_tmp_path(custom_name)
        file.save(str(path))
        return upload_file(open(path, "rb"), custom_name)

    # FileResponse. TODO: check with isinstance without circular import
    if hasattr(file, "_url"):
        if file._url.startswith("http"):
            return file._url  # already an absolute URL, browser can fetch directly
        return upload_file(file.file)  # local /_files/ URL (legacy), re-upload

    raise ValueError(f"Cannot convert {type(file)}")


def download_to_path(url: str) -> pathlib.Path:
    # TODO: circular import - god help me
    from abstra_internals.controllers.sdk.sdk_context import (
        SDKContextStore,
    )

    execution = SDKContextStore.get_execution()
    save_dir = get_uploads_dir() / execution.id
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / pathlib.Path(url).name

    local = _local_uploads_path(url)
    if local is not None:
        shutil.copy(local, save_path)
        return save_path

    if url.startswith("http://") or url.startswith("https://"):
        with save_path.open("wb") as f, requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=FILE_CHUNK_SIZE):
                f.write(chunk)

        return save_path

    elif url.startswith("/_files/"):
        tmp_name = url[len("/_files/") :]
        path = get_tmp_upload_dir() / tmp_name
        shutil.copy(path, save_path)

        return save_path

    raise ValueError(f"Cannot download {url}")
