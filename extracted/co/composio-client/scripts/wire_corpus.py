"""Shared vocabulary for the Python request-wire parity gate.

The TypeScript side pins the published Stainless client as a devDependency and
runs a differential wire suite against it (``test/unit/differential-wire.test.ts``).
Python cannot do that in one environment: the PyPI distribution
``composio-client`` 1.43.0 and *this* repo's package both import as
``composio_client``, so they collide in a single venv.

The Python gate is therefore split in two:

* ``scripts/capture_stainless_oracle.py`` runs the corpus through the Stainless
  1.43.0 client in an isolated interpreter and records the exact wire requests
  into ``tests/fixtures/stainless_wire_oracle.json`` (see ``REGENERATE_COMMAND``).
* ``tests/test_wire_parity.py`` runs the same logical calls through *our* client
  and asserts every recorded request matches.

This module is the only thing both halves share: the fixture location and
provenance, the client construction constants, the request snapshotter, and the
payload literals that must be byte-identical on both sides. It deliberately
imports nothing from ``composio_client`` — the capture half runs where that name
resolves to the Stainless distribution.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple

import httpx

#: The committed golden capture, and how to rebuild it.
FIXTURE_PATH = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "stainless_wire_oracle.json"
ORACLE_PACKAGE = "composio-client"
ORACLE_VERSION = "1.43.0"
REGENERATE_COMMAND = (
    "cd python && uv run --isolated --no-project "
    f"--with {ORACLE_PACKAGE}=={ORACLE_VERSION} python scripts/capture_stainless_oracle.py"
)

#: Both clients are constructed with exactly these options, so `host`, `accept`
#: and `x-api-key` are directly comparable.
BASE_URL = "https://api.test"
API_KEY = "ak_wire_parity"

SESSION_ID = "trs_wire_parity"
MOUNT_ID = "workspace"

#: A path parameter needing percent-encoding of characters both clients agree on
#: (space, slash).
ENCODED_SESSION_ID = "trs a b/c"
#: A path parameter containing RFC 3986 `sub-delims`, which the two clients
#: encode *differently* — see the `path-subdelims` case in the test module.
SUBDELIMS_SESSION_ID = "trs déjà+vu,x"

# --------------------------------------------------------------------------
# Headers that identify the generator or the transport rather than the API
# call — the agreed carve-out, mirroring the TS suite's `x-stainless-*` /
# `user-agent` exclusion. `content-length`, `accept-encoding` and `connection`
# are httpx/environment artifacts (the oracle runs under its own resolved
# httpx), and the body itself is compared as parsed JSON.
# --------------------------------------------------------------------------
# Explicit client identity fields differ from Stainless; telemetry tests pin their values.
_IGNORED_HEADERS = frozenset(
    {
        "user-agent",
        "content-length",
        "accept-encoding",
        "connection",
        "x-client-provenance",
        "x-client-version",
        "x-client-library",
        "x-client-library-version",
        "x-client-language",
        "x-client-runtime",
        "x-runtime",
        "x-runtime-version",
    }
)


def is_ignored_header(name: str) -> bool:
    lowered = name.lower()
    return lowered.startswith("x-stainless-") or lowered in _IGNORED_HEADERS


def _snapshot(request: httpx.Request) -> dict[str, Any]:
    """The wire request, reduced to what the parity claim is about."""
    raw_target = request.url.raw_path.decode("ascii")
    raw_path, _, raw_query = raw_target.partition("?")
    content = request.content
    return {
        "method": request.method,
        # percent-encoded, exactly as it goes out
        "path": raw_path,
        "query": raw_query,
        "headers": {
            name.lower(): value for name, value in request.headers.items() if not is_ignored_header(name)
        },
        # parsed: JSON object key order is not part of the wire contract
        "body": json.loads(content) if content else None,
    }


class Case(NamedTuple):
    """One logical API call, expressed in one client's calling convention.

    ``oracle`` names the fixture entry the call must reproduce and defaults to
    ``id``; several of our cases may point at one oracle entry (e.g. the same
    payload passed as a plain dict and as the generated pydantic model).
    """

    id: str
    invoke: Callable[[Any], object]
    client_options: Mapping[str, Any] | None = None
    oracle: str | None = None

    @property
    def oracle_id(self) -> str:
        return self.oracle or self.id


def capture(composio_cls: Any, case: Case, *, credentials: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Drive ``case`` through ``composio_cls`` and return the wire request.

    Both clients accept the same constructor options and an ``http_client``, so
    one helper serves the oracle capture and the parity test. They differ only
    in how a credential is spelled: the oracle takes ``api_key=`` (the default
    here), the owned client ``auth=ProjectAuth(key)`` since 2.0.0-rc.18, which
    its caller passes as ``credentials``.

    The mock transport answers every call with ``{}``, which does not satisfy the
    response models; the resulting client-side error is swallowed because this
    harness only cares about the *request*. A call that never reached the
    transport is a hard failure, so a swallowed error can never hide a
    non-dispatch.
    """
    seen: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(_snapshot(request))
        return httpx.Response(200, json={})

    client = composio_cls(
        **({"api_key": API_KEY} if credentials is None else credentials),
        base_url=BASE_URL,
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        **(case.client_options or {}),
    )
    error: BaseException | None = None
    try:
        case.invoke(client)
    except Exception as exc:  # noqa: BLE001 - response parsing is out of scope
        error = exc
    finally:
        client.close()

    if len(seen) != 1:
        raise AssertionError(
            f"case {case.id!r}: expected exactly one dispatched request, captured {len(seen)}"
        ) from error
    return seen[0]


# --------------------------------------------------------------------------
# Payload literals shared by both halves.
#
# `custom_connection_data` on `session.proxy_execute` is the only place in the
# tool_router surface with non-pythonic wire names: `authScheme`, `toolkitSlug`,
# `your-domain`, `COMPANYDOMAIN`, `instanceEndpoint`, `instanceName` on every
# `authScheme` variant, plus `redirectUrl` on the OAUTH1 variant. The `*_SNAKE`
# dicts are the Stainless call idiom (per-field snake_case); the `*_ALIASED`
# dicts in the test module are the same payloads keyed by wire name.
# --------------------------------------------------------------------------

CCD_OAUTH2_SNAKE: dict[str, Any] = {
    "auth_scheme": "OAUTH2",
    "toolkit_slug": "gmail",
    "val": {
        "access_token": "tok_oauth2",
        "refresh_token": "refresh_oauth2",
        "your_domain": "acme.example.com",
        "companydomain": "acme-corp",
        "instance_endpoint": "https://acme.service-now.com",
        "instance_name": "acme-prod",
        "scope": ["read", "write"],
    },
}

CCD_OAUTH1_SNAKE: dict[str, Any] = {
    "auth_scheme": "OAUTH1",
    "toolkit_slug": "trello",
    "val": {
        "oauth_token": "ot_1",
        "oauth_token_secret": "ots_1",
        "redirect_url": "https://example.com/callback",
        "your_domain": "acme.example.com",
    },
}

CCD_API_KEY_SNAKE: dict[str, Any] = {
    "auth_scheme": "API_KEY",
    "toolkit_slug": "notion",
    "val": {
        "generic_api_key": "sk_live_1",
        "instance_name": "acme-prod",
    },
}

CCD_BEARER_TOKEN_SNAKE: dict[str, Any] = {
    "auth_scheme": "BEARER_TOKEN",
    "toolkit_slug": "linear",
    "val": {
        "token": "bearer_1",
        "companydomain": "acme-corp",
    },
}

#: A `proxy_execute` body with everything but `custom_connection_data`.
PROXY_PARAMETERS: list[dict[str, str]] = [
    {"name": "x-extra", "value": "1", "type": "header"},
    {"name": "expand", "value": "all", "type": "query"},
]

# --------------------------------------------------------------------------
# Value-shape payloads: the corpus's guard against a client that renames keys
# correctly but rewrites the *values* on the way past.
#
# The oracle never validates a request body, so whatever JSON type the caller
# wrote is the JSON type that goes out. Routing a dict body through a pydantic
# model does not preserve that for free: lax validation coerces on the way in
# and `model_dump(mode="json")` serializes on the way out, which used to turn
# `3600` into `3600.0`, `"20000"` into `20000.0` and `https://example.com` into
# `https://example.com/`. Each literal below pins one of those.
# --------------------------------------------------------------------------

#: `expires_in` is a spec `number` unioned with `string`, so it exercises all
#: three JSON spellings a caller can legitimately use for one field.
CCD_NUMBER_INT: dict[str, Any] = {
    "auth_scheme": "OAUTH2",
    "toolkit_slug": "gmail",
    "val": {"access_token": "tok_number_int", "expires_in": 3600},
}

CCD_NUMBER_FLOAT: dict[str, Any] = {
    "auth_scheme": "OAUTH2",
    "toolkit_slug": "gmail",
    "val": {"access_token": "tok_number_float", "expires_in": 3599.5},
}

CCD_NUMBER_STRING: dict[str, Any] = {
    "auth_scheme": "OAUTH2",
    "toolkit_slug": "gmail",
    "val": {"access_token": "tok_number_string", "expires_in": "3600"},
}

#: A value no member of the `custom_connection_data` union admits. The oracle
#: dispatches it — and still renames the keys around it — so a client that can
#: only alias what it can validate loses `authScheme`/`toolkitSlug` here.
CCD_UNMODELLABLE_VALUE: dict[str, Any] = {
    "auth_scheme": "OAUTH2",
    "toolkit_slug": "gmail",
    "val": {"access_token": "tok_unmodellable", "expires_in": {"unmodellable": 1}},
}

#: `workbench.auto_offload_threshold` is a bare `number` on a *different*
#: endpoint (`session.create`), so the number contract is not pinned only where
#: the aliases happen to be.
WORKBENCH_INT_THRESHOLD: dict[str, Any] = {"auto_offload_threshold": 20000}

#: `binary_body.url` used to be typed `AnyUrl`, whose pydantic round-trip
#: appends a trailing slash to an authority-only URL and lowercases the scheme
#: and host. This literal pins the trailing slash...
BINARY_BODY_URL: dict[str, Any] = {
    "url": "https://example.com",
    "content_type": "application/pdf",
}

#: ...and this one the case folding, which an already-lowercase authority cannot
#: catch. `binary_body` is also one of the two undiscriminated body unions, so
#: its member is resolved by trial validation — a URL the old `AnyUrl` grammar
#: normalized is exactly where a value rewrite and a variant choice meet.
BINARY_BODY_MIXED_CASE_URL: dict[str, Any] = {
    "url": "HTTPS://Example.COM/Upload?Token=A%2Fb",
    "content_type": "application/pdf",
}

#: The same URL contract on a second endpoint and a second field, so it is not
#: pinned only where `binary_body` happens to sit. `session.link.callback_url`
#: is a redirect target: a rewritten host or an appended path is not a cosmetic
#: difference there.
LINK_MIXED_CASE_URL: dict[str, Any] = {
    "toolkit": "github",
    "callback_url": "HTTPS://Example.COM",
    "alias": "gh",
}


# --------------------------------------------------------------------------
# The derived corpus: one case per covered operation.
#
# The hand-written cases above are *targeted* — they exist because a specific
# value shape, alias or path encoding once went wrong. They cover the sixteen
# `tool_router` operations densely and nothing else, which was the whole surface
# when they were written.
#
# At 104 operations, writing that density by hand for every route would take
# longer than it would buy, and would leave the coverage claim resting on
# whether someone remembered to add a case. These derive one minimal call per
# operation from the spec instead: path parameters substituted, every *required*
# body property, query parameter and header parameter present, and nothing else.
# The two halves spell that call in their own convention — Stainless flattens
# all of them into keyword arguments, we pass `body=`, `query=` and `headers=`
# mappings — but the values
# come from one place, so the comparison is still between two clients and not
# between two derivations.
#
# What they cannot do is invent evidence where the oracle has none: 1.43.0
# publishes 64 of them, so the rest have no differential counterpart at all.
# Those are recorded in the fixture by name rather than quietly skipped — see
# `test_wire_parity.py`.
# --------------------------------------------------------------------------

SPEC_PATH = Path(__file__).resolve().parents[2] / "spec" / "openapi.json"
COVERAGE_PATH = Path(__file__).resolve().parent.parent / "surface-coverage.json"


def snake_case(name: str) -> str:
    """A wire property name as Stainless spells it in Python.

    Both halves need the same spelling — it is the keyword the oracle takes and
    the key we hand to `body=` — so it is derived once, here.
    """
    out: list[str] = []
    for index, char in enumerate(name.replace("-", "_")):
        if char.isupper():
            previous = name[index - 1] if index else ""
            if index and (not previous.isupper() or (index + 1 < len(name) and name[index + 1].islower())):
                out.append("_")
            out.append(char.lower())
        else:
            out.append(char)
    return "".join(out).replace("__", "_")


def _deref(spec: Mapping[str, Any], schema: Mapping[str, Any]) -> dict[str, Any]:
    seen = 0
    current = dict(schema)
    while "$ref" in current and seen < 16:
        pointer = str(current["$ref"]).removeprefix("#/").split("/")
        target: Any = spec
        for step in pointer:
            target = target[step]
        current = dict(target)
        seen += 1
    return current


def sample_value(spec: Mapping[str, Any], schema: Mapping[str, Any], name: str) -> Any:
    """A deterministic value for one field, chosen by its declared shape.

    Deterministic because the fixture is committed: the same corpus must produce
    the same bytes on every capture, so nothing here may be random or
    time-dependent. Values are *not* meant to be semantically plausible — no
    request is ever dispatched to the API — only to be the right JSON type, so
    that a client which rewrites values on the way past is caught.
    """
    resolved = _deref(spec, schema)
    variants = resolved.get("oneOf") or resolved.get("anyOf") or resolved.get("allOf")
    if variants:
        return sample_value(spec, variants[0], name)
    enum = resolved.get("enum")
    if enum:
        return enum[0]
    declared = resolved.get("type")
    kind = declared[0] if isinstance(declared, list) else declared
    if kind == "array":
        items = resolved.get("items")
        return [] if items is None else [sample_value(spec, items, name)]
    if kind == "object":
        properties = resolved.get("properties") or {}
        required = resolved.get("required") or []
        return {
            snake_case(key): sample_value(spec, properties[key], key) for key in required if key in properties
        }
    if kind == "boolean":
        return True
    if kind in ("number", "integer"):
        return 1
    return f"wp_{snake_case(name)}"


INTERNAL_ACCESSOR = "_internal"


def oracle_location(parts: tuple[str, ...]) -> tuple[str, ...]:
    return parts[1:] if parts[:1] == (INTERNAL_ACCESSOR,) else parts


class DerivedCall(NamedTuple):
    """One operation's minimal call before it is flattened for both clients."""

    key: str
    #: `client.tool_router.session.retrieve` as accessor segments.
    accessor: tuple[str, ...]
    #: Path parameter spec names, in URL order.
    path_names: tuple[str, ...]
    #: Path parameter values in URL order; ``oracle_call`` flattens them.
    path_args: tuple[str, ...]
    #: Whether the operation declares a JSON request body at all. An operation
    #: that declares one but requires nothing of it still sends `{}` — on both
    #: clients — so this is not `bool(body)`.
    declares_body: bool
    #: Required body properties, plus `ORACLE_REQUIRED_BODY`, keyed as Stainless
    #: spells them.
    body: dict[str, Any]
    #: Required query parameters, same keying.
    query: dict[str, Any]
    #: Required header parameters, same keying. Both clients take them as flat
    #: keyword arguments like every other request field. Three operations declare one
    #: (``cli.create_codact_failure`` and the two ``org.consumer`` routes); the
    #: pinned oracle publishes none of the three, so no fixture case carries a
    #: header parameter and adding them here leaves the committed capture
    #: untouched. They still exercise the owned-only live surface.
    headers: dict[str, Any]

    @property
    def oracle_accessor(self) -> tuple[str, ...]:
        """The accessor the pinned 1.43.0 client spells: ``accessor`` without the
        ``_internal`` root the spec's ``x-internal`` operations moved under."""
        return oracle_location(self.accessor)


#: Where Stainless's flatten collides a body property with a query parameter of
#: the same name, it prefixes both. The owned client preserves those names too.
#: One operation needs them.
ORACLE_KWARG_PREFIXES: Mapping[str, Mapping[str, str]] = {
    "post /api/v3.1/connected_accounts/{nanoid}/refresh": {
        "body.redirect_url": "body_redirect_url",
        "query.redirect_url": "query_redirect_url",
    },
}

#: Where two *wire* properties of one body normalize to the same Python name,
#: the oracle numbers them and neither number is the wire name.
#:
#: `trigger_instances.upsert` declares both `triggerConfig` and `trigger_config`,
#: and both become `trigger_config` in Python. The oracle resolves the collision
#: by position — `body_trigger_config_1` reaches the wire as `trigger_config`,
#: `body_trigger_config_2` as `triggerConfig` — so a caller cannot name either
#: one by its wire spelling. Ours keeps them apart through the generated request
#: model's aliases instead, which is why only the oracle half needs this. The
#: owned client's numbered keywords must still mean what the oracle's do — the
#: corpus never sets one, which is how they drifted apart once — so that is
#: pinned by the `numbered ... keyword` cases in `tests/test_wire_parity.py`.
#:
#: Keyed by the **wire** name rather than the snake_case one, because that is the
#: distinction being preserved: snake_case erases it, which is the whole problem.
#:
#: Consumed by `parity_driver.py` and not by `oracle_call`: the derived corpus
#: sends only the properties the spec marks required, and neither of these is.
#: The live scenarios send optional ones, which is where the collision surfaces.
ORACLE_KWARG_RENAMES: Mapping[str, Mapping[str, str]] = {
    "post /api/v3.1/trigger_instances/{slug}/upsert": {
        "trigger_config": "body_trigger_config_1",
        "triggerConfig": "body_trigger_config_2",
        "connectedAuthId": "connected_auth_id",
    },
}

#: Body properties the pinned oracle still requires but the current spec has
#: since made optional, keyed by wire name.
#:
#: The corpus samples what the *current* spec requires, while 1.43.0's
#: signatures are frozen. When upstream relaxes a required property, the derived
#: call stops passing it, the oracle raises `TypeError` before it dispatches, and
#: the capture records nothing. Sampling these alongside the required ones keeps
#: the call one the oracle accepts. Both halves derive from here, so the owned
#: client sends the same body it is compared against.
#:
#: `trigger_instances.manage.update` made `status` optional in September 2026, so
#: an update can change only `egress_url` or `user_id`.
ORACLE_REQUIRED_BODY: Mapping[str, tuple[str, ...]] = {
    "patch /api/v3.1/trigger_instances/manage/{triggerId}": ("status",),
}


@cache
def derived_calls() -> tuple[DerivedCall, ...]:
    """One minimal call per covered operation, in `surface-coverage.json` order.

    Memoized because deriving the corpus parses the 4.5 MB spec and walks every
    operation's schema, while `test_wire_parity.py` alone asks for it five times
    — three of those during collection. Both inputs are committed files that
    cannot change mid-run, so one derivation serves all callers.
    """
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))

    calls: list[DerivedCall] = []
    for entry in coverage["operations"]:
        method, path = str(entry["key"]).split(" ", 1)
        operation = spec["paths"][path][method]

        parameters = [_deref(spec, param) for param in operation.get("parameters", [])]
        path_names = tuple(
            segment[1:-1] for segment in path.split("/") if segment.startswith("{") and segment.endswith("}")
        )
        path_args = tuple(f"wp_{name}" for name in path_names)
        query = {
            snake_case(param["name"]): sample_value(spec, param.get("schema") or {}, param["name"])
            for param in parameters
            if param.get("in") == "query" and param.get("required") is True
        }
        headers = {
            snake_case(param["name"]): sample_value(spec, param.get("schema") or {}, param["name"])
            for param in parameters
            if param.get("in") == "header" and param.get("required") is True
        }

        content = (operation.get("requestBody") or {}).get("content") or {}
        schema = content.get("application/json", {}).get("schema")
        # `sample_value` resolves a `oneOf` body to its first variant, which is
        # what makes `auth_configs.update` — whose `type` is required on every
        # variant and on none of the composite — produce a call the oracle's
        # signature accepts.
        sampled = {} if schema is None else sample_value(spec, schema, "body")
        body = sampled if isinstance(sampled, dict) else {}
        properties = {} if schema is None else _deref(spec, schema).get("properties") or {}
        body.update(
            {
                snake_case(name): sample_value(spec, properties[name], name)
                for name in ORACLE_REQUIRED_BODY.get(entry["key"], ())
            }
        )

        calls.append(
            DerivedCall(
                key=entry["key"],
                accessor=tuple(entry["accessor"]),
                path_names=path_names,
                path_args=path_args,
                declares_body=schema is not None,
                body=body,
                query=query,
                headers=headers,
            )
        )
    return tuple(calls)


def oracle_call(call: DerivedCall) -> tuple[tuple[str, ...], dict[str, Any]]:
    """The derived call as the Stainless client takes it: `(positional, kwargs)`.

    Two spelling rules of the oracle's, neither of which is ours. **Only the
    last path parameter is positional** — the leading ones are keyword arguments
    named after the spec parameter (`files.list(mount_id, session_id=...)`),
    which is the deep-subpath layout showing through. And body, query, declared
    header parameters and those leading path parameters all land in one flat
    keyword namespace, so a body property colliding with a query parameter has
    to be prefixed (`ORACLE_KWARG_PREFIXES`).

    The owned client now accepts this same shape, so this is also the shared
    invocation used by the parity driver and all-operation wire tests.
    """
    prefixes = ORACLE_KWARG_PREFIXES.get(call.key, {})
    leading = {
        snake_case(name): value for name, value in zip(call.path_names[:-1], call.path_args[:-1], strict=True)
    }
    return (
        call.path_args[-1:],
        {
            **leading,
            **{prefixes.get(f"body.{name}", name): value for name, value in call.body.items()},
            **{prefixes.get(f"query.{name}", name): value for name, value in call.query.items()},
            **call.headers,
        },
    )


def resolve_accessor(client: Any, accessor: tuple[str, ...]) -> Any:
    """The bound method at `accessor`, or `None` when the client lacks it."""
    target = client
    for segment in accessor:
        target = getattr(target, segment, None)
        if target is None:
            return None
    return target
