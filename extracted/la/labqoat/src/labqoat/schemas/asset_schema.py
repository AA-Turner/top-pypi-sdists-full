"""Shared static schema ownership for hydrated file/audio references."""

from labqoat.json_document import JsonValue
from labqoat.manifests.manifest_formats import ManifestFormats


class AssetSchema:
    """Require the platform's structured immutable identity for an asset annotation."""

    @staticmethod
    def document() -> dict[str, JsonValue]:
        """Return the backend-owned schema to embed or reference in a captured dataset."""
        return ManifestFormats.schema("asset_reference")

    @classmethod
    def check(cls, schema: dict[str, JsonValue], pointer: str) -> None:
        """Annotations cannot turn arbitrary strings or weaker records into asset references."""
        if "x-labqoat-type" not in schema:
            return
        if schema["x-labqoat-type"] != "asset":
            raise ValueError(f"{pointer}/x-labqoat-type: unsupported semantic type")
        expected = cls.document()
        for key in ("properties", "required", "additionalProperties"):
            if schema.get(key) != expected[key]:
                raise ValueError(f"{pointer}/{key}: asset references require the captured immutable asset shape")
        if schema.get("type") not in ("object", ["object", "null"], ["null", "object"]):
            raise ValueError(f"{pointer}/type: asset references require object storage")
