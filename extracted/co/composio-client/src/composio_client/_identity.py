"""The product calling through this client, and the headers it owns.

The same contract as the TypeScript ``ClientIdentity``: the library headers are
always the package's own, and once a client has an ``identity`` the product
headers are its too, so ``default_headers`` and a call's
``request_options.headers`` can no longer carry any of them.
"""

from __future__ import annotations

import platform
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, fields

from ._exceptions import ComposioError
from ._version import __version__

#: The library sending the request. Never caller-settable, with or without an identity.
_LIBRARY_HEADERS = ("x-client-library", "x-client-library-version", "x-client-language")

#: The calling product and its runtime. Reserved once a client has an
#: ``identity``; without one they default to the package and stay
#: caller-settable, which is how a wrapper identified itself before ``identity``.
_PRODUCT_HEADERS = (
    "x-client-provenance",
    "x-client-version",
    "x-sdk-version",
    "x-source",
    "x-framework",
    "x-runtime",
    "x-client-runtime",
    "x-runtime-version",
)

_LIBRARY_RESERVED = frozenset(_LIBRARY_HEADERS)
_IDENTITY_RESERVED = frozenset(_LIBRARY_HEADERS + _PRODUCT_HEADERS)

CREDENTIAL_HEADERS = ("x-api-key", "x-user-api-key", "x-org-api-key")

SCOPE_HEADERS = ("x-org-id", "x-project-id")

#: Printable ASCII with no leading or trailing whitespace.
_HEADER_SAFE = re.compile(r"[\x21-\x7e](?:[\x20-\x7e]*[\x21-\x7e])?")

_RUNTIME = "python"


@dataclass(frozen=True)
class ClientIdentity:
    """The calling product, such as ``composio`` (the Python SDK).

    ``product`` and ``version`` are sent as ``x-client-provenance`` and
    ``x-client-version`` (``version`` also as ``x-sdk-version``); ``source``,
    ``framework`` and ``runtime`` are the legacy labels the platform still
    reads, sent as ``x-source``, ``x-framework`` and ``x-runtime``.
    """

    product: str
    version: str
    source: str | None = None
    framework: str | None = None
    runtime: str | None = None

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None and field.name not in ("product", "version"):
                continue
            if not isinstance(value, str) or _HEADER_SAFE.fullmatch(value) is None:
                raise ValueError(
                    f"`identity.{field.name}` must be a non-empty string of printable ASCII "
                    "with no leading or trailing whitespace."
                )


@dataclass(frozen=True)
class ResolvedIdentity:
    """The identity headers a client sends, and the names a caller may therefore not set."""

    headers: Mapping[str, str]
    reserved: frozenset[str]


def resolve_identity(identity: ClientIdentity | None) -> ResolvedIdentity:
    """The headers ``identity`` owns, resolved once per client.

    The detected runtime stays in ``x-client-runtime`` and ``x-runtime-version``
    either way: ``identity.runtime`` is the legacy ``x-runtime`` label, and the
    platform does not read the two as aliases.
    """
    if identity is not None and not isinstance(identity, ClientIdentity):
        raise TypeError("`identity` must be a `ClientIdentity`.")
    library = {
        "x-client-library": "composio-client",
        "x-client-library-version": __version__,
        "x-client-language": "python",
        "x-client-runtime": _RUNTIME,
    }
    if identity is None:
        return ResolvedIdentity(
            headers={
                "x-client-provenance": "composio-client",
                "x-client-version": __version__,
                **library,
                "x-runtime": _RUNTIME,
                "x-runtime-version": platform.python_version(),
            },
            reserved=_LIBRARY_RESERVED,
        )
    headers = {
        "x-client-provenance": identity.product,
        "x-client-version": identity.version,
        **library,
        "x-runtime": identity.runtime if identity.runtime is not None else _RUNTIME,
        "x-runtime-version": platform.python_version(),
        "x-sdk-version": identity.version,
    }
    if identity.source is not None:
        headers["x-source"] = identity.source
    if identity.framework is not None:
        headers["x-framework"] = identity.framework
    return ResolvedIdentity(headers=headers, reserved=_IDENTITY_RESERVED)


def reserved_headers(identity: ResolvedIdentity, *, credentialed: bool, scoped: bool) -> Mapping[str, str]:
    """Credential names are reserved while ``auth`` is not ``NoAuth``, routing ids while ``scope`` is set."""
    owners = {name: "client" if name in _LIBRARY_RESERVED else "identity" for name in identity.reserved}
    if credentialed:
        owners.update(dict.fromkeys(CREDENTIAL_HEADERS, "auth"))
    if scoped:
        owners.update(dict.fromkeys(SCOPE_HEADERS, "scope"))
    return owners


_SETTER = {"client": "the client", "identity": "`identity`", "auth": "`auth`", "scope": "`scope`"}

_REMEDY = {
    "client": " Pass `identity` to describe the calling product.",
    "identity": "",
    "auth": (
        " Configure the credential through `auth`;"
        " derive a client with `with_options(auth=...)` for another one."
    ),
    "scope": (
        " Configure the organization and project through `scope`;"
        " derive a client with `with_options(scope=...)` for another one."
    ),
}


def assert_no_reserved_headers(names: Iterable[str], reserved: Mapping[str, str], option: str) -> None:
    """Refuse a generic header source that names a reserved header, to set or to delete it."""
    for name in names:
        lowered = name.lower()
        owner = reserved.get(lowered)
        if owner is not None:
            message = f"The `{lowered}` header is set by {_SETTER[owner]} and cannot be passed in `{option}`."
            raise ComposioError(message + _REMEDY[owner])
