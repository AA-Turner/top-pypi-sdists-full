"""Stored secrets in steps — a workflow NAMES a secret, never holds its value.

A step input may carry ``{"$secret": "<name>"}`` wherever a text value goes (an
http header, a query parameter, a body field), optionally with a ``format`` that
wraps the value: ``{"$secret": "GITHUB_PAT", "format": "Bearer {}"}`` sends
``Bearer <value>`` (``{}`` marks where the value goes; nothing else in the format
is interpreted). The step resolves it at the last
moment, uses the value for the outgoing call only, and every value it hands
back (output, failure message, details) passes through ``redact`` first, so the
secret never reaches an output, event, checkpoint, log or error.

Resolution is host-owned: the vault lives in the host (aidream wires the
matrx-orm secrets battery), which this package must never import. The host
injects its resolver once via ``configure_secret_resolver(...)``. Unconfigured
(standalone), any ``$secret`` reference is a plain failure naming the secret —
never a silent pass-through of the reference as a literal value.

The resolver decides scope (the run's organization, plus — when the step knows it —
the ``workflow_id`` being run, so a host can let a platform-owned workflow use its
owner's secrets; the host decides what else)
and raises ``SecretUnavailable`` with a sentence that names the secret, never its
value.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

SECRET_KEY = "$secret"
FORMAT_KEY = "format"
FORMAT_SLOT = "{}"
REDACTED = "[secret]"

# (name, *, user_id, organization_id[, workflow_id]) -> value. Raises SecretUnavailable.
# ``workflow_id`` is passed only when the step knows the workflow it runs in.
SecretResolver = Callable[..., Awaitable[str]]

_resolver: SecretResolver | None = None

# Values in use by the step running in THIS task — the http client's own log lines
# (httpx logs every request URL at INFO, query string included) are redacted with them.
_ACTIVE: ContextVar[tuple[str, ...]] = ContextVar("matrx_graph_active_secret_values", default=())


class _RedactActiveSecrets(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        values = _ACTIVE.get()
        if values:
            message = record.getMessage()
            redacted = _redact(message, list(values))
            if redacted != message:
                record.msg, record.args = redacted, None
        return True


_LOG_FILTER = _RedactActiveSecrets()
for _name in ("httpx", "httpcore"):
    logging.getLogger(_name).addFilter(_LOG_FILTER)


class SecretUnavailable(LookupError):
    """A named secret could not be used — missing, empty, or not shared with this run."""


class SecretRef(BaseModel):
    """``{"$secret": "<name>"}`` — a pointer to a stored secret, safe to store and show."""

    model_config = ConfigDict(extra="forbid", populate_by_name=False, serialize_by_alias=True)

    name: str = Field(
        alias=SECRET_KEY,
        min_length=1,
        description="The name of a stored secret (for example GITHUB_TOKEN).",
    )
    format: str | None = Field(
        default=None,
        pattern=r"^[^{}]*\{\}[^{}]*$",
        description='Wraps the value: "Bearer {}" sends "Bearer <value>". {} marks where the value goes.',
    )


def configure_secret_resolver(resolver: SecretResolver | None) -> None:
    """Register (or clear, with None) the host's secret resolver."""
    global _resolver
    _resolver = resolver


def is_secret_resolver_configured() -> bool:
    return _resolver is not None


def _valid_format(fmt: Any) -> bool:
    return isinstance(fmt, str) and fmt.count(FORMAT_SLOT) == 1 and fmt.replace(FORMAT_SLOT, "").count("{") == 0 \
        and fmt.replace(FORMAT_SLOT, "").count("}") == 0


def is_secret_ref(value: Any) -> bool:
    if isinstance(value, SecretRef):
        return True
    if not (isinstance(value, dict) and isinstance(value.get(SECRET_KEY), str) and bool(value[SECRET_KEY])):
        return False
    extra = set(value) - {SECRET_KEY}
    return not extra or (extra == {FORMAT_KEY} and (value[FORMAT_KEY] is None or _valid_format(value[FORMAT_KEY])))


def _ref_name(value: Any) -> str:
    return value.name if isinstance(value, SecretRef) else str(value[SECRET_KEY])


def _ref_format(value: Any) -> str | None:
    return value.format if isinstance(value, SecretRef) else value.get(FORMAT_KEY)


def apply_format(value: str, fmt: str | None) -> str:
    """``fmt`` with its one ``{}`` replaced by ``value`` (a plain replace: nothing else is interpreted)."""
    return fmt.replace(FORMAT_SLOT, value, 1) if fmt else value


def contains_secret_ref(data: Any) -> bool:
    if is_secret_ref(data):
        return True
    if isinstance(data, BaseModel):
        return any(contains_secret_ref(getattr(data, k)) for k in type(data).model_fields)
    if isinstance(data, dict):
        return any(contains_secret_ref(v) for v in data.values())
    if isinstance(data, list | tuple):
        return any(contains_secret_ref(v) for v in data)
    return False


class SecretValues:
    """The values resolved for ONE step invocation — used to redact what it returns."""

    def __init__(self) -> None:
        self._values: dict[str, str] = {}

    def add(self, name: str, value: str) -> None:
        self._values[name] = value

    def __bool__(self) -> bool:
        return bool(self._values)

    @property
    def names(self) -> list[str]:
        return sorted(self._values)

    @contextmanager
    def active(self) -> Iterator[None]:
        """While the request is sent, the http client's log lines are redacted too."""
        if not self._values:
            yield
            return
        token = _ACTIVE.set(tuple(sorted({v for v in self._values.values() if v}, key=len, reverse=True)))
        try:
            yield
        finally:
            _ACTIVE.reset(token)

    def redact(self, data: Any) -> Any:
        """A copy of ``data`` with every resolved value replaced by ``[secret]``.

        Walks strings, dicts (keys and values), lists, tuples and pydantic models.
        Longest values first, so a value that contains another is removed whole."""
        if not self._values:
            return data
        values = sorted({v for v in self._values.values() if v}, key=len, reverse=True)
        return _redact(data, values)


def _redact(data: Any, values: list[str]) -> Any:
    if isinstance(data, str):
        for value in values:
            if value in data:
                data = data.replace(value, REDACTED)
        return data
    if isinstance(data, BaseModel):
        dumped = data.model_dump(mode="python", by_alias=True)
        return type(data).model_validate(_redact(dumped, values))
    if isinstance(data, dict):
        return {_redact(k, values): _redact(v, values) for k, v in data.items()}
    if isinstance(data, list):
        return [_redact(v, values) for v in data]
    if isinstance(data, tuple):
        return tuple(_redact(v, values) for v in data)
    return data


async def resolve_secret_refs(
    data: Any,
    *,
    user_id: str | None,
    organization_id: str | None,
    found: SecretValues,
    workflow_id: str | None = None,
) -> Any:
    """A copy of ``data`` with every ``{"$secret": name}`` replaced by its value
    (wrapped by its ``format``, when it has one).

    Every value resolved is recorded in ``found`` (for ``found.redact``; the raw
    value, so a formatted one is redacted too). Raises ``SecretUnavailable``
    naming the secret when one cannot be used."""
    if not contains_secret_ref(data):
        return data
    cache: dict[str, str] = {}

    async def walk(node: Any) -> Any:
        if is_secret_ref(node):
            name = _ref_name(node)
            if name not in cache:
                cache[name] = await _resolve_one(
                    name, user_id=user_id, organization_id=organization_id, workflow_id=workflow_id
                )
                found.add(name, cache[name])
            return apply_format(cache[name], _ref_format(node))
        if isinstance(node, BaseModel):
            return {k: await walk(getattr(node, k)) for k in type(node).model_fields}
        if isinstance(node, dict):
            return {k: await walk(v) for k, v in node.items()}
        if isinstance(node, list | tuple):
            return [await walk(v) for v in node]
        return node

    return await walk(data)


async def _resolve_one(
    name: str, *, user_id: str | None, organization_id: str | None, workflow_id: str | None = None
) -> str:
    if _resolver is None:
        raise SecretUnavailable(
            f"The secret {name!r} can't be used: this server has no secret store connected."
        )
    try:
        extra = {"workflow_id": workflow_id} if workflow_id else {}
        value = await _resolver(name, user_id=user_id, organization_id=organization_id, **extra)
    except SecretUnavailable:
        raise
    except Exception as exc:  # noqa: BLE001 — the store's own message may carry anything; name only the type
        raise SecretUnavailable(
            f"The secret {name!r} could not be read ({type(exc).__name__})."
        ) from None
    if not isinstance(value, str) or not value:
        raise SecretUnavailable(f"The secret {name!r} is empty.")
    return value


__all__ = [
    "FORMAT_KEY",
    "REDACTED",
    "SECRET_KEY",
    "apply_format",
    "SecretRef",
    "SecretResolver",
    "SecretUnavailable",
    "SecretValues",
    "configure_secret_resolver",
    "contains_secret_ref",
    "is_secret_ref",
    "is_secret_resolver_configured",
    "resolve_secret_refs",
]
