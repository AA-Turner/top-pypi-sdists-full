"""An http.* step's output never carries cookies or infrastructure headers.

A step result is stored, shown on pages (a Space block rendered `Set Cookie`, `Cf Ray`, `Etag`,
`X Envoy Upstream Service Time`) and handed to later steps. Status + body are the answer; only a
small allowlist of response headers rides along.
"""

from __future__ import annotations

import httpx
from matrx_graph.nodes.http.get import HttpGetConfig, HttpGetExecutor, HttpGetInput

_LEAKY = {
    "content-type": "application/json",
    "set-cookie": "__cf_bm=abc123; path=/; HttpOnly; Secure",
    "cf-ray": "8a1b2c3d4e5f-LAX",
    "etag": 'W/"deadbeef"',
    "x-envoy-upstream-service-time": "42",
    "server": "cloudflare",
}


def test_funnel_drops_cookies_and_infra_headers() -> None:
    from matrx_graph.nodes.http._shared import build_response_from_httpx

    resp = httpx.Response(200, json={"ok": True}, headers=_LEAKY)
    out = build_response_from_httpx(resp, "https://example.com", 5, 1000)
    assert out.status == 200 and out.body == {"ok": True}
    assert out.headers["content-type"] == "application/json"
    assert not any(k in out.headers for k in ("set-cookie", "cf-ray", "etag", "server"))
    assert "abc123" not in out.model_dump_json()


async def test_get_node_output_has_no_leaky_headers() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"a": 1}, headers=_LEAKY))
    original_init = httpx.AsyncClient.__init__

    def patched(self, *args, **kwargs):
        kwargs.pop("transport", None)
        original_init(self, *args, transport=transport, **kwargs)

    from unittest.mock import patch

    with patch.object(httpx.AsyncClient, "__init__", patched):
        out = await HttpGetExecutor().execute(
            ctx=None, inputs=HttpGetInput(url="https://example.com/x"), config=HttpGetConfig()  # type: ignore[arg-type]
        )
    assert out.status == "success"
    dumped = out.result.model_dump_json()
    assert "set-cookie" not in dumped and "cf-ray" not in dumped and "etag" not in dumped
