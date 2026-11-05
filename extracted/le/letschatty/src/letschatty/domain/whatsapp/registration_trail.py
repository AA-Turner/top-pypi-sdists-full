"""The trail of a WhatsApp registration («rastro del alta»): the `MetaRegister` of one connection — the form, and in
`activity` what Meta answered at each step — kept as one document of `registration_activity`. The port every store of
it implements.

Not a catalog (ADR-010 of api-chatty): nobody reads it in the code, lists it or edits it by hand. The registration opens
it before touching Meta and saves it after each step. It keeps `access_token` and `code` on purpose (api-chatty's
`common/redaction.py`): it is the record of what happened.
"""
from __future__ import annotations

from typing import Protocol

from ...models.forms.company.meta_register import MetaRegister


class RegistrationTrail(Protocol):
    async def open(self, company_id: str, form: MetaRegister) -> None:
        """Stores the form as a new document, with the form's own id."""
        ...

    async def save(self, company_id: str, form: MetaRegister) -> None:
        """Stamps `updated_at` on the form and overwrites the stored fields of its document. Raises `NotFoundError`
        when there is no document with the form's id."""
        ...
