"""Form fields of a company's catalog: the port every form-field store implements, and the rules of the system fields.

The entity is `letschatty.models.company.form_field.FormField`, unchanged: CINTIA reads the `form_fields` collection
directly. There are two kinds of document in it:

- an own field of the company (`is_system_field=False`), and
- the company's customization of a system field (`is_system_field=True`, same `field_key` as the system field): only
  its `question_example` and `description` count. The five system fields themselves are not stored
  (`SystemFormFields`).

The values a contact gave for these fields live with the person (`clients`), not here.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol

from ...models.company.form_field import FormField, SystemFormFields
from ...models.utils.types import StrObjectId


class FormFieldRepository(Protocol):
    """Raises `NotFoundError` when the field does not exist."""

    async def list_live(self, company_id: StrObjectId) -> List[FormField]:
        """Every live document of the company (own fields and customizations), in storage order."""
        ...

    async def add(self, form_field: FormField) -> FormField: ...

    async def update(self, company_id: StrObjectId, field_id: StrObjectId, changes: FormField) -> FormField:
        """Writes only the fields `changes` was built with; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, field_id: StrObjectId) -> FormField:
        """Marks the field deleted (the document stays) and returns it as it was before."""
        ...

    async def add_customization(self, customization: FormField) -> None: ...

    async def replace_customization(self, customization: FormField) -> None:
        """Rewrites the whole stored customization with the same id."""
        ...

    async def remove_customization(self, company_id: StrObjectId, customization_id: StrObjectId) -> None: ...


def find_by_key(fields: List[FormField], field_key: str, is_system_field: bool) -> Optional[FormField]:
    """The first of `fields` with that key and kind."""
    for form_field in fields:
        if form_field.field_key == field_key and form_field.is_system_field == is_system_field:
            return form_field
    return None


def customization_data(field_key: str, company_id: StrObjectId, existing: Optional[FormField],
                       question_example: Optional[str], description: Optional[str]) -> Dict[str, Any]:
    """The document of a customization: what was sent, else what the stored one had (if not empty), else the
    system field's default. Its name is always the system field's."""
    base = SystemFormFields.get_by_key(field_key)
    data: Dict[str, Any] = {"company_id": str(company_id), "is_system_field": True, "name": base["name"],
                            "field_key": field_key}
    if question_example is not None:
        data["question_example"] = question_example
    elif existing and existing.question_example:
        data["question_example"] = existing.question_example
    else:
        data["question_example"] = base.get("question_example")
    if description is not None:
        data["description"] = description
    elif existing and existing.description:
        data["description"] = existing.description
    else:
        data["description"] = base.get("description", "")
    return data
