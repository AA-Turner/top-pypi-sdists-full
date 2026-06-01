"""Public types for the Flags SDK: Context, FlagDeclaration, Op, Rule."""

from __future__ import annotations

import dataclasses
import datetime
import enum
from typing import Any, overload


class Op(str, enum.Enum):
    """Operators supported by :meth:`Rule.when`.

    Customers should prefer ``Op.EQ`` etc. over raw strings so the IDE
    can validate calls.  Raw strings are still accepted for backward
    compatibility.
    """

    CONTAINS = "contains"
    EQ = "=="
    GT = ">"
    GTE = ">="
    IN = "in"
    LT = "<"
    LTE = "<="
    NEQ = "!="


_CONTEXT_FIELDS = frozenset(
    {
        "type",
        "key",
        "name",
        "attributes",
        "created_at",
        "updated_at",
        "_client",
    }
)


class _ContextBase:
    """Shared state + validation for :class:`Context` / :class:`AsyncContext`."""

    type: str
    key: str
    name: str | None
    attributes: dict[str, Any]
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    def __init__(
        self,
        type: str,
        key: str,
        attributes: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
        **kwargs: Any,
    ) -> None:
        if not isinstance(type, str):
            raise TypeError(f"Context type must be a string, got {type.__class__.__name__}: {type!r}")
        if not isinstance(key, str):
            raise TypeError(
                f"Context key must be a string, got {key.__class__.__name__}: {key!r}. "
                "If your identifier is numeric, stringify it at the SDK boundary."
            )
        self.type = type
        self.key = key
        self.name = name
        self.attributes = {**(attributes or {}), **kwargs}
        self.created_at = created_at
        self.updated_at = updated_at
        self._client = None  # set by SDK parsers when constructed server-side

    def __setattr__(self, name: str, value: Any) -> None:
        # Block dotted assignment of unknown names — silently mis-routes
        # what customers usually mean to put in ``attributes``.
        if name not in _CONTEXT_FIELDS:
            raise AttributeError(
                f"Cannot set unknown attribute {name!r} on Context. "
                f"To add a context attribute use ctx.attributes[{name!r}] = ...; "
                "to bulk-replace, set ctx.attributes = {...}."
            )
        # Identity fields are immutable once the context is persisted;
        # changing them would mean a different entity, not a mutation.
        if name in ("type", "key") and getattr(self, "created_at", None) is not None:
            raise AttributeError(
                f"Cannot reassign {name!r} on a persisted Context "
                "(identity is fixed after save). Delete and create a new Context "
                "if you need a different (type, key)."
            )
        object.__setattr__(self, name, value)

    def _apply(self, other: _ContextBase) -> None:
        # Bypass __setattr__ — the persisted-identity guard would otherwise
        # block the legitimate post-save copy of fields from the server.
        object.__setattr__(self, "type", other.type)
        object.__setattr__(self, "key", other.key)
        self.name = other.name
        self.attributes = dict(other.attributes)
        self.created_at = other.created_at
        self.updated_at = other.updated_at

    @property
    def id(self) -> str:
        """Composite ``"{type}:{key}"`` identifier."""
        return f"{self.type}:{self.key}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(type={self.type!r}, key={self.key!r}, "
            f"name={self.name!r}, attributes={self.attributes!r})"
        )


class Context(_ContextBase):
    """A typed entity referenced by targeting rules and registered with smplkit.

    Represents a single entity (user, account, device, etc.).  The *type*
    and *key* identify the entity; *attributes* (provided as a dict and/or
    keyword arguments) carry the data that targeting rules evaluate against.

    Used for both authoring (``flag.get(context=[...])``,
    ``client.set_context([...])``, ``mgmt.contexts.register([...])``)
    and reading (``mgmt.contexts.list/get`` return populated ``Context``
    instances with ``save()`` / ``delete()`` ready to call).

    Examples::

        Context("user", "user-123", plan="enterprise")
        Context("account", "acme-corp", {"region": "us"}, employee_count=500)
    """

    def save(self) -> None:
        """Persist this context to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("Context was constructed without a client; cannot save")
        updated = self._client._save_context(self)
        self._apply(updated)

    def delete(self) -> None:
        """Delete this context from the server."""
        if self._client is None:
            raise RuntimeError("Context was constructed without a client; cannot delete")
        self._client.delete(self.id)


class AsyncContext(_ContextBase):
    """Async variant of :class:`Context`.

    Returned by ``await mgmt.contexts.list/get`` on the async client.
    For authoring use cases (``flag.get(context=[...])``,
    ``client.set_context([...])``, etc.), construct a regular
    :class:`Context` — input usage doesn't require the async variant.
    """

    async def save(self) -> None:
        """Persist this context to the server (create or update)."""
        if self._client is None:
            raise RuntimeError("AsyncContext was constructed without a client; cannot save")
        updated = await self._client._save_context(self)
        self._apply(updated)

    async def delete(self) -> None:
        """Delete this context from the server."""
        if self._client is None:
            raise RuntimeError("AsyncContext was constructed without a client; cannot delete")
        await self._client.delete(self.id)


@dataclasses.dataclass
class FlagDeclaration:
    """Describes a flag declaration for buffered registration.

    Used by :meth:`smplkit.SmplManagementClient.flags.register` to queue
    declarations for bulk registration.  ``service`` and ``environment``
    default to ``None``; the runtime client fills them from the active
    ``SmplClient`` when it forwards declarations.
    """

    id: str
    type: str
    default: Any
    service: str | None = None
    environment: str | None = None


class Rule:
    """Fluent builder for flag targeting rules.

    Usage::

        Rule("Enable for enterprise users", environment="staging")
            .when("user.plan", Op.EQ, "enterprise")
            .serve(True)

    Multiple ``.when()`` calls are AND'd.  ``environment`` is required so the
    target environment is unambiguous when the rule is passed to
    :meth:`Flag.add_rule`.  ``.serve()`` finalizes the rule and returns the
    built dict ready to pass to ``add_rule``.
    """

    def __init__(self, description: str, *, environment: str) -> None:
        self._description = description
        self._conditions: list[dict[str, Any]] = []
        self._environment = environment

    @overload
    def when(self, expr: dict[str, Any], /) -> Rule: ...
    @overload
    def when(self, var: str, op: Op | str, value: Any, /) -> Rule: ...

    def when(self, *args: Any) -> Rule:
        """Add a condition.  Multiple calls are AND'd at the top level.

        Two forms:

        - ``when(var, op, value)`` — convenience for simple comparisons.
          ``op`` accepts an :class:`Op` enum value (preferred) or a raw
          string (e.g. ``"=="``, ``"contains"``).

        - ``when(expr)`` — escape hatch accepting an arbitrary JSON Logic
          expression (use this for OR, nested AND/OR, ``if``, etc.).
          See https://jsonlogic.com/ for the full expression grammar.
        """
        if len(args) == 1 and isinstance(args[0], dict):
            self._conditions.append(args[0])
            return self
        if len(args) == 3:
            var, op, value = args
            op_str = op.value if isinstance(op, Op) else op
            if op_str == "contains":
                # JSON Logic "in" with reversed operands: value in var
                self._conditions.append({"in": [value, {"var": var}]})
            else:
                self._conditions.append({op_str: [{"var": var}, value]})
            return self
        raise TypeError(f"Rule.when() takes either (var, op, value) or a single JSON Logic dict; got args={args!r}")

    def serve(self, value: Any) -> dict[str, Any]:
        """Finalize the rule with *value* served on match and return the built dict."""
        if len(self._conditions) == 1:
            logic = self._conditions[0]
        elif len(self._conditions) > 1:
            logic = {"and": self._conditions}
        else:
            logic = {}

        return {
            "description": self._description,
            "logic": logic,
            "value": value,
            "environment": self._environment,
        }
