"""Config and AsyncConfig — rich model objects for a single configuration."""

from __future__ import annotations

import datetime
import logging
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from smplkit.config.client import AsyncConfigClient, ConfigClient
    from smplkit.management.client import (
        AsyncConfigClient as AsyncMgmtConfigClient,
        ConfigClient as MgmtConfigClient,
    )

logger = logging.getLogger("smplkit")


class ItemType(str, Enum):
    """Type of a :class:`ConfigItem` value."""

    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    NUMBER = "NUMBER"
    STRING = "STRING"


class ConfigItem:
    """A single typed item in a :class:`Config`."""

    name: str
    value: Any
    type: ItemType
    description: str | None

    def __init__(
        self,
        name: str,
        value: Any,
        type: ItemType | str,
        *,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.value = value
        self.type = type if isinstance(type, ItemType) else ItemType(type)
        self.description = description

    def __repr__(self) -> str:
        return f"ConfigItem(name={self.name!r}, value={self.value!r}, type={self.type.value})"


class ConfigEnvironment:
    """Per-environment value overrides for a :class:`Config`.

    Read-only inspection container.  Mutation is performed via :class:`Config`'s
    setters with ``environment="..."`` (e.g. ``cfg.set_string("k", "v",
    environment="production")``).

    Per ADR-024 §2.4 each env entry on the wire is the flat override map
    ``{key: rawValue}`` — no per-override ``type`` / ``description``.
    """

    def __init__(self, values: dict[str, Any] | None = None) -> None:
        self._values_raw: dict[str, Any] = {}
        if values:
            for k, v in values.items():
                # Tolerate legacy wrapped inputs ``{key: {"value": v}}`` for
                # constructor compatibility, but store flat going forward.
                if isinstance(v, dict) and "value" in v and set(v.keys()).issubset({"value", "type", "description"}):
                    self._values_raw[k] = v["value"]
                else:
                    self._values_raw[k] = v

    @property
    def values(self) -> dict[str, Any]:
        """Return overrides as a plain dict ``{key: raw_value}``."""
        return dict(self._values_raw)

    @property
    def values_raw(self) -> dict[str, Any]:
        """Return the flat overrides ``{key: raw_value}`` (read-only shallow copy).

        Aliased to :attr:`values` now that the wire shape no longer carries
        per-override ``type`` / ``description`` metadata.
        """
        return dict(self._values_raw)

    def __repr__(self) -> str:
        return f"ConfigEnvironment(values={self.values!r})"


def _convert_environments(value: dict[str, Any] | None) -> dict[str, ConfigEnvironment]:
    """Coerce a dict input into ``dict[str, ConfigEnvironment]``.

    Accepts pre-built :class:`ConfigEnvironment` instances and the flat
    wire-shaped ``{env_id: {key: rawValue}}`` dicts produced by
    :func:`_extract_environments`.
    """
    if not value:
        return {}
    result: dict[str, ConfigEnvironment] = {}
    for env_id, env_data in value.items():
        if isinstance(env_data, ConfigEnvironment):
            result[env_id] = env_data
        elif isinstance(env_data, dict):
            result[env_id] = ConfigEnvironment(values=env_data)
        else:
            result[env_id] = ConfigEnvironment()
    return result


def _environments_to_wire(environments: dict[str, ConfigEnvironment]) -> dict[str, Any]:
    """Convert a typed environments dict to the flat wire-shaped dict.

    Per ADR-024 §2.4 the wire shape is ``{env: {key: rawValue}}``. The same
    shape is what the resolver consumes, so this output is suitable for both
    the mgmt save path and chain assembly.
    """
    return {env_id: dict(env._values_raw) for env_id, env in environments.items()}


class Config:
    """A configuration resource fetched from the Smpl Config service.

    Attributes:
        id: The config identifier (slug), or ``None`` for unsaved configs.
        name: Display name.
        description: Optional description.
        parent: Parent config id (slug), or ``None`` for root configs.
        items: Base values dict (``{key: raw_value}``), settable.
        items_raw: Full typed items (``{key: {value, type, description}}``).
        environments: Dict mapping environment names to their overrides.
        created_at: Creation timestamp.
        updated_at: Last-modified timestamp.
    """

    id: str | None
    name: str
    description: str | None
    parent: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    def __init__(
        self,
        client: MgmtConfigClient | ConfigClient | None = None,
        *,
        id: str | None = None,
        name: str,
        description: str | None = None,
        parent: str | None = None,
        items: dict[str, Any] | None = None,
        environments: dict[str, Any] | None = None,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.description = description
        self.parent = parent
        self._items_raw = items or {}
        self._environments: dict[str, ConfigEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def items(self) -> dict[str, Any]:
        """Read-only plain ``{key: raw_value}`` view of base items.

        Mutate via :meth:`set` / :meth:`set_string` / :meth:`set_number` /
        :meth:`set_boolean` / :meth:`set_json` / :meth:`remove`.
        """
        return {k: v["value"] if isinstance(v, dict) and "value" in v else v for k, v in self._items_raw.items()}

    @property
    def items_raw(self) -> dict[str, Any]:
        """Return the full typed items ``{key: {value, type, description}}`` (read-only deep copy)."""
        return {k: dict(v) if isinstance(v, dict) else v for k, v in self._items_raw.items()}

    @property
    def environments(self) -> dict[str, ConfigEnvironment]:
        """Read-only view of per-environment overrides keyed by environment id.

        Mutate via the ``environment="..."`` kwarg on :meth:`set` / :meth:`set_string`
        / :meth:`set_number` / :meth:`set_boolean` / :meth:`set_json` / :meth:`remove`.
        """
        return dict(self._environments)

    def _items_target(self, environment: str | None) -> dict[str, Any]:
        """Return the dict that ``set()`` / ``remove()`` should mutate.

        For the base config this is the typed-items dict storing
        ``{key: {value, type, description}}``. For an environment override
        it is the flat overrides dict storing ``{key: raw_value}`` per
        ADR-024 §2.4.
        """
        if environment is None:
            return self._items_raw
        env = self._environments.get(environment)
        if env is None:
            env = ConfigEnvironment()
            self._environments[environment] = env
        return env._values_raw

    def set(self, item: ConfigItem, *, environment: str | None = None) -> None:
        """Set (or replace) an item.  When ``environment`` is given, sets an override on that environment.

        Per ADR-024 §2.4 environment overrides on the wire carry only the
        raw value — the declared ``type`` / ``description`` come from the
        base item — so the ``ConfigItem``'s type and description are
        ignored when ``environment`` is supplied.
        """
        if environment is None:
            raw: dict[str, Any] = {"value": item.value, "type": item.type.value}
            if item.description is not None:
                raw["description"] = item.description
            self._items_target(environment)[item.name] = raw
        else:
            self._items_target(environment)[item.name] = item.value

    def remove(self, name: str, *, environment: str | None = None) -> None:
        """Remove an item by name.  When ``environment`` is given, removes the per-environment override only."""
        self._items_target(environment).pop(name, None)

    def set_string(
        self, name: str, value: str, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a STRING item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.STRING, description=description), environment=environment)

    def set_number(
        self, name: str, value: int | float, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a NUMBER item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.NUMBER, description=description), environment=environment)

    def set_boolean(
        self, name: str, value: bool, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a BOOLEAN item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.BOOLEAN, description=description), environment=environment)

    def set_json(
        self, name: str, value: Any, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a JSON item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.JSON, description=description), environment=environment)

    def save(self) -> None:
        """Persist this config to the server.

        Creates a new config if unsaved, or updates the existing one.

        Raises:
            NotFoundError: If the config no longer exists (update).
            ValidationError: If the server rejects the request.
            RuntimeError: If the model was constructed without a management client.
        """
        if self._client is None:
            raise RuntimeError("Config was constructed without a client; cannot save")
        if self.created_at is None:
            other = self._client._create_config(self)
        else:
            other = self._client._update_config_from_model(self)
        self._apply(other)

    def delete(self) -> None:
        """Delete this config from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("Config was constructed without a client or id; cannot delete")
        self._client.delete(self.id)

    def _apply(self, other: Config) -> None:
        """Copy all properties from *other* into this instance."""
        self.id = other.id
        self.name = other.name
        self.description = other.description
        self.parent = other.parent
        self._items_raw = other._items_raw
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def _build_chain(self, configs: list[Config] | None = None) -> list[dict[str, Any]]:
        """Walk the parent chain and return config data dicts child-to-root.

        Args:
            configs: Optional pre-fetched list of configs to look up parents
                by ID, avoiding extra network calls.
        """
        chain = [
            {
                "id": self.id,
                "items": self._items_raw,
                "environments": _environments_to_wire(self._environments),
            }
        ]
        current = self
        configs_by_id = {c.id: c for c in configs} if configs else {}
        while current.parent is not None:
            parent_config = configs_by_id.get(current.parent)
            if parent_config is None:
                if self._client is None:
                    raise RuntimeError(
                        f"cannot resolve parent config {current.parent!r} without a client",
                    )
                parent_config = self._client.get(current.parent)
            chain.append(
                {
                    "id": parent_config.id,
                    "items": parent_config._items_raw,
                    "environments": _environments_to_wire(parent_config._environments),
                }
            )
            current = parent_config
        return chain

    def __repr__(self) -> str:
        return f"Config(id={self.id!r}, name={self.name!r})"


class AsyncConfig:
    """Async variant of :class:`Config`.

    Attributes:
        id: The config identifier (slug), or ``None`` for unsaved configs.
        name: Display name.
        description: Optional description.
        parent: Parent config id (slug), or ``None`` for root configs.
        items: Base values dict (``{key: raw_value}``), settable.
        items_raw: Full typed items (``{key: {value, type, description}}``).
        environments: Dict mapping environment names to their overrides.
        created_at: Creation timestamp.
        updated_at: Last-modified timestamp.
    """

    id: str | None
    name: str
    description: str | None
    parent: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    def __init__(
        self,
        client: AsyncMgmtConfigClient | AsyncConfigClient | None = None,
        *,
        id: str | None = None,
        name: str,
        description: str | None = None,
        parent: str | None = None,
        items: dict[str, Any] | None = None,
        environments: dict[str, Any] | None = None,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.description = description
        self.parent = parent
        self._items_raw = items or {}
        self._environments: dict[str, ConfigEnvironment] = _convert_environments(environments)
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def items(self) -> dict[str, Any]:
        """Read-only plain ``{key: raw_value}`` view of base items.

        Mutate via :meth:`set` / :meth:`set_string` / :meth:`set_number` /
        :meth:`set_boolean` / :meth:`set_json` / :meth:`remove`.
        """
        return {k: v["value"] if isinstance(v, dict) and "value" in v else v for k, v in self._items_raw.items()}

    @property
    def items_raw(self) -> dict[str, Any]:
        """Return the full typed items ``{key: {value, type, description}}`` (read-only deep copy)."""
        return {k: dict(v) if isinstance(v, dict) else v for k, v in self._items_raw.items()}

    @property
    def environments(self) -> dict[str, ConfigEnvironment]:
        """Read-only view of per-environment overrides keyed by environment id.

        Mutate via the ``environment="..."`` kwarg on :meth:`set` / :meth:`set_string`
        / :meth:`set_number` / :meth:`set_boolean` / :meth:`set_json` / :meth:`remove`.
        """
        return dict(self._environments)

    def _items_target(self, environment: str | None) -> dict[str, Any]:
        """Return the dict that ``set()`` / ``remove()`` should mutate.

        For the base config this is the typed-items dict storing
        ``{key: {value, type, description}}``. For an environment override
        it is the flat overrides dict storing ``{key: raw_value}`` per
        ADR-024 §2.4.
        """
        if environment is None:
            return self._items_raw
        env = self._environments.get(environment)
        if env is None:
            env = ConfigEnvironment()
            self._environments[environment] = env
        return env._values_raw

    def set(self, item: ConfigItem, *, environment: str | None = None) -> None:
        """Set (or replace) an item.  When ``environment`` is given, sets an override on that environment.

        Per ADR-024 §2.4 environment overrides on the wire carry only the
        raw value — the declared ``type`` / ``description`` come from the
        base item — so the ``ConfigItem``'s type and description are
        ignored when ``environment`` is supplied.
        """
        if environment is None:
            raw: dict[str, Any] = {"value": item.value, "type": item.type.value}
            if item.description is not None:
                raw["description"] = item.description
            self._items_target(environment)[item.name] = raw
        else:
            self._items_target(environment)[item.name] = item.value

    def remove(self, name: str, *, environment: str | None = None) -> None:
        """Remove an item by name.  When ``environment`` is given, removes the per-environment override only."""
        self._items_target(environment).pop(name, None)

    def set_string(
        self, name: str, value: str, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a STRING item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.STRING, description=description), environment=environment)

    def set_number(
        self, name: str, value: int | float, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a NUMBER item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.NUMBER, description=description), environment=environment)

    def set_boolean(
        self, name: str, value: bool, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a BOOLEAN item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.BOOLEAN, description=description), environment=environment)

    def set_json(
        self, name: str, value: Any, *, description: str | None = None, environment: str | None = None
    ) -> None:
        """Convenience: set a JSON item (or environment override)."""
        self.set(ConfigItem(name, value, ItemType.JSON, description=description), environment=environment)

    async def save(self) -> None:
        """Persist this config to the server.

        Creates a new config if unsaved, or updates the existing one.

        Raises:
            NotFoundError: If the config no longer exists (update).
            ValidationError: If the server rejects the request.
            RuntimeError: If the model was constructed without a management client.
        """
        if self._client is None:
            raise RuntimeError("AsyncConfig was constructed without a client; cannot save")
        if self.created_at is None:
            other = await self._client._create_config(self)
        else:
            other = await self._client._update_config_from_model(self)
        self._apply(other)

    async def delete(self) -> None:
        """Delete this config from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("AsyncConfig was constructed without a client or id; cannot delete")
        await self._client.delete(self.id)

    def _apply(self, other: AsyncConfig) -> None:
        """Copy all properties from *other* into this instance."""
        self.id = other.id
        self.name = other.name
        self.description = other.description
        self.parent = other.parent
        self._items_raw = other._items_raw
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    async def _build_chain(self, configs: list[AsyncConfig] | None = None) -> list[dict[str, Any]]:
        """Walk the parent chain and return config data dicts child-to-root.

        Args:
            configs: Optional pre-fetched list of configs to look up parents
                by ID, avoiding extra network calls.
        """
        chain = [
            {
                "id": self.id,
                "items": self._items_raw,
                "environments": _environments_to_wire(self._environments),
            }
        ]
        current = self
        configs_by_id = {c.id: c for c in configs} if configs else {}
        while current.parent is not None:
            parent_config = configs_by_id.get(current.parent)
            if parent_config is None:
                if self._client is None:
                    raise RuntimeError(
                        f"cannot resolve parent config {current.parent!r} without a client",
                    )
                parent_config = await self._client.get(current.parent)
            chain.append(
                {
                    "id": parent_config.id,
                    "items": parent_config._items_raw,
                    "environments": _environments_to_wire(parent_config._environments),
                }
            )
            current = parent_config
        return chain

    def __repr__(self) -> str:
        return f"AsyncConfig(id={self.id!r}, name={self.name!r})"
