"""Canonical immutable file dataset membership."""

import hashlib
import json
from dataclasses import dataclass

from labqoat.argument_codec import encode_result
from labqoat.dataset_files.dataset_file import DatasetFile
from labqoat.json_document import JsonValue
from labqoat.references import Sha256


@dataclass(frozen=True, slots=True, kw_only=True)
class DatasetFileManifest:
    """An ordered set of uniquely named dataset files, including empty revisions."""

    files: tuple[DatasetFile, ...]

    def __post_init__(self) -> None:
        """Require canonical ordering and unique membership."""
        paths = tuple(item.path for item in self.files)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("Dataset files must be ordered and unique")
        self._validate_layout(set(paths))

    @staticmethod
    def _validate_layout(paths: set[str]) -> None:
        """Reject files that would also have to be directories in a logical view."""
        from pathlib import PurePosixPath

        parents = {str(parent) for path in paths for parent in PurePosixPath(path).parents}
        if paths & parents:
            raise ValueError("Dataset file paths cannot also be directories")

    def document(self) -> dict[str, JsonValue]:
        """Return the portable file manifest document."""
        return {"files": [encode_result(item) for item in self.files], "version": 1}

    def encode(self) -> bytes:
        """Encode deterministic manifest bytes."""
        return json.dumps(self.document(), separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()

    def sha256(self) -> Sha256:
        """Return the content identity of the canonical manifest."""
        return Sha256(hashlib.sha256(self.encode()).hexdigest())
