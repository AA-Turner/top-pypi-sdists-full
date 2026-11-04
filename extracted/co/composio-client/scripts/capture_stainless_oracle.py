"""Record the wire requests the Stainless ``composio-client`` 1.43.0 emits.

1.43.0 is the frozen predecessor of this package and the differential oracle for
the Python request wire, exactly as ``composio-client-stainless`` is on the
TypeScript side. It cannot be a dev dependency here: the PyPI distribution and
this repo's package both import as ``composio_client``, so they cannot coexist in
one venv. This script therefore runs in an isolated interpreter that has only the
Stainless distribution installed:

    cd python && uv run --isolated --no-project \\
        --with composio-client==1.43.0 python scripts/capture_stainless_oracle.py

It writes ``tests/fixtures/stainless_wire_oracle.json``, which
``tests/test_wire_parity.py`` diffs our client against. Re-run it (and commit the
result) only when the corpus changes or the pinned oracle version moves — never
to make a failing parity test pass.

Every call below is written in the *Stainless* calling convention (per-field
keyword arguments, ``files`` methods taking ``mount_id`` positionally and
``session_id`` as a keyword). ``tests/test_wire_parity.py`` expresses the same
logical calls in ours (a single ``body`` / ``query`` object, both path params
positional) — see MIGRATION.md for why they differ.
"""

from __future__ import annotations

import importlib
import json
import sys
from collections.abc import Callable
from typing import Any

# `wire_corpus` sits next to this file, so a flat import works under the isolated
# interpreter without any sys.path surgery. The test half, which runs from the
# package root, imports the same module as `scripts.wire_corpus`.
from wire_corpus import (
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
    ORACLE_PACKAGE,
    ORACLE_VERSION,
    PROXY_PARAMETERS,
    REGENERATE_COMMAND,
    SESSION_ID,
    SUBDELIMS_SESSION_ID,
    WORKBENCH_INT_THRESHOLD,
    Case,
    DerivedCall,
    capture,
    derived_calls,
    oracle_call,
    resolve_accessor,
)

# Imported dynamically on purpose: in the *dev* venv the name `composio_client`
# resolves to this repo's package, so a static import would type-check against
# the wrong client (and mypy would reject the Stainless call signatures). Under
# the isolated interpreter above it resolves to the 1.43.0 distribution.
_stainless: Any = importlib.import_module("composio_client")
Composio: Any = _stainless.Composio


CASES: list[Case] = [
    # ---- session (12 methods) ----
    Case(
        "session.create",
        lambda c: c.tool_router.session.create(
            user_id="wire@example.com",
            toolkits={"enable": ["github", "slack"]},
            manage_connections={"enable": True},
            auth_configs={"github": "ac_1"},
            tags={"include": ["prod"]},
        ),
    ),
    Case("session.create.minimal", lambda c: c.tool_router.session.create(user_id="wire@example.com")),
    # an integer written into a spec `number` must stay an integer on the wire
    Case(
        "session.create.number-workbench",
        lambda c: c.tool_router.session.create(user_id="wire@example.com", workbench=WORKBENCH_INT_THRESHOLD),
    ),
    Case("session.retrieve", lambda c: c.tool_router.session.retrieve(SESSION_ID)),
    Case("session.retrieve.encoded-path", lambda c: c.tool_router.session.retrieve(ENCODED_SESSION_ID)),
    Case("session.retrieve.subdelims-path", lambda c: c.tool_router.session.retrieve(SUBDELIMS_SESSION_ID)),
    Case(
        "session.retrieve.extra-headers",
        lambda c: c.tool_router.session.retrieve(
            SESSION_ID, extra_headers={"x-team": "per-request-wins", "x-trace": "abc"}
        ),
        client_options={"default_headers": {"x-team": "overridden-by-default"}},
    ),
    Case("session.attach.default-body", lambda c: c.tool_router.session.attach(SESSION_ID)),
    Case(
        "session.attach.body",
        lambda c: c.tool_router.session.attach(SESSION_ID, experimental={"skip_cache": True}),
    ),
    Case("session.config_history.no-query", lambda c: c.tool_router.session.config_history(SESSION_ID)),
    Case(
        "session.config_history.query",
        lambda c: c.tool_router.session.config_history(SESSION_ID, cursor="c1", limit=5),
    ),
    Case(
        "session.execute",
        lambda c: c.tool_router.session.execute(
            SESSION_ID,
            tool_slug="GITHUB_GET_REPO",
            arguments={"owner": "composiohq", "repo": "composio"},
            enable_auto_workbench_offload=False,
        ),
    ),
    Case(
        "session.execute_meta",
        lambda c: c.tool_router.session.execute_meta(
            SESSION_ID,
            slug="COMPOSIO_SEARCH_TOOLS",
            arguments={"queries": [{"use_case": "send a message"}]},
        ),
    ),
    Case(
        "session.link",
        lambda c: c.tool_router.session.link(
            SESSION_ID, toolkit="github", callback_url="https://example.com/cb", alias="gh"
        ),
    ),
    # a URL must reach the wire exactly as written: same case, no appended path
    Case(
        "session.link.mixed-case-url",
        lambda c: c.tool_router.session.link(SESSION_ID, **LINK_MIXED_CASE_URL),
    ),
    Case("session.patch.default-body", lambda c: c.tool_router.session.patch(SESSION_ID)),
    Case(
        "session.patch.body",
        lambda c: c.tool_router.session.patch(SESSION_ID, manage_connections={"enable": False}),
    ),
    # an explicitly nulled field must reach the wire as JSON null, not be dropped
    Case(
        "session.patch.explicit-null",
        lambda c: c.tool_router.session.patch(SESSION_ID, multi_account=None),
    ),
    Case(
        "session.proxy_execute",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/repos/composiohq/composio",
            method="GET",
            toolkit_slug="github",
            parameters=PROXY_PARAMETERS,
        ),
    ),
    Case(
        "session.proxy_execute.body",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="POST",
            toolkit_slug="slack",
            body={"channel": "#general", "text": "hi"},
        ),
    ),
    # the aliased corner of the surface: `custom_connection_data`
    Case(
        "session.proxy_execute.ccd-oauth2",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="GET",
            toolkit_slug="gmail",
            custom_connection_data=CCD_OAUTH2_SNAKE,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-oauth1",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/1/members/me",
            method="GET",
            toolkit_slug="trello",
            custom_connection_data=CCD_OAUTH1_SNAKE,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-api-key",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/v1/pages",
            method="GET",
            toolkit_slug="notion",
            custom_connection_data=CCD_API_KEY_SNAKE,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-bearer-token",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/graphql",
            method="POST",
            toolkit_slug="linear",
            custom_connection_data=CCD_BEARER_TOKEN_SNAKE,
        ),
    ),
    # ---- value shapes: the wire must carry the caller's JSON types, not the
    # model's (see the `wire_corpus` literals for what each one pins) ----
    Case(
        "session.proxy_execute.ccd-number-int",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="GET",
            toolkit_slug="gmail",
            custom_connection_data=CCD_NUMBER_INT,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-number-float",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="GET",
            toolkit_slug="gmail",
            custom_connection_data=CCD_NUMBER_FLOAT,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-number-string",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="GET",
            toolkit_slug="gmail",
            custom_connection_data=CCD_NUMBER_STRING,
        ),
    ),
    Case(
        "session.proxy_execute.ccd-unmodellable-value",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/messages",
            method="GET",
            toolkit_slug="gmail",
            custom_connection_data=CCD_UNMODELLABLE_VALUE,
        ),
    ),
    Case(
        "session.proxy_execute.binary-body-url",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/upload",
            method="POST",
            toolkit_slug="gmail",
            binary_body=BINARY_BODY_URL,
        ),
    ),
    Case(
        "session.proxy_execute.binary-body-mixed-case-url",
        lambda c: c.tool_router.session.proxy_execute(
            SESSION_ID,
            endpoint="/upload",
            method="POST",
            toolkit_slug="gmail",
            binary_body=BINARY_BODY_MIXED_CASE_URL,
        ),
    ),
    Case(
        "session.search",
        lambda c: c.tool_router.session.search(
            SESSION_ID,
            queries=[{"use_case": "send a slack message", "known_fields": "channel"}],
            model="gpt-4o",
        ),
    ),
    Case("session.toolkits.no-query", lambda c: c.tool_router.session.toolkits(SESSION_ID)),
    Case(
        "session.toolkits.array-query",
        lambda c: c.tool_router.session.toolkits(
            SESSION_ID, toolkits=["github", "slack"], is_connected=True, limit=5, search="git"
        ),
    ),
    Case("session.tools.no-query", lambda c: c.tool_router.session.tools(SESSION_ID)),
    Case("session.tools.query", lambda c: c.tool_router.session.tools(SESSION_ID, cursor="c2", limit=3)),
    # ---- session.files (4 methods) ----
    Case(
        "files.list.no-query",
        lambda c: c.tool_router.session.files.list(MOUNT_ID, session_id=SESSION_ID),
    ),
    Case(
        "files.list.query",
        lambda c: c.tool_router.session.files.list(
            MOUNT_ID, session_id=SESSION_ID, cursor="n", limit=10, mount_relative_prefix="data/"
        ),
    ),
    Case(
        "files.delete",
        lambda c: c.tool_router.session.files.delete(
            MOUNT_ID, session_id=SESSION_ID, mount_relative_path="report.pdf"
        ),
    ),
    Case(
        "files.create_download_url",
        lambda c: c.tool_router.session.files.create_download_url(
            MOUNT_ID, session_id=SESSION_ID, mount_relative_path="report.pdf"
        ),
    ),
    Case(
        "files.create_upload_url",
        lambda c: c.tool_router.session.files.create_upload_url(
            MOUNT_ID, session_id=SESSION_ID, mount_relative_path="data/output.csv", mimetype="text/csv"
        ),
    ),
]


def _derived_invoke(call: DerivedCall) -> Callable[[Any], object]:
    """The derived call, spelled the oracle's way. A factory rather than a
    lambda in the loop, so each closure binds its own `call`."""
    positional, kwargs = oracle_call(call)

    def invoke(client: Any) -> object:
        method = resolve_accessor(client, call.oracle_accessor)
        return method(*positional, **kwargs)

    return invoke


def main() -> int:
    installed = importlib.import_module("composio_client._version").__version__
    if installed != ORACLE_VERSION:
        print(
            f"error: expected {ORACLE_PACKAGE} {ORACLE_VERSION}, found {installed}.\n"
            f"       run: {REGENERATE_COMMAND}",
            file=sys.stderr,
        )
        return 1

    ids = [case.id for case in CASES]
    if len(set(ids)) != len(ids):
        print("error: duplicate case ids in CASES", file=sys.stderr)
        return 1

    cases = [{"id": case.id, **capture(Composio, case)} for case in CASES]

    # One derived case per operation the oracle publishes, and the *names* of
    # the ones it does not. 1.43.0 stops at 64 of the operations this package
    # covers, and an operation with no oracle must read as "no evidence
    # available here" rather than as one more silently absent case.
    # The body+query collision, spelled the oracle's way. Our client keeps the
    # two apart (see MIGRATION.md / KTD5), so the prefixes exist only here.
    cases.append(
        {
            "id": "connected_accounts.refresh.body-and-query",
            **capture(
                Composio,
                Case(
                    "connected_accounts.refresh.body-and-query",
                    lambda c: c.connected_accounts.refresh(
                        "ca_wire_parity",
                        query_redirect_url="https://example.com/after-query",
                        body_redirect_url="https://example.com/after-body",
                        validate_credentials=True,
                    ),
                ),
            ),
        }
    )

    probe = Composio(api_key=API_KEY, base_url=BASE_URL)
    absent: list[str] = []
    for call in derived_calls():
        if resolve_accessor(probe, call.oracle_accessor) is None:
            absent.append(".".join(call.oracle_accessor))
            continue
        derived = Case(f"derived.{'.'.join(call.oracle_accessor)}", _derived_invoke(call))
        cases.append({"id": derived.id, **capture(Composio, derived)})
    probe.close()
    document = {
        "oracle": {
            "package": ORACLE_PACKAGE,
            "version": ORACLE_VERSION,
            "regenerate": REGENERATE_COMMAND,
            "note": (
                "Golden capture of the wire requests the Stainless client emits. Generated by "
                "scripts/capture_stainless_oracle.py; asserted by tests/test_wire_parity.py. "
                "Do not hand-edit."
            ),
        },
        "cases": cases,
        "absent": sorted(absent),
    }
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(cases)} cases ({len(absent)} operation(s) absent from the oracle) to {FIXTURE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
