"""Request-wire parity against the pinned Stainless oracle.

The Python counterpart of ``test/unit/differential-wire.test.ts``: for every
``tool_router`` method, the same logical call goes out over the wire from our
client and from the frozen Stainless ``composio-client`` 1.43.0 — same method,
same percent-encoded path, same query string, same JSON body, same headers,
modulo ``x-stainless-*`` / ``user-agent`` and transport artifacts.

The oracle cannot be a dev dependency (both distributions import as
``composio_client``), so its side of the comparison is a committed golden capture
produced by ``scripts/capture_stainless_oracle.py``; see ``scripts/wire_corpus.py``
for the split and the regeneration command. Stainless's actual behavior is the
oracle here — never edit the fixture to make a case pass.

The derived all-operation cases use one Stainless invocation for both clients.
Focused cases also retain the aggregate request form as a compatibility check.
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from scripts.wire_corpus import (
    API_KEY,
    BASE_URL,
    BINARY_BODY_MIXED_CASE_URL,
    BINARY_BODY_URL,
    CCD_API_KEY_SNAKE,
    CCD_BEARER_TOKEN_SNAKE,
    CCD_NUMBER_FLOAT,
    CCD_NUMBER_INT,
    CCD_NUMBER_STRING,
    CCD_OAUTH1_SNAKE,
    CCD_OAUTH2_SNAKE,
    CCD_UNMODELLABLE_VALUE,
    ENCODED_SESSION_ID,
    FIXTURE_PATH,
    LINK_MIXED_CASE_URL,
    MOUNT_ID,
    ORACLE_REQUIRED_BODY,
    ORACLE_VERSION,
    PROXY_PARAMETERS,
    SESSION_ID,
    SPEC_PATH,
    SUBDELIMS_SESSION_ID,
    WORKBENCH_INT_THRESHOLD,
    Case,
    derived_calls,
    oracle_call,
    resolve_accessor,
    snake_case,
)
from wire_corpus import capture as _capture

from composio_client import Composio, ProjectAuth, RequestOptions
from composio_client._models import (
    FileListQuery,
    SessionCreateBody,
    SessionLinkBody,
    SessionProxyExecuteBody,
)


def capture(composio_cls: Any, case: Case) -> dict[str, Any]:
    """The corpus capture with the owned client's credential spelling: the
    oracle takes ``api_key=``, this client ``auth=ProjectAuth(key)``."""
    return _capture(composio_cls, case, credentials={"auth": ProjectAuth(API_KEY)})


_ORACLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
_ORACLE_CASES: dict[str, dict[str, Any]] = {case["id"]: case for case in _ORACLE["cases"]}

#: The complete non-pythonic wire-name inventory of the tool_router surface. Every
#: entry lives under `custom_connection_data` on `session.proxy_execute`; the
#: first two are on the variant itself, the rest on its `val`.
_WIRE_ALIASES = {
    "auth_scheme": "authScheme",
    "toolkit_slug": "toolkitSlug",
    "your_domain": "your-domain",
    "companydomain": "COMPANYDOMAIN",
    "instance_endpoint": "instanceEndpoint",
    "instance_name": "instanceName",
    "redirect_url": "redirectUrl",
}

# The `custom_connection_data` payloads keyed by wire name — what the API is
# specified to receive, and what the generated pydantic variants validate.
CCD_OAUTH2_ALIASED: dict[str, Any] = {
    "authScheme": "OAUTH2",
    "toolkitSlug": "gmail",
    "val": {
        "access_token": "tok_oauth2",
        "refresh_token": "refresh_oauth2",
        "your-domain": "acme.example.com",
        "COMPANYDOMAIN": "acme-corp",
        "instanceEndpoint": "https://acme.service-now.com",
        "instanceName": "acme-prod",
        "scope": ["read", "write"],
    },
}

CCD_OAUTH1_ALIASED: dict[str, Any] = {
    "authScheme": "OAUTH1",
    "toolkitSlug": "trello",
    "val": {
        "oauth_token": "ot_1",
        "oauth_token_secret": "ots_1",
        "redirectUrl": "https://example.com/callback",
        "your-domain": "acme.example.com",
    },
}

CCD_API_KEY_ALIASED: dict[str, Any] = {
    "authScheme": "API_KEY",
    "toolkitSlug": "notion",
    "val": {
        "generic_api_key": "sk_live_1",
        "instanceName": "acme-prod",
    },
}

CCD_BEARER_TOKEN_ALIASED: dict[str, Any] = {
    "authScheme": "BEARER_TOKEN",
    "toolkitSlug": "linear",
    "val": {
        "token": "bearer_1",
        "COMPANYDOMAIN": "acme-corp",
    },
}

CCD_NUMBER_INT_ALIASED: dict[str, Any] = {
    "authScheme": "OAUTH2",
    "toolkitSlug": "gmail",
    "val": {"access_token": "tok_number_int", "expires_in": 3600},
}

CCD_NUMBER_FLOAT_ALIASED: dict[str, Any] = {
    "authScheme": "OAUTH2",
    "toolkitSlug": "gmail",
    "val": {"access_token": "tok_number_float", "expires_in": 3599.5},
}

_CCD_PAIRS = [
    (CCD_OAUTH2_SNAKE, CCD_OAUTH2_ALIASED),
    (CCD_OAUTH1_SNAKE, CCD_OAUTH1_ALIASED),
    (CCD_API_KEY_SNAKE, CCD_API_KEY_ALIASED),
    (CCD_BEARER_TOKEN_SNAKE, CCD_BEARER_TOKEN_ALIASED),
    (CCD_NUMBER_INT, CCD_NUMBER_INT_ALIASED),
    (CCD_NUMBER_FLOAT, CCD_NUMBER_FLOAT_ALIASED),
]


def _proxy_body(
    endpoint: str,
    method: str,
    toolkit_slug: str,
    ccd: dict[str, Any] | None = None,
    binary_body: dict[str, Any] | None = None,
) -> Any:
    """A `proxy_execute` body as the generated pydantic model.

    Built through `model_validate` on the wire-name keys, which is the one
    construction path that behaves identically whether or not the generated
    variants carry `populate_by_name`.
    """
    body: dict[str, Any] = {"endpoint": endpoint, "method": method, "toolkit_slug": toolkit_slug}
    if ccd is not None:
        body["custom_connection_data"] = ccd
    if binary_body is not None:
        body["binary_body"] = binary_body
    return SessionProxyExecuteBody.model_validate(body)


CASES: list[Case] = [
    # ---- session (12 methods) ----
    Case(
        "session.create",
        lambda c: c.tool_router.session.create(
            {
                "user_id": "wire@example.com",
                "toolkits": {"enable": ["github", "slack"]},
                "manage_connections": {"enable": True},
                "auth_configs": {"github": "ac_1"},
                "tags": {"include": ["prod"]},
            }
        ),
    ),
    Case(
        "session.create.minimal",
        lambda c: c.tool_router.session.create({"user_id": "wire@example.com"}),
    ),
    Case(
        "session.create.number-workbench.dict",
        lambda c: c.tool_router.session.create(
            {"user_id": "wire@example.com", "workbench": WORKBENCH_INT_THRESHOLD}
        ),
        oracle="session.create.number-workbench",
    ),
    Case(
        "session.create.number-workbench.model",
        lambda c: c.tool_router.session.create(
            SessionCreateBody.model_validate(
                {"user_id": "wire@example.com", "workbench": WORKBENCH_INT_THRESHOLD}
            )
        ),
        oracle="session.create.number-workbench",
    ),
    Case("session.retrieve", lambda c: c.tool_router.session.retrieve(SESSION_ID)),
    Case("session.retrieve.encoded-path", lambda c: c.tool_router.session.retrieve(ENCODED_SESSION_ID)),
    Case("session.retrieve.subdelims-path", lambda c: c.tool_router.session.retrieve(SUBDELIMS_SESSION_ID)),
    Case(
        "session.retrieve.extra-headers",
        lambda c: c.tool_router.session.retrieve(
            SESSION_ID,
            request_options=RequestOptions(headers={"x-team": "per-request-wins", "x-trace": "abc"}),
        ),
        client_options={"default_headers": {"x-team": "overridden-by-default"}},
    ),
    Case("session.attach.default-body", lambda c: c.tool_router.session.attach(SESSION_ID)),
    Case(
        "session.attach.body",
        lambda c: c.tool_router.session.attach(SESSION_ID, {"experimental": {"skip_cache": True}}),
    ),
    Case("session.config_history.no-query", lambda c: c.tool_router.session.config_history(SESSION_ID)),
    Case(
        "session.config_history.query",
        lambda c: c.tool_router.session.config_history(SESSION_ID, query={"cursor": "c1", "limit": 5}),
    ),
    Case(
        "session.execute",
        lambda c: c.tool_router.session.execute(
            SESSION_ID,
            {
                "tool_slug": "GITHUB_GET_REPO",
                "arguments": {"owner": "composiohq", "repo": "composio"},
                "enable_auto_workbench_offload": False,
            },
        ),
    ),
    Case(
        "session.execute_meta",
        lambda c: c.tool_router.session.execute_meta(
            SESSION_ID,
            {
                "slug": "COMPOSIO_SEARCH_TOOLS",
                "arguments": {"queries": [{"use_case": "send a message"}]},
            },
        ),
    ),
    Case(
        "session.link",
        lambda c: c.tool_router.session.link(
            SESSION_ID,
            {"toolkit": "github", "callback_url": "https://example.com/cb", "alias": "gh"},
        ),
    ),
    Case(
        "session.link.mixed-case-url.dict",
        lambda c: c.tool_router.session.link(SESSION_ID, LINK_MIXED_CASE_URL),
        oracle="session.link.mixed-case-url",
    ),
    Case(
        "session.link.mixed-case-url.model",
        lambda c: c.tool_router.session.link(SESSION_ID, SessionLinkBody.model_validate(LINK_MIXED_CASE_URL)),
        oracle="session.link.mixed-case-url",
    ),
    Case("session.patch.default-body", lambda c: c.tool_router.session.patch(SESSION_ID)),
    Case(
        "session.patch.body",
        lambda c: c.tool_router.session.patch(SESSION_ID, {"manage_connections": {"enable": False}}),
    ),
    Case(
        "session.patch.explicit-null",
        lambda c: c.tool_router.session.patch(SESSION_ID, {"multi_account": None}),
    ),
    Case(
        "session.proxy_execute",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/repos/composiohq/composio",
                "method": "GET",
                "toolkit_slug": "github",
                "parameters": PROXY_PARAMETERS,
            },
        ),
    ),
    Case(
        "session.proxy_execute.body",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "POST",
                "toolkit_slug": "slack",
                "body": {"channel": "#general", "text": "hi"},
            },
        ),
    ),
    # ---- the aliased corner: `custom_connection_data`, dict-typed and
    # model-typed, against one oracle capture each ----
    Case(
        "session.proxy_execute.ccd-oauth2.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "GET",
                "toolkit_slug": "gmail",
                "custom_connection_data": CCD_OAUTH2_SNAKE,
            },
        ),
        oracle="session.proxy_execute.ccd-oauth2",
    ),
    Case(
        "session.proxy_execute.ccd-oauth2.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/messages", "GET", "gmail", CCD_OAUTH2_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-oauth2",
    ),
    Case(
        "session.proxy_execute.ccd-oauth1.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/1/members/me",
                "method": "GET",
                "toolkit_slug": "trello",
                "custom_connection_data": CCD_OAUTH1_SNAKE,
            },
        ),
        oracle="session.proxy_execute.ccd-oauth1",
    ),
    Case(
        "session.proxy_execute.ccd-oauth1.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/1/members/me", "GET", "trello", CCD_OAUTH1_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-oauth1",
    ),
    Case(
        "session.proxy_execute.ccd-api-key.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/v1/pages",
                "method": "GET",
                "toolkit_slug": "notion",
                "custom_connection_data": CCD_API_KEY_SNAKE,
            },
        ),
        oracle="session.proxy_execute.ccd-api-key",
    ),
    Case(
        "session.proxy_execute.ccd-api-key.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/v1/pages", "GET", "notion", CCD_API_KEY_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-api-key",
    ),
    Case(
        "session.proxy_execute.ccd-bearer-token.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/graphql",
                "method": "POST",
                "toolkit_slug": "linear",
                "custom_connection_data": CCD_BEARER_TOKEN_SNAKE,
            },
        ),
        oracle="session.proxy_execute.ccd-bearer-token",
    ),
    Case(
        "session.proxy_execute.ccd-bearer-token.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/graphql", "POST", "linear", CCD_BEARER_TOKEN_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-bearer-token",
    ),
    # ---- value shapes: neither route re-types a value. Each case pins a JSON
    # type or spelling that a validate-and-dump round-trip rewrote, and the
    # number/URL ones run twice — once as a dict, once as the generated model —
    # because the two routes are separately capable of rewriting it. The dict
    # route was fixed in the kernel (`_aliasing`); the model route only in the
    # generated annotations (`packages/codegen`'s `python-postgen`) ----
    Case(
        "session.proxy_execute.ccd-number-int.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "GET",
                "toolkit_slug": "gmail",
                "custom_connection_data": CCD_NUMBER_INT,
            },
        ),
        oracle="session.proxy_execute.ccd-number-int",
    ),
    Case(
        "session.proxy_execute.ccd-number-int.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/messages", "GET", "gmail", ccd=CCD_NUMBER_INT_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-number-int",
    ),
    Case(
        "session.proxy_execute.ccd-number-float.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "GET",
                "toolkit_slug": "gmail",
                "custom_connection_data": CCD_NUMBER_FLOAT,
            },
        ),
        oracle="session.proxy_execute.ccd-number-float",
    ),
    Case(
        "session.proxy_execute.ccd-number-float.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/messages", "GET", "gmail", ccd=CCD_NUMBER_FLOAT_ALIASED)
        ),
        oracle="session.proxy_execute.ccd-number-float",
    ),
    Case(
        "session.proxy_execute.ccd-number-string",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "GET",
                "toolkit_slug": "gmail",
                "custom_connection_data": CCD_NUMBER_STRING,
            },
        ),
    ),
    Case(
        "session.proxy_execute.ccd-unmodellable-value",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/messages",
                "method": "GET",
                "toolkit_slug": "gmail",
                "custom_connection_data": CCD_UNMODELLABLE_VALUE,
            },
        ),
    ),
    Case(
        "session.proxy_execute.binary-body-url.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/upload",
                "method": "POST",
                "toolkit_slug": "gmail",
                "binary_body": BINARY_BODY_URL,
            },
        ),
        oracle="session.proxy_execute.binary-body-url",
    ),
    Case(
        "session.proxy_execute.binary-body-url.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/upload", "POST", "gmail", binary_body=BINARY_BODY_URL)
        ),
        oracle="session.proxy_execute.binary-body-url",
    ),
    Case(
        "session.proxy_execute.binary-body-mixed-case-url.dict",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            {
                "endpoint": "/upload",
                "method": "POST",
                "toolkit_slug": "gmail",
                "binary_body": BINARY_BODY_MIXED_CASE_URL,
            },
        ),
        oracle="session.proxy_execute.binary-body-mixed-case-url",
    ),
    Case(
        "session.proxy_execute.binary-body-mixed-case-url.model",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID, _proxy_body("/upload", "POST", "gmail", binary_body=BINARY_BODY_MIXED_CASE_URL)
        ),
        oracle="session.proxy_execute.binary-body-mixed-case-url",
    ),
    Case(
        "session.search",
        lambda c: c.tool_router.session.search(
            SESSION_ID,
            {
                "queries": [{"use_case": "send a slack message", "known_fields": "channel"}],
                "model": "gpt-4o",
            },
        ),
    ),
    Case("session.toolkits.no-query", lambda c: c.tool_router.session.toolkits(SESSION_ID)),
    Case(
        "session.toolkits.array-query",
        lambda c: c.tool_router.session.toolkits(
            SESSION_ID,
            query={"toolkits": ["github", "slack"], "is_connected": True, "limit": 5, "search": "git"},
        ),
    ),
    Case("session.tools.no-query", lambda c: c.tool_router.session.tools(SESSION_ID)),
    Case(
        "session.tools.query",
        lambda c: c.tool_router.session.tools(SESSION_ID, query={"cursor": "c2", "limit": 3}),
    ),
    # ---- session.files (4 methods): both path params positional, in URL order ----
    Case("files.list.no-query", lambda c: c.tool_router.session.files.list(SESSION_ID, MOUNT_ID)),
    # `limit` is a spec `number` on the *query* side, which serializes through
    # `str(...)`: a model-typed query used to send `limit=10.0`.
    Case(
        "files.list.query.dict",
        lambda c: c.tool_router.session.files.list(
            SESSION_ID,
            MOUNT_ID,
            query={"cursor": "n", "limit": 10, "mount_relative_prefix": "data/"},
        ),
        oracle="files.list.query",
    ),
    Case(
        "files.list.query.model",
        lambda c: c.tool_router.session.files.list(
            SESSION_ID,
            MOUNT_ID,
            query=FileListQuery.model_validate(
                {"cursor": "n", "limit": 10, "mount_relative_prefix": "data/"}
            ),
        ),
        oracle="files.list.query",
    ),
    Case(
        "files.delete",
        lambda c: c.tool_router.session.files.delete(
            SESSION_ID, MOUNT_ID, {"mount_relative_path": "report.pdf"}
        ),
    ),
    Case(
        "files.create_download_url",
        lambda c: c.tool_router.session.files.create_download_url(
            SESSION_ID, MOUNT_ID, {"mount_relative_path": "report.pdf"}
        ),
    ),
    Case(
        "files.create_upload_url",
        lambda c: c.tool_router.session.files.create_upload_url(
            SESSION_ID, MOUNT_ID, {"mount_relative_path": "data/output.csv", "mimetype": "text/csv"}
        ),
    ),
]

#: Cases the oracle proves we get wrong today. Each is a strict xfail, so fixing
#: the underlying bug turns the entry into a failure and forces its removal.
#: Empty: every recorded divergence has been fixed.
#: The oracle puts ``content-type: application/json`` on a request that carries
#: no body at all — every bodyless DELETE, and the one PATCH whose wire sides are
#: both path parameters. We do not, and that is deliberate rather than an
#: oversight: the TypeScript client is this kernel's golden reference and
#: ``src/compat/request.ts`` states the rule outright — "operations with no body
#: at all (GET/DELETE) send neither body nor content-type". Changing it here
#: would break parity with the artifact this package is a drop-in for, to match
#: a header that describes a payload that does not exist.
#:
#: Derived from the capture rather than listed by id, so it stays true as the
#: corpus grows, and `strict=True` below means a case that stops diverging fails
#: instead of quietly passing.
_KNOWN_DIVERGENCES: dict[str, str] = {
    case["id"]: "oracle sets content-type on a bodyless request; the TS golden reference does not"
    for case in _ORACLE["cases"]
    if case["body"] is None and "content-type" in case["headers"]
}


def _query_pairs(raw: str) -> list[str]:
    """The raw, still-percent-encoded ``key=value`` pairs, order-normalized.

    Parameter *order* is the one carve-out on the query side: Stainless builds
    its query mapping itself (alphabetical by generated field), while our
    convention takes the caller's mapping and preserves its insertion order. The
    pairs and their encoding are the contract; their order is not.
    """
    return sorted(raw.split("&")) if raw else []


# --------------------------------------------------------------------------
# The derived cases: one shared Stainless invocation per covered operation.
# --------------------------------------------------------------------------


def invoke_stainless(client: Any, call: Any) -> Any:
    positional, keywords = oracle_call(call)
    return resolve_accessor(client, call.accessor)(*positional, **keywords)


DERIVED_BY_ACCESSOR: dict[tuple[str, ...], Any] = {
    call.accessor: (lambda client, call=call: invoke_stainless(client, call)) for call in derived_calls()
}

#: The operations the oracle does not publish. Every derived case still runs —
#: our client must dispatch it — but there is no recorded request to diff it
#: against, so it is compared to the spec's own method and path instead.
NO_ORACLE: frozenset[str] = frozenset(_ORACLE["absent"])

CASES += [
    Case(f"derived.{'.'.join(call.oracle_accessor)}", DERIVED_BY_ACCESSOR[call.accessor])
    for call in derived_calls()
    if ".".join(call.oracle_accessor) not in NO_ORACLE
]


def _params() -> list[Any]:
    params = []
    for case in CASES:
        reason = _KNOWN_DIVERGENCES.get(case.id)
        marks = [pytest.mark.xfail(strict=True, reason=reason)] if reason else []
        params.append(pytest.param(case, marks=marks, id=case.id))
    return params


@pytest.mark.parametrize("call", [pytest.param(call, id=".".join(call.accessor)) for call in derived_calls()])
def test_every_covered_operation_dispatches_its_declared_request(call: Any) -> None:
    """The floor under all 116, oracle or not: the accessor exists, dispatches
    exactly one request, and puts it on the method and path the spec declares
    with every path parameter substituted.

    For the 64 the oracle publishes this is subsumed by the differential case
    below. For the other 52 it is the whole of the evidence, which is why it
    asserts against `spec/openapi.json` rather than against our own output.
    """
    case = Case(f"derived.{'.'.join(call.accessor)}", DERIVED_BY_ACCESSOR[call.accessor])
    actual = capture(Composio, case)

    method, template = call.key.split(" ", 1)
    expected_path = template
    for name, value in zip(call.path_names, call.path_args, strict=True):
        expected_path = expected_path.replace("{" + name + "}", value)

    assert actual["method"] == method.upper()
    assert actual["path"] == expected_path
    assert "{" not in actual["path"]


def test_the_oracle_absence_list_is_the_one_this_package_outgrew() -> None:
    """52 of the 116 have no differential counterpart, because 1.43.0 publishes
    64. Named rather than skipped: an operation with no oracle must read as "no
    evidence available here", never as one more quietly missing case — and a
    *shrinking* list would mean the pin moved without the fixture being
    reviewed."""
    covered = {".".join(call.oracle_accessor) for call in derived_calls()}

    assert NO_ORACLE <= covered
    assert len(NO_ORACLE) == 52
    assert len(covered) == 116
    assert "webhook_subscriptions.create" in NO_ORACLE
    assert "org.owner.project.create" in NO_ORACLE
    assert "tool_router.session.delete" in NO_ORACLE
    assert "custom.create_toolkit" in NO_ORACLE
    assert "custom.update_toolkits" in NO_ORACLE
    assert "tool_router.session.create" not in NO_ORACLE


def test_every_oracle_required_body_property_is_one_the_spec_relaxed() -> None:
    """``ORACLE_REQUIRED_BODY`` exists only for properties the frozen oracle
    still requires and the current spec does not. One the spec requires again
    would be inert, and each must reach the request the fixture recorded."""
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    by_key = {call.key: call for call in derived_calls()}
    for key, names in ORACLE_REQUIRED_BODY.items():
        method, path = key.split(" ", 1)
        schema = spec["paths"][path][method]["requestBody"]["content"]["application/json"]["schema"]
        recorded = _ORACLE_CASES[f"derived.{'.'.join(by_key[key].oracle_accessor)}"]["body"]

        assert set(names) <= set(schema["properties"]), key
        assert not set(names) & set(schema.get("required", [])), key
        assert {snake_case(name) for name in names} <= set(recorded), key


@pytest.mark.parametrize("case", _params())
def test_request_wire_matches_stainless_oracle(case: Case) -> None:
    expected = _ORACLE_CASES[case.oracle_id]
    # guard against a vacuous pass: the oracle capture must carry a real request
    assert expected["headers"]["accept"] == "application/json"
    assert expected["headers"]["x-api-key"]

    actual = capture(Composio, case)
    assert actual["method"] == expected["method"]
    assert actual["path"] == expected["path"]
    assert _query_pairs(actual["query"]) == _query_pairs(expected["query"])
    assert actual["body"] == expected["body"]
    assert actual["headers"] == expected["headers"]


def test_oracle_fixture_is_the_pinned_version() -> None:
    assert _ORACLE["oracle"]["version"] == ORACLE_VERSION
    assert _ORACLE["cases"], "the oracle capture is empty"


def test_oracle_capture_is_not_vacuous() -> None:
    """Every recorded request must be a real, fully-formed API call, and the
    corpus as a whole must actually exercise bodies, queries and headers —
    otherwise the per-case comparisons could agree on nothing."""
    for case in _ORACLE["cases"]:
        assert case["headers"]["accept"] == "application/json", case["id"]
        assert case["headers"]["x-api-key"] == API_KEY, case["id"]
        assert case["path"].startswith("/api/v3.1/"), case["id"]
        # A GET never carries one; a body always announces its type.
        assert case["method"] != "GET" or case["body"] is None, case["id"]
        assert case["body"] is None or case["headers"]["content-type"] == "application/json", case["id"]

    # A derived case carries a body exactly when the spec declares one for that
    # operation — the corpus's own claim about what it sends.
    declared = {f"derived.{'.'.join(call.oracle_accessor)}": call.declares_body for call in derived_calls()}
    for case in _ORACLE["cases"]:
        expected = declared.get(case["id"])
        assert expected is None or (case["body"] is not None) == expected, case["id"]

    assert any(case["body"] for case in _ORACLE["cases"])
    assert any(case["query"] for case in _ORACLE["cases"])
    assert any("x-team" in case["headers"] for case in _ORACLE["cases"])
    # The corpus reaches past `tool_router`, which is what U5 widened it for.
    assert any(not case["path"].startswith("/api/v3.1/tool_router") for case in _ORACLE["cases"])


#: Oracle entries no `Case` in `CASES` points at, because the parity assertion
#: for them is written out longhand rather than driven by the table — the
#: body+query collision is the one shape our client cannot express in the
#: oracle's spelling, so it cannot share a `Case`.
_LONGHAND_ORACLE_CASES = {"connected_accounts.refresh.body-and-query"}


def test_every_oracle_case_is_exercised() -> None:
    assert {case.oracle_id for case in CASES} | _LONGHAND_ORACLE_CASES == set(_ORACLE_CASES)


def test_all_sixteen_tool_router_methods_are_densely_covered() -> None:
    """The hand-written half. These sixteen carry the *targeted* cases — value
    shapes, aliases, path encodings — that the derived corpus does not attempt
    for 116 operations, so they are asserted to still be there."""
    expected = {
        "session.create",
        "session.retrieve",
        "session.attach",
        "session.config_history",
        "session.execute",
        "session.execute_meta",
        "session.link",
        "session.patch",
        "session.proxy_execute",
        "session.search",
        "session.toolkits",
        "session.tools",
        "files.list",
        "files.delete",
        "files.create_download_url",
        "files.create_upload_url",
    }
    handwritten = {case.id for case in CASES if not case.id.startswith("derived.")}
    assert {".".join(case_id.split(".")[:2]) for case_id in handwritten} == expected


def test_oracle_bodies_carry_the_expected_aliased_wire_names() -> None:
    """The oracle really does rename the aliased fields — without this the
    `custom_connection_data` cases could pass for the wrong reason."""
    body = _ORACLE_CASES["session.proxy_execute.ccd-oauth2"]["body"]
    ccd = body["custom_connection_data"]
    assert ccd["authScheme"] == "OAUTH2"
    assert ccd["toolkitSlug"] == "gmail"
    assert ccd["val"]["your-domain"] == "acme.example.com"
    assert ccd["val"]["COMPANYDOMAIN"] == "acme-corp"
    assert ccd["val"]["instanceEndpoint"] == "https://acme.service-now.com"
    assert ccd["val"]["instanceName"] == "acme-prod"
    oauth1 = _ORACLE_CASES["session.proxy_execute.ccd-oauth1"]["body"]
    assert oauth1["custom_connection_data"]["val"]["redirectUrl"] == "https://example.com/callback"


def test_oracle_bodies_carry_the_callers_json_types_verbatim() -> None:
    """The value-shape cases are only meaningful if the oracle really does send
    the caller's JSON types through untouched — otherwise they could pass by
    agreeing on a rewrite rather than on the absence of one.

    ``json.loads`` distinguishes ``3600`` from ``3600.0`` as ``int`` vs
    ``float``, so the ``type(...) is`` checks are the real assertion here.
    """

    def expires_in(case_id: str) -> Any:
        return _ORACLE_CASES[case_id]["body"]["custom_connection_data"]["val"]["expires_in"]

    integer = expires_in("session.proxy_execute.ccd-number-int")
    assert integer == 3600
    assert type(integer) is int  # not 3600.0

    real = expires_in("session.proxy_execute.ccd-number-float")
    assert real == 3599.5
    assert type(real) is float

    assert expires_in("session.proxy_execute.ccd-number-string") == "3600"
    # a value no member of the union admits, alongside keys that are still renamed
    unmodellable = _ORACLE_CASES["session.proxy_execute.ccd-unmodellable-value"]["body"]
    assert unmodellable["custom_connection_data"]["authScheme"] == "OAUTH2"
    assert unmodellable["custom_connection_data"]["toolkitSlug"] == "gmail"
    assert unmodellable["custom_connection_data"]["val"]["expires_in"] == {"unmodellable": 1}

    threshold = _ORACLE_CASES["session.create.number-workbench"]["body"]["workbench"][
        "auto_offload_threshold"
    ]
    assert threshold == 20000
    assert type(threshold) is int

    # an authority-only URL: not normalized to a trailing slash
    assert (
        _ORACLE_CASES["session.proxy_execute.binary-body-url"]["body"]["binary_body"]["url"]
        == "https://example.com"
    )


def _rekey(value: Any) -> Any:
    if isinstance(value, dict):
        return {_WIRE_ALIASES.get(k, k): _rekey(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_rekey(item) for item in value]
    return value


@pytest.mark.parametrize(("snake", "aliased"), _CCD_PAIRS)
def test_aliased_payloads_are_the_snake_payloads_rekeyed(
    snake: dict[str, Any], aliased: dict[str, Any]
) -> None:
    """The dict-typed and model-typed cases must be the *same* payload, differing
    only by the documented wire-name inventory."""
    assert _rekey(snake) == aliased


# --------------------------------------------------------------------------
# The two shapes where Python's calling convention diverges from TypeScript's
# on purpose (KTD5), asserted on the wire rather than left implicit.
# --------------------------------------------------------------------------


def test_refresh_puts_each_redirect_url_on_its_own_wire_side() -> None:
    """`connected_accounts.refresh` declares `redirect_url` twice — once in the
    body and once in the query.

    TypeScript resolves that by flattening both into one params object with
    `query_redirect_url` / `body_redirect_url` collision prefixes, and the
    Stainless *Python* oracle does the same. Ours does not need to: `body` and
    `query` are separate arguments, so the collision never arises and neither
    prefix appears in a Python signature. The wire is where the two conventions
    have to agree, and this is that agreement.
    """
    actual = capture(
        Composio,
        Case(
            "refresh.body-and-query",
            lambda c: c.connected_accounts.refresh(
                "ca_wire_parity",
                body={
                    "redirect_url": "https://example.com/after-body",
                    "validate_credentials": True,
                },
                query={"redirect_url": "https://example.com/after-query"},
            ),
        ),
    )
    expected = _ORACLE_CASES["connected_accounts.refresh.body-and-query"]

    assert actual["method"] == expected["method"] == "POST"
    assert actual["path"] == expected["path"]
    assert _query_pairs(actual["query"]) == _query_pairs(expected["query"])
    assert actual["body"] == expected["body"]
    # Neither prefix reaches the wire from either client.
    assert actual["body"] == {
        "redirect_url": "https://example.com/after-body",
        "validate_credentials": True,
    }
    assert "query_redirect_url" not in actual["query"]
    assert "body_redirect_url" not in json.dumps(actual["body"])


def test_upsert_parses_the_pinned_2xx_and_tolerates_the_others() -> None:
    """`trigger_instances.upsert` declares 200, 201 and 204. The published
    client is typed by one of them — 200, pinned in the nesting map's
    `responseStatusOverrides` and shared with TypeScript through
    `successStatus` — but the *runtime* must not fail on the other two, which
    the server is equally entitled to send.
    """
    import httpx

    from composio_client.types.trigger_instance_upsert_response import TriggerInstanceUpsertResponse

    for status in (200, 201):
        client = Composio(
            auth=ProjectAuth(API_KEY),
            base_url=BASE_URL,
            max_retries=0,
            http_client=httpx.Client(
                transport=httpx.MockTransport(
                    lambda _request, status=status: httpx.Response(status, json={"trigger_id": "ti_1"})
                )
            ),
        )
        try:
            parsed = client.trigger_instances.upsert("SLACK_NEW_MESSAGE", body={})
        finally:
            client.close()

        assert isinstance(parsed, TriggerInstanceUpsertResponse)
        assert parsed.trigger_id == "ti_1"


# --------------------------------------------------------------------------
# Aliasing outside `tool_router`.
#
# The hand-written corpus pinned the whole non-pythonic wire-name inventory of
# the tool_router surface, all of it under `custom_connection_data`. The widened
# surface has nine more operations carrying one, across six roots, and they are
# the ones a rename bug would now reach.
# --------------------------------------------------------------------------

_ALIASED_BODIES: list[tuple[str, Any, dict[str, Any], dict[str, Any]]] = [
    (
        "auth_configs.create",
        lambda c, body: c.auth_configs.create(body=body),
        {"toolkit": {"slug": "gmail"}, "auth_config": {"type": "use_custom_auth", "auth_scheme": "OAUTH2"}},
        {"toolkit": {"slug": "gmail"}, "auth_config": {"type": "use_custom_auth", "authScheme": "OAUTH2"}},
    ),
    (
        "connected_accounts.create",
        lambda c, body: c.connected_accounts.create(body=body),
        {
            "auth_config": {"id": "ac_1"},
            "connection": {
                "user_id": "u_1",
                "state": {
                    "auth_scheme": "OAUTH2",
                    "val": {"status": "ACTIVE", "access_token": "t", "your_domain": "acme.example.com"},
                },
            },
        },
        {
            "auth_config": {"id": "ac_1"},
            "connection": {
                "user_id": "u_1",
                "state": {
                    "authScheme": "OAUTH2",
                    "val": {"status": "ACTIVE", "access_token": "t", "your-domain": "acme.example.com"},
                },
            },
        },
    ),
    (
        "org.owner.project.create",
        lambda c, body: c.org.owner.project.create(body=body),
        {
            "name": "acme",
            "config": {
                "is_2fa_enabled": True,
                "mask_secret_keys_in_connected_account": False,
                "log_visibility_setting": "ALL",
            },
        },
        {
            "name": "acme",
            "config": {
                "is_2FA_enabled": True,
                "mask_secret_keys_in_connected_account": False,
                "log_visibility_setting": "ALL",
            },
        },
    ),
    (
        "tools.execute",
        lambda c, body: c.tools.execute("GITHUB_STAR", body=body),
        {"custom_connection_data": {"auth_scheme": "OAUTH2", "toolkit_slug": "gmail"}},
        {"custom_connection_data": {"authScheme": "OAUTH2", "toolkitSlug": "gmail"}},
    ),
    (
        # The `_LEGACY_PROPERTY_NAMES` rename, on the wire: a camelCase alias
        # whose normalized Python name would collide with its snake_case sibling
        # keeps both, and each reaches its own key.
        "trigger_instances.upsert",
        lambda c, body: c.trigger_instances.upsert("SLACK_NEW_MESSAGE", body=body),
        {
            "connected_account_id": "ca_1",
            "trigger_config": {"channel": "#general"},
            "deprecated_trigger_config": {"legacy": 1},
        },
        {
            "connected_account_id": "ca_1",
            "trigger_config": {"channel": "#general"},
            "triggerConfig": {"legacy": 1},
        },
    ),
]


@pytest.mark.parametrize(
    ("accessor", "invoke", "pythonic", "wire"),
    [pytest.param(*row, id=row[0]) for row in _ALIASED_BODIES],
)
def test_a_pythonic_body_reaches_the_wire_with_the_specs_aliases(
    accessor: str, invoke: Any, pythonic: dict[str, Any], wire: dict[str, Any]
) -> None:
    """One operation per newly covered root that carries a non-pythonic name."""
    actual = capture(Composio, Case(f"aliasing.{accessor}", lambda c: invoke(c, pythonic)))

    assert actual["body"] == wire


@pytest.mark.parametrize(
    ("accessor", "invoke", "pythonic", "wire"),
    [pytest.param(*row, id=row[0]) for row in _ALIASED_BODIES],
)
def test_the_wire_spelling_is_accepted_on_input_too(
    accessor: str, invoke: Any, pythonic: dict[str, Any], wire: dict[str, Any]
) -> None:
    """`populate_by_name` means a caller may write either spelling; both must
    produce the same bytes."""
    actual = capture(Composio, Case(f"aliasing.{accessor}.wire", lambda c: invoke(c, wire)))

    assert actual["body"] == wire


def test_a_numbered_body_keyword_reaches_the_wire_key_the_oracle_gives_it() -> None:
    """`body_trigger_config_1` is `trigger_config` and `_2` is the deprecated
    `triggerConfig` — what 1.43.0's own params type says. The generator once
    numbered them in spec order, which sent `_1` as `triggerConfig`; the derived
    corpus never set an optional colliding keyword, so only a live run saw it."""
    actual = capture(
        Composio,
        Case(
            "collision.trigger_instances.upsert",
            lambda c: c.trigger_instances.upsert(
                "SLACK_NEW_MESSAGE",
                body_trigger_config_1={"channel": "#general"},
                body_trigger_config_2={"legacy": 1},
            ),
        ),
    )

    assert actual["body"] == {"trigger_config": {"channel": "#general"}, "triggerConfig": {"legacy": 1}}


def test_a_numbered_query_keyword_reaches_the_wire_key_the_oracle_gives_it() -> None:
    """The query half of the same rule, on the operation whose spec order already
    agreed with it — so it is pinned rather than assumed to keep agreeing."""
    actual = capture(
        Composio,
        Case(
            "collision.trigger_instances.list_active",
            lambda c: c.trigger_instances.list_active(
                query_show_disabled_1=True, query_show_disabled_2=False
            ),
        ),
    )
    pairs = dict(pair.split("=", 1) for pair in _query_pairs(actual["query"]))

    assert (pairs["show_disabled"].lower(), pairs["showDisabled"].lower()) == ("true", "false")


def test_an_unknown_key_outside_tool_router_is_forwarded_verbatim() -> None:
    """Top-level and nested. The rename is a key rename and nothing else: a key
    no model declares is not a key the client may drop."""
    actual = capture(
        Composio,
        Case(
            "aliasing.unknown-keys",
            lambda c: c.auth_configs.create(
                body={
                    "toolkit": {"slug": "gmail", "unknown_nested": {"deeper": 1}},
                    "auth_config": {"type": "use_custom_auth", "auth_scheme": "OAUTH2"},
                    "unknown_top": [1, "two", None],
                }
            ),
        ),
    )

    assert actual["body"]["unknown_top"] == [1, "two", None]
    assert actual["body"]["toolkit"]["unknown_nested"] == {"deeper": 1}
    assert actual["body"]["auth_config"] == {"type": "use_custom_auth", "authScheme": "OAUTH2"}


@pytest.mark.parametrize(
    ("value", "encoded"),
    [
        ("gmail slug", "gmail%20slug"),
        ("a/b", "a%2Fb"),
        ("déjà", "d%C3%A9j%C3%A0"),
    ],
)
def test_a_path_parameter_outside_tool_router_is_percent_encoded(value: str, encoded: str) -> None:
    actual = capture(Composio, Case("path.toolkits", lambda c: c.toolkits.retrieve(value)))

    assert actual["path"] == f"/api/v3.1/toolkits/{encoded}"


@pytest.mark.parametrize("value", ["..", ".", "%2e%2e"])
def test_a_dot_segment_outside_tool_router_never_dispatches(value: str) -> None:
    """`_PATH_SAFE` refuses a value that could climb the path, before any
    request is built — the same rule the tool_router cases pin, now on a route
    that reaches it through a different resource module."""
    client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
    try:
        with pytest.raises(ValueError):
            client.toolkits.retrieve(value)
    finally:
        client.close()
