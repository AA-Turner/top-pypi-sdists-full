"""Read the generated static protocol snapshot bundled in the SDK wheel."""

import json
from importlib.resources import files

from labqoat.json_document import JsonDocument


class ManifestFormats:
    """Keep static-format declarations owned by the backend exporter."""

    @staticmethod
    def schema(kind: str) -> JsonDocument:
        """Read trusted SDK data without recanonicalizing every unrelated format."""
        text = files("labqoat.schemas").joinpath("formats.json").read_text(encoding="utf-8")
        formats = JsonDocument.expect_dict(json.loads(text))
        if kind not in formats:
            raise ValueError(f"unknown manifest format: {kind}")
        return JsonDocument.expect_dict(formats[kind])
