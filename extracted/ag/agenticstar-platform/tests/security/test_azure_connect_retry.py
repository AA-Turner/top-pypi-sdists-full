"""Azure の要求を送る前の失敗 (プロキシの CONNECT 拒否・接続できない・接続の時間切れ) だけを送り直す (3.1.3)。

Marketplace の Pod は egress のサイドカー (Envoy) 経由で外へ出る。サイドカーの起動直後は上流につなげず CONNECT に
503 を返すので、ワークフロー型の Agent は最初の Content Safety の呼び出しで `SecurityAPIError` になっていた
(devdocs 3.2req reviews 06)。要求は Azure に届いていないので、送り直しても二重にならない。
応答を受けた後の失敗 (エラーの status・読み取りの時間切れ) は送り直さない。
"""

import asyncio

import httpx
import pytest

from agenticstar_platform.security import AzureSecurityClient, AzureSecurityConfig
from agenticstar_platform.security import azure as az
from agenticstar_platform.security.base import SecurityAPIError

pytestmark = pytest.mark.asyncio

_CS = "https://cs.invalid"
_LANG = "https://lang.invalid"


def _moderation_ok(_request):
    return httpx.Response(200, json={"categoriesAnalysis": [{"category": "Hate", "severity": 0}]})


def _shield_ok(_request):
    return httpx.Response(200, json={"userPromptAnalysis": {"attackDetected": False}, "documentsAnalysis": []})


def _pii_ok(request):
    import json

    docs = [{"id": d["id"], "entities": [], "warnings": []}
            for d in json.loads(request.content)["analysisInput"]["documents"]]
    return httpx.Response(200, json={"results": {"documents": docs, "errors": []}})


class _Flaky:
    """最初の fail_times 回は exc を上げ、その後は ok を返す。呼ばれた回数を数える。"""

    def __init__(self, exc_factory, fail_times, ok):
        self.calls = 0
        self._exc_factory = exc_factory
        self._fail_times = fail_times
        self._ok = ok

    def __call__(self, request):
        self.calls += 1
        if self.calls <= self._fail_times:
            raise self._exc_factory(request)
        return self._ok(request)


def _client(handler) -> AzureSecurityClient:
    client = AzureSecurityClient(AzureSecurityConfig(
        content_safety_endpoint=_CS, content_safety_api_key="k",
        language_endpoint=_LANG, language_api_key="k", pii_enabled=True,
        prompt_shield_enabled=True, moderation_enabled=True,
    ))
    client._http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


@pytest.fixture(autouse=True)
def _no_wait(monkeypatch):
    slept = []

    async def _sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(az.asyncio, "sleep", _sleep)
    return slept


def _proxy_503(request):
    return httpx.ProxyError("503 Service Unavailable", request=request)


async def test_moderation_retries_a_refused_connect_and_succeeds(_no_wait):
    handler = _Flaky(_proxy_503, 2, _moderation_ok)

    result = await _client(handler).check_content_moderation("hello")

    assert not result.blocked and result.error is None
    assert handler.calls == 3
    assert _no_wait == [0.5, 1.0]


async def test_prompt_shield_and_pii_use_the_same_retry():
    shield = _Flaky(lambda r: httpx.ConnectError("refused", request=r), 1, _shield_ok)
    assert not (await _client(shield).check_prompt_shield("hello")).attack_detected
    assert shield.calls == 2

    pii = _Flaky(lambda r: httpx.ConnectTimeout("timed out", request=r), 1, _pii_ok)
    result = await _client(pii).detect_pii("hello")
    assert result.success and result.masked_text == "hello"
    assert pii.calls == 2


async def test_gives_up_after_three_retries_with_the_same_error_as_before(_no_wait):
    handler = _Flaky(_proxy_503, 99, _moderation_ok)

    with pytest.raises(SecurityAPIError) as e:
        await _client(handler).check_content_moderation("hello")

    assert e.value.error_code == "REQUEST_ERROR"  # 従来と同じ変換
    assert handler.calls == 4
    assert _no_wait == [0.5, 1.0, 2.0]


@pytest.mark.parametrize("exc_factory", [
    lambda r: httpx.ReadTimeout("read timed out", request=r),     # 送った後の失敗
    lambda r: httpx.RemoteProtocolError("server closed", request=r),
])
async def test_failures_after_sending_are_not_retried(exc_factory, _no_wait):
    handler = _Flaky(exc_factory, 99, _moderation_ok)

    with pytest.raises(SecurityAPIError):
        await _client(handler).check_content_moderation("hello")

    assert handler.calls == 1 and _no_wait == []


async def test_error_status_is_not_retried(_no_wait):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(503, text="upstream unavailable")

    with pytest.raises(SecurityAPIError) as e:
        await _client(handler).check_content_moderation("hello")

    assert e.value.status_code == 503 and len(calls) == 1 and _no_wait == []


async def test_a_real_proxy_refusing_connect_raises_proxy_error():
    """httpx は、プロキシが CONNECT に 503 を返すと httpx.ProxyError を上げる (再試行の対象の型であることの確認)。"""

    async def _proxy(reader, writer):
        await reader.readuntil(b"\r\n\r\n")
        writer.write(b"HTTP/1.1 503 Service Unavailable\r\ncontent-length: 0\r\n\r\n")
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(_proxy, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    try:
        async with httpx.AsyncClient(proxy=f"http://127.0.0.1:{port}", timeout=5) as client:
            with pytest.raises(az._CONNECT_PHASE_ERRORS) as e:
                await client.post("https://cs.invalid/contentsafety/text:analyze", json={})
        assert isinstance(e.value, httpx.ProxyError)
    finally:
        server.close()
        await server.wait_closed()
