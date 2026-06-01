"""Flag model classes."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from smplkit.flags.client import AsyncFlagsClient, FlagsClient
    from smplkit.management.client import AsyncFlagsClient as AsyncMgmtFlagsClient
    from smplkit.management.client import FlagsClient as MgmtFlagsClient


@dataclasses.dataclass(frozen=True)
class FlagValue:
    """A constrained value entry on a :class:`Flag`.

    Lives in :attr:`Flag.values`.  Frozen — author values via
    :meth:`Flag.add_value` / :meth:`Flag.remove_value` /
    :meth:`Flag.clear_values`.
    """

    name: str
    value: Any


@dataclasses.dataclass(frozen=True)
class FlagRule:
    """A single targeting rule on a :class:`Flag`.

    Lives in :attr:`FlagEnvironment.rules`.  Frozen — author rules via the
    :class:`smplkit.Rule` fluent builder and pass through :meth:`Flag.add_rule`.

    Attributes:
        logic: JSON Logic predicate.  Empty dict means "always match".
        value: Value to serve when ``logic`` evaluates truthy.
        description: Human-readable label (optional).
    """

    logic: dict[str, Any]
    value: Any = None
    description: str | None = None


@dataclasses.dataclass(frozen=True)
class FlagEnvironment:
    """Per-environment configuration on a :class:`Flag`.

    Lives at ``flag.environments[env_name]`` (a ``dict[str, FlagEnvironment]``).
    Frozen — mutate via :meth:`Flag.add_rule` / :meth:`Flag.enable_rules` /
    :meth:`Flag.disable_rules` / :meth:`Flag.set_default` / :meth:`Flag.clear_rules`
    (with ``environment="..."``).

    Attributes:
        enabled: Whether the flag is active in this environment.
        default: Environment-specific default override (``None`` means no override).
        rules: Targeting rules to evaluate, in order.
    """

    enabled: bool = True
    default: Any = None
    rules: tuple[FlagRule, ...] = ()


def _replace_env(
    environments: dict[str, FlagEnvironment],
    env_key: str,
    **fields: Any,
) -> None:
    """Replace per-env config (frozen), creating a default instance if missing."""
    existing = environments.get(env_key, FlagEnvironment())
    environments[env_key] = dataclasses.replace(existing, **fields)


class Flag:
    """A flag resource (sync).

    Provides management operations (save, add_rule, environment settings)
    and runtime evaluation via :meth:`get`.

    Use typed variants (BooleanFlag, StringFlag, NumberFlag, JsonFlag)
    for type-safe :meth:`get` return values.
    """

    id: str | None
    name: str
    type: str
    default: Any
    description: str | None
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: FlagsClient | MgmtFlagsClient | None = None,
        *,
        id: str | None = None,
        name: str,
        type: str,
        default: Any,
        values: list[FlagValue] | None = None,
        description: str | None = None,
        environments: dict[str, FlagEnvironment] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.type = type
        self.default = default
        self._values: list[FlagValue] | None = list(values) if values is not None else None
        self.description = description
        self._environments: dict[str, FlagEnvironment] = dict(environments) if environments is not None else {}
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def values(self) -> list[FlagValue] | None:
        """Read-only view of constrained values.

        ``None`` means unconstrained.  Mutate via :meth:`add_value` /
        :meth:`remove_value` / :meth:`clear_values`.
        """
        return list(self._values) if self._values is not None else None

    @property
    def environments(self) -> dict[str, FlagEnvironment]:
        """Read-only view of per-environment configuration.

        Mutate via :meth:`add_rule` / :meth:`enable_rules` / :meth:`disable_rules` /
        :meth:`set_default` (with ``environment="..."``) / :meth:`clear_rules`.
        """
        return dict(self._environments)

    # ------------------------------------------------------------------
    # Management: save (create or update)
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Persist this flag to the server.

        Creates a new flag if unsaved, or updates the existing one.
        Requires a management client (i.e. the flag was constructed via
        ``mgmt.flags.new*`` or returned from ``mgmt.flags.get/list``).
        """
        if self._client is None:
            raise RuntimeError("Flag was constructed without a client; cannot save")
        if self.created_at is None:
            created = self._client._create_flag(self)
            self._apply(created)
        else:
            updated = self._client._update_flag(flag=self)
            self._apply(updated)

    def delete(self) -> None:
        """Delete this flag from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("Flag was constructed without a client or id; cannot delete")
        self._client.delete(self.id)

    # ------------------------------------------------------------------
    # Management: local mutations
    # ------------------------------------------------------------------

    def add_rule(self, built_rule: dict[str, Any]) -> Flag:
        """Append a rule to a specific environment.

        The *built_rule* dict must include an ``"environment"`` key.
        Call :meth:`save` to persist.

        Returns *self* for chaining.
        """
        env_key = built_rule.get("environment")
        if env_key is None:
            raise ValueError(
                "Built rule must include 'environment' key. Use Rule(..., environment='env_key').when(...).serve(...)"
            )
        flag_rule = FlagRule(
            logic=dict(built_rule.get("logic") or {}),
            value=built_rule.get("value"),
            description=built_rule.get("description"),
        )
        existing = self._environments.get(env_key, FlagEnvironment())
        _replace_env(self._environments, env_key, rules=(*existing.rules, flag_rule))
        return self

    def enable_rules(self, *, environment: str | None = None) -> None:
        """Enable rule evaluation.  Call :meth:`save` to persist.

        With ``environment="..."`` scopes to that single environment; without,
        enables rules in every environment configured on this flag.
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, enabled=True)
        else:
            _replace_env(self._environments, environment, enabled=True)

    def disable_rules(self, *, environment: str | None = None) -> None:
        """Disable rule evaluation (kill switch).  Call :meth:`save` to persist.

        With ``environment="..."`` scopes to that single environment; without,
        disables rules in every environment configured on this flag.  When
        disabled, :meth:`get` skips rules and returns the env-specific default
        (or the flag's base default).
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, enabled=False)
        else:
            _replace_env(self._environments, environment, enabled=False)

    def set_default(self, value: Any, *, environment: str | None = None) -> None:
        """Set the flag's default served value.

        With ``environment=None`` (the default), updates the flag-level default
        used when no environment-specific override applies.  With ``environment="..."``,
        sets the per-environment default served when no rule matches.

        Call :meth:`save` to persist.
        """
        if environment is None:
            self.default = value
        else:
            _replace_env(self._environments, environment, default=value)

    def clear_default(self, *, environment: str) -> None:
        """Clear the per-environment default override on *environment*.

        After clearing, the environment falls back to the flag's base default
        when no rule matches.  Call :meth:`save` to persist.
        """
        if environment in self._environments:
            _replace_env(self._environments, environment, default=None)

    def clear_rules(self, *, environment: str | None = None) -> None:
        """Remove rules.  Call :meth:`save` to persist.

        With ``environment="..."`` scopes to that single environment; without,
        removes rules from every environment configured on this flag.
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, rules=())
        else:
            _replace_env(self._environments, environment, rules=())

    def add_value(self, name: str, value: Any) -> Flag:
        """Append a constrained value to the flag's values list. Returns *self* for chaining."""
        if self._values is None:
            self._values = []
        self._values.append(FlagValue(name=name, value=value))
        return self

    def remove_value(self, value: Any) -> Flag:
        """Remove the first values entry whose ``value`` field matches.  Returns *self* for chaining."""
        if self._values is None:
            return self
        self._values = [v for v in self._values if v.value != value]
        return self

    def clear_values(self) -> None:
        """Set values to ``None`` (unconstrained). Call :meth:`save` to persist."""
        self._values = None

    # ------------------------------------------------------------------
    # Runtime: evaluation
    # ------------------------------------------------------------------

    def get(self, context: list | None = None) -> Any:
        """Evaluate this flag and return its current value."""
        return self._client._evaluate_handle(self.id, self.default, context)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _apply(self, other: Flag) -> None:
        """Copy properties from *other* into this instance."""
        self.id = other.id
        self.name = other.name
        self.type = other.type
        self.default = other.default
        self._values = other._values
        self.description = other.description
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"Flag(id={self.id!r}, type={self.type!r}, default={self.default!r})"


class BooleanFlag(Flag):
    """A boolean flag — .get() returns bool."""

    def get(self, context: list | None = None) -> bool:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, bool):
            return value
        return self.default


class StringFlag(Flag):
    """A string flag — .get() returns str."""

    def get(self, context: list | None = None) -> str:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, str):
            return value
        return self.default


class NumberFlag(Flag):
    """A numeric flag — .get() returns int | float."""

    def get(self, context: list | None = None) -> int | float:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        return self.default


class JsonFlag(Flag):
    """A JSON flag — .get() returns dict."""

    def get(self, context: list | None = None) -> dict[str, Any]:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, dict):
            return value
        return self.default


# ===================================================================
# Async variants
# ===================================================================


class AsyncFlag:
    """A flag resource (async).

    Same interface as :class:`Flag` but :meth:`save` is async.
    """

    id: str | None
    name: str
    type: str
    default: Any
    description: str | None
    created_at: Any
    updated_at: Any

    def __init__(
        self,
        client: AsyncFlagsClient | AsyncMgmtFlagsClient | None = None,
        *,
        id: str | None = None,
        name: str,
        type: str,
        default: Any,
        values: list[FlagValue] | None = None,
        description: str | None = None,
        environments: dict[str, FlagEnvironment] | None = None,
        created_at: Any = None,
        updated_at: Any = None,
    ) -> None:
        self._client = client
        self.id = id
        self.name = name
        self.type = type
        self.default = default
        self._values: list[FlagValue] | None = list(values) if values is not None else None
        self.description = description
        self._environments: dict[str, FlagEnvironment] = dict(environments) if environments is not None else {}
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def values(self) -> list[FlagValue] | None:
        """Read-only view of constrained values."""
        return list(self._values) if self._values is not None else None

    @property
    def environments(self) -> dict[str, FlagEnvironment]:
        """Read-only view of per-environment configuration."""
        return dict(self._environments)

    # ------------------------------------------------------------------
    # Management: save (create or update)
    # ------------------------------------------------------------------

    async def save(self) -> None:
        """Persist this flag to the server (async).

        Creates a new flag if unsaved, or updates the existing one.
        Requires a management client.
        """
        if self._client is None:
            raise RuntimeError("AsyncFlag was constructed without a client; cannot save")
        if self.created_at is None:
            created = await self._client._create_flag(self)
            self._apply(created)
        else:
            updated = await self._client._update_flag(flag=self)
            self._apply(updated)

    async def delete(self) -> None:
        """Delete this flag from the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("AsyncFlag was constructed without a client or id; cannot delete")
        await self._client.delete(self.id)

    # ------------------------------------------------------------------
    # Management: local mutations (sync)
    # ------------------------------------------------------------------

    def add_rule(self, built_rule: dict[str, Any]) -> AsyncFlag:
        env_key = built_rule.get("environment")
        if env_key is None:
            raise ValueError(
                "Built rule must include 'environment' key. Use Rule(..., environment='env_key').when(...).serve(...)"
            )
        flag_rule = FlagRule(
            logic=dict(built_rule.get("logic") or {}),
            value=built_rule.get("value"),
            description=built_rule.get("description"),
        )
        existing = self._environments.get(env_key, FlagEnvironment())
        _replace_env(self._environments, env_key, rules=(*existing.rules, flag_rule))
        return self

    def enable_rules(self, *, environment: str | None = None) -> None:
        """Enable rule evaluation.  Without ``environment``, applies to every
        environment configured on this flag.  Call :meth:`save` to persist.
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, enabled=True)
        else:
            _replace_env(self._environments, environment, enabled=True)

    def disable_rules(self, *, environment: str | None = None) -> None:
        """Disable rule evaluation.  Without ``environment``, applies to every
        environment configured on this flag.  Call :meth:`save` to persist.
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, enabled=False)
        else:
            _replace_env(self._environments, environment, enabled=False)

    def set_default(self, value: Any, *, environment: str | None = None) -> None:
        """Set the flag's default served value (base or per-environment).

        Call :meth:`save` to persist.
        """
        if environment is None:
            self.default = value
        else:
            _replace_env(self._environments, environment, default=value)

    def clear_default(self, *, environment: str) -> None:
        """Clear the per-environment default override on *environment*."""
        if environment in self._environments:
            _replace_env(self._environments, environment, default=None)

    def clear_rules(self, *, environment: str | None = None) -> None:
        """Remove rules.  Without ``environment``, applies to every environment
        configured on this flag.  Call :meth:`save` to persist.
        """
        if environment is None:
            for env_key in list(self._environments.keys()):
                _replace_env(self._environments, env_key, rules=())
        else:
            _replace_env(self._environments, environment, rules=())

    def add_value(self, name: str, value: Any) -> AsyncFlag:
        """Append a constrained value to the flag's values list. Returns *self* for chaining."""
        if self._values is None:
            self._values = []
        self._values.append(FlagValue(name=name, value=value))
        return self

    def remove_value(self, value: Any) -> AsyncFlag:
        """Remove the first values entry whose ``value`` field matches.  Returns *self* for chaining."""
        if self._values is None:
            return self
        self._values = [v for v in self._values if v.value != value]
        return self

    def clear_values(self) -> None:
        """Set values to ``None`` (unconstrained). Call :meth:`save` to persist."""
        self._values = None

    # ------------------------------------------------------------------
    # Runtime: evaluation
    # ------------------------------------------------------------------

    def get(self, context: list | None = None) -> Any:
        return self._client._evaluate_handle(self.id, self.default, context)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _apply(self, other: AsyncFlag) -> None:
        self.id = other.id
        self.name = other.name
        self.type = other.type
        self.default = other.default
        self._values = other._values
        self.description = other.description
        self._environments = other._environments
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    def __repr__(self) -> str:
        return f"AsyncFlag(id={self.id!r}, type={self.type!r}, default={self.default!r})"


class AsyncBooleanFlag(AsyncFlag):
    def get(self, context: list | None = None) -> bool:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, bool):
            return value
        return self.default


class AsyncStringFlag(AsyncFlag):
    def get(self, context: list | None = None) -> str:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, str):
            return value
        return self.default


class AsyncNumberFlag(AsyncFlag):
    def get(self, context: list | None = None) -> int | float:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        return self.default


class AsyncJsonFlag(AsyncFlag):
    def get(self, context: list | None = None) -> dict[str, Any]:
        value = self._client._evaluate_handle(self.id, self.default, context)
        if isinstance(value, dict):
            return value
        return self.default
