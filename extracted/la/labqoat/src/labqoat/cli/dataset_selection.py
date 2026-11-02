"""Validate and select logical manifest files before acquiring any bytes."""

from collections.abc import Mapping, Sequence
from fnmatch import fnmatchcase

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.storage.verified_file import VerifiedFile


class DatasetSelection:
    """Apply repeatable inclusive glob patterns to canonical logical paths."""

    @staticmethod
    def select(files: Sequence[Mapping[str, JsonValue]], patterns: Sequence[str]) -> list[Mapping[str, JsonValue]]:
        """Select the union, requiring each explicit pattern to match at least once."""
        paths = [str(VerifiedFile.relative(JsonDocument.expect_scalar(item.get("path"), str))) for item in files]
        if len(paths) != len(set(paths)):
            raise ValueError("Dataset manifest contains duplicate paths")
        for pattern in patterns:
            VerifiedFile.relative(pattern)
            if not any(fnmatchcase(path, pattern) for path in paths):
                raise ValueError(f"Dataset include pattern matched no files: {pattern}")
        return [
            entry
            for path, entry in zip(paths, files, strict=True)
            if not patterns or any(fnmatchcase(path, pattern) for pattern in patterns)
        ]
