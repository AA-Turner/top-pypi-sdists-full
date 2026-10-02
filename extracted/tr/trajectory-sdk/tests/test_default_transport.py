import os
import socket
import ssl
import time
from collections import deque
from typing import Any

import httpx
import pytest

from trajectory import APITimeoutError, Client
from trajectory._base_client import _DefaultHttpxClient


class RecordingSocket:
  def __init__(self, responses: list[bytes], read_error: Exception | None = None) -> None:
    self.responses = deque(responses)
    self.read_error = read_error
    self.write_error: Exception | None = None
    self.options: list[tuple[int, int, int]] = []
    self.timeouts: list[float | None] = []
    self.sent = bytearray()
    self.closed = False
    self.read_socket, self.write_socket = socket.socketpair()
    self.options_at_first_send: list[tuple[int, int, int]] | None = None

  def setsockopt(self, level: int, option: int, value: int) -> None:
    self.options.append((level, option, value))

  def settimeout(self, value: float | None) -> None:
    self.timeouts.append(value)

  def send(self, data: bytes) -> int:
    if self.options_at_first_send is None:
      self.options_at_first_send = list(self.options)
    self.sent.extend(data)
    if self.write_error is not None:
      raise self.write_error
    return len(data)

  def recv(self, count: int) -> bytes:
    if self.read_error is not None:
      raise self.read_error
    return self.responses.popleft()

  def fileno(self) -> int:
    return -1 if self.closed else self.read_socket.fileno()

  def close(self) -> None:
    if not self.closed:
      self.read_socket.close()
      self.write_socket.close()
      self.closed = True


class RecordingNetwork:
  def __init__(self) -> None:
    self.addresses: list[tuple[str, int]] = []
    self.sockets: list[RecordingSocket] = []
    self.tls_contexts: list[ssl.SSLContext] = []
    self.tls_hosts: list[str] = []
    self.connect_error: Exception | None = None
    self.write_error: Exception | None = None
    self.connect_timeouts: list[float] = []
    self.read_error: Exception | None = None
    self.proxy_tunnel = False

  def connect(
    self, address: tuple[str, int], timeout: float, source_address: Any = None
  ) -> RecordingSocket:
    self.addresses.append(address)
    self.connect_timeouts.append(timeout)
    if self.connect_error is not None:
      raise self.connect_error
    responses = [
      b'HTTP/1.1 200 OK\r\nContent-Length: 11\r\nContent-Type: application/json\r\n\r\n{"ok":true}'
    ]
    if self.proxy_tunnel:
      responses.insert(0, b"HTTP/1.1 200 Connection Established\r\n\r\n")
    sock = RecordingSocket(responses, self.read_error)
    sock.write_error = self.write_error
    self.sockets.append(sock)
    return sock

  def wrap_tls(
    self, context: ssl.SSLContext, sock: RecordingSocket, **kwargs: Any
  ) -> RecordingSocket:
    self.tls_contexts.append(context)
    self.tls_hosts.append(kwargs["server_hostname"])
    return sock


@pytest.fixture
def network(monkeypatch: pytest.MonkeyPatch) -> RecordingNetwork:
  for name in tuple(os.environ):
    if name.lower().endswith("_proxy"):
      monkeypatch.delenv(name)
  result = RecordingNetwork()
  monkeypatch.setattr(socket, "create_connection", result.connect)
  monkeypatch.setattr(
    ssl.SSLContext,
    "wrap_socket",
    lambda context, sock, **kwargs: result.wrap_tls(context, sock, **kwargs),
  )
  return result


@pytest.mark.parametrize(
  ("options", "connect_timeout", "read_timeout"),
  [({}, 5.0, 600.0), ({"timeout": 120.0}, 120.0, 120.0)],
)
def test_default_network_deadlines_allow_slow_responses(
  network: RecordingNetwork,
  options: dict[str, Any],
  connect_timeout: float,
  read_timeout: float,
) -> None:
  with Client(api_key="test-key", base_url="https://api.example.com", **options) as sdk:
    assert sdk.get("/ping", cast_to=dict) == {"ok": True}
  assert network.connect_timeouts == [connect_timeout]
  assert network.sockets[0].timeouts[-1] == read_timeout


@pytest.mark.parametrize(
  ("client_options", "request_options", "copy_options", "http_options", "expected"),
  [
    ({}, {}, None, None, httpx.Timeout(600, connect=5)),
    ({}, {}, {}, None, httpx.Timeout(600, connect=5)),
    ({}, {}, None, {"timeout": 5}, httpx.Timeout(5)),
    ({}, {}, {}, {"timeout": 5}, httpx.Timeout(5)),
    ({}, {}, None, {}, httpx.Timeout(5)),
    ({"timeout": 120}, {}, None, {"timeout": 5}, httpx.Timeout(120)),
    ({"timeout": 120}, {"timeout": 9}, None, None, httpx.Timeout(9)),
    ({}, {"timeout": None}, None, None, httpx.Timeout(None)),
    ({}, {}, {"timeout": 60}, None, httpx.Timeout(60)),
  ],
)
def test_inference_preserves_explicit_deadlines_without_extra_retries(
  monkeypatch: pytest.MonkeyPatch,
  client_options: dict[str, Any],
  request_options: dict[str, Any],
  copy_options: dict[str, Any] | None,
  http_options: dict[str, Any] | None,
  expected: httpx.Timeout,
) -> None:
  requests = []

  def handle_request(request: httpx.Request) -> httpx.Response:
    requests.append(request)
    raise httpx.ReadTimeout("offline read timeout", request=request)

  monkeypatch.setattr(
    httpx.HTTPTransport, "handle_request", lambda _transport, request: handle_request(request)
  )
  http_client = (
    httpx.Client(transport=httpx.MockTransport(handle_request), **http_options)
    if http_options is not None
    else None
  )
  with Client(
    api_key="test-key", http_client=http_client, max_retries=0, **client_options
  ) as client:
    selected = client if copy_options is None else client.with_options(**copy_options)
    with pytest.raises(APITimeoutError):
      selected.chat.completions.create(
        model="model_test",
        messages=[{"role": "user", "content": "Question"}],
        **request_options,
      )

  assert len(requests) == 1
  assert requests[0].extensions["timeout"] == expected.as_dict()


@pytest.mark.parametrize("idle_name", ["TCP_KEEPIDLE", "TCP_KEEPALIVE"])
def test_default_client_enables_tcp_probes_before_request(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch, idle_name: str
) -> None:
  for name in ("TCP_KEEPIDLE", "TCP_KEEPALIVE"):
    monkeypatch.delattr(socket, name, raising=False)
  monkeypatch.setattr(socket, idle_name, 12345, raising=False)
  with Client(
    api_key="test-key", base_url="https://api.example.com", timeout=900, max_retries=0
  ) as sdk:
    assert sdk.get("/ping", cast_to=dict) == {"ok": True}
  assert network.addresses == [("api.example.com", 443)]
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in network.sockets[0].options_at_first_send
  assert (socket.IPPROTO_TCP, 12345, 60) in network.sockets[0].options_at_first_send
  assert network.sockets[0].sent.startswith(b"GET /ping HTTP/1.1\r\n")
  assert network.sockets[0].timeouts[-1] == 900


def test_system_without_idle_timer_still_enables_keepalive(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch
) -> None:
  for name in ("TCP_KEEPIDLE", "TCP_KEEPALIVE"):
    monkeypatch.delattr(socket, name, raising=False)
  with _DefaultHttpxClient() as client:
    assert client.get("http://api.example.com/ping").json() == {"ok": True}
  assert network.addresses == [("api.example.com", 80)]
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in network.sockets[0].options


def test_native_socket_enables_keepalive_with_sixty_second_idle_timer() -> None:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    for level, option, value in _DefaultHttpxClient._get_keepalive_options():
      sock.setsockopt(level, option, value)
    assert sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) != 0
    idle_option = socket.TCP_KEEPIDLE if hasattr(socket, "TCP_KEEPIDLE") else socket.TCP_KEEPALIVE
    assert sock.getsockopt(socket.IPPROTO_TCP, idle_option) == 60


@pytest.mark.parametrize(
  ("environment", "url", "expected_host", "tunnel"),
  [
    ({"HTTP_PROXY": "http://proxy.example:8080"}, "http://api.example.com", "proxy.example", False),
    (
      {"HTTPS_PROXY": "http://proxy.example:8080"},
      "https://api.example.com",
      "proxy.example",
      True,
    ),
    (
      {"https_proxy": "http://proxy.example:8080"},
      "https://api.example.com",
      "proxy.example",
      True,
    ),
    ({"ALL_PROXY": "http://proxy.example:8080"}, "http://api.example.com", "proxy.example", False),
    (
      {"HTTP_PROXY": "http://proxy.example:8080"},
      "https://api.example.com",
      "api.example.com",
      False,
    ),
    (
      {"HTTPS_PROXY": "http://proxy.example:8080", "NO_PROXY": "api.example.com"},
      "https://api.example.com",
      "api.example.com",
      False,
    ),
    (
      {"HTTPS_PROXY": "http://proxy.example:8080", "NO_PROXY": "*"},
      "https://api.example.com",
      "api.example.com",
      False,
    ),
    (
      {"HTTPS_PROXY": "http://proxy.example:8080", "NO_PROXY": "other.example.com"},
      "https://api.example.com",
      "proxy.example",
      True,
    ),
  ],
)
def test_proxy_environment_keeps_routing_and_socket_behavior(
  network: RecordingNetwork,
  monkeypatch: pytest.MonkeyPatch,
  environment: dict[str, str],
  url: str,
  expected_host: str,
  tunnel: bool,
) -> None:
  for key, value in environment.items():
    monkeypatch.setenv(key, value)
  network.proxy_tunnel = tunnel
  with _DefaultHttpxClient() as client:
    assert client.get(url).json() == {"ok": True}
  assert network.addresses[0][0] == expected_host
  assert all(option[1] != socket.SO_KEEPALIVE for option in network.sockets[0].options)


@pytest.mark.parametrize(
  ("name", "value"),
  [
    ("NO_PROXY", "api.example.com"),
    ("NO_PROXY", "other.example.com"),
    ("NO_PROXY", "*"),
    ("no_proxy", "api.example.com"),
  ],
)
def test_proxy_bypass_without_a_proxy_server_keeps_connections_alive(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch, name: str, value: str
) -> None:
  monkeypatch.setenv(name, value)
  with _DefaultHttpxClient() as client:
    assert client.get("https://api.example.com/ping").json() == {"ok": True}
  assert network.addresses == [("api.example.com", 443)]
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in network.sockets[0].options_at_first_send
  assert any(
    level == socket.IPPROTO_TCP and value == 60
    for level, _option, value in network.sockets[0].options
  )


def test_explicit_proxy_is_preserved(network: RecordingNetwork) -> None:
  network.proxy_tunnel = True
  with _DefaultHttpxClient(proxy="http://proxy.example:8080") as client:
    assert client.get("https://api.example.com/ping").json() == {"ok": True}
  assert network.addresses == [("proxy.example", 8080)]
  assert b"CONNECT api.example.com:443 HTTP/1.1" in network.sockets[0].sent
  assert all(option[1] != socket.SO_KEEPALIVE for option in network.sockets[0].options)


def test_trust_env_false_keeps_direct_transport(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch
) -> None:
  monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example:8080")
  with _DefaultHttpxClient(trust_env=False) as client:
    assert client.get("https://api.example.com/ping").json() == {"ok": True}
  assert network.addresses == [("api.example.com", 443)]
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in network.sockets[0].options


def test_custom_transport_keeps_its_socket_options(network: RecordingNetwork) -> None:
  transport = httpx.HTTPTransport(socket_options=[(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 0)])
  with _DefaultHttpxClient(transport=transport) as client:
    assert client.get("http://api.example.com/ping").json() == {"ok": True}
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 0) in network.sockets[0].options
  assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) not in network.sockets[0].options


def test_custom_mount_routes_without_default_socket_changes(network: RecordingNetwork) -> None:
  requests = []
  transport = httpx.MockTransport(lambda request: requests.append(request) or httpx.Response(200))
  with _DefaultHttpxClient(mounts={"https://custom.example.com": transport}) as client:
    assert client.get("https://custom.example.com").status_code == 200
    assert client.get("http://api.example.com").json() == {"ok": True}
  assert len(requests) == 1
  assert network.addresses == [("api.example.com", 80)]
  assert all(option[1] != socket.SO_KEEPALIVE for option in network.sockets[0].options)


def test_supplied_http_client_and_copies_keep_custom_transport(network: RecordingNetwork) -> None:
  requests = []
  transport = httpx.MockTransport(
    lambda request: requests.append(request) or httpx.Response(200, json={"ok": True})
  )
  http_client = httpx.Client(transport=transport, timeout=12)
  with Client(api_key="test-key", http_client=http_client, max_retries=0) as sdk:
    copied = sdk.with_options(timeout=17)
    assert sdk._client is http_client
    assert copied._client is http_client
    assert sdk.get("/ping", cast_to=dict) == {"ok": True}
    assert copied.get("/ping", cast_to=dict) == {"ok": True}
    assert sdk.timeout == http_client.timeout
    assert copied.timeout == 17
  assert len(requests) == 2
  assert http_client.is_closed
  assert not network.addresses


@pytest.mark.parametrize("verify", [True, False])
def test_tls_verification_is_not_replaced(network: RecordingNetwork, verify: bool) -> None:
  with _DefaultHttpxClient(verify=verify) as client:
    assert client.get("https://api.example.com").status_code == 200
  context = network.tls_contexts[0]
  assert context.verify_mode == (ssl.CERT_REQUIRED if verify else ssl.CERT_NONE)
  assert context.check_hostname == verify


def test_custom_tls_context_and_certificate_are_retained(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch
) -> None:
  context = ssl.create_default_context()
  loaded = []
  monkeypatch.setattr(
    ssl.SSLContext, "load_cert_chain", lambda self, *args: loaded.append((self, args))
  )
  with pytest.warns(DeprecationWarning, match="cert"):
    with _DefaultHttpxClient(verify=context, cert=("client.pem", "client.key")) as client:
      assert client.get("https://api.example.com").status_code == 200
  assert network.tls_contexts == [context]
  assert loaded == [(context, ("client.pem", "client.key"))]


@pytest.mark.parametrize("trust_env", [True, False])
def test_environment_ca_respects_trust_env(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch, trust_env: bool
) -> None:
  monkeypatch.setenv("SSL_CERT_FILE", "/missing-test-ca.pem")
  if trust_env:
    with pytest.raises(FileNotFoundError):
      _DefaultHttpxClient(trust_env=True)
    assert not network.addresses
  else:
    with _DefaultHttpxClient(trust_env=False) as client:
      assert client.get("https://api.example.com").status_code == 200


def test_connection_limit_remains_enforced(network: RecordingNetwork) -> None:
  with _DefaultHttpxClient(limits=httpx.Limits(max_connections=1), timeout=0) as client:
    with client.stream("GET", "http://api.example.com/first"):
      with pytest.raises(httpx.PoolTimeout):
        client.get("http://api.example.com/second")
  assert len(network.addresses) == 1


def test_disabled_pool_reuse_remains_disabled(network: RecordingNetwork) -> None:
  with _DefaultHttpxClient(limits=httpx.Limits(max_keepalive_connections=0)) as client:
    assert client.get("http://api.example.com/first").status_code == 200
    assert client.get("http://api.example.com/second").status_code == 200
  assert len(network.addresses) == 2
  assert all(sock.closed for sock in network.sockets)


@pytest.mark.parametrize("max_retries", [0, 1])
def test_socket_keepalive_does_not_add_connection_retries(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch, max_retries: int
) -> None:
  network.connect_error = socket.timeout("offline connection timeout")
  monkeypatch.setattr("trajectory._base_client.time.sleep", lambda _: None)
  with Client(api_key="test-key", max_retries=max_retries, timeout=7) as sdk:
    with pytest.raises(APITimeoutError):
      sdk.get("/ping", cast_to=dict)
  assert len(network.addresses) == 1 + max_retries


def test_read_timeout_and_single_request_remain_unchanged(network: RecordingNetwork) -> None:
  network.read_error = socket.timeout("offline read timeout")
  with Client(api_key="test-key", timeout=900, max_retries=0) as sdk:
    with pytest.raises(APITimeoutError):
      sdk.get("/ping", cast_to=dict)
  assert len(network.addresses) == 1
  assert network.sockets[0].timeouts[-1] == 900
  assert network.sockets[0].sent.count(b"GET /ping HTTP/1.1") == 1


@pytest.mark.parametrize("http1", [True, False])
def test_http_version_options_reach_the_wire(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch, http1: bool
) -> None:
  pytest.importorskip("h2")
  protocols = []
  monkeypatch.setattr(
    ssl.SSLContext, "set_alpn_protocols", lambda self, offered: protocols.append(offered)
  )
  network.write_error = OSError("offline stop after recording the protocol preface")
  with _DefaultHttpxClient(http1=http1, http2=True) as client:
    if http1:
      assert client.get("https://api.example.com/ping").status_code == 200
    else:
      with pytest.raises(httpx.WriteError):
        client.get("https://api.example.com/ping")
  assert ["http/1.1", "h2"] in protocols
  expected = b"GET /ping HTTP/1.1" if http1 else b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
  assert network.sockets[0].sent.startswith(expected)


def test_connection_expiry_remains_enforced(
  network: RecordingNetwork, monkeypatch: pytest.MonkeyPatch
) -> None:
  now = 0.0
  monkeypatch.setattr(time, "monotonic", lambda: now)
  with _DefaultHttpxClient(limits=httpx.Limits(keepalive_expiry=1)) as client:
    assert client.get("http://api.example.com/first").status_code == 200
    now = 2.0
    assert client.get("http://api.example.com/second").status_code == 200
  assert len(network.addresses) == 2


def test_separate_timeout_values_remain_effective(network: RecordingNetwork) -> None:
  timeout = httpx.Timeout(connect=2, read=900, write=3, pool=4)
  with _DefaultHttpxClient(timeout=timeout) as client:
    assert client.get("https://api.example.com/ping").status_code == 200
  assert network.connect_timeouts == [2]
  assert 3 in network.sockets[0].timeouts
  assert network.sockets[0].timeouts[-1] == 900
