"""Issue #30's reproductions, run against whatever ``composio_client`` is installed.

The offline suite proves the annotations are right and that the construction
path builds models from them. Neither can see a *packaging* mistake, so this
runs the same reproductions against an installed distribution::

    uv run --isolated --no-project --refresh-package composio-client \
      --with dist/composio_client-<version>-py3-none-any.whl --with httpx \
      python scripts/verify_issue_30.py

Without arguments it runs against the current environment, which is faster
while iterating and is the same check one level less strict.

Every reproduction runs twice: once on the default path, and once with
``_strict_response_validation=True``. The default path is not sufficient on its
own -- ``_construct_response`` catches ``ValidationError`` and falls through, so
a restored annotation that disagreed with a real payload would present as the
same silent dict issue #30 reports rather than as a rejection. Strict mode is
the only lever that surfaces an oracle-versus-wire disagreement.

Exits non-zero on the first failed expectation, and prints the divergent-payload
timing so the adapter memoization has a reviewable number behind it.
"""

from __future__ import annotations

import json
import time
from typing import Any

import httpx
from pydantic import TypeAdapter

from composio_client import Composio, ProjectAuth, _base_client
from composio_client.types.mcp.custom_create_response import Commands, CustomCreateResponse
from composio_client.types.tool_router.session_toolkits_response import (
    Item,
    ItemConnectedAccount,
    ItemMeta,
    SessionToolkitsResponse,
)

BASE_URL = "https://api.invalid"

MCP_PAYLOAD: dict[str, Any] = {
    "id": "mcp_1",
    "name": "n",
    "mcp_url": "https://x",
    "allowed_tools": ["A"],
    "auth_config_ids": ["ac_1"],
    "commands": {"claude": "c", "cursor": "cu", "windsurf": "w"},
}

TOOLKITS_PAYLOAD: dict[str, Any] = {
    "current_page": 1,
    "total_items": 1,
    "total_pages": 1,
    "next_cursor": None,
    "items": [
        {
            "slug": "gmail",
            "name": "Gmail",
            "enabled": True,
            "is_no_auth": False,
            "composio_managed_auth_schemes": ["OAUTH2"],
            "meta": {"description": "d", "logo": "https://logo"},
            "connected_account": {
                "id": "ca_1",
                "status": "ACTIVE",
                "user_id": "u_1",
                "created_at": "2026-08-20T00:00:00Z",
                "auth_config": {"id": "ac_1", "auth_scheme": "OAUTH2", "is_composio_managed": True},
            },
        }
    ],
}

AUTH_CONFIG_PAYLOAD: dict[str, Any] = {
    "auth_config": {"id": "ac_1", "auth_scheme": "OAUTH2", "is_composio_managed": True},
    "toolkit": {"slug": "gmail"},
}

failures: list[str] = []


def _time_divergent(payload: dict[str, Any]) -> float:
    with client(payload, strict=False) as composio:
        composio.tool_router.session.toolkits("s_1")  # warm
        start = time.perf_counter()
        for _ in range(20):
            composio.tool_router.session.toolkits("s_1")
        return time.perf_counter() - start


def check(label: str, condition: bool, detail: str = "") -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {label}{'' if condition else f'  -- {detail}'}")
    if not condition:
        failures.append(label)


def client(payload: dict[str, Any], *, strict: bool) -> Composio:
    transport = httpx.MockTransport(lambda _request: httpx.Response(200, json=payload))
    return Composio(
        auth=ProjectAuth("verify-issue-30"),
        base_url=BASE_URL,
        http_client=httpx.Client(transport=transport),
        _strict_response_validation=strict,
    )


def main() -> int:
    # The issue's two reproductions, verbatim.
    mcp = CustomCreateResponse.model_validate(MCP_PAYLOAD)
    check(
        "CustomCreateResponse.commands is Commands",
        type(mcp.commands) is Commands,
        str(type(mcp.commands)),
    )
    check("r.commands.claude resolves", mcp.commands.claude == "c")

    toolkits = SessionToolkitsResponse.model_validate(TOOLKITS_PAYLOAD)
    check("items[0] is Item", type(toolkits.items[0]) is Item, str(type(toolkits.items[0])))
    check("items[0].slug resolves", toolkits.items[0].slug == "gmail")

    # The three downstream call paths the issue names, through the client, on
    # both the default and the strict path.
    for strict in (False, True):
        mode = "strict" if strict else "default"

        with client(MCP_PAYLOAD, strict=strict) as composio:
            created = composio.mcp.custom.create(allowed_tools=["A"], auth_config_ids=["ac_1"], name="n")
            check(f"[{mode}] mcp.custom.create().commands.claude", created.commands.claude == "c")

        with client(TOOLKITS_PAYLOAD, strict=strict) as composio:
            listed = composio.tool_router.session.toolkits("s_1")
            item = listed.items[0]
            check(f"[{mode}] session.toolkits() item.slug", item.slug == "gmail")
            check(f"[{mode}] session.toolkits() item.meta.logo", isinstance(item.meta, ItemMeta))
            check(
                f"[{mode}] session.toolkits() nested auth config",
                isinstance(item.connected_account, ItemConnectedAccount)
                and item.connected_account.auth_config.id == "ac_1",
            )

        with client(AUTH_CONFIG_PAYLOAD, strict=strict) as composio:
            auth = composio.auth_configs.create(toolkit={"slug": "gmail"})
            check(f"[{mode}] auth_configs.create().auth_config.id", auth.auth_config.id == "ac_1")

    # A payload that diverges from a restored annotation drives every optional
    # field through the union branch's fallback -- the path the adapter cache
    # exists for. Measure it against its own uncached baseline rather than
    # printing one absolute number: machines differ, so the ratio is the claim.
    divergent = json.loads(json.dumps(TOOLKITS_PAYLOAD))
    item = divergent["items"][0]
    item["connected_account"]["status"] = {"unexpected": "object"}
    divergent["items"] = [json.loads(json.dumps(item)) for _ in range(100)]

    memoized = _time_divergent(divergent)
    cached_adapter = _base_client._adapter
    # The pre-memoization baseline: one adapter built per call.
    _base_client._adapter = lambda type_: TypeAdapter(type_)
    try:
        uncached = _time_divergent(divergent)
    finally:
        _base_client._adapter = cached_adapter

    print(
        f"INFO  20 x 100-item divergent list: {memoized * 1000:.0f} ms memoized, "
        f"{uncached * 1000:.0f} ms uncached ({uncached / memoized:.1f}x)"
    )
    check("memoization is not a regression", memoized <= uncached, f"{memoized:.3f}s vs {uncached:.3f}s")

    print()
    print("FAILURES:", failures or "none")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
