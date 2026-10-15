"""3.1.0: ApiPostgreSQLManager (`/db/execute` proxy)

- proxy が処理の前に返す 503 (退避の `draining` + Retry-After、呼び出し元の Pod を確かめられない `caller binding
  unavailable`) は Retry-After 以上待って送り直す。他の 503 / 5xx は処理の後かもしれないので送り直さない。最後の試行
  では今までどおり API_ERROR
- 使っていない接続は 4 秒で捨てる (proxy の uvicorn は 5 秒で閉じる)。接続数の上限は httpx の既定 (100 / 20) のまま
- headers_provider: 要求ごとに足すヘッダ。Authorization・Host 等は上書きできない。送れない名前・値・例外は足さない
  (本物の httpx の client と MockTransport で確かめる)
"""
import httpx
import pytest

import agenticstar_platform.db.api_manager as am
from agenticstar_platform.db.api_manager import ApiPostgreSQLManager
from agenticstar_platform.db.config import PostgreSQLConfig

DRAIN = '{"detail":"cli-api is draining for memory recycle, retry on another replica"}'


class _Resp:
    def __init__(self, status=200, text='{"success": true, "data": []}', headers=None):
        self.status_code, self.text, self.headers = status, text, httpx.Headers(headers or {})

    def json(self):
        import json
        return json.loads(self.text)


class _Client:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    async def post(self, url, json=None, headers=None):
        self.calls.append(headers)
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


@pytest.fixture
def waits(monkeypatch):
    out = []

    async def _sleep(sec):
        out.append(sec)

    monkeypatch.setattr(am.asyncio, "sleep", _sleep)
    monkeypatch.setattr(am.random, "random", lambda: 0.5)  # jitter 0
    return out


def _mgr(monkeypatch, responses, **kw):
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok", **kw)
    client = _Client(responses)

    async def _get(_timeout):
        return client

    monkeypatch.setattr(mgr, "_get_http_client", _get)
    return mgr, client


async def test_drain_503_is_resent_after_retry_after(monkeypatch, waits):
    mgr, client = _mgr(monkeypatch, [_Resp(503, DRAIN, {"Retry-After": "3"}), _Resp(503, DRAIN, {"Retry-After": "1"}), _Resp()])
    out = await mgr._api_request("execute", "INSERT INTO t VALUES ($1)", (1,))
    assert out == {"success": True, "data": []}
    assert len(client.calls) == 3
    assert waits == [3.0, 2.0]  # max(Retry-After, 1 s / 2 s の backoff)


async def test_retry_after_is_capped(monkeypatch, waits):
    mgr, _ = _mgr(monkeypatch, [_Resp(503, DRAIN, {"Retry-After": "3600"}), _Resp()])
    await mgr._api_request("execute", "SELECT 1", ())
    assert waits == [am._DRAIN_RETRY_AFTER_CAP_SEC]


async def test_caller_binding_unavailable_is_resent(monkeypatch, waits):
    """P-07 の束縛が K8s の読み取りに失敗したときの 503 も処理の前に返る (cli-api の auth middleware)"""
    body = '{"detail":"caller binding unavailable (retryable)"}'
    mgr, client = _mgr(monkeypatch, [_Resp(503, body), _Resp()])
    out = await mgr._api_request("execute", "INSERT INTO t VALUES ($1)", (1,))
    assert out["success"] is True and len(client.calls) == 2 and waits == [1.0]


@pytest.mark.parametrize("retry_after", ["nan", "inf", "-5", "Wed, 21 Oct 2015 07:28:00 GMT", "x", ""])
async def test_unusable_retry_after_falls_back_to_the_backoff(monkeypatch, waits, retry_after):
    mgr, _ = _mgr(monkeypatch, [_Resp(503, DRAIN, {"Retry-After": retry_after}), _Resp()])
    await mgr._api_request("execute", "SELECT 1", ())
    assert waits == [1.0]


async def test_retry_after_as_an_http_date_is_honoured(monkeypatch, waits):
    import email.utils
    import time

    later = email.utils.formatdate(time.time() + 6, usegmt=True)
    mgr, _ = _mgr(monkeypatch, [_Resp(503, DRAIN, {"Retry-After": later}), _Resp()])
    await mgr._api_request("execute", "SELECT 1", ())
    assert 4.0 <= waits[0] <= 6.0


@pytest.mark.parametrize("resp", [
    _Resp(503, '{"detail":"database unavailable"}', {"Retry-After": "1"}),  # 処理の後かもしれない 503
    # proxy 以外 (途中の中継など) が返した 503 は、本文に draining を含んでも送り直さない (処理の後かもしれない)
    _Resp(503, '<html>upstream draining</html>', {"Retry-After": "1"}),
    _Resp(503, '{"detail":"service draining"}', {"Retry-After": "1"}),
    _Resp(503, '{"error":"cli-api is draining for memory recycle, retry on another replica"}'),
    _Resp(503, '{"detail":[]}'), _Resp(503, '{"detail":{}}'), _Resp(503, '[]'), _Resp(503, 'not json'),
    _Resp(502, DRAIN),
    _Resp(500, "boom"),
])
async def test_other_errors_are_not_resent(monkeypatch, waits, resp):
    mgr, client = _mgr(monkeypatch, [resp, _Resp()])
    out = await mgr._api_request("execute", "INSERT INTO t VALUES ($1)", (1,))
    assert out["success"] is False and out["error_code"] == "API_ERROR"
    assert len(client.calls) == 1 and waits == []


async def test_drain_on_every_attempt_returns_the_api_error_after_the_budget(monkeypatch, waits):
    mgr, client = _mgr(monkeypatch, [_Resp(503, DRAIN, {"Retry-After": "1"})] * am._CONNECT_RETRY_MAX_ATTEMPTS)
    out = await mgr._api_request("execute", "SELECT 1", ())
    assert out["error_code"] == "API_ERROR" and "503" in out["error"]
    assert len(client.calls) == am._CONNECT_RETRY_MAX_ATTEMPTS and len(waits) == am._CONNECT_RETRY_MAX_ATTEMPTS - 1


async def test_drain_and_connect_errors_share_one_budget(monkeypatch, waits):
    seq = [_Resp(503, DRAIN, {"Retry-After": "1"}), httpx.ConnectError("refused")] * 2 + [_Resp()]
    mgr, client = _mgr(monkeypatch, seq)
    out = await mgr._api_request("execute", "SELECT 1", ())
    assert out["success"] is True and len(client.calls) == 5 and waits == [1.0, 2.0, 4.0, 8.0]


def _real_mgr(provider=None):
    """本物の httpx.AsyncClient (MockTransport) で送る。h11 / httpx が送れないヘッダはここで例外になる"""
    seen = []

    def handler(request):
        seen.append(request.headers)
        return httpx.Response(200, json={"success": True, "data": []})

    kw = {"headers_provider": provider} if provider is not None else {}
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok", **kw)
    mgr._http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler), limits=am._HTTP_LIMITS)
    return mgr, seen


async def test_headers_provider_adds_only_sendable_headers():
    provided = {"X-Execution-Id": "conv-1", "X-Conversation-Id": "conv-1", "X-Spaced": "a b",
                "authorization": "Bearer stolen", "Host": "evil", "Content-Type": "text/plain", "Content-Length": "1",
                "X-Bad": "a\r\nInjected: 1", "X-Jp": "会話", "X-Pad": " v ", "X Bad": "v", "X-Id:": "v", "会話": "v",
                "X-Empty": "", "X-None": None, "X-Bool": True, "X-Num": 7, "X-Nl": "value\n", "X-Nl2\n": "v"}
    mgr, seen = _real_mgr(lambda: provided)
    out = await mgr._api_request("execute", "SELECT 1", ())
    assert out == {"success": True, "data": []}
    h = seen[0]
    assert h["authorization"] == "Bearer tok" and h["host"] == "cli-api:8100" and h["content-type"] == "application/json"
    assert h["x-execution-id"] == "conv-1" and h["x-conversation-id"] == "conv-1" and h["x-spaced"] == "a b"
    assert h["x-num"] == "7"
    for name in ("x-bad", "x-jp", "x-pad", "x-empty", "x-none", "x-bool", "x-nl", "x-nl2"):
        assert name not in h
    await mgr.close()


def test_every_added_header_passes_h11_validation():
    """MockTransport は h11 の検査を通らないので、足したヘッダを h11 そのもので確かめる"""
    import h11

    provided = {"X-Ok": "conv-1", "X-Nl": "value\n", "X-Nl2\n": "v", "X-Tab": "a\tb", "X-Sp": "a b", "X-Del": "a\x7f"}
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok",
                               headers_provider=lambda: provided)
    extra = mgr._extra_headers()
    assert extra == {"X-Ok": "conv-1", "X-Sp": "a b"}
    h11.Request(method="POST", target="/db/execute", headers=[("Host", "cli-api"), *extra.items()])


@pytest.mark.parametrize("provider", [lambda: None, lambda: {}, lambda: 1 / 0, lambda: "X-A: b"])
async def test_headers_provider_failures_change_nothing(provider):
    mgr, seen = _real_mgr(provider)
    out = await mgr._api_request("execute", "SELECT 1", ())
    assert out["success"] is True and "x-a" not in seen[0] and seen[0]["authorization"] == "Bearer tok"
    await mgr.close()


async def test_without_headers_provider_requests_are_as_before(monkeypatch, waits):
    mgr, client = _mgr(monkeypatch, [_Resp()])
    await mgr._api_request("execute", "SELECT 1", ())
    assert client.calls == [{"Authorization": "Bearer tok"}]


async def test_idle_connections_expire_before_the_proxy_closes_them(monkeypatch):
    seen = {}

    class _AC:
        def __init__(self, **kw):
            seen.update(kw)
            self.is_closed = False

    monkeypatch.setattr(am.httpx, "AsyncClient", _AC)
    mgr = ApiPostgreSQLManager(PostgreSQLConfig(api_url="http://cli-api:8100/db"), token_provider=lambda: "tok")
    await mgr._get_http_client(httpx.Timeout(30.0, connect=10.0))
    limits = seen["limits"]
    assert limits.keepalive_expiry == 4.0 < 5.0  # uvicorn の既定 keep-alive 5 秒より短い
    assert (limits.max_connections, limits.max_keepalive_connections) == (100, 20)  # httpx の既定のまま (無制限にしない)
