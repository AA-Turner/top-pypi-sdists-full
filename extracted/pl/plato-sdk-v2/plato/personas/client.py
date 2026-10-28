from __future__ import annotations

from typing import TYPE_CHECKING

from plato.chronos.login_vault import normalize_key
from plato.personas.models import PersonaRecord, PersonaUpdate

if TYPE_CHECKING:
    from plato.chronos.login_vault import LoginVault


class PersonaVault:
    """Persona records in the Chronos login vault. ``vault`` is an open LoginVault; the caller closes it."""

    def __init__(self, vault: LoginVault) -> None:
        self.vault = vault

    def get(self, login_key: str, account: str) -> PersonaRecord | None:
        """The account's persona record, or None when it has none."""
        found = self.vault.get_account_persona(login_key, account)
        return None if found is None else PersonaRecord.model_validate(found.model_dump(mode="json"))

    def put(self, login_key: str, account: str, update: PersonaUpdate) -> PersonaRecord:
        """Merge ``update`` into the record. Only the keys set on ``update`` are sent."""
        body = update.model_dump(mode="json", exclude_unset=True)
        return PersonaRecord.model_validate(
            self.vault.set_account_persona(login_key, account, body).model_dump(mode="json")
        )

    def records(self, login_key: str | None = None) -> list[PersonaRecord]:
        """Every live account's persona record (of ``login_key`` only, when given), by (login_key, account)."""
        listing = self.vault.list_account_personas(login_key)
        return [PersonaRecord.model_validate(r.model_dump(mode="json")) for r in listing.accounts]

    def others_with_persona(self, login_key: str, exclude_account: str) -> list[PersonaRecord]:
        """The persona records of the other accounts of ``login_key``, sorted by account."""
        return sorted(
            (r for r in self.records(login_key) if normalize_key(r.account) != normalize_key(exclude_account)),
            key=lambda r: r.account,
        )
