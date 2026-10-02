import os
from pathlib import Path
from typing import Union

from pydantic import BaseModel

from istari_digital_client.legacy.v2.models.new_source import NewSource

PathLike = Union[str, os.PathLike, Path]

class RevisionBulkCreateItem(BaseModel):
    path: PathLike
    sources: list[NewSource | str] | None = None
    description: str | None = None
    version_name: str | None = None
    external_identifier: str | None = None
    display_name: str | None = None
