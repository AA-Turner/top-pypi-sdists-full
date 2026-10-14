from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import ValidationError

from plato.personas.models import LoginInventory, PersonaRecord, PersonaUpdate

if TYPE_CHECKING:
    from plato.cli.vault.client import VaultConsoleClient

# plato.cli.vault imports this module (the persona commands), so its console client is imported inside the
# methods: a top-level import is a circular import when a fresh process imports this module first.


class PersonaConsole:
    """Read and write persona records. Pass ``client`` to reuse an open VaultConsoleClient."""

    def __init__(self, console_url: str | None = None, *, client: VaultConsoleClient | None = None) -> None:
        self._owned = client is None
        if client is None:
            from plato.cli.vault.client import VaultConsoleClient, resolve_base_url

            client = VaultConsoleClient(resolve_base_url(console_url))
        self.client = client

    def __enter__(self) -> PersonaConsole:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owned:
            self.client.close()

    def get(self, login_key: str, account: str) -> PersonaRecord | None:
        """The account's persona record, or None when it has none."""
        from plato.cli.vault.client import NotFound

        try:
            return PersonaRecord.model_validate(self.client.get_persona(login_key, account))
        except NotFound:
            return None

    def put(self, login_key: str, account: str, update: PersonaUpdate) -> PersonaRecord:
        """Merge ``update`` into the record. Only the keys set on ``update`` reach the console."""
        body = update.model_dump(mode="json", exclude_unset=True)
        return PersonaRecord.model_validate(self.client.put_persona(login_key, account, body))

    def inventory(self) -> LoginInventory:
        """The console's login list. Raises VaultConsoleError when it lacks the group or account lists."""
        from plato.cli.vault.client import VaultConsoleError

        try:
            return LoginInventory.model_validate(self.client.list_logins())
        except ValidationError as e:
            where = "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors(include_input=False))
            raise VaultConsoleError(f"the console's login list is unreadable ({where})") from None

    def others_with_persona(self, login_key: str, exclude_account: str) -> list[PersonaRecord]:
        """The persona records of the other accounts of ``login_key``, sorted by account. Raises VaultConsoleError
        when the console's account list may be incomplete: a missing account would move the others into its slot."""
        from plato.cli.vault.client import VaultConsoleError

        inventory = self.inventory()
        if inventory.vault_error:
            raise VaultConsoleError(
                f"the console's account list may be incomplete ({inventory.vault_error}), "
                "so the other accounts cannot be bound to their slots"
            )
        accounts = sorted(
            a.account
            for g in inventory.groups
            if g.login_key.lower() == login_key.lower()
            for a in g.accounts
            if a.has_persona and a.account.lower() != exclude_account.lower()
        )
        records = [self.get(login_key, a) for a in accounts]
        return [r for r in records if r is not None]
