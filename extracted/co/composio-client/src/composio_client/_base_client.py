"""The hand-written dispatch kernel — sync and async.

A port of the TypeScript golden reference (``src/compat/request.ts``) onto
httpx: per-attempt timeouts, the same retry policy
(408/409/429/5xx + ``x-should-retry``, connection errors and timeouts retried),
``retry-after`` honored as ms / seconds / HTTP-date, exponential backoff with
downward jitter, and the Stainless header-merge precedence. The generated
pydantic models are codegen-only; nothing from hey-api's runtime ships here.

The credential transport boundary is part of that port too and lives in
:mod:`._credentials`: HTTPS (or loopback) for a credentialed origin, and the API
key attached only on that origin. Redirects are followed by this kernel rather
than by httpx, so that every hop re-derives its own headers and an
origin-changing one carries no credential.

``BaseClient`` holds the pure request-building and response-processing logic;
``SyncAPIClient`` / ``AsyncAPIClient`` add the httpx client and the retry loop,
duplicated across sync/async exactly as Stainless does (there is no clean way to
share a loop that ``await``s in one arm and not the other).
"""

from __future__ import annotations

import email.utils
import inspect
import logging
import random
import time
from collections.abc import AsyncIterator, Callable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from types import UnionType
from typing import Annotated, Any, ClassVar, Literal, TypeVar, Union, cast, get_args, get_origin, overload
from urllib.parse import urljoin, urlsplit

import httpx
from pydantic import BaseModel, RootModel, TypeAdapter, ValidationError

from ._aliasing import rename_to_wire_names
from ._auth import (
    AUTH_TYPES,
    Auth,
    AuthMode,
    AutoAuth,
    NoAuth,
    Scope,
    is_sendable_key,
)
from ._credentials import (
    CREDENTIAL_SCHEME_HEADERS,
    Credentials,
    assert_credential_transport,
    credential_destination,
    credential_for_request,
    has_alternate_credential,
    same_origin,
    select_scheme,
    withdraw_credentials,
)
from ._deprecation import (
    ComposioDeprecationWarning,
    inspect_deprecated_inputs,
    inspect_deprecation,
    match_operation,
)
from ._exceptions import (
    APIConnectionError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    ComposioError,
    status_error,
)
from ._identity import (
    CREDENTIAL_HEADERS,
    SCOPE_HEADERS,
    ClientIdentity,
    assert_no_reserved_headers,
    reserved_headers,
    resolve_identity,
)
from ._operations import OPERATIONS, Operation
from ._response import APIResponse, AsyncAPIResponse
from ._streaming import SSEBytesDecoder, SSEDecoder
from ._types import DEFAULT_MAX_RETRIES as DEFAULT_MAX_RETRIES
from ._types import AsyncBinaryTypes, BinaryTypes, RequestFiles
from ._types import RequestOptions as RequestOptions

ResponseT = TypeVar("ResponseT")

_RETRYABLE_STATUSES = frozenset({408, 409, 429})
_IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})
_DEFAULT_REQUEST_OPTIONS = RequestOptions()
_logger = logging.getLogger("composio_client")
_NON_REPLAYABLE_REDIRECT = "An async iterator request body cannot be replayed across a redirect."

#: A request body or query may be passed as a generated pydantic model or as a
#: plain mapping (the relaxed contract).
BodyParam = BaseModel | Mapping[str, object]
QueryParam = BaseModel | Mapping[str, object]

#: The header parameters an operation declares, placed by the caller.
#:
#: A mapping rather than an argument each, because a header name is not a Python
#: identifier (``x-user-api-key``). A ``None`` value deletes a client default of
#: that name, which is what :func:`_merge_headers` means by ``None`` everywhere
#: else.
HeaderParam = Mapping[str, str | None]

#: The generated request model an endpoint's body is shaped by. Resource methods
#: pass theirs to ``_request`` so a plain-mapping body gets the same alias
#: treatment as a model-typed one.
BodyModel = type[BaseModel]

# The element type httpx accepts for `params` as a list of pairs.
_QueryPairs = list[tuple[str, str | int | float | bool | None]]


def _safe_log(level: int, message: str, *args: object) -> None:
    """Emit an advisory lifecycle record without changing request behavior."""
    try:
        _logger.log(level, message, *args)
    except Exception:
        pass


def _as_mapping(value: BodyParam | None, model: BodyModel | None = None) -> dict[str, Any] | None:
    """Serialize a request payload into the JSON object that goes on the wire.

    TS parity (``JSON.stringify``): fields never set are omitted (like
    ``undefined``), fields explicitly set to ``None`` are kept as JSON null.

    A plain mapping is routed through ``model`` — the generated request model
    for that endpoint — so the spec's wire aliases reach a dict body exactly as
    they already do a model-typed one (``auth_scheme`` -> ``authScheme``,
    ``your_domain`` -> ``your-domain``, ...). That routing is a **key rename and
    nothing else** (:mod:`._aliasing`): both the pythonic and the wire spelling
    are accepted on input, unknown keys — top-level or nested — are forwarded
    verbatim, and every *value* the caller wrote reaches the wire byte for byte.

    This client performs no request validation, matching the Stainless oracle it
    is pinned against, whose ``maybe_transform`` likewise walks annotations to
    remap aliases and nothing more. The rename cannot fail on a caller's body,
    so there is no error path to be lenient about; the server stays the authority
    on what a valid body is. See :mod:`._aliasing` for why validate-and-dump was
    not good enough — it coerced ``3600`` into ``3600.0``, ``"20000"`` into
    ``20000.0`` and ``https://example.com`` into ``https://example.com/``.

    ``model=None`` (the query path, and any endpoint without a body model) sends
    the mapping as-is.
    """
    if value is None:
        return None
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", by_alias=True, exclude_unset=True)
    mapping = dict(value)
    if model is None:
        return mapping
    return rename_to_wire_names(model, mapping)


def _scalar(item: Any) -> str:
    """One array element, with JS ``Array.prototype.join`` semantics:
    ``None`` renders as the empty string, booleans lowercase."""
    if item is None:
        return ""
    if isinstance(item, bool):
        return "true" if item else "false"
    return str(item)


def _encode_query(query: Mapping[str, Any]) -> _QueryPairs:
    """Stainless-flavored query serialization: arrays comma-joined, ``None``
    dropped, nested mappings expanded qs-style into ``key[sub]`` — mirrors
    ``stringifyQuery`` in the TS kernel."""
    parts: _QueryPairs = []

    def append(key: str, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, Mapping):
            for sub_key, sub_value in value.items():
                append(f"{key}[{sub_key}]", sub_value)
        elif isinstance(value, (list, tuple)):
            parts.append((key, ",".join(_scalar(item) for item in value)))
        elif isinstance(value, bool):
            parts.append((key, "true" if value else "false"))
        else:
            parts.append((key, str(value)))

    for key, value in query.items():
        append(key, value)
    return parts


def _merge_headers(
    sources: list[Mapping[str, str | None] | None],
) -> dict[str, str]:
    """Merge header sources in precedence order (later wins); ``None`` deletes,
    missing leaves untouched. Header names are matched case-insensitively."""
    headers: dict[str, str] = {}
    lowered: dict[str, str] = {}  # lowercase name -> stored name
    for source in sources:
        if not source:
            continue
        for name, value in source.items():
            key = name.lower()
            existing = lowered.get(key)
            if value is None:
                if existing is not None:
                    headers.pop(existing, None)
                    lowered.pop(key, None)
                continue
            if existing is not None:
                headers[existing] = value
            else:
                headers[name] = value
                lowered[key] = name
    return headers


_REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})

#: How many hops one attempt will follow before giving up. Twenty is what the
#: Fetch spec budgets and what every browser and httpx enforce, so a chain this
#: kernel refuses is one the stack would have refused too.
MAX_REDIRECTS = 20

_TOO_MANY_REDIRECTS = f"The API redirected more than {MAX_REDIRECTS} times; the chain was abandoned."


def _redirect_target(location: str, from_url: str) -> str | None:
    """The ``Location`` a hop points at, resolved against the URL it arrived on,
    or ``None`` when there is nothing followable there — unparseable, or a
    scheme this client does not speak. ``None`` hands the 3xx back as the
    response it is, which is what a redirect-following stack does with a
    ``Location`` it cannot use."""
    try:
        target = urljoin(from_url, location)
    except ValueError:
        return None
    scheme = urlsplit(target).scheme.lower()
    return target if scheme in ("http", "https") else None


def _rewrite_for_redirect(status_code: int, method: str) -> bool:
    """The standard method rewrite (Fetch §4.4 "HTTP-redirect fetch", step 13,
    and RFC 9110 §15.4): a 303 turns any non-GET into a GET, and a 301/302 does
    the same to a POST — both dropping the body. 307 and 308 preserve the method
    and the body, which is what they exist for. Following by hand means
    reproducing this, or a caller's POST silently becomes a POST to somewhere it
    was never sent before."""
    return (status_code == 303 and method not in ("GET", "HEAD")) or (
        status_code in (301, 302) and method == "POST"
    )


def _should_retry(response: httpx.Response) -> bool:
    explicit = response.headers.get("x-should-retry")
    if explicit == "true":
        return True
    if explicit == "false":
        return False
    return response.status_code in _RETRYABLE_STATUSES or response.status_code >= 500


def _model_type(type_: Any) -> type[BaseModel] | None:
    try:
        return type_ if issubclass(type_, BaseModel) else None
    except TypeError:
        return None


def _literal_annotation(annotation: Any) -> Any:
    """A field annotation with ``Annotated`` and ``Optional`` peeled off.

    A tag is still a tag when the field may be absent: the class a legacy
    response collapses into declares ``Optional[Literal[...]]`` so a payload
    that predates the tag still validates, and a payload that carries it must
    still select that class.
    """
    if get_origin(annotation) is Annotated:
        return _literal_annotation(get_args(annotation)[0])
    if get_origin(annotation) in (Union, UnionType):
        present = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(present) == 1:
            return _literal_annotation(present[0])
    return annotation


def _discriminated_variant(type_: Any, value: Any) -> Any | None:
    if not isinstance(value, Mapping):
        return None
    for variant in get_args(type_):
        model = _model_type(variant)
        if model is None:
            continue
        for name, field in model.model_fields.items():
            annotation = _literal_annotation(field.annotation)
            key = field.alias or name
            if get_origin(annotation) is Literal and value.get(key) in get_args(annotation):
                return variant
    return None


# Bounded so a caller minting dynamic `cast_to` types through the raw HTTP
# escape hatch cannot grow it without limit. The generated surface resolves to
# roughly 160 distinct annotations, so the cap is never approached in ordinary
# use; past it, adapters are built per call rather than cached.
_ADAPTER_CACHE_MAX = 2048
_ADAPTERS: dict[int, tuple[Any, TypeAdapter[Any]]] = {}


def _adapter(type_: Any) -> TypeAdapter[Any]:
    """A memoized ``TypeAdapter`` for a response annotation.

    Building the adapter is the expensive half of both branches that use one.
    The generated response models declare 5,722 ``Optional[...]`` fields and two
    ``datetime`` ones inside list element types, so without memoization a large
    response rebuilds the same adapter once per field per item.

    Keyed on **identity**, because neither of the obvious keys is sound:

    * The annotation itself compares unions by member *set*, so ``A | B`` and
      ``B | A`` are equal and hash alike -- while pydantic's smart-union
      tiebreak reads them in order and returns different models for a value
      satisfying both, which ``extra="allow"`` makes easy to hit. That key hands
      whichever spelling arrived second the first one's adapter.
    * The annotation's ``repr`` distinguishes those, but two distinct classes
      sharing a module and name have one ``repr`` between them, so that key
      answers for the wrong type.

    Identity has neither failure, and the hot path is identity-stable: a field's
    annotation is one object on its ``FieldInfo``, and ``typing`` interns its
    own generics. The annotation is retained beside the adapter both to keep the
    entry alive -- an id is only unique while its object is -- and to verify the
    match, so a recycled id cannot answer for a later annotation. An equal but
    distinct annotation simply misses and builds its own, which is correct if
    not maximally frugal.
    """
    key = id(type_)
    cached = _ADAPTERS.get(key)
    if cached is not None and cached[0] is type_:
        return cached[1]
    adapter = TypeAdapter(type_)
    if len(_ADAPTERS) < _ADAPTER_CACHE_MAX or key in _ADAPTERS:
        _ADAPTERS[key] = (type_, adapter)
    return adapter


def _construct_response(value: Any, type_: Any) -> Any:
    """Recursively construct response models without enforcing their schema.

    This is the Pydantic v2 equivalent of Stainless's ``construct_type``:
    callers still receive the expected model tree when the API returns a value
    that its declared schema would reject. Strict parsing is handled separately
    by ``TypeAdapter``.
    """
    origin = get_origin(type_)
    args = get_args(type_)

    if origin is Annotated:
        return _construct_response(value, args[0])
    if origin in (Union, UnionType):
        try:
            return _adapter(type_).validate_python(value)
        except ValidationError:
            variant = _discriminated_variant(type_, value)
            candidates = (variant,) if variant is not None else args
            for candidate in candidates:
                if candidate is type(None) and value is not None:
                    continue
                return _construct_response(value, candidate)
            return value
    if origin is list and isinstance(value, list):
        item_type = args[0] if args else Any
        return [_construct_response(item, item_type) for item in value]
    if origin is dict and isinstance(value, Mapping):
        item_type = args[1] if len(args) > 1 else Any
        return {key: _construct_response(item, item_type) for key, item in value.items()}

    model = _model_type(type_)
    if model is not None and issubclass(model, RootModel):
        root_type = model.model_fields["root"].annotation
        return model.model_construct(_construct_response(value, root_type))
    if model is not None and isinstance(value, Mapping):
        fields: dict[str, Any] = {}
        consumed: set[str] = set()
        for name, field in model.model_fields.items():
            key = field.alias if field.alias is not None and field.alias in value else name
            if key in value:
                fields[name] = _construct_response(value[key], field.annotation)
                consumed.add(key)
        fields.update((key, item) for key, item in value.items() if key not in consumed)
        return model.model_construct(_fields_set=set(fields), **fields)
    if type_ in (date, datetime):
        try:
            return _adapter(type_).validate_python(value)
        except ValidationError:
            return value
    if type_ is float and isinstance(value, int):
        converted = float(value)
        return converted if converted == value else value
    return value


def _header_retry_delay_seconds(headers: httpx.Headers | None) -> float | None:
    """The server-requested delay: ``retry-after-ms`` (milliseconds), then
    ``retry-after`` (seconds or HTTP-date); ``None`` when absent/unparseable."""
    if headers is None:
        return None
    retry_after_ms = headers.get("retry-after-ms")
    if retry_after_ms is not None:
        try:
            return float(retry_after_ms) / 1000
        except ValueError:
            pass
    retry_after = headers.get("retry-after")
    if retry_after is not None:
        try:
            return float(retry_after)
        except ValueError:
            try:
                parsed = email.utils.parsedate_to_datetime(retry_after)
            except (ValueError, TypeError):
                parsed = None
            if parsed is not None:
                return parsed.timestamp() - time.time()
    return None


def _retry_delay_seconds(num_retries: int, headers: httpx.Headers | None) -> float:
    """Seconds to wait before retry ``num_retries + 1``: a header-derived delay
    (``retry-after-ms``, then ``retry-after`` as seconds or HTTP-date) is
    honored only when it is finite and ``0 <= delay < 60`` seconds; anything
    else falls back to exponential backoff ``min(0.5 * 2**n, 8)`` with up to
    25% downward jitter."""
    delay = _header_retry_delay_seconds(headers)
    if delay is not None and 0 <= delay < 60:  # NaN/inf fail the comparison too
        return delay
    backoff = min(0.5 * (2.0**num_retries), 8.0)
    return backoff * (1 - random.random() * 0.25)


def _safe_json(response: httpx.Response) -> object:
    try:
        return response.json()
    except ValueError:
        return response.text


@dataclass
class _Prepared:
    method: str
    url: str
    #: Built once the credential is known (after a provider is called).
    headers: dict[str, str]
    params: _QueryPairs
    json_body: dict[str, Any] | None
    form_body: dict[str, Any] | None
    content: BinaryTypes | AsyncBinaryTypes | None
    files: RequestFiles | None
    stream: bool
    replayable_content: bool
    #: Carried rather than baked into ``headers``: ``_headers_for`` runs again on every redirect hop.
    method_headers: HeaderParam | None
    #: The credential-safe label lifecycle logs print: the matched operation's
    #: path template, or ``<custom>`` when nothing matched. Derived from the
    #: same ``match_operation`` call the scheme selector and the deprecated-
    #: input check read, so logging never re-runs the match.
    log_path: str
    operation: Operation | None
    #: ``(header, key)``, resolved once and reused by every attempt and hop.
    credential: tuple[str, str] | None
    #: ``(header, provider)`` still to be called, once.
    provider: tuple[str, Callable[[], Any]] | None
    scope_headers: Mapping[str, str]


_SCHEME_OF_MODE = {"project": "ApiKeyAuth", "user": "UserApiKeyAuth", "organization": "OrgApiKeyAuth"}

_SCOPE_FIELDS = (("organization_id", "x-org-id"), ("project_id", "x-project-id"))

_PROVIDER_FAILED = "The `auth` credential provider failed."


def _usable(header: str, key: object) -> tuple[str, str]:
    if not is_sendable_key(key):
        raise ComposioError(
            f"The `{header}` credential is not a usable key: it must be a string with a non-whitespace "
            "character and no line break, NUL or character outside Latin-1."
        )
    return (header, cast(str, key))


def _is_async_provider(credential: object) -> bool:
    call = getattr(credential, "__call__", None)  # noqa: B004
    return inspect.iscoroutinefunction(credential) or inspect.iscoroutinefunction(call)


def _credentials_by_mode(auth: Auth) -> dict[str, object]:
    if isinstance(auth, NoAuth):
        return {}
    if not isinstance(auth, AutoAuth):
        return {auth.mode: auth.credential}
    given = {"project": auth.project, "user": auth.user, "organization": auth.organization}
    return {mode: value for mode, value in given.items() if value is not None}


def _credential_source(auth: Auth, operation: Operation | None) -> tuple[str, object] | None:
    """``(header, key or provider)``; a fixed mode never consults the operation table."""
    if isinstance(auth, NoAuth):
        return None
    if not isinstance(auth, AutoAuth):
        return (CREDENTIAL_SCHEME_HEADERS[_SCHEME_OF_MODE[auth.mode]], auth.credential)
    credentials = Credentials(auth.project, auth.user, auth.organization)
    scheme = "ApiKeyAuth"
    if has_alternate_credential(credentials):
        scheme = select_scheme(None if operation is None else operation.schemes, credentials)
    value = credentials.value_for(scheme)
    if value is None:
        return None
    return (CREDENTIAL_SCHEME_HEADERS[scheme], value)


def _split_operation_headers(
    operation_headers: Mapping[str, str | None] | None,
) -> tuple[tuple[str, str] | None, dict[str, str], dict[str, str | None]]:
    """The operation credential, the operation scope ids, and the declared headers the client does not own."""
    credential: tuple[str, str] | None = None
    scope: dict[str, str] = {}
    rest: dict[str, str | None] = {}
    for name, value in (operation_headers or {}).items():
        lowered = name.lower()
        if lowered in SCOPE_HEADERS:
            if value is not None:
                scope[lowered] = value
        elif lowered in CREDENTIAL_HEADERS:
            if value is not None:
                credential = _usable(lowered, value)
        else:
            rest[name] = value
    return credential, scope, rest


def _split_source(
    source: tuple[str, object] | None,
) -> tuple[tuple[str, str] | None, tuple[str, Callable[[], Any]] | None]:
    """A key is checked now; a provider is called later, once."""
    if source is None:
        return None, None
    header, value = source
    if isinstance(value, str):
        return _usable(header, value), None
    return None, (header, cast(Callable[[], Any], value))


def _scope_headers(scope: Scope | None, operation_scope: Mapping[str, str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for field_name, header in _SCOPE_FIELDS:
        value = None if scope is None else getattr(scope, field_name)
        if value is not None:
            headers[header] = value
    for header, value in operation_scope.items():
        configured = headers.get(header)
        if configured is not None and configured != value:
            raise ComposioError(
                f"The `{header}` parameter disagrees with the client's `scope`. "
                "Derive a client with `with_options(scope=...)` to address another one."
            )
        headers[header] = value
    return headers


class BaseClient:
    _accepts_async_credentials: ClassVar[bool] = False

    def __init__(
        self,
        *,
        base_url: str,
        auth: Auth,
        scope: Scope | None = None,
        max_retries: int,
        timeout: float | httpx.Timeout | None,
        user_agent: str,
        default_headers: Mapping[str, str | None] | None = None,
        identity: ClientIdentity | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        if not isinstance(auth, AUTH_TYPES):
            raise TypeError(
                "`auth` must be `NoAuth()`, `ProjectAuth(key)`, `UserAuth(key)`, "
                "`OrganizationAuth(key)` or `AutoAuth(...)`."
            )
        if scope is not None and not isinstance(scope, Scope):
            raise TypeError("`scope` must be a `Scope` or `None`.")
        providers = _credentials_by_mode(auth).values()
        if not self._accepts_async_credentials and any(map(_is_async_provider, providers)):
            raise TypeError(
                "An async credential provider needs `AsyncComposio`; `Composio` calls providers directly."
            )
        self._auth = auth
        self._scope = scope
        self._identity = identity
        self._identity_headers = resolve_identity(identity)
        self._reserved = reserved_headers(
            self._identity_headers,
            credentialed=not isinstance(auth, NoAuth),
            scoped=scope is not None,
        )
        assert_no_reserved_headers(default_headers or (), self._reserved, "default_headers")
        self._base_url = base_url.rstrip("/")
        assert_credential_transport(self._base_url, not isinstance(auth, NoAuth))
        self._configured_max_retries = max_retries
        self._configured_timeout = timeout
        self.user_agent = user_agent
        self._default_headers = default_headers
        self._strict_response_validation = _strict_response_validation
        # The (operation, notice) pairs this instance has already warned about,
        # so a deprecated endpoint called in a loop announces itself once --
        # while a *revised* notice from that same endpoint, say once a `Sunset`
        # date is committed, still gets through. Per instance, not per process,
        # and independent of the `warnings` filters in force.
        self._deprecation_seen: set[str] = set()

    @property
    def default_headers(self) -> dict[str, str]:
        """The caller-provided client defaults, with deleted values omitted."""
        return _merge_headers([self._default_headers])

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def max_retries(self) -> int:
        return self._configured_max_retries

    @property
    def timeout(self) -> float | httpx.Timeout | None:
        return self._configured_timeout

    @property
    def auth_mode(self) -> AuthMode:
        return self._auth.mode

    @property
    def scope(self) -> Scope | None:
        return self._scope

    def _note_deprecation(
        self,
        response: httpx.Response,
        method: str,
        path: str,
        operation: Operation | None,
    ) -> None:
        """The single response exit's deprecation check, run after the retry
        decision has settled and before the body is parsed or an error raised.

        Advisory by construction: a bug here must not fail a call that the
        server answered.

        The one way a notice can reach the caller as an exception is the one the
        caller configured: under ``-W error`` / ``filterwarnings = ["error"]``,
        :func:`warnings.warn` raises. That intent is honored, but only for a
        response that *succeeded*. On an error response the warning is swallowed
        so ``_process`` still raises the real ``NotFoundError`` /
        ``RateLimitError`` / etc. -- an advisory notice must never displace the
        error that actually explains the failure.
        """
        try:
            inspect_deprecation(
                response,
                method=method,
                path=path,
                base_url=self.base_url,
                seen=self._deprecation_seen,
                operation=operation,
                # Frames above `warnings.warn`, which is called inside
                # `inspect_deprecation`:
                #   1 inspect_deprecation -> 2 _note_deprecation
                #   -> 3 _request_response -> 4 _request / _request_raw
                #   -> 5 resource or raw verb -> 6 the caller's own line
                stacklevel=6,
            )
        except ComposioDeprecationWarning:
            if response.is_success:
                raise
        except Exception:  # noqa: BLE001 - an observer never fails the call it observed
            pass

    def _note_deprecated_inputs(
        self,
        operation: Operation | None,
        query: Mapping[str, Any],
        body: Mapping[str, Any] | None,
        headers: Mapping[str, str],
    ) -> None:
        """The static parameter-level check, run inside ``_prepare`` before
        dispatch -- unlike ``_note_deprecation``, no response is involved.

        Under ``-W error`` the warning is allowed to raise: there is no real
        API error here for it to displace, since the request has not even
        gone out yet.
        """
        try:
            inspect_deprecated_inputs(
                operation=operation,
                query=query,
                body=body,
                headers=headers,
                seen=self._deprecation_seen,
                # Frames above `warnings.warn`, which is called inside
                # `inspect_deprecated_inputs`:
                #   1 inspect_deprecated_inputs -> 2 _note_deprecated_inputs
                #   -> 3 _prepare -> 4 _request_response
                #   -> 5 _request / _request_raw -> 6 resource or raw verb
                #   -> 7 the caller's own line
                stacklevel=7,
            )
        except ComposioDeprecationWarning:
            raise
        except Exception:  # noqa: BLE001 - an observer never fails the call it observed
            pass

    def _prepare(
        self,
        method: str,
        path: str,
        *,
        body: BodyParam | None,
        body_model: BodyModel | None,
        query: QueryParam | None,
        headers: HeaderParam | None,
        options: RequestOptions | None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: BinaryTypes | AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> _Prepared:
        options = options or RequestOptions()
        mapped_body = _as_mapping(body, body_model)
        extra_json = options.get("extra_json")
        if extra_json:
            mapped_body = {**(mapped_body or {}), **extra_json}
        form_body = mapped_body if files is not None else None
        json_body = mapped_body if files is None and content is None else None

        merged_query: dict[str, Any] = {}
        # No query model on this surface declares a field alias, so the query
        # path needs no model routing; a mapping is already the wire shape.
        query_map = _as_mapping(query)
        if query_map:
            merged_query.update(query_map)
        option_query = options.get("params") or options.get("query")
        if option_query:
            merged_query.update(option_query)

        url = f"{self.base_url}{path}"
        # Matched once per logical call, not per attempt or per hop, and
        # shared by both consumers below: a retry re-issues the same caller's
        # request, so it authenticates the same way and reports the same
        # deprecated inputs.
        resolved_operation = operation if operation is not None else match_operation(method, path, OPERATIONS)
        operation_credential, operation_scope, declared_rest = _split_operation_headers(operation_headers)
        method_headers: HeaderParam | None = headers
        if declared_rest:
            method_headers = {**dict(headers or {}), **declared_rest}
        option_headers = options.get("headers")
        assert_no_reserved_headers(method_headers or (), self._reserved, "headers")
        assert_no_reserved_headers(option_headers or (), self._reserved, "headers")
        scope_headers = _scope_headers(self._scope, operation_scope)
        # Caller-set headers only -- client defaults, the method's declared
        # headers, then the per-call override -- never the kernel's own
        # accept/user-agent/credential headers, which a caller never set.
        caller_headers = _merge_headers([self._default_headers, headers, operation_headers, option_headers])
        self._note_deprecated_inputs(resolved_operation, merged_query, mapped_body, caller_headers)

        # An operation credential replaces `auth`; off the API origin there is nothing to resolve.
        source = operation_credential or _credential_source(self._auth, resolved_operation)
        if source is not None and not credential_destination(self.base_url, url):
            source = None
        credential, provider = _split_source(source)

        prepared = _Prepared(
            method=method.upper(),
            url=url,
            headers={},
            params=_encode_query(merged_query),
            json_body=json_body,
            form_body=form_body,
            content=content,
            files=files,
            stream=stream,
            replayable_content=not isinstance(content, AsyncIterator),
            method_headers=method_headers,
            log_path="<custom>" if resolved_operation is None else resolved_operation.path,
            operation=resolved_operation,
            credential=credential,
            provider=provider,
            scope_headers=scope_headers,
        )
        if provider is None:
            prepared.headers = self._first_headers(prepared, options)
        return prepared

    def _first_headers(self, prepared: _Prepared, options: RequestOptions) -> dict[str, str]:
        return self._headers_for(
            prepared.url,
            json_body=prepared.json_body,
            method_headers=prepared.method_headers,
            options=options,
            withdrawn=False,
            credential=prepared.credential,
            scope_headers=prepared.scope_headers,
        )

    def _accept_provided(self, prepared: _Prepared, value: object, options: RequestOptions | None) -> None:
        assert prepared.provider is not None
        prepared.credential = _usable(prepared.provider[0], value)
        prepared.provider = None
        prepared.headers = self._first_headers(prepared, options or RequestOptions())

    def _headers_for(
        self,
        url: str,
        *,
        json_body: dict[str, Any] | None,
        method_headers: HeaderParam | None,
        options: RequestOptions,
        withdrawn: bool,
        credential: tuple[str, str] | None,
        scope_headers: Mapping[str, str],
    ) -> dict[str, str]:
        """The headers for one dispatch, built fresh from the URL it is going to.

        This is where rule 3 mostly stops needing machinery of its own: on a
        redirect the credential is re-derived from *that hop's* URL rather than
        carried along, so a hop that leaves the configured API origin simply
        does not get a key. ``withdrawn`` covers what that cannot — the caller's
        own credential headers, legitimate on the URL the caller chose and
        dropped once the *server* has chosen one.

        The credential boundary raises when the target origin cannot carry a
        credential at all (see :mod:`._credentials`).
        """
        option_headers = options.get("headers")
        idempotency_key = options.get("idempotency_key")
        attached = None if withdrawn else credential_for_request(self.base_url, credential, url)
        own_origin = same_origin(url, self.base_url)
        headers = _merge_headers(
            [
                # Stamped first — lowest precedence, the Stainless alpha.76 order
                # the drop-in contract pins — so an ``idempotency-key`` the caller
                # names anywhere later (default_headers, method headers,
                # ``request_options.headers``) still wins. A ``None`` value would
                # delete, so the key is only present when the option was set.
                None if idempotency_key is None else {"idempotency-key": idempotency_key},
                {"accept": "application/json", "user-agent": self.user_agent},
                # Identity and scope go to this client's own API origin only, judged per hop.
                self._identity_headers.headers if own_origin else None,
                scope_headers if own_origin else None,
                None if attached is None else {attached[0]: attached[1]},
                None if json_body is None else {"content-type": "application/json"},
                self._default_headers,
                # A method-level header names something the *operation* declares,
                # so it outranks a client-wide default; `request_options.headers`
                # is the caller's general escape hatch and stays the last word.
                method_headers,
                option_headers,
            ]
        )
        return withdraw_credentials(headers) if withdrawn else headers

    def _decode(self, response: httpx.Response) -> Any:
        """The response body as JSON, with an error status raised first.

        Everything a typed call does to a response *except* handing it to a
        model. Split out so the untyped escape hatch (:meth:`SyncAPIClient.get`
        and friends) reaches the same error hierarchy and the same parse
        failure as the generated surface — an escape hatch that answered a 404
        with a dict instead of ``NotFoundError`` would be a second contract.
        """
        if not response.is_success:
            raise self._status_error(response)
        try:
            return response.json()
        except ValueError as exc:
            raise APIResponseValidationError(response, message=str(exc)) from exc

    def _process(self, response: httpx.Response, cast_to: type[ResponseT]) -> ResponseT:
        return cast(ResponseT, self._process_response(response, cast_to))

    def _process_response(self, response: httpx.Response, cast_to: type[Any] | None) -> Any:
        """Cast a low-level response without narrowing it to generated models."""
        if cast_to is None or cast_to is object:
            return self._decode(response)
        if cast_to is httpx.Response:
            if not response.is_success:
                raise self._status_error(response)
            return response
        if cast_to is bytes:
            if not response.is_success:
                raise self._status_error(response)
            return response.content
        if cast_to is str:
            if not response.is_success:
                raise self._status_error(response)
            return response.text
        data = self._decode(response)
        return self._process_response_data(data=data, cast_to=cast_to, response=response)

    def _status_error(self, response: httpx.Response) -> APIStatusError:
        return self._make_status_error(response.reason_phrase, body=_safe_json(response), response=response)

    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        """Create an HTTP status error.

        This Stainless-compatible hook lets wrappers preserve their own error
        hierarchy while the kernel keeps one error-routing path.
        """
        del err_msg
        return status_error(response, body)

    def _process_response_data(
        self,
        *,
        data: object,
        cast_to: type[Any],
        response: httpx.Response,
    ) -> Any:
        if data is None or cast_to is object:
            return data
        try:
            if self._strict_response_validation:
                model = _model_type(cast_to)
                if model is not None:
                    return model.model_validate(data)
                return _adapter(cast_to).validate_python(data)
            return _construct_response(data, cast_to)
        except ValidationError as exc:
            raise APIResponseValidationError(response, body=data) from exc

    def _make_sse_decoder(self) -> SSEDecoder | SSEBytesDecoder:
        return SSEDecoder()

    def _timeout(self, options: RequestOptions | None) -> float | httpx.Timeout | None:
        if options is not None and "timeout" in options:
            return options["timeout"]
        return self.timeout

    def _max_retries(self, method: str, options: RequestOptions | None) -> int:
        if options is not None and "max_retries" in options:
            return options["max_retries"]
        return self.max_retries if method.upper() in _IDEMPOTENT_METHODS else 0


# The retry loop, once for sync and once for async. Injectable sleep functions
# keep the tests fast (a ``retry-after: 0`` header drives the delay to zero).
def _sleep(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


class SyncAPIClient(BaseClient):
    _client: httpx.Client

    def __init__(self, *, http_client: httpx.Client | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = http_client if http_client is not None else httpx.Client()

    def _resolve_credential(self, prepared: _Prepared, options: RequestOptions | None) -> None:
        assert prepared.provider is not None
        try:
            value = prepared.provider[1]()
        except Exception as exc:
            raise ComposioError(_PROVIDER_FAILED) from exc
        if inspect.isawaitable(value):
            close = getattr(value, "close", None)
            if callable(close):
                close()
            raise ComposioError(
                "The `auth` credential provider returned an awaitable; use `AsyncComposio` to await one."
            )
        self._accept_provided(prepared, value, options)

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: BodyParam | None = ...,
        body_model: BodyModel | None = ...,
        query: QueryParam | None = ...,
        headers: HeaderParam | None = ...,
        options: RequestOptions | None = ...,
        operation: Operation | None = ...,
        operation_headers: HeaderParam | None = ...,
        content: BinaryTypes | None = ...,
        files: RequestFiles | None = ...,
        stream: bool = ...,
    ) -> ResponseT: ...

    @overload
    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        body: BodyParam | None = ...,
        body_model: BodyModel | None = ...,
        query: QueryParam | None = ...,
        headers: HeaderParam | None = ...,
        options: RequestOptions | None = ...,
        operation: Operation | None = ...,
        operation_headers: HeaderParam | None = ...,
        content: BinaryTypes | None = ...,
        files: RequestFiles | None = ...,
        stream: bool = ...,
    ) -> Any: ...

    def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT] | None,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: BinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> Any:
        """One logical request: prepare, dispatch, retry, decode.

        ``cast_to=None`` is the untyped path the escape hatch takes — it decodes
        the body and hands it back rather than validating it into a model. The
        overloads keep that from leaking into the generated surface, where every
        call names a model and must still be typed as returning one.

        The escape-hatch methods below call this directly rather than through a
        helper, which is what keeps ``_note_deprecation``'s ``stacklevel`` right
        for both: ``client.get(...)`` and a generated resource method sit at the
        same depth above it.
        """
        response, _ = self._request_response(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        return self._decode(response) if cast_to is None else self._process(response, cast_to)

    def _request_response(
        self,
        method: str,
        path: str,
        *,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: BinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> tuple[httpx.Response, int]:
        prepared = self._prepare(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        if prepared.provider is not None:
            self._resolve_credential(prepared, options)
        max_retries = self._max_retries(method, options)
        timeout = self._timeout(options)
        info_enabled = _logger.isEnabledFor(logging.INFO)
        debug_enabled = _logger.isEnabledFor(logging.DEBUG)
        log_path = prepared.log_path if info_enabled else ""

        for num_retries in range(max_retries + 1):
            remaining = max_retries - num_retries
            if debug_enabled:
                _safe_log(
                    logging.DEBUG,
                    "request attempt method=%s path=%s attempt=%d/%d",
                    prepared.method,
                    log_path,
                    num_retries + 1,
                    max_retries + 1,
                )
            started_at = time.perf_counter() if info_enabled else 0.0
            try:
                response = self._dispatch(prepared, timeout=timeout, options=options)
            except httpx.TimeoutException as exc:
                if info_enabled:
                    _safe_log(
                        logging.INFO,
                        "request failed method=%s path=%s reason=timeout duration_ms=%.2f",
                        prepared.method,
                        log_path,
                        (time.perf_counter() - started_at) * 1000,
                    )
                if remaining > 0:
                    if info_enabled:
                        _safe_log(
                            logging.INFO,
                            "request retry method=%s path=%s reason=timeout next_attempt=%d remaining=%d",
                            prepared.method,
                            log_path,
                            num_retries + 2,
                            remaining,
                        )
                    _sleep(_retry_delay_seconds(num_retries, None))
                    continue
                raise APITimeoutError(exc.request) from exc
            except httpx.RequestError as exc:
                if info_enabled:
                    _safe_log(
                        logging.INFO,
                        "request failed method=%s path=%s reason=connection duration_ms=%.2f",
                        prepared.method,
                        log_path,
                        (time.perf_counter() - started_at) * 1000,
                    )
                if remaining > 0:
                    if info_enabled:
                        _safe_log(
                            logging.INFO,
                            "request retry method=%s path=%s reason=connection next_attempt=%d remaining=%d",
                            prepared.method,
                            log_path,
                            num_retries + 2,
                            remaining,
                        )
                    _sleep(_retry_delay_seconds(num_retries, None))
                    continue
                raise APIConnectionError(request=exc.request) from exc

            if info_enabled:
                _safe_log(
                    logging.INFO,
                    "request response method=%s path=%s status=%d outcome=%s duration_ms=%.2f",
                    prepared.method,
                    log_path,
                    response.status_code,
                    "success" if response.is_success else "http_error",
                    (time.perf_counter() - started_at) * 1000,
                )
            if response.is_success or remaining <= 0:
                self._note_deprecation(response, method, path, prepared.operation)
                return response, num_retries
            retryable = _should_retry(response)
            if not retryable:
                self._note_deprecation(response, method, path, prepared.operation)
                return response, num_retries
            if info_enabled:
                _safe_log(
                    logging.INFO,
                    "request retry method=%s path=%s reason=status_%d next_attempt=%d remaining=%d",
                    prepared.method,
                    log_path,
                    response.status_code,
                    num_retries + 2,
                    remaining,
                )

            response.close()
            _sleep(_retry_delay_seconds(num_retries, response.headers))

        raise RuntimeError("unreachable: retry loop exited without returning")  # pragma: no cover

    def _request_raw(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT] | None,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: BinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> APIResponse[ResponseT | Any]:
        response, retries_taken = self._request_response(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        return APIResponse(
            raw=response,
            cast_to=cast_to,
            client=self,
            stream=stream,
            stream_cls=None,
            options=options or RequestOptions(),
            retries_taken=retries_taken,
        )

    def _parse_response(self, response: httpx.Response, cast_to: type[Any] | None) -> Any:
        if not response.is_stream_consumed:
            response.read()
        return self._process_response(response, cast_to)

    # ── the raw HTTP escape hatch ────────────────────────────────────────────
    #
    # The same five verbs the TypeScript client exposes (`src/compat/client.ts`)
    # and the pinned Stainless Python client exposes. They are not a
    # convenience: four operations downstream calls have no typed method on the
    # Stainless surface at all — the three `webhook_subscriptions` operations
    # and `tool_router.session.delete` — so this is the only surface a consumer
    # has for them, and the only one a differential comparison can run them on.
    #
    # `cast_to` is optional here and required on the Stainless client: omit it
    # and the decoded JSON comes back as-is. That is the same relaxed-types
    # widening the rest of this package takes, and it is a superset — a
    # Stainless-shaped call that names a model still returns that model.
    #
    # Each verb calls `_request` directly rather than delegating to a shared
    # one. Delegating would add a frame between the caller and the deprecation
    # warning, and `_note_deprecation` counts frames.

    def request(
        self,
        cast_to: type[ResponseT],
        options: Mapping[str, Any],
        *,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
    ) -> Any:
        method = str(options.get("method", "get"))
        path = str(options.get("url", options.get("path", "")))
        request_options = cast(RequestOptions, options)
        raw = self._request_raw(
            method,
            path,
            cast_to=cast_to,
            body=cast(BodyParam | None, options.get("json_data", options.get("body"))),
            query=cast(QueryParam | None, options.get("params", options.get("query"))),
            headers=cast(HeaderParam | None, options.get("headers")),
            options=request_options,
            content=cast(BinaryTypes | None, options.get("content")),
            files=cast(RequestFiles | None, options.get("files")),
            stream=stream,
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to,
                response=raw.http_response,
                client=self,
                options=request_options,
            )
        return raw.parse()

    def get(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = self._request_raw(
            "get", path, cast_to=cast_to, query=query, headers=headers, options=options, stream=stream
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to or object, response=raw.http_response, client=self, options=options
            )
        return raw.parse()

    def post(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: BinaryTypes | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        files: RequestFiles | None = None,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = self._request_raw(
            "post",
            path,
            cast_to=cast_to,
            body=body,
            query=query,
            headers=headers,
            options=options,
            content=content,
            files=files,
            stream=stream,
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to or object, response=raw.http_response, client=self, options=options
            )
        return raw.parse()

    def put(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: BinaryTypes | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = self._request_raw(
            "put",
            path,
            cast_to=cast_to,
            body=body,
            query=query,
            headers=headers,
            options=options,
            content=content,
            files=files,
        )
        return raw.parse()

    def patch(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: BinaryTypes | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = self._request_raw(
            "patch",
            path,
            cast_to=cast_to,
            body=body,
            query=query,
            headers=headers,
            options=options,
            content=content,
            files=files,
        )
        return raw.parse()

    def delete(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: BinaryTypes | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        return self._request_raw(
            "delete",
            path,
            cast_to=cast_to,
            body=body,
            query=query,
            headers=headers,
            options=options,
            content=content,
        ).parse()

    def _dispatch(
        self,
        prepared: _Prepared,
        *,
        timeout: float | httpx.Timeout | None,
        options: RequestOptions | None,
    ) -> httpx.Response:
        """One attempt: the request, plus however many redirects it takes to
        land on a non-3xx response.

        The whole chain sits **inside one attempt** — one entry in the retry
        budget. That follows from what a redirect is: the caller made one
        logical request, so a chain must not consume ``max_retries`` (a 3xx is
        not a failure to retry), and a retry re-issues the *original* request,
        chain and all. It also keeps the deprecation interceptor's
        once-per-logical-call guarantee intact, since the single response exit
        is still reached once.

        Everything the server chose is re-derived rather than carried: the
        headers (:meth:`_headers_for`), the method and body (the standard
        301/302/303 rewrite), and the query, which is left to the ``Location``
        URL because the server picked it.
        """
        opts = options or RequestOptions()
        url = prepared.url
        method = prepared.method
        json_body = prepared.json_body
        form_body = prepared.form_body
        content = prepared.content
        files = prepared.files
        headers = prepared.headers
        params: _QueryPairs | None = prepared.params
        withdrawn = False

        for hop in range(MAX_REDIRECTS + 1):
            request = self._client.build_request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_body,
                data=cast(Any, form_body),
                content=cast(Any, content),
                files=cast(Any, files),
                timeout=timeout,
            )
            response = self._client.send(
                request,
                stream=prepared.stream,
                follow_redirects=False,
            )
            if response.status_code not in _REDIRECT_STATUSES or opts.get("follow_redirects") is False:
                return response
            location = response.headers.get("location")
            if location is None:
                return response
            target = _redirect_target(location, url)
            if target is None:
                return response
            if hop >= MAX_REDIRECTS:
                raise APIConnectionError(message=_TOO_MANY_REDIRECTS, request=response.request)

            response.close()
            if not same_origin(target, url):
                withdrawn = True
            if _rewrite_for_redirect(response.status_code, method):
                method = "GET"
                json_body = None
                form_body = None
                content = None
                files = None
            url = target
            params = None
            headers = self._headers_for(
                url,
                json_body=json_body,
                method_headers=prepared.method_headers,
                options=opts,
                withdrawn=withdrawn,
                credential=prepared.credential,
                scope_headers=prepared.scope_headers,
            )

        raise RuntimeError("unreachable: redirect loop exited without returning")  # pragma: no cover

    def close(self) -> None:
        self._client.close()

    def is_closed(self) -> bool:
        return self._client.is_closed


async def _async_sleep(seconds: float) -> None:
    if seconds > 0:
        import asyncio

        await asyncio.sleep(seconds)


class AsyncAPIClient(BaseClient):
    _client: httpx.AsyncClient

    def __init__(self, *, http_client: httpx.AsyncClient | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._client = http_client if http_client is not None else httpx.AsyncClient()

    _accepts_async_credentials: ClassVar[bool] = True

    async def _resolve_credential(self, prepared: _Prepared, options: RequestOptions | None) -> None:
        assert prepared.provider is not None
        try:
            value = prepared.provider[1]()
            if inspect.isawaitable(value):
                value = await value
        except Exception as exc:
            raise ComposioError(_PROVIDER_FAILED) from exc
        self._accept_provided(prepared, value, options)

    @overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: BodyParam | None = ...,
        body_model: BodyModel | None = ...,
        query: QueryParam | None = ...,
        headers: HeaderParam | None = ...,
        options: RequestOptions | None = ...,
        operation: Operation | None = ...,
        operation_headers: HeaderParam | None = ...,
        content: AsyncBinaryTypes | None = ...,
        files: RequestFiles | None = ...,
        stream: bool = ...,
    ) -> ResponseT: ...

    @overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        body: BodyParam | None = ...,
        body_model: BodyModel | None = ...,
        query: QueryParam | None = ...,
        headers: HeaderParam | None = ...,
        options: RequestOptions | None = ...,
        operation: Operation | None = ...,
        operation_headers: HeaderParam | None = ...,
        content: AsyncBinaryTypes | None = ...,
        files: RequestFiles | None = ...,
        stream: bool = ...,
    ) -> Any: ...

    async def _request(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT] | None,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> Any:
        """See :meth:`SyncAPIClient._request` — the same loop, awaited."""
        response, _ = await self._request_response(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        if not response.is_stream_consumed:
            await response.aread()
        return self._decode(response) if cast_to is None else self._process(response, cast_to)

    async def _request_response(
        self,
        method: str,
        path: str,
        *,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> tuple[httpx.Response, int]:
        prepared = self._prepare(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        if prepared.provider is not None:
            await self._resolve_credential(prepared, options)
        max_retries = self._max_retries(method, options)
        timeout = self._timeout(options)
        info_enabled = _logger.isEnabledFor(logging.INFO)
        debug_enabled = _logger.isEnabledFor(logging.DEBUG)
        log_path = prepared.log_path if info_enabled else ""

        for num_retries in range(max_retries + 1):
            remaining = max_retries - num_retries
            if debug_enabled:
                _safe_log(
                    logging.DEBUG,
                    "request attempt method=%s path=%s attempt=%d/%d",
                    prepared.method,
                    log_path,
                    num_retries + 1,
                    max_retries + 1,
                )
            started_at = time.perf_counter() if info_enabled else 0.0
            try:
                response = await self._dispatch(prepared, timeout=timeout, options=options)
            except httpx.TimeoutException as exc:
                if info_enabled:
                    _safe_log(
                        logging.INFO,
                        "request failed method=%s path=%s reason=timeout duration_ms=%.2f",
                        prepared.method,
                        log_path,
                        (time.perf_counter() - started_at) * 1000,
                    )
                if remaining > 0 and prepared.replayable_content:
                    if info_enabled:
                        _safe_log(
                            logging.INFO,
                            "request retry method=%s path=%s reason=timeout next_attempt=%d remaining=%d",
                            prepared.method,
                            log_path,
                            num_retries + 2,
                            remaining,
                        )
                    await _async_sleep(_retry_delay_seconds(num_retries, None))
                    continue
                raise APITimeoutError(exc.request) from exc
            except httpx.RequestError as exc:
                if info_enabled:
                    _safe_log(
                        logging.INFO,
                        "request failed method=%s path=%s reason=connection duration_ms=%.2f",
                        prepared.method,
                        log_path,
                        (time.perf_counter() - started_at) * 1000,
                    )
                if remaining > 0 and prepared.replayable_content:
                    if info_enabled:
                        _safe_log(
                            logging.INFO,
                            "request retry method=%s path=%s reason=connection next_attempt=%d remaining=%d",
                            prepared.method,
                            log_path,
                            num_retries + 2,
                            remaining,
                        )
                    await _async_sleep(_retry_delay_seconds(num_retries, None))
                    continue
                raise APIConnectionError(request=exc.request) from exc

            if info_enabled:
                _safe_log(
                    logging.INFO,
                    "request response method=%s path=%s status=%d outcome=%s duration_ms=%.2f",
                    prepared.method,
                    log_path,
                    response.status_code,
                    "success" if response.is_success else "http_error",
                    (time.perf_counter() - started_at) * 1000,
                )
            if response.is_success or remaining <= 0:
                self._note_deprecation(response, method, path, prepared.operation)
                return response, num_retries
            retryable = _should_retry(response) and prepared.replayable_content
            if not retryable:
                self._note_deprecation(response, method, path, prepared.operation)
                return response, num_retries
            if info_enabled:
                _safe_log(
                    logging.INFO,
                    "request retry method=%s path=%s reason=status_%d next_attempt=%d remaining=%d",
                    prepared.method,
                    log_path,
                    response.status_code,
                    num_retries + 2,
                    remaining,
                )

            await response.aclose()
            await _async_sleep(_retry_delay_seconds(num_retries, response.headers))

        raise RuntimeError("unreachable: retry loop exited without returning")  # pragma: no cover

    async def _request_raw(
        self,
        method: str,
        path: str,
        *,
        cast_to: type[ResponseT] | None,
        body: BodyParam | None = None,
        body_model: BodyModel | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        options: RequestOptions | None = None,
        operation: Operation | None = None,
        operation_headers: HeaderParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        stream: bool = False,
    ) -> AsyncAPIResponse[ResponseT | Any]:
        response, retries_taken = await self._request_response(
            method,
            path,
            body=body,
            body_model=body_model,
            query=query,
            headers=headers,
            options=options,
            operation=operation,
            operation_headers=operation_headers,
            content=content,
            files=files,
            stream=stream,
        )
        if not stream and not response.is_stream_consumed:
            await response.aread()
        return AsyncAPIResponse(
            raw=response,
            cast_to=cast_to,
            client=self,
            stream=stream,
            stream_cls=None,
            options=options or RequestOptions(),
            retries_taken=retries_taken,
        )

    def _parse_response(self, response: httpx.Response, cast_to: type[Any] | None) -> Any:
        return self._process_response(response, cast_to)

    # The raw escape hatch, awaited. See :class:`SyncAPIClient` for why each verb
    # calls ``_request_raw`` itself and why ``cast_to`` is optional.

    async def request(
        self,
        cast_to: type[ResponseT],
        options: Mapping[str, Any],
        *,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
    ) -> Any:
        method = str(options.get("method", "get"))
        path = str(options.get("url", options.get("path", "")))
        request_options = cast(RequestOptions, options)
        raw = await self._request_raw(
            method,
            path,
            cast_to=cast_to,
            body=cast(BodyParam | None, options.get("json_data", options.get("body"))),
            query=cast(QueryParam | None, options.get("params", options.get("query"))),
            headers=cast(HeaderParam | None, options.get("headers")),
            options=request_options,
            content=cast(AsyncBinaryTypes | None, options.get("content")),
            files=cast(RequestFiles | None, options.get("files")),
            stream=stream,
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to,
                response=raw.http_response,
                client=self,
                options=request_options,
            )
        return await raw.parse()

    async def get(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = await self._request_raw(
            "get", path, cast_to=cast_to, query=query, headers=headers, options=options, stream=stream
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to or object, response=raw.http_response, client=self, options=options
            )
        return await raw.parse()

    async def post(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        stream: bool = False,
        stream_cls: type[Any] | None = None,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        raw = await self._request_raw(
            "post",
            path,
            cast_to=cast_to,
            body=body,
            query=query,
            headers=headers,
            options=options,
            content=content,
            files=files,
            stream=stream,
        )
        if stream and stream_cls is not None:
            return stream_cls(
                cast_to=cast_to or object, response=raw.http_response, client=self, options=options
            )
        return await raw.parse()

    async def put(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        return await (
            await self._request_raw(
                "put",
                path,
                cast_to=cast_to,
                body=body,
                query=query,
                headers=headers,
                options=options,
                content=content,
                files=files,
            )
        ).parse()

    async def patch(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: AsyncBinaryTypes | None = None,
        files: RequestFiles | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        return await (
            await self._request_raw(
                "patch",
                path,
                cast_to=cast_to,
                body=body,
                query=query,
                headers=headers,
                options=options,
                content=content,
                files=files,
            )
        ).parse()

    async def delete(
        self,
        path: str,
        *,
        cast_to: type[ResponseT] | None = None,
        body: BodyParam | None = None,
        content: AsyncBinaryTypes | None = None,
        options: RequestOptions = _DEFAULT_REQUEST_OPTIONS,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
    ) -> Any:
        return await (
            await self._request_raw(
                "delete",
                path,
                cast_to=cast_to,
                body=body,
                query=query,
                headers=headers,
                options=options,
                content=content,
            )
        ).parse()

    async def _dispatch(
        self,
        prepared: _Prepared,
        *,
        timeout: float | httpx.Timeout | None,
        options: RequestOptions | None,
    ) -> httpx.Response:
        """See :meth:`SyncAPIClient._dispatch` — the same hop loop, awaited.
        Duplicated across sync/async like the retry loop above it."""
        opts = options or RequestOptions()
        url = prepared.url
        method = prepared.method
        json_body = prepared.json_body
        form_body = prepared.form_body
        content = prepared.content
        files = prepared.files
        headers = prepared.headers
        params: _QueryPairs | None = prepared.params
        withdrawn = False

        for hop in range(MAX_REDIRECTS + 1):
            request = self._client.build_request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_body,
                data=cast(Any, form_body),
                content=cast(Any, content),
                files=cast(Any, files),
                timeout=timeout,
            )
            response = await self._client.send(
                request,
                stream=prepared.stream,
                follow_redirects=False,
            )
            if response.status_code not in _REDIRECT_STATUSES or opts.get("follow_redirects") is False:
                return response
            location = response.headers.get("location")
            if location is None:
                return response
            target = _redirect_target(location, url)
            if target is None:
                return response
            if hop >= MAX_REDIRECTS:
                raise APIConnectionError(message=_TOO_MANY_REDIRECTS, request=response.request)

            rewrite = _rewrite_for_redirect(response.status_code, method)
            await response.aclose()
            if not prepared.replayable_content and not rewrite:
                raise APIConnectionError(message=_NON_REPLAYABLE_REDIRECT, request=response.request)
            if not same_origin(target, url):
                withdrawn = True
            if rewrite:
                method = "GET"
                json_body = None
                form_body = None
                content = None
                files = None
            url = target
            params = None
            headers = self._headers_for(
                url,
                json_body=json_body,
                method_headers=prepared.method_headers,
                options=opts,
                withdrawn=withdrawn,
                credential=prepared.credential,
                scope_headers=prepared.scope_headers,
            )

        raise RuntimeError("unreachable: redirect loop exited without returning")  # pragma: no cover

    async def aclose(self) -> None:
        await self._client.aclose()

    async def close(self) -> None:
        await self.aclose()

    def is_closed(self) -> bool:
        return self._client.is_closed
