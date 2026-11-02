import pytest

from zapros import Response
from zapros._constants import CHUNK_SIZE
from zapros._decoders import iter_chunks
from zapros._handlers._std._common import connection_wants_close


@pytest.fixture(scope="session")
def body() -> bytes:
    return b"x" * (4 * 1024 * 1024)


@pytest.fixture(scope="session")
def response_headers() -> list[tuple[str, str]]:
    return [
        ("Content-Type", "application/x-amz-json-1.0"),
        ("Content-Length", "204800"),
        ("Date", "Fri, 29 Aug 2026 00:00:00 GMT"),
        ("Server", "Server"),
        ("Connection", "keep-alive"),
        ("x-amzn-RequestId", "0f1b2c3d-4e5f-6071-8293-a4b5c6d7e8f9"),
        ("x-amz-crc32", "1234567890"),
    ]


@pytest.fixture(scope="session")
def body_chunks(body: bytes) -> list[bytes]:
    socket_sized_inbound_pease_size = 64 * 1024
    return [body[i : i + socket_sized_inbound_pease_size] for i in range(0, len(body), socket_sized_inbound_pease_size)]


@pytest.fixture(
    scope="session",
    params=[
        pytest.param(1024, id="1KiB"),
        pytest.param(CHUNK_SIZE // 2, id="8KiB"),
        pytest.param(CHUNK_SIZE, id="16KiB"),
        pytest.param(64 * 1024, id="64KiB"),
        pytest.param(1024 * 1024, id="1MiB"),
        pytest.param(4 * 1024 * 1024, id="4MiB"),
        pytest.param(8 * 1024 * 1024, id="8MiB"),
    ],
)
def single_feed_body(request: pytest.FixtureRequest, body: bytes) -> bytes:
    return body[: request.param]


@pytest.mark.benchmark
def test_bench_iter_chunks_stream(body_chunks: list[bytes], body: bytes) -> None:
    total = sum(len(chunk) for piece in body_chunks for chunk in iter_chunks(piece, CHUNK_SIZE))
    assert total == len(body)


@pytest.mark.benchmark
def test_bench_iter_chunks_single_feed(single_feed_body: bytes) -> None:
    total = sum(len(c) for c in iter_chunks(single_feed_body, CHUNK_SIZE))
    assert total == len(single_feed_body)


@pytest.mark.benchmark
def test_bench_iter_bytes_identity_e2e(body_chunks: list[bytes], body: bytes) -> None:
    response = Response(200, content=iter(body_chunks))
    assert sum(len(c) for c in response.iter_bytes()) == len(body)


@pytest.mark.benchmark
def test_bench_connection_wants_close(response_headers: list[tuple[str, str]]) -> None:
    assert connection_wants_close(response_headers) is False
