"""Shared encoding helpers. Owned by the schema emitter."""

from __future__ import annotations

from labqoat.json_document import JsonDocument, JsonValue


class EmitterHelpers:
    """Encode dataclass models without per-field branches."""

    @staticmethod
    def encode_model(obj: object, specs: list[tuple[str, bool, str, str]]) -> JsonDocument:
        """Encode fields, skipping unset optional values."""
        values: JsonDocument = JsonDocument()
        for name, required, annotation, inner in specs:
            value = getattr(obj, name)
            if value is None and not required:
                continue
            values[name] = EmitterHelpers.encode_value(value, annotation, inner)
        return values

    @staticmethod
    def encode_value(value: object, annotation: str, inner: str) -> JsonValue:
        """Encode one value, handling nested models."""
        if value is None:
            return None
        if isinstance(value, list):
            return [EmitterHelpers.encode_item(item, inner) for item in value]
        return EmitterHelpers.encode_item(value, annotation)

    @staticmethod
    def encode_item(value: object, inner: str) -> JsonValue:
        """Encode one list item."""
        if inner in EmitterHelpers.model_titles():
            encode = getattr(value, "to_dict", None)
            if callable(encode):
                return JsonDocument.expect_dict(encode())
        if isinstance(value, dict):
            return JsonDocument(value)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        raise TypeError(f"Cannot encode {inner or 'value'} as JSON.")

    @staticmethod
    def model_titles() -> set[str]:
        """Return known model titles for nested encoding."""
        try:
            from labqoat._generated import MODEL_TITLES

            return set(MODEL_TITLES)
        except ImportError:
            return set()
