import json
import os
from unittest.mock import MagicMock

import grpc
import pytest
from dotenv import load_dotenv

from seltz import (
    AnswerResponse,
    AnswerStreamResponse,
    AsyncSeltz,
    Citation,
    Citations,
    Document,
    SearchResponse,
)
from seltz._types import Omit
from seltz.exceptions import SeltzAuthenticationError, SeltzConfigurationError
from seltz.services.answer_service import AsyncAnswerService
from seltz.services.monitor_service import AsyncMonitorService
from seltz.services.search_service import AsyncSearchService


async def _aiter(items):
    """Yield items as an async iterator, standing in for a server stream."""
    for item in items:
        yield item


load_dotenv()

HAS_API_KEY = bool(os.environ.get("SELTZ_API_KEY"))
needs_api_key = pytest.mark.skipif(not HAS_API_KEY, reason="SELTZ_API_KEY not set")


# ---------------------------------------------------------------------------
# Unit tests — no network calls
# ---------------------------------------------------------------------------


def test_init_raises_without_api_key(monkeypatch):
    """Raise SeltzConfigurationError when no API key is provided and env var is absent."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    with pytest.raises(SeltzConfigurationError):
        AsyncSeltz()


def test_init_raises_without_api_key_explicit_none(monkeypatch):
    """Raise SeltzConfigurationError when api_key=None is passed explicitly and env var is absent."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    with pytest.raises(SeltzConfigurationError):
        AsyncSeltz(api_key=None)


async def test_init_with_explicit_api_key(monkeypatch):
    """Store the API key passed directly to the constructor."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    client = AsyncSeltz(api_key="test-key")
    try:
        assert client._client.api_key == "test-key"
    finally:
        await client.close()


async def test_init_reads_api_key_from_env(monkeypatch):
    """Read the API key from the SELTZ_API_KEY environment variable when no key is passed."""
    monkeypatch.setenv("SELTZ_API_KEY", "env-key")
    client = AsyncSeltz()
    try:
        assert client._client.api_key == "env-key"
    finally:
        await client.close()


async def test_explicit_api_key_overrides_env(monkeypatch):
    """Use the explicitly passed API key instead of the one in the environment."""
    monkeypatch.setenv("SELTZ_API_KEY", "env-key")
    client = AsyncSeltz(api_key="explicit-key")
    try:
        assert client._client.api_key == "explicit-key"
    finally:
        await client.close()


async def test_default_endpoint():
    """Use grpc.seltz.ai as the default endpoint."""
    client = AsyncSeltz(api_key="test-key")
    try:
        assert client.endpoint == "grpc.seltz.ai"
    finally:
        await client.close()


async def test_init_insecure(monkeypatch):
    """Accept insecure=True without raising."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    client = AsyncSeltz(api_key="test-key", insecure=True)
    try:
        assert client._client.api_key == "test-key"
    finally:
        await client.close()


async def test_search_service_initialized():
    """Initialize the search service on construction."""
    client = AsyncSeltz(api_key="test-key")
    try:
        assert client._search is not None
    finally:
        await client.close()


async def test_answer_service_initialized():
    """Initialize the answer service on construction."""
    client = AsyncSeltz(api_key="test-key")
    try:
        assert client._answer is not None
    finally:
        await client.close()


async def test_monitor_service_initialized():
    """Initialize the monitor service on construction and expose it."""
    client = AsyncSeltz(api_key="test-key")
    try:
        assert client._monitor is not None
        assert client.monitor is client._monitor
        assert isinstance(client.monitor, AsyncMonitorService)
    finally:
        await client.close()


async def test_context_manager_closes_channel():
    """Exiting the async context manager closes the underlying channel."""
    client = AsyncSeltz(api_key="test-key")
    closed = {"called": False}
    real_close = client._client.channel.close

    async def tracking_close(*args, **kwargs):
        closed["called"] = True
        return await real_close(*args, **kwargs)

    client._client.channel.close = tracking_close

    async with client as entered:
        assert entered is client
        assert closed["called"] is False

    assert closed["called"] is True


@pytest.mark.parametrize("scope", ["news"])
async def test_search_valid_scope_does_not_raise(scope, monkeypatch):
    """Accept valid scope values without raising."""

    async def fake_search(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "seltz.services.search_service.AsyncSearchService.search", fake_search
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.search("query", scope=scope)
    finally:
        await client.close()


async def test_search_forwards_filter_params(monkeypatch):
    """Filter parameters are forwarded from AsyncSeltz.search() to AsyncSearchService.search()."""
    captured = {}

    async def fake_search(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.search_service.AsyncSearchService.search", fake_search
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.search(
            "AI news",
            from_date="2026-01-01",
            to_date="2026-05-01",
            include_domains=["techcrunch.com", "wired.com"],
            exclude_domains=["wikipedia.org"],
        )
    finally:
        await client.close()

    assert captured["from_date"] == "2026-01-01"
    assert captured["to_date"] == "2026-05-01"
    assert captured["include_domains"] == ["techcrunch.com", "wired.com"]
    assert captured["exclude_domains"] == ["wikipedia.org"]


async def test_search_omitted_filters_use_sentinel(monkeypatch):
    """Omitted filter parameters are passed as OMIT sentinel, not None."""
    captured = {}

    async def fake_search(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.search_service.AsyncSearchService.search", fake_search
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.search("query")
    finally:
        await client.close()

    assert isinstance(captured["include_domains"], Omit)
    assert isinstance(captured["exclude_domains"], Omit)
    assert isinstance(captured["from_date"], Omit)
    assert isinstance(captured["to_date"], Omit)


async def test_search_builds_request_and_returns_response():
    """search() builds a SearchRequest with provided fields and Bearer metadata, then returns the stub response."""
    channel = MagicMock()
    service = AsyncSearchService(channel, api_key="test-key")

    captured = {}

    async def fake_search(req, metadata=None, timeout=None):
        captured["req"] = req
        captured["metadata"] = metadata
        captured["timeout"] = timeout
        return SearchResponse(
            documents=[Document(url="https://example.com", content="hello")]
        )

    service._stub.Search = fake_search

    response = await service.search(
        "ai",
        max_results=3,
        scope="news",
        include_domains=["techcrunch.com"],
        from_date="2026-01-01",
    )

    assert captured["req"].query == "ai"
    assert captured["req"].api_key == "test-key"
    assert captured["req"].max_results == 3
    assert captured["req"].scope == "news"
    assert list(captured["req"].include_domains) == ["techcrunch.com"]
    assert captured["req"].from_date == "2026-01-01"
    assert ("authorization", "Bearer test-key") in captured["metadata"]
    assert captured["timeout"] == 30
    assert isinstance(response, SearchResponse)
    assert len(response.documents) == 1


async def test_search_omits_filters_when_not_provided():
    """Omitted scope/date filters are left unset on the request; repeated fields stay empty."""
    channel = MagicMock()
    service = AsyncSearchService(channel, api_key="test-key")

    captured = {}

    async def fake_search(req, metadata=None, timeout=None):
        captured["req"] = req
        return SearchResponse(documents=[])

    service._stub.Search = fake_search

    await service.search("ai")

    req = captured["req"]
    assert not req.HasField("scope")
    assert not req.HasField("from_date")
    assert not req.HasField("to_date")
    assert list(req.include_domains) == []
    assert list(req.exclude_domains) == []


async def test_answer_builds_request_and_returns_response():
    """answer() builds an AnswerRequest with all fields and Bearer metadata, then returns the stub response."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    async def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        captured["metadata"] = metadata
        captured["timeout"] = timeout
        return AnswerResponse(
            answer="An answer.", citations=[Citation(url="https://example.com")]
        )

    service._stub.Answer = fake_answer

    response = await service.answer("who is the CEO?", include_content=True)

    assert captured["req"].query == "who is the CEO?"
    assert captured["req"].api_key == "test-key"
    assert captured["req"].include_content is True
    assert ("authorization", "Bearer test-key") in captured["metadata"]
    assert captured["timeout"] == 30
    assert response.answer == "An answer."
    assert len(response.citations) == 1


async def test_answer_maps_unauthenticated_to_auth_error():
    """A gRPC UNAUTHENTICATED status is surfaced as SeltzAuthenticationError."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="bad-key")

    class FakeRpcError(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNAUTHENTICATED

        def details(self):
            return "invalid api key"

    async def fake_answer(req, metadata=None, timeout=None):
        raise FakeRpcError()

    service._stub.Answer = fake_answer

    with pytest.raises(SeltzAuthenticationError):
        await service.answer("who is the CEO?")


async def test_answer_forwards_params(monkeypatch):
    """query and include_content are forwarded from AsyncSeltz.answer() to AsyncAnswerService.answer()."""
    captured = {}

    async def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AsyncAnswerService.answer", fake_answer
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.answer("AI news", include_content=True)
    finally:
        await client.close()

    assert captured["query"] == "AI news"
    assert captured["include_content"] is True


async def test_answer_builds_request_with_scope():
    """A non-empty scope is forwarded verbatim onto the AnswerRequest."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    async def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    await service.answer("AI news", scope="news")

    assert captured["req"].scope == "news"
    assert captured["req"].HasField("scope")


async def test_answer_omits_scope_when_not_provided():
    """When scope is not provided, the field is left unset on the request
    (the server then falls back to the default scope)."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    async def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    await service.answer("AI news")

    assert not captured["req"].HasField("scope")
    assert not captured["req"].HasField("model")


async def test_answer_forwards_scope(monkeypatch):
    """scope is forwarded from AsyncSeltz.answer() to AsyncAnswerService.answer()."""
    captured = {}

    async def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AsyncAnswerService.answer", fake_answer
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.answer("AI news", scope="news")
    finally:
        await client.close()

    assert captured["scope"] == "news"


async def test_answer_builds_request_with_model():
    """A non-empty model (answer tier) is forwarded verbatim onto the AnswerRequest."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    async def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    await service.answer("who is the CEO?", model="seltz-pro")

    assert captured["req"].model == "seltz-pro"
    assert captured["req"].HasField("model")


async def test_answer_forwards_model(monkeypatch):
    """model is forwarded from AsyncSeltz.answer() to AsyncAnswerService.answer()."""
    captured = {}

    async def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AsyncAnswerService.answer", fake_answer
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        await client.answer("who is the CEO?", model="seltz-pro")
    finally:
        await client.close()

    assert captured["model"] == "seltz-pro"


async def test_answer_stream_builds_request_and_yields_events():
    """answer_stream() builds an AnswerStreamRequest with Bearer metadata and no
    deadline, then yields each event from the stub stream."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        captured["metadata"] = metadata
        return _aiter(
            [
                AnswerStreamResponse(
                    citations=Citations(citations=[Citation(url="https://example.com")])
                ),
                AnswerStreamResponse(text_delta="Hello"),
                AnswerStreamResponse(finish_reason="stop"),
            ]
        )

    service._stub.AnswerStream = fake_answer_stream

    events = [
        event
        async for event in service.answer_stream(
            "who is the CEO?", include_content=True
        )
    ]

    assert captured["req"].query == "who is the CEO?"
    assert captured["req"].api_key == "test-key"
    assert captured["req"].include_content is True
    assert ("authorization", "Bearer test-key") in captured["metadata"]
    assert len(events) == 3
    assert events[0].WhichOneof("event") == "citations"
    assert events[0].citations.citations[0].url == "https://example.com"
    assert events[1].WhichOneof("event") == "text_delta"
    assert events[1].text_delta == "Hello"
    assert events[2].WhichOneof("event") == "finish_reason"
    assert events[2].finish_reason == "stop"


async def test_answer_stream_maps_unauthenticated_to_auth_error():
    """A gRPC UNAUTHENTICATED status on the stream is surfaced as
    SeltzAuthenticationError when iteration begins."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="bad-key")

    class FakeRpcError(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNAUTHENTICATED

        def details(self):
            return "invalid api key"

    def fake_answer_stream(req, metadata=None):
        raise FakeRpcError()

    service._stub.AnswerStream = fake_answer_stream

    with pytest.raises(SeltzAuthenticationError):
        [event async for event in service.answer_stream("who is the CEO?")]


async def test_answer_stream_builds_request_with_scope():
    """A non-empty scope is forwarded verbatim onto the AnswerStreamRequest."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return _aiter([])

    service._stub.AnswerStream = fake_answer_stream

    [event async for event in service.answer_stream("AI news", scope="news")]

    assert captured["req"].scope == "news"
    assert captured["req"].HasField("scope")


async def test_answer_stream_omits_scope_when_not_provided():
    """When scope is not provided, the field is left unset on the stream request."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return _aiter([])

    service._stub.AnswerStream = fake_answer_stream

    [event async for event in service.answer_stream("AI news")]

    assert not captured["req"].HasField("scope")
    assert not captured["req"].HasField("model")


async def test_answer_stream_builds_request_with_model():
    """A non-empty model (answer tier) is forwarded verbatim onto the AnswerStreamRequest."""
    channel = MagicMock()
    service = AsyncAnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return _aiter([])

    service._stub.AnswerStream = fake_answer_stream

    [
        event
        async for event in service.answer_stream("who is the CEO?", model="seltz-pro")
    ]

    assert captured["req"].model == "seltz-pro"
    assert captured["req"].HasField("model")


async def test_answer_stream_forwards_params(monkeypatch):
    """query, include_content, scope, and model are forwarded from
    AsyncSeltz.answer_stream() to AsyncAnswerService.answer_stream()."""
    captured = {}

    def fake_answer_stream(*args, **kwargs):
        captured.update(kwargs)
        return _aiter([])

    monkeypatch.setattr(
        "seltz.services.answer_service.AsyncAnswerService.answer_stream",
        fake_answer_stream,
    )
    client = AsyncSeltz(api_key="test-key")
    try:
        [
            event
            async for event in client.answer_stream(
                "AI news", include_content=True, scope="news", model="seltz-pro"
            )
        ]
    finally:
        await client.close()

    assert captured["query"] == "AI news"
    assert captured["include_content"] is True
    assert captured["scope"] == "news"
    assert captured["model"] == "seltz-pro"


# ---------------------------------------------------------------------------
# Integration tests — require SELTZ_API_KEY
# ---------------------------------------------------------------------------


@pytest.mark.integration
@needs_api_key
async def test_search_returns_response():
    """Return a SearchResponse instance for a standard query."""
    async with AsyncSeltz() as client:
        response = await client.search("best ai search engines")
    assert isinstance(response, SearchResponse)


@pytest.mark.integration
@needs_api_key
async def test_search_returns_results():
    """Return at least one document for a non-empty query."""
    async with AsyncSeltz() as client:
        response = await client.search("best ai search engines", max_results=5)
    assert len(response.documents) > 0


@pytest.mark.integration
@needs_api_key
async def test_search_max_results_respected():
    """Return no more documents than the requested max_results."""
    async with AsyncSeltz() as client:
        response = await client.search("best ai search engines", max_results=3)
    assert len(response.documents) <= 3


@pytest.mark.integration
@needs_api_key
async def test_search_result_fields():
    """Each document in the response has url and content as strings."""
    async with AsyncSeltz() as client:
        response = await client.search("best ai search engines")
    for doc in response.documents:
        assert isinstance(doc.url, str)
        assert isinstance(doc.content, str)


@pytest.mark.integration
@needs_api_key
async def test_search_empty_query():
    """Return a SearchResponse without raising for an empty query string."""
    async with AsyncSeltz() as client:
        response = await client.search("")
    assert isinstance(response, SearchResponse)
    assert len(response.documents) == 0


@pytest.mark.integration
@needs_api_key
async def test_answer_returns_response():
    """Return an AnswerResponse with a non-empty markdown answer."""
    async with AsyncSeltz() as client:
        response = await client.answer("Who is Apple's next CEO?")
    assert isinstance(response, AnswerResponse)
    assert isinstance(response.answer, str)
    assert len(response.answer) > 0


@pytest.mark.integration
@needs_api_key
async def test_answer_returns_citations():
    """Return at least one citation, each carrying a URL string."""
    async with AsyncSeltz() as client:
        response = await client.answer("Who is Apple's next CEO?")
    assert len(response.citations) >= 1
    for citation in response.citations:
        assert isinstance(citation.url, str)


@pytest.mark.integration
@needs_api_key
async def test_answer_with_scope_returns_response():
    """answer(scope="news") reaches the live API and returns a non-empty answer."""
    async with AsyncSeltz() as client:
        response = await client.answer(
            "What is the latest news about AI?", scope="news"
        )
    assert isinstance(response, AnswerResponse)
    assert isinstance(response.answer, str)
    assert len(response.answer) > 0


@pytest.mark.integration
@needs_api_key
async def test_answer_stream_yields_events():
    """Streaming answer yields a leading citations event, text deltas, and a
    terminal finish_reason, reconstructing a non-empty answer."""
    kinds = []
    text = ""
    async with AsyncSeltz() as client:
        async for event in client.answer_stream("Who is Apple's next CEO?"):
            kind = event.WhichOneof("event")
            kinds.append(kind)
            if kind == "text_delta":
                text += event.text_delta

    assert kinds[0] == "citations"
    assert "text_delta" in kinds
    assert kinds[-1] == "finish_reason"
    assert len(text) > 0


@pytest.mark.integration
@needs_api_key
async def test_answer_with_response_format_returns_json():
    """answer(response_format=...) reaches the live API and returns an answer
    that is a JSON string conforming to the requested schema; citations are
    still returned."""
    async with AsyncSeltz() as client:
        response = await client.answer(
            "Summarize the latest AI news",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "news_summary",
                    "schema": {
                        "type": "object",
                        "properties": {"summary": {"type": "string"}},
                        "required": ["summary"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        )
    assert isinstance(response, AnswerResponse)
    payload = json.loads(response.answer)
    assert isinstance(payload["summary"], str)
    assert len(response.citations) > 0
