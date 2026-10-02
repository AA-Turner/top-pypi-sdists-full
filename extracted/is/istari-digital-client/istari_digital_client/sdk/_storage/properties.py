from pathlib import Path
from typing import Optional
import mimetypes
import json
from pydantic import BaseModel, model_validator
from typing_extensions import Self


class Properties(BaseModel):
    """
    Class for holding file properties.

    Properties represent metadata about a file — information that describes the file,
    such as its name, size, extension, and other attributes, but not its actual content.

    These properties are typically stored in the filesystem or metadata layers and are
    exposed by Istari's core API.
    """

    file_name: str
    size: int
    extension: str
    mime: Optional[str] = None
    description: Optional[str] = None
    version_name: Optional[str] = None
    external_identifier: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_path(
        cls,
        path: Path,
        description: Optional[str] = None,
        version_name: Optional[str] = None,
        external_identifier: Optional[str] = None,
        display_name: Optional[str] = None,
    ) -> Self:
        # Handle Creo filenames like foo.prt.1 as a special case. We may have a more general case in the future, but this immediate
        # fix is tested and will address an immediate customer pain point.
        extension = "".join(path.suffixes).lstrip(".") if path.suffixes and path.suffixes[0] == ".prt" else path.suffix.lstrip(".")
        return cls(
            file_name=path.name,
            size=path.stat().st_size,
            extension=cls._normalize_extension(extension),
            mime=mimetypes.guess_type(path)[0],
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
            display_name=display_name,
        )

    @staticmethod
    def _normalize_extension(extension: str) -> str:
        """Normalize extension."""
        lc_ext = extension.strip().lower()

        if lc_ext == "catpart":
            return "CATPart"
        elif lc_ext == "catproduct":
            return "CATProduct"
        else:
            return lc_ext

    @model_validator(mode="before")
    def normalize_extension_validator(cls, data):
        """Ensure extension is normalized even when created from dict/JSON."""
        if isinstance(data, dict) and "extension" in data:
            data["extension"] = cls._normalize_extension(data["extension"])
        return data

    @property
    def name(self) -> str:
        """
        The file name.
        """
        return self.file_name

    @property
    def suffix(self) -> str:
        """
        The file suffix (extension with dot).
        """
        return Path(self.file_name).suffix

    @property
    def stem(self) -> str:
        """
        The file stem (name without extension).
        """
        return Path(self.file_name).stem

    def to_bytes(self) -> bytes:
        """
        Convert Properties to bytes using JSON serialization.
        """
        # Use model_dump to get dict, then json.dumps for exact control over format
        return json.dumps(self.model_dump(), separators=(",", ":")).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """
        Create Properties from bytes using JSON deserialization.
        """
        return cls.model_validate_json(data)
