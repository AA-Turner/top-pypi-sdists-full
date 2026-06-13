"""Active-record models for ``client.account.*`` resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from smplkit.account.clients import (
        AsyncSettingsClient,
        SettingsClient,
    )


# ---------------------------------------------------------------------------
# AccountSettings
# ---------------------------------------------------------------------------


class _AccountSettingsBase:
    """Active-record account-settings model.

    The wire format is opaque JSON. Documented keys are exposed as
    typed properties; unknown keys live in :attr:`raw`. ``save()``
    writes the full settings object back.
    """

    _data: dict[str, Any]

    def __init__(self, *, data: dict[str, Any] | None = None) -> None:
        self._data = dict(data) if data else {}

    @property
    def raw(self) -> dict[str, Any]:
        """The full settings dict. Mutations are persisted on save()."""
        return self._data

    @raw.setter
    def raw(self, value: dict[str, Any]) -> None:
        self._data = dict(value)

    @property
    def environment_order(self) -> list[str]:
        """Canonical ordering of STANDARD environments. Empty list if unset."""
        return list(self._data.get("environment_order") or [])

    @environment_order.setter
    def environment_order(self, value: list[str]) -> None:
        self._data["environment_order"] = list(value)

    def __repr__(self) -> str:
        return f"AccountSettings({self._data!r})"

    def _apply(self, other: _AccountSettingsBase) -> None:
        self._data = dict(other._data)


class AccountSettings(_AccountSettingsBase):
    """Active-record account-settings model (sync ``save()``)."""

    def __init__(
        self,
        client: SettingsClient | None = None,
        *,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(data=data)
        self._client = client

    def save(self) -> None:
        """Write the full settings object back to the account.

        Raises:
            RuntimeError: If this model was constructed without a client
                (e.g. built by hand rather than returned from ``get()``).
        """
        if self._client is None:
            raise RuntimeError("AccountSettings was constructed without a client; cannot save")
        other = self._client._save(self._data)
        self._apply(other)


class AsyncAccountSettings(_AccountSettingsBase):
    """Active-record account-settings model (async ``save()``)."""

    def __init__(
        self,
        client: AsyncSettingsClient | None = None,
        *,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(data=data)
        self._client = client

    async def save(self) -> None:
        """Write the full settings object back to the account.

        Raises:
            RuntimeError: If this model was constructed without a client
                (e.g. built by hand rather than returned from ``get()``).
        """
        if self._client is None:
            raise RuntimeError("AsyncAccountSettings was constructed without a client; cannot save")
        other = await self._client._save(self._data)
        self._apply(other)
