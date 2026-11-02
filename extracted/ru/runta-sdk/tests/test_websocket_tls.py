from concurrent.futures import ThreadPoolExecutor
import ssl
from unittest.mock import Mock

import pytest

from runta._internal import streaming_transfer as transfer
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.sync_http import _SyncHttpClient


def test_context_initializes_once_under_concurrent_use(monkeypatch):
    factory = Mock(wraps=ssl.create_default_context)
    monkeypatch.setattr(transfer.ssl, "create_default_context", factory)
    provider = transfer._WebSocketTLS()
    assert factory.call_count == 0
    with ThreadPoolExecutor(max_workers=16) as pool:
        contexts = list(pool.map(lambda _: provider.context(), range(64)))
    assert len({id(context) for context in contexts}) == 1
    assert factory.call_count == 1
    assert contexts[0].verify_mode == ssl.CERT_REQUIRED
    assert contexts[0].check_hostname


@pytest.mark.parametrize("sync", [False, True])
def test_sockets_reuse_context_only_for_secure_connections(monkeypatch, sync):
    connection = Mock()
    monkeypatch.setattr(
        transfer, "sync_connect" if sync else "async_connect", connection
    )
    provider = transfer._WebSocketTLS()
    socket = transfer._sync_socket if sync else transfer._async_socket
    socket("http://localhost", "token", "id", 1, _tls=provider)
    assert "ssl" not in connection.call_args.kwargs
    assert provider._context is None
    socket("https://localhost", "token", "id", 1, _tls=provider)
    first = connection.call_args.kwargs["ssl"]
    socket("https://localhost", "token", "id", 1, _tls=provider)
    assert connection.call_args.kwargs["ssl"] is first


def test_tls_configuration_is_owned_by_each_sdk_client():
    clients = [
        _SyncHttpClient("https://test", "token"),
        _AsyncHttpClient("https://test", "token"),
    ]
    assert clients[0]._websocket_tls is not clients[1]._websocket_tls
    assert clients[0]._websocket_tls._context is None
    assert clients[1]._websocket_tls._resumption is None


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_reused_context_still_rejects_untrusted_certificate(tmp_path, sync):
    import asyncio
    import subprocess
    from websockets.asyncio.server import serve

    cert, key = tmp_path / "cert.pem", tmp_path / "key.pem"
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            str(key),
            "-out",
            str(cert),
            "-days",
            "1",
            "-subj",
            "/CN=localhost",
            "-addext",
            "subjectAltName=DNS:localhost",
        ],
        check=True,
        capture_output=True,
    )
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.load_cert_chain(cert, key)

    async def handler(socket):
        await socket.wait_closed()

    provider = transfer._WebSocketTLS()
    async with serve(handler, "127.0.0.1", 0, ssl=server_context) as server:
        endpoint = f"https://localhost:{server.sockets[0].getsockname()[1]}"
        for _ in range(2):
            with pytest.raises(ssl.SSLCertVerificationError):
                if sync:

                    def connect():
                        with transfer._sync_socket(
                            endpoint, "token", "id", 2, _tls=provider
                        ):
                            pass

                    await asyncio.to_thread(connect)
                else:
                    async with transfer._async_socket(
                        endpoint, "token", "id", 2, _tls=provider
                    ):
                        pass
