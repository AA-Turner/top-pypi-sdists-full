import mimetypes
import shutil
from pathlib import Path
from typing import Union
from urllib.parse import quote
from uuid import uuid4

import requests

from abstra_internals.constants import (
    get_persistent_dir,
    get_project_url,
    get_public_dir,
)
from abstra_internals.environment import IS_PRODUCTION
from abstra_internals.logger import AbstraLogger
from abstra_internals.settings import Settings


def _upload_public_file_to_cloud(file_path: Path, relative_path: str) -> None:
    project_url = get_project_url()
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        response = requests.put(
            f"{project_url}/_public/{relative_path}",
            data=f,
            headers={"Content-Type": content_type},
            timeout=300,
        )
        response.raise_for_status()


def create_public_link(path: Union[str, Path]) -> str:
    """
    Create a public link for a file by copying it to the public directory

    Args:
        path (Union[str, pathlib.Path]): Path to the file

    Returns:
        str: Public link to the file
    """

    if isinstance(path, str):
        path = Settings.root_path / path

    if not path.exists():
        raise Exception("path does not exist")

    file_id = str(uuid4())
    local_path = f"{file_id}/{path.name}"
    url_path = f"{file_id}/{quote(path.name, safe='')}"

    public_path = get_public_dir() / local_path
    public_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(path, public_path)

    if IS_PRODUCTION:
        try:
            _upload_public_file_to_cloud(public_path, url_path)
        except Exception as e:
            AbstraLogger.capture_exception(e)

    return f"{get_project_url()}/_public/{url_path}"


__all__ = [
    "get_public_dir",
    "get_persistent_dir",
    "create_public_link",
]
