# Copyright 2023 Agnostiq Inc.

"""Models for volumes"""
import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, field_validator

from covalent_cloud.shared.classes.exceptions import CovalentSDKError

# Regex pattern for a valid directory name
# ^(/)? - Optionally starts with '/'
# ([\w-]+)$ - Followed by word characters or hyphens, and must end here
VOLUME_NAME_PATTERN = r"^/?([\w-]+)$"


class BaseVolume(BaseModel):
    name: str

    @staticmethod
    def get_valid_volume_name(name):
        """Get valid volume name.

        Args:
            name: Volume name

        Returns:
            Sanitized Volume name [str] if valid, else None

        """
        VOLUME_NAME_PATTERN = r"^/?([\w-]+)$"
        match = re.match(VOLUME_NAME_PATTERN, name)
        sanitized_name = match.group(1) if match else None
        is_matched = match is not None
        is_valid = is_matched and len(name) < 50
        return sanitized_name if is_valid else None

    @field_validator("name")
    def name_must_be_valid_directory(cls, v):
        valid_name = BaseVolume.get_valid_volume_name(v)
        if not valid_name:
            raise CovalentSDKError(
                "Name must be a valid directory name without subdirectories", "volume/invalid-name"
            )
        return valid_name

    @property
    def path(self):
        return f"/{self.name}"

    def __str__(self):
        return self.path

    def __truediv__(self, other):
        return Path(f"/volumes/{self.path}") / other


class Volume(BaseVolume):
    """Volume model"""

    id: int
    name: str
    deployment_id: Optional[str] = None
