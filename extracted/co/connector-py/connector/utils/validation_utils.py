from __future__ import annotations

from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo


def _get_model_field_info(model: type[BaseModel], field_name: str) -> FieldInfo | None:
    return model.model_fields.get(field_name) if hasattr(model, "model_fields") else None


def _extract_field_title(model: type[BaseModel], field_name: str) -> str:
    field = _get_model_field_info(model, field_name)
    if field is None:
        return field_name

    return field.title or field_name


def get_missing_field_titles(
    error: ValidationError, model: type[BaseModel]
) -> tuple[list[str], bool]:
    """Return a list of titles for fields reported as missing."""

    titles: list[str] = []
    other_errors = False

    for err in error.errors():
        if err.get("type") != "missing":
            other_errors = True
            continue

        loc = err.get("loc", ())
        if not loc:
            continue

        # the last part of the location tuple is the field name
        field_name: str | None = None
        for part in reversed(loc):
            if isinstance(part, str):
                field_name = part
                break
        if field_name is None:
            continue

        title = _extract_field_title(model, field_name)
        titles.append(title)

    return titles, other_errors
