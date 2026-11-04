"""The runtime deprecation interceptor, plus the static
parameter-level warning (``docs/deprecation-alerts-fix-plan.md`` steps 3-4).

The Python half of the interceptor-parity evidence: the same field corpus the
TypeScript suite pins (``test/unit/deprecation.test.ts``), asserted against the
same expected readings, plus the two things only this language has — the
``ComposioDeprecationWarning`` category and the sync/async kernel arms.

The operation table is hand-written here (Python's resource classes still are),
so this module also pins it against the spec snapshot and against the paths the
resource classes actually dispatch to.

``TestParameterInterceptor`` pins the static trigger: unlike everything above,
it needs no response at all, and its warning names the caller's own
disambiguated keyword (``query_show_disabled_2``, not the wire name
``showDisabled``) rather than the operation.
"""

from __future__ import annotations

import contextlib
import json
import os
import pathlib
import time
import warnings
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import AsyncComposio, Composio, ComposioDeprecationWarning, ProjectAuth, RequestOptions
from composio_client._deprecated_inputs import DeprecatedInput
from composio_client._deprecation import (
    _isoformat,
    inspect_deprecated_inputs,
    inspect_deprecation,
    match_operation,
    match_successor_chain,
    parse_deprecation,
    parse_http_date,
    parse_link_field,
    parse_structured_date,
)
from composio_client._operations import OPERATIONS, Operation

from .conftest import API_KEY, BASE_URL

# RFC 9745's own example: Friday, 30 June 2023 23:59:59 UTC.
ANNOUNCED = "@1688169599"
ANNOUNCED_ISO = "2023-06-30T23:59:59.000Z"
SUNSET = "Sun, 30 Jun 2024 23:59:59 GMT"
SUNSET_ISO = "2024-06-30T23:59:59.000Z"

DEPRECATED_HEADERS = {
    "deprecation": ANNOUNCED,
    "sunset": SUNSET,
    "link": (
        '<https://developer.example.com/deprecation>; rel="deprecation", '
        '</api/v3.1/tool_router/session/trs_1/tools>; rel="successor-version"'
    ),
}

SESSION_PATH = "/api/v3.1/tool_router/session/trs_1"

#: Shared with the TypeScript suite; see the file's own `$comment`.
HTTP_DATE_VECTORS: list[dict[str, str | None]] = json.loads(
    (Path(__file__).resolve().parents[2] / "test" / "fixtures" / "http-date-vectors.json").read_text()
)["vectors"]


def _to_iso_z(value: datetime) -> str:
    """The TypeScript ``Date.toISOString()`` spelling the vector table uses.

    Deliberately the shipped :func:`composio_client._deprecation._isoformat`
    rather than a re-spelling of it, so the vectors check the string a caller
    actually sees in a warning.
    """
    return _isoformat(value)


@contextlib.contextmanager
def _timezone(name: str) -> Iterator[None]:
    previous = os.environ.get("TZ")
    os.environ["TZ"] = name
    time.tzset()
    try:
        yield
    finally:
        if previous is None:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = previous
        time.tzset()


class Echo(BaseModel):
    ok: bool


def headers_of(values: dict[str, str]) -> httpx.Headers:
    return httpx.Headers(values)


class TestFieldParsing:
    def test_reads_a_structured_field_date(self) -> None:
        announced = parse_structured_date(ANNOUNCED)
        assert announced is not None
        assert announced.isoformat() == "2023-06-30T23:59:59+00:00"
        assert parse_structured_date("  @0  ") is not None
        assert parse_structured_date("@-1") is not None

    @pytest.mark.parametrize("value", ["true", "1688169599", SUNSET, "@", "@1.5", "@nope", ""])
    def test_refuses_what_is_not_a_structured_field_date(self, value: str) -> None:
        # The pre-RFC drafts used `true` and a bare HTTP-date; neither is RFC 9745.
        assert parse_structured_date(value) is None

    def test_reads_an_http_date_sunset(self) -> None:
        sunset = parse_http_date(SUNSET)
        assert sunset is not None
        assert sunset.isoformat() == "2024-06-30T23:59:59+00:00"
        assert parse_http_date("not a date") is None

    @pytest.mark.parametrize("vector", HTTP_DATE_VECTORS, ids=[v["value"] for v in HTTP_DATE_VECTORS])
    def test_http_date_conformance_shared_with_typescript(self, vector: dict[str, str | None]) -> None:
        # `test/fixtures/http-date-vectors.json` is read by
        # test/unit/deprecation.test.ts too. The two parsers are required to
        # agree on every input, so a divergence has to be introduced in one
        # language and then repeated in that table before either suite is green.
        parsed = parse_http_date(str(vector["value"]))
        actual = None if parsed is None else _to_iso_z(parsed)
        assert actual == vector["expect"], vector["why"]

    @pytest.mark.parametrize(
        ("year", "expected"),
        [(50, "0050"), (999, "0999"), (1994, "1994"), (2024, "2024")],
    )
    def test_isoformat_zero_pads_a_year_below_1000(self, year: int, expected: str) -> None:
        # `strftime("%Y")` delegates to the platform's C library, which does not
        # agree here: glibc renders year 50 as `50`, macOS as `0050`. That is
        # reachable -- `parse_http_date` accepts any year from 1 -- and it would
        # make the warning text a caller sees depend on the host, which is the
        # defect the Sunset parser was rewritten to remove. Caught by CI, not
        # locally, because the developing machine was the one that padded.
        stamped = _isoformat(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        assert stamped == f"{expected}-12-31T23:59:59.000Z"

    def test_http_date_parsing_does_not_depend_on_the_host_timezone(self) -> None:
        # `datetime` here is timezone-aware by construction, so this is a pin
        # rather than a fix -- but it is the property the TypeScript client had
        # to be rewritten to obtain, and it must not regress on either side.
        with _timezone("Pacific/Kiritimati"):
            parsed = parse_http_date("Sun Nov  6 08:49:37 1994")
        assert parsed is not None
        assert _to_iso_z(parsed) == "1994-11-06T08:49:37.000Z"

    def test_parses_a_link_field_including_quoted_parameters(self) -> None:
        links = parse_link_field(
            '<https://docs.example.com/a,b;c>; rel="deprecation"; type="text/html", '
            "</api/v3.1/tool_router/session>; rel=successor-version"
        )
        assert links == (
            ("https://docs.example.com/a,b;c", ("deprecation",), False),
            ("/api/v3.1/tool_router/session", ("successor-version",), False),
        )

    def test_treats_rel_as_a_space_separated_list(self) -> None:
        assert parse_link_field('</next>; rel="Successor-Version Alternate"') == (
            ("/next", ("successor-version", "alternate"), False),
        )

    def test_keeps_what_parsed_before_malformed_input(self) -> None:
        assert parse_link_field('</a>; rel="deprecation", <unterminated') == (
            ("/a", ("deprecation",), False),
        )
        assert parse_link_field("garbage") == ()


class TestNoticeAssembly:
    def test_returns_nothing_without_a_deprecation_field(self) -> None:
        assert parse_deprecation(headers_of({"sunset": SUNSET}), BASE_URL, BASE_URL) is None

    def test_assembles_the_full_notice(self) -> None:
        notice = parse_deprecation(headers_of(DEPRECATED_HEADERS), BASE_URL, BASE_URL)
        assert notice is not None
        assert notice.deprecated_at is not None
        assert notice.sunset_at is not None
        assert notice.documentation == "https://developer.example.com/deprecation"
        assert str(notice.successor) == f"{BASE_URL}/api/v3.1/tool_router/session/trs_1/tools"

    def test_fires_when_the_value_does_not_parse(self) -> None:
        notice = parse_deprecation(headers_of({"deprecation": "true"}), BASE_URL, BASE_URL)
        assert notice is not None
        assert notice.deprecated_at is None

    def test_drops_an_oversized_field(self) -> None:
        assert parse_deprecation(headers_of({"deprecation": "@" + "9" * 3000}), BASE_URL, BASE_URL) is None

        notice = parse_deprecation(
            headers_of({"deprecation": ANNOUNCED, "link": f'<https://x/{"a" * 3000}>; rel="deprecation"'}),
            BASE_URL,
            BASE_URL,
        )
        assert notice is not None
        assert notice.documentation is None

    def test_drops_a_field_carrying_control_characters(self) -> None:
        injected = "@1688169599\r\nx-injected: 1"
        assert parse_deprecation(headers_of({"deprecation": injected}), BASE_URL, BASE_URL) is None

    @pytest.mark.parametrize(
        ("target", "accepted"),
        [
            ("/api/v3.1/tool_router/session", True),
            (f"{BASE_URL}/api/v3.1/tool_router/session", True),
            ("https://evil.example.com/api/v3.1/tool_router/session", False),
            # A network-path reference changes origin without naming a scheme.
            ("//evil.example.com/api/v3.1/tool_router/session", False),
            ("javascript:alert(1)", False),
        ],
    )
    def test_accepts_only_a_same_origin_successor(self, target: str, accepted: bool) -> None:
        notice = parse_deprecation(
            headers_of({"deprecation": ANNOUNCED, "link": f'<{target}>; rel="successor-version"'}),
            BASE_URL,
            BASE_URL,
        )
        assert notice is not None
        assert (notice.successor is not None) is accepted

    def test_honors_only_the_first_rel_on_a_link(self) -> None:
        # RFC 8288 3.3. Accumulating later `rel`s would let an attacker-chosen
        # target ride in under a relation the client acts on.
        notice = parse_deprecation(
            headers_of(
                {
                    "deprecation": ANNOUNCED,
                    "link": "<https://evil.example.com/phish>; rel=alternate; rel=deprecation",
                }
            ),
            BASE_URL,
            BASE_URL,
        )
        assert notice is not None
        assert notice.documentation is None

    def test_ignores_an_anchored_link(self) -> None:
        # RFC 8288 3.2: `anchor` re-points the link's context at another resource.
        notice = parse_deprecation(
            headers_of(
                {
                    "deprecation": ANNOUNCED,
                    "link": '</api/v3.1/tool_router/session>; anchor="/other"; rel="successor-version"',
                }
            ),
            BASE_URL,
            BASE_URL,
        )
        assert notice is not None
        assert notice.successor is None

    def test_resolves_a_relative_target_against_the_response_url(self) -> None:
        # RFC 8288 3.1: the context is the URL the response came from.
        notice = parse_deprecation(
            headers_of({"deprecation": ANNOUNCED, "link": '<tools>; rel="successor-version"'}),
            f"{BASE_URL}/api/v3.1/tool_router/session/trs_1/",
            BASE_URL,
        )
        assert notice is not None
        assert str(notice.successor) == f"{BASE_URL}/api/v3.1/tool_router/session/trs_1/tools"

    def test_refuses_a_relative_successor_from_a_redirected_response(self) -> None:
        # Resolving against the context but validating against base_url is what
        # stops a foreign hop nominating an operation on our own origin.
        notice = parse_deprecation(
            headers_of({"deprecation": ANNOUNCED, "link": '<session>; rel="successor-version"'}),
            "https://evil.example.com/api/v3.1/tool_router/",
            BASE_URL,
        )
        assert notice is not None
        assert notice.successor is None

    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            ("https://developer.example.com/notes", "https://developer.example.com/notes"),
            ("javascript:alert(1)", None),
            ("data:text/html,<b>hi", None),
        ],
    )
    def test_allows_a_cross_origin_documentation_link_over_http_only(
        self, target: str, expected: str | None
    ) -> None:
        notice = parse_deprecation(
            headers_of({"deprecation": ANNOUNCED, "link": f'<{target}>; rel="deprecation"'}),
            BASE_URL,
            BASE_URL,
        )
        assert notice is not None
        assert notice.documentation == expected


class TestOperationTable:
    """``_operations.py`` is manufactured output now, so these guard the
    *generator* rather than a hand-kept list.

    The direction the hand-kept table could not close — a resource method with
    no entry — is closed by construction: both the table and the classes are
    emitted from one plan. What is still worth pinning is that the emission
    agrees with the other artifact derived from that plan
    (``surface-coverage.json``), that every path is real, and that every chain
    resolves; a renderer bug would break exactly those.
    """

    def test_matches_the_coverage_declaration_row_for_row(self) -> None:
        coverage = json.loads((Path(__file__).resolve().parents[1] / "surface-coverage.json").read_text())

        assert sorted((operation.method, operation.path) for operation in OPERATIONS) == sorted(
            tuple(entry["key"].split(" ", 1)) for entry in coverage["operations"]
        )
        assert sorted(list(operation.chain) for operation in OPERATIONS) == sorted(
            entry["accessor"] for entry in coverage["operations"]
        )

    def test_omits_schemes_wherever_the_runtime_default_is_already_right(self) -> None:
        """The omit rule (``security.ts:DEFAULT_SCHEME``): a row that says
        nothing and a path that matches no row must mean the same thing.

        48 rows carry schemes, which is the count the TypeScript twin
        (``src/compat/generated-operations.ts``) carries — the two tables are
        emitted from one resolution, so they cannot disagree without a
        generator bug.
        """
        declared = {
            " ".join((operation.method, operation.path)): operation.schemes
            for operation in OPERATIONS
            if operation.schemes is not None
        }

        assert len(declared) == 48
        # A carried row is never the default spelled out longhand.
        for key, schemes in declared.items():
            assert schemes != ("ApiKeyAuth",), key
            assert schemes, key
        assert declared["delete /api/v3.1/org/owner/project/{nano_id}"] == ("OrgApiKeyAuth",)
        assert declared["post /api/v3.1/tool_router/session/{session_id}/proxy_execute"] == (
            "ApiKeyAuth",
            "UserApiKeyAuth",
        )

    def test_every_entry_exists_in_the_spec_snapshot(self) -> None:
        spec = json.loads((Path(__file__).resolve().parents[2] / "spec" / "openapi.json").read_text())
        for operation in OPERATIONS:
            item = spec["paths"].get(operation.path)
            assert item is not None, f"{operation.path} is not in the spec"
            assert operation.method in item, f"{operation.method} {operation.path} is not in the spec"

    def test_covers_every_path_the_resource_classes_dispatch(self) -> None:
        # The accessor chains the table claims must be reachable on a client,
        # so a renamed resource method cannot leave a stale entry behind.
        client = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
        try:
            for operation in OPERATIONS:
                target: object = client
                for accessor in operation.chain:
                    target = getattr(target, accessor)
                assert callable(target), f"{'.'.join(operation.chain)} is not callable"
        finally:
            client.close()

    def test_matches_a_substituted_path(self) -> None:
        matched = match_operation("get", SESSION_PATH, OPERATIONS)
        assert matched is not None
        assert matched.chain == ("tool_router", "session", "retrieve")

        mounts = match_operation("get", "/api/v3.1/tool_router/session/trs_1/mounts/m_1/items", OPERATIONS)
        assert mounts is not None
        assert mounts.chain == ("tool_router", "session", "files", "list")

    def test_keys_on_the_method_and_ignores_a_query_string(self) -> None:
        # `delete` on the session path *is* an operation now, so the method key
        # is shown with one the spec does not declare on that path at all.
        assert match_operation("put", SESSION_PATH, OPERATIONS) is None
        assert match_operation("delete", SESSION_PATH, OPERATIONS) is not None
        assert match_operation("get", f"{SESSION_PATH}?x=1", OPERATIONS) is not None
        assert match_operation("get", "/api/v3.1/not/an/endpoint", OPERATIONS) is None

    def test_matches_an_arbitrary_operation_table(self) -> None:
        operations = (
            Operation("get", "/items/{item_id}", ("parameterized",)),
            Operation("get", "/items/special", ("literal",)),
        )

        matched = match_operation("get", "/items/special", operations)

        assert matched is operations[1]

    def test_names_the_successor_operation(self) -> None:
        successor = httpx.URL(f"{BASE_URL}/api/v3.1/tool_router/session")
        assert match_successor_chain("post", successor, OPERATIONS) == (
            "tool_router",
            "session",
            "create",
        )
        # A successor under a DIFFERENT method is not a successor for this
        # operation: answering a deprecated GET with `session.create` (a POST)
        # would tell the caller to replace a read with a write.
        assert match_successor_chain("get", successor, OPERATIONS) is None
        assert (
            match_successor_chain("get", httpx.URL(f"{BASE_URL}/api/v3.1/not/an/endpoint"), OPERATIONS)
            is None
        )


class TestInterceptor:
    @respx.mock
    def test_warns_once_naming_the_operation_dates_successor_and_notes(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client._request("get", SESSION_PATH, cast_to=Echo)

        assert len(caught) == 1
        assert str(caught[0].message) == (
            "`client.tool_router.session.retrieve` is deprecated. "
            f"Announced {ANNOUNCED_ISO}. "
            f"Scheduled for removal on {SUNSET_ISO}. "
            "Use `client.tool_router.session.tools` instead. "
            "See https://developer.example.com/deprecation"
        )

    @respx.mock
    def test_warns_again_when_the_same_operation_sends_a_different_notice(self, client: Composio) -> None:
        # The case the record exists to serve: `Deprecation` is announced first
        # with no `Sunset`, and the committed removal date lands later. Keying
        # the warn-once set on the operation alone would swallow it forever.
        announced_only = {"deprecation": ANNOUNCED}
        with_sunset = {"deprecation": ANNOUNCED, "sunset": SUNSET}
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            side_effect=[
                httpx.Response(200, json={"ok": True}, headers=announced_only),
                httpx.Response(200, json={"ok": True}, headers=with_sunset),
                # The third call repeats the second notice, already recorded.
                httpx.Response(200, json={"ok": True}, headers=with_sunset),
            ]
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(3):
                client._request("get", SESSION_PATH, cast_to=Echo)

        messages = [str(record.message) for record in caught]
        assert messages == [
            f"`client.tool_router.session.retrieve` is deprecated. Announced {ANNOUNCED_ISO}.",
            (
                f"`client.tool_router.session.retrieve` is deprecated. Announced {ANNOUNCED_ISO}. "
                f"Scheduled for removal on {SUNSET_ISO}."
            ),
        ]

    @respx.mock
    def test_keys_the_record_on_the_parsed_notice_not_the_header_bytes(self, client: Composio) -> None:
        # Identity is the announcement instant, the sunset instant and the
        # successor. A requoted `Link`, padding around `Deprecation`, and a
        # moved documentation URL all read as the same notice.
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            side_effect=[
                httpx.Response(
                    200,
                    json={"ok": True},
                    headers={
                        "deprecation": ANNOUNCED,
                        "link": (
                            '<https://developer.example.com/notes>; rel="deprecation", '
                            f'<{SESSION_PATH}/tools>; rel="successor-version"'
                        ),
                    },
                ),
                httpx.Response(
                    200,
                    json={"ok": True},
                    headers={
                        "deprecation": f"  {ANNOUNCED}  ",
                        "link": (
                            "<https://developer.example.com/moved>; rel=deprecation, "
                            f'<{SESSION_PATH}/tools>; rel=successor-version; type="text/html"'
                        ),
                    },
                ),
            ]
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client._request("get", SESSION_PATH, cast_to=Echo)
            client._request("get", SESSION_PATH, cast_to=Echo)

        assert len(caught) == 1

    @respx.mock
    def test_keys_the_unmatched_path_record_on_the_notice_too(self, client: Composio) -> None:
        # The escape-hatch branch keys on the substituted path rather than a
        # client chain, and follows the same (operation, notice) rule.
        respx.get(f"{BASE_URL}/api/v3.1/unmapped").mock(
            side_effect=[
                httpx.Response(200, json={"ok": True}, headers={"deprecation": ANNOUNCED}),
                httpx.Response(200, json={"ok": True}, headers={"deprecation": ANNOUNCED, "sunset": SUNSET}),
                httpx.Response(200, json={"ok": True}, headers={"deprecation": ANNOUNCED, "sunset": SUNSET}),
            ]
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(3):
                client._request("get", "/api/v3.1/unmapped", cast_to=Echo)

        messages = [str(record.message) for record in caught]
        assert messages == [
            f"GET /api/v3.1/unmapped is deprecated. Announced {ANNOUNCED_ISO}.",
            (
                f"GET /api/v3.1/unmapped is deprecated. Announced {ANNOUNCED_ISO}. "
                f"Scheduled for removal on {SUNSET_ISO}."
            ),
        ]

    @respx.mock
    def test_warns_once_per_operation_per_client_instance_for_the_same_notice(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )
        respx.get(f"{BASE_URL}{SESSION_PATH}/tools").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client._request("get", SESSION_PATH, cast_to=Echo)
            client._request("get", SESSION_PATH, cast_to=Echo)
            client._request("get", f"{SESSION_PATH}/tools", cast_to=Echo)

        messages = [str(record.message) for record in caught]
        assert len(messages) == 2
        assert "session.retrieve`" in messages[0]
        assert "session.tools`" in messages[1]

    @respx.mock
    def test_a_second_client_starts_a_fresh_record(self) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(2):
                other = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
                other._request("get", SESSION_PATH, cast_to=Echo)
                other.close()

        assert len(caught) == 2

    @respx.mock
    def test_says_nothing_without_a_notice(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(return_value=httpx.Response(200, json={"ok": True}))

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client._request("get", SESSION_PATH, cast_to=Echo)

        assert caught == []

    @respx.mock
    def test_ignores_a_notice_on_a_discarded_attempt(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            side_effect=[
                httpx.Response(429, json={}, headers={**DEPRECATED_HEADERS, "retry-after": "0"}),
                httpx.Response(200, json={"ok": True}),
            ]
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client._request("get", SESSION_PATH, cast_to=Echo)

        assert caught == []

    @respx.mock
    def test_warns_on_an_error_response_without_disturbing_the_error(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(404, json={"error": "gone"}, headers=DEPRECATED_HEADERS)
        )

        from composio_client import NotFoundError

        with pytest.warns(ComposioDeprecationWarning), pytest.raises(NotFoundError):
            client._request("get", SESSION_PATH, cast_to=Echo)

    @respx.mock
    def test_names_the_request_when_the_path_matches_no_operation(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/unmapped").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers={"deprecation": ANNOUNCED})
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client._request("get", "/api/v3.1/unmapped", cast_to=Echo)

        assert str(caught[0].message) == (f"GET /api/v3.1/unmapped is deprecated. Announced {ANNOUNCED_ISO}.")

    @respx.mock
    async def test_the_async_arm_warns_the_same_way(self, async_client: AsyncComposio) -> None:
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            await async_client._request("get", SESSION_PATH, cast_to=Echo)

        assert len(caught) == 1
        assert "`client.tool_router.session.retrieve`" in str(caught[0].message)
        await async_client.aclose()

    @respx.mock
    def test_warnings_as_errors_propagates_on_a_successful_call(self, client: Composio) -> None:
        # `-W error` is an explicit instruction that warnings are fatal; the
        # client honors it rather than defeating it.
        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True}, headers=DEPRECATED_HEADERS)
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error", ComposioDeprecationWarning)
            with pytest.raises(ComposioDeprecationWarning):
                client._request("get", SESSION_PATH, cast_to=Echo)

    @respx.mock
    def test_warnings_as_errors_never_displaces_the_real_api_error(self, client: Composio) -> None:
        # An advisory notice must not stand in for the error that actually
        # explains the failure: a deprecated 404 still raises NotFoundError.
        from composio_client import NotFoundError

        respx.get(f"{BASE_URL}{SESSION_PATH}").mock(
            return_value=httpx.Response(404, json={"error": "gone"}, headers=DEPRECATED_HEADERS)
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error", ComposioDeprecationWarning)
            with pytest.raises(NotFoundError):
                client._request("get", SESSION_PATH, cast_to=Echo)

    @respx.mock
    def test_generated_overlap_keeps_the_invoked_operation_identity(self, client: Composio) -> None:
        route = respx.get(f"{BASE_URL}/api/v3.1/toolkits/categories").mock(
            return_value=httpx.Response(200, json={}, headers={"deprecation": ANNOUNCED})
        )

        with pytest.warns(ComposioDeprecationWarning) as generated:
            response = client.toolkits.with_raw_response.retrieve("categories")
        response.close()
        with pytest.warns(ComposioDeprecationWarning) as raw:
            client.get("/api/v3.1/toolkits/categories")

        assert "`client.toolkits.retrieve`" in str(generated[0].message)
        assert "`client.toolkits.retrieve_categories`" in str(raw[0].message)
        assert route.call_count == 2

    def test_the_warning_is_attributed_to_the_callers_line(self) -> None:
        # stacklevel must point past the SDK's own frames at the user's call.
        import composio_client

        sdk_root = pathlib.Path(composio_client.__file__).parent

        with respx.mock:
            respx.post(f"{BASE_URL}/api/v3.1/tool_router/session").mock(
                return_value=httpx.Response(200, json={"ok": True}, headers={"deprecation": ANNOUNCED})
            )
            other = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                # Called through the public accessor, as a user would. The
                # stub body does not satisfy the real response model, but the
                # warning is emitted before the body is parsed, which is the
                # only thing under test here.
                with contextlib.suppress(Exception):
                    other.tool_router.session.create({"user_id": "user_1"})
            other.close()

        assert len(caught) == 1
        blamed = pathlib.Path(caught[0].filename)
        assert sdk_root not in blamed.parents, f"warning blamed the SDK: {blamed}"
        assert blamed == pathlib.Path(__file__)

    def test_stops_warning_past_the_tracking_ceiling(self) -> None:
        # The set is bounded so neither an escape-hatch caller keying on
        # substituted paths nor a server rotating notices can grow it without
        # limit. Mirrors the TypeScript suite's equivalent.
        response = httpx.Response(200, headers={"deprecation": ANNOUNCED})
        seen = {f"filler-{index}" for index in range(1024)}

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            inspect_deprecation(
                response,
                method="get",
                path="/api/v3.1/unmapped",
                base_url=BASE_URL,
                seen=seen,
            )

        assert caught == []
        assert len(seen) == 1024


class TestParameterInterceptor:
    """The static trigger: fires from the request alone, before dispatch, and
    never from a response."""

    @respx.mock
    def test_warns_once_naming_the_input_and_its_replacement(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"items": []}))

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client.tools.list(search="repo")

        assert len(caught) == 1
        assert str(caught[0].message) == (
            "the `search` parameter of `client.tools.list` is deprecated. Use `query` instead."
        )

    @respx.mock
    def test_never_warns_with_only_the_replacement(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"items": []}))

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.tools.list(query="repo")

        assert caught == []

    @respx.mock
    def test_two_deprecated_inputs_both_surface_and_are_not_collapsed(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/trigger_instances/active").mock(
            return_value=httpx.Response(200, json={"items": []})
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.trigger_instances.list_active(query_show_disabled_2=True, query_trigger_ids_2=["ti_1"])

        messages = [str(record.message) for record in caught]
        assert messages == [
            "the `query_trigger_ids_2` parameter of `client.trigger_instances.list_active` is deprecated. "
            "Use `query_trigger_ids_1` instead.",
            "the `query_show_disabled_2` parameter of `client.trigger_instances.list_active` is deprecated. "
            "Use `query_show_disabled_1` instead.",
        ]

        # Same set of deprecated wire names, again: the warn-once key is
        # (operation, sorted wire-name set), so neither fires a second time.
        with warnings.catch_warnings(record=True) as caught_again:
            warnings.simplefilter("always")
            client.trigger_instances.list_active(query_show_disabled_2=True, query_trigger_ids_2=["ti_2"])
        assert caught_again == []

    @respx.mock
    def test_warns_without_a_replacement_clause(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/auth_configs").mock(
            return_value=httpx.Response(200, json={"items": []})
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client.auth_configs.list(deprecated_status="DISABLED")

        assert str(caught[0].message) == (
            "the `deprecated_status` parameter of `client.auth_configs.list` is deprecated."
        )

    @respx.mock
    def test_warns_on_a_deprecated_body_property(self, client: Composio) -> None:
        respx.post(f"{BASE_URL}/api/v3.1/tools/execute/my_tool").mock(
            return_value=httpx.Response(200, json={"data": {}, "successful": True})
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client.tools.execute("my_tool", entity_id="e_1")

        assert str(caught[0].message) == (
            "the `entity_id` parameter of `client.tools.execute` is deprecated. Use `user_id` instead."
        )

    @respx.mock
    def test_raw_escape_hatch_resolves_through_the_same_match_operation(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"items": []}))
        respx.get(f"{BASE_URL}/api/v3.1/unmapped").mock(return_value=httpx.Response(200, json={"ok": True}))

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client.get("/api/v3.1/tools", query={"search": "repo"})
        assert len(caught) == 1

        # A path matching no known operation has no chain to key
        # `DEPRECATED_INPUTS` by, so there is nothing to warn from.
        with warnings.catch_warnings(record=True) as none_caught:
            warnings.simplefilter("always")
            client.get("/api/v3.1/unmapped", query={"search": "repo"})
        assert none_caught == []

    @respx.mock
    def test_fires_even_when_the_transport_raises_before_a_response_exists(self, client: Composio) -> None:
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(side_effect=httpx.ConnectError("boom"))

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            with pytest.raises(Exception):  # noqa: B017, PT011 - the transport failure itself is not under test
                client._request(
                    "get",
                    "/api/v3.1/tools",
                    cast_to=Echo,
                    query={"search": "repo"},
                    options=RequestOptions(max_retries=0),
                )

        assert len(caught) == 1
        assert "the `search` parameter" in str(caught[0].message)

    @respx.mock
    def test_names_the_disambiguated_keyword_and_blames_the_callers_line(self) -> None:
        # stacklevel must point past the SDK's own frames at the user's call,
        # the same property `TestInterceptor.test_the_warning_is_attributed_to_the_callers_line`
        # pins for the response-driven notice — recomputed here, since `_prepare`
        # sits at a different depth than the response exit.
        import composio_client

        sdk_root = pathlib.Path(composio_client.__file__).parent

        respx.get(f"{BASE_URL}/api/v3.1/trigger_instances/active").mock(
            return_value=httpx.Response(200, json={"items": []})
        )
        other = Composio(auth=ProjectAuth(API_KEY), base_url=BASE_URL)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            other.trigger_instances.list_active(query_show_disabled_2=True)
        other.close()

        assert len(caught) == 1
        assert str(caught[0].message) == (
            "the `query_show_disabled_2` parameter of `client.trigger_instances.list_active` is deprecated. "
            "Use `query_show_disabled_1` instead."
        )
        blamed = pathlib.Path(caught[0].filename)
        assert sdk_root not in blamed.parents, f"warning blamed the SDK: {blamed}"
        assert blamed == pathlib.Path(__file__)

    def test_stops_warning_past_the_tracking_ceiling(self) -> None:
        # Mirrors TestInterceptor's equivalent for the response-driven notice.
        seen = {f"filler-{index}" for index in range(1024)}

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            inspect_deprecated_inputs(
                operation=next(op for op in OPERATIONS if op.chain == ("tools", "list")),
                query={"search": "repo"},
                body=None,
                seen=seen,
            )

        assert caught == []
        assert len(seen) == 1024

    @respx.mock
    def test_never_warns_for_a_query_value_explicitly_none(self, client: Composio) -> None:
        # `_encode_query` drops a `None` query value outright -- it never
        # reaches the wire -- so `search=None` must not warn, unlike a
        # genuinely-sent value.
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"items": []}))

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.tools.list(search=None)

        assert caught == []

    @respx.mock
    def test_still_warns_for_a_body_value_explicitly_none(self, client: Composio) -> None:
        # The converse: `compact()` preserves an explicit `None` body field,
        # which is genuinely sent as JSON `null` -- so it is a real signal.
        respx.post(f"{BASE_URL}/api/v3.1/tools/execute/my_tool").mock(
            return_value=httpx.Response(200, json={"data": {}, "successful": True})
        )

        with pytest.warns(ComposioDeprecationWarning) as caught:
            client.tools.execute("my_tool", entity_id=None)

        assert str(caught[0].message) == (
            "the `entity_id` parameter of `client.tools.execute` is deprecated. Use `user_id` instead."
        )

    def test_detects_a_deprecated_header_against_a_synthetic_table(self) -> None:
        # No spec-declared header input exists today (measured), so this pins
        # the header branch directly -- codegen already emits table entries
        # for it, and the interceptor must still act on one.
        table: dict[tuple[str, ...], tuple[DeprecatedInput, ...]] = {
            ("tools", "list"): (
                DeprecatedInput(
                    "X-Deprecated-Header", "header", "X-Deprecated-Header", "X-Header", "X-Header"
                ),
            ),
        }
        operation = next(op for op in OPERATIONS if op.chain == ("tools", "list"))

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            inspect_deprecated_inputs(
                operation=operation,
                query={},
                body=None,
                headers={"x-deprecated-header": "yes"},
                table=table,
                seen=set(),
            )

        assert len(caught) == 1
        assert str(caught[0].message) == (
            "the `X-Deprecated-Header` parameter of `client.tools.list` is deprecated. "
            "Use `X-Header` instead."
        )

    @respx.mock
    def test_warnings_as_errors_propagates_even_though_no_response_exists(self, client: Composio) -> None:
        # Unlike the response-driven notice, the static warning fires before
        # dispatch: there is no real API error here for `-W error` to
        # displace, so it always propagates.
        respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"items": []}))

        with warnings.catch_warnings():
            warnings.simplefilter("error", ComposioDeprecationWarning)
            with pytest.raises(ComposioDeprecationWarning):
                client.tools.list(search="repo")
            with pytest.raises(ComposioDeprecationWarning):
                client.tools.list(search="repo")

        assert len(respx.calls) == 0
