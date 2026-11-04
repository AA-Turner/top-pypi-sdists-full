"""Shared resource plumbing for the generated resource classes."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import quote

from .._types import NOT_GIVEN, NotGiven, Omit, RequestOptions

if TYPE_CHECKING:
    from .._base_client import AsyncAPIClient, BodyParam, SyncAPIClient


#: The RFC 3986 §3.3 ``pchar`` characters that are legal unescaped inside a path
#: segment beyond the unreserved set ``quote`` already leaves alone: the
#: ``sub-delims`` plus ``:`` and ``@``. Matches Stainless Python's
#: ``_utils/_path.py``. ``/`` is deliberately *not* safe — encoding it is what
#: keeps a path parameter confined to a single segment.
#:
#: Our TypeScript client differs here by design: ``src/compat/request.ts`` uses
#: ``encodeURIComponent`` semantics because that is what Stainless *TypeScript*
#: does. The two Stainless clients disagree with each other on this; for a
#: Python package the Python oracle wins.
_PATH_SAFE = "!$&'()*+,;=:@"

#: A dot-segment: ``.`` or ``..``, which RFC 3986 §5.2.4 tells a server to
#: resolve away, plus their percent-encoded spellings. A caller-influenced path
#: parameter of ``..`` would otherwise rewrite the request target —
#: ``/api/v3.1/tool_router/session/../attach`` resolves to
#: ``/api/v3.1/tool_router/attach``.
#:
#: The percent-encoded spellings cannot actually reach the wire through this
#: function (``%`` is not in ``_PATH_SAFE``, so ``%2e`` is escaped to ``%252e``),
#: but they are rejected anyway, exactly as Stainless Python does, "to protect
#: against incorrectly implemented normalization in servers/proxies" — and so
#: the guard stays correct if the safe set is ever widened.
_DOT_SEGMENT = re.compile(r"^(?:\.|%2[eE]){1,2}$")


def path_segment(value: str, name: str) -> str:
    """Percent-encode a path parameter, rejecting empty values and dot-segments.

    Both rejections raise ``ValueError``, before dispatch: that is what the
    empty case has always done here (matching Stainless Python, which raises
    ``ValueError`` for both), and a bad *argument* is not an API error, so the
    ``ComposioError`` hierarchy in ``_exceptions`` is the wrong home for it —
    every class under it carries an ``httpx`` request or response. Our
    TypeScript client raises ``ComposioError`` for the dot-segment case instead,
    because that is what Stainless TypeScript does; each client follows its own
    oracle.

    The dot-segment check is **per parameter**, where Stainless Python checks the
    assembled path. It checks the assembled path because its templates may place
    two placeholders side by side, or a placeholder next to static text, so a
    dot-segment can be *composed* out of pieces that are individually harmless.
    No template in this client can do that: :func:`build_path` substitutes each
    OpenAPI path parameter as a complete segment — the spec's templates always
    surround a placeholder with a literal ``/`` or the end of the path, never
    another placeholder — and ``/`` is not in ``_PATH_SAFE``, so an encoded
    parameter cannot introduce a segment boundary of its own. Per-parameter is
    therefore exactly per-segment here, and it buys a precise error naming the
    offending argument.
    """
    if not value:
        raise ValueError(f"Expected a non-empty value for `{name}` but received {value!r}")
    if _DOT_SEGMENT.match(value):
        raise ValueError(f"Path parameter `{name}` would result in a path with invalid segments: {value!r}")
    return quote(value, safe=_PATH_SAFE)


_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")


def build_path(template: str, params: Mapping[str, str]) -> str:
    """Substitute percent-encoded path parameters into a spec path template.

    The generated resource methods carry the OpenAPI path *template* verbatim
    (``/api/v3.1/tool_router/session/{session_id}/attach``) and hand their
    arguments here keyed by the spec's own parameter names, so the wire path a
    method builds is legible next to the operation it comes from. Every
    substituted value goes through :func:`path_segment`, which is what confines
    a caller-supplied value to one segment.

    Both mismatch directions raise ``ValueError`` before dispatch. Generation
    makes them unreachable — the template and the argument list come from the
    same operation plan — so this guards a hand-edit of a manufactured file,
    which is exactly the case the banner says not to create.
    """
    supplied = set(params)
    used: set[str] = set()

    def substitute(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in params:
            raise ValueError(f"Path template {template!r} has no value for parameter `{name}`")
        used.add(name)
        return path_segment(params[name], name)

    path = _PLACEHOLDER.sub(substitute, template)
    unused = supplied - used
    if unused:
        raise ValueError(f"Path template {template!r} declares no parameter(s) {sorted(unused)!r}")
    return path


def compact(values: Mapping[str, Any]) -> dict[str, Any]:
    """Drop omitted-value sentinels while preserving explicit ``None``."""
    return {name: value for name, value in values.items() if not isinstance(value, (NotGiven, Omit))}


def merge_mapping(
    aggregate: object | None,
    flat: Mapping[str, Any],
) -> dict[str, Any] | None:
    if aggregate is None and not flat:
        return None
    if hasattr(aggregate, "model_dump"):
        merged = cast("dict[str, Any]", cast(Any, aggregate).model_dump(exclude_unset=True))
    elif isinstance(aggregate, Mapping):
        merged = dict(aggregate)
    else:
        merged = {}
    merged.update(flat)
    return merged


def merge_body(
    aggregate: BodyParam | None,
    flat: Mapping[str, Any],
) -> BodyParam:
    if aggregate is None:
        return dict(flat)
    if not flat:
        return aggregate
    if hasattr(aggregate, "model_dump"):
        merged = cast(Any, aggregate).model_dump(exclude_unset=True)
    else:
        merged = dict(aggregate)
    merged.update(flat)
    return cast("BodyParam", merged)


def require_fields(
    aggregate: object | None,
    flat: Mapping[str, Any],
    required: tuple[str, ...],
    location: str,
) -> None:
    """Enforce required flat fields while permitting a transitional aggregate."""
    if not required:
        return
    if hasattr(aggregate, "model_dump"):
        aggregate_values = cast(Any, aggregate).model_dump(exclude_unset=True)
    elif isinstance(aggregate, Mapping):
        aggregate_values = aggregate
    else:
        aggregate_values = {}
    missing = [name for name in required if name not in flat and name not in aggregate_values]
    if missing:
        names = ", ".join(repr(name) for name in missing)
        raise TypeError(f"Missing required {location} argument(s): {names}")


def split_body_argument(
    value: Any,
    other_flat: Mapping[str, Any],
    aggregate_keys: tuple[str, ...],
) -> tuple[BodyParam | None, Any]:
    """Distinguish the two proxy methods' flat ``body`` field from old aggregate calls."""
    if isinstance(value, Omit):
        return None, value
    looks_aggregate = hasattr(value, "model_dump") or (
        not other_flat
        and isinstance(value, Mapping)
        and any(key in value for key in aggregate_keys if key != "body")
    )
    return (cast("BodyParam", value), Omit()) if looks_aggregate else (None, value)


def normalize_body_argument(value: Any, legacy_args: tuple[object, ...]) -> Any:
    """Move the former positional aggregate into the colliding flat ``body`` slot."""
    if not legacy_args:
        return value
    if len(legacy_args) != 1:
        raise TypeError("Expected at most one positional aggregate body")
    if not isinstance(value, Omit):
        raise TypeError("Body was supplied both positionally and by keyword")
    return legacy_args[0]


def split_mapping_argument(value: Any) -> tuple[Mapping[str, Any] | None, Any]:
    """Treat a mapping as the transitional aggregate, otherwise as one flat field."""
    return (value, Omit()) if isinstance(value, Mapping) else (None, value)


def normalize_path_arguments(
    trailing_value: str,
    legacy_args: tuple[object, ...],
    *,
    leading_values: tuple[str | None, ...],
    leading_names: tuple[str, ...],
    trailing_name: str,
    body: BodyParam | None = None,
    accepts_body: bool,
) -> tuple[str, tuple[str, ...], BodyParam | None]:
    """Accept Stainless path placement and the former all-positional order.

    Stainless makes only the final path component positional. The first owned
    generator made every component positional, followed by an optional body.
    Generated methods expose the Stainless names while collecting any extra
    positional values here so both forms reach one normalized request.
    """
    if not legacy_args:
        missing = [name for name, value in zip(leading_names, leading_values, strict=True) if value is None]
        if missing:
            names = ", ".join(repr(name) for name in missing)
            raise TypeError(f"Missing required keyword-only path argument(s): {names}")
        return trailing_value, cast("tuple[str, ...]", leading_values), body

    if any(value is not None for value in leading_values):
        raise TypeError("Cannot mix legacy positional path arguments with Stainless keyword path arguments")

    path_tail_count = len(leading_names)
    allowed = {path_tail_count}
    if accepts_body:
        allowed.add(path_tail_count + 1)
    if len(legacy_args) not in allowed:
        raise TypeError(
            f"Legacy call for `{trailing_name}` expected {path_tail_count} path argument(s)"
            + (" and at most one body" if accepts_body else "")
        )

    path_values = (trailing_value, *legacy_args[:path_tail_count])
    legacy_body = legacy_args[path_tail_count] if len(legacy_args) > path_tail_count else None
    if legacy_body is not None:
        if body is not None:
            raise TypeError("Body was supplied both positionally and by keyword")
        body = cast("BodyParam", legacy_body)
    return cast(str, path_values[-1]), cast("tuple[str, ...]", path_values[:-1]), body


def make_request_options(
    request_options: RequestOptions | None,
    *,
    extra_headers: Mapping[str, str | None] | None,
    extra_query: Mapping[str, object] | None,
    extra_body: Mapping[str, Any] | None,
    timeout: float | object | None | NotGiven = NOT_GIVEN,
) -> RequestOptions:
    options = RequestOptions(**(request_options or {}))
    if extra_headers is not None:
        options["headers"] = {**(options.get("headers") or {}), **extra_headers}
    if extra_query is not None:
        options["params"] = {**(options.get("params") or options.get("query") or {}), **extra_query}
    if extra_body is not None:
        options["extra_json"] = {**(options.get("extra_json") or {}), **extra_body}
    if not isinstance(timeout, NotGiven):
        options["timeout"] = cast(Any, timeout)
    return options


class SyncAPIResource:
    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client


class AsyncAPIResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client
