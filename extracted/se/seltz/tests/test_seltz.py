import json
import os
from unittest.mock import MagicMock

import grpc
import pytest
from dotenv import load_dotenv

from seltz import (
    AnswerResponse,
    AnswerStreamResponse,
    Citation,
    Citations,
    SearchResponse,
    Seltz,
)
from seltz.services.monitor_service import MonitorService
from seltz.exceptions import (
    SeltzAPIError,
    SeltzAuthenticationError,
    SeltzConfigurationError,
)
from seltz.services.answer_service import AnswerService

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
        Seltz()


def test_init_raises_without_api_key_explicit_none(monkeypatch):
    """Raise SeltzConfigurationError when api_key=None is passed explicitly and env var is absent."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    with pytest.raises(SeltzConfigurationError):
        Seltz(api_key=None)


def test_init_with_explicit_api_key(monkeypatch):
    """Store the API key passed directly to the constructor."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    client = Seltz(api_key="test-key")
    assert client._client.api_key == "test-key"


def test_init_reads_api_key_from_env(monkeypatch):
    """Read the API key from the SELTZ_API_KEY environment variable when no key is passed."""
    monkeypatch.setenv("SELTZ_API_KEY", "env-key")
    client = Seltz()
    assert client._client.api_key == "env-key"


def test_explicit_api_key_overrides_env(monkeypatch):
    """Use the explicitly passed API key instead of the one in the environment."""
    monkeypatch.setenv("SELTZ_API_KEY", "env-key")
    client = Seltz(api_key="explicit-key")
    assert client._client.api_key == "explicit-key"


def test_default_endpoint():
    """Use grpc.seltz.ai as the default endpoint."""
    client = Seltz(api_key="test-key")
    assert client.endpoint == "grpc.seltz.ai"


def test_init_insecure(monkeypatch):
    """Accept insecure=True without raising."""
    monkeypatch.delenv("SELTZ_API_KEY", raising=False)
    client = Seltz(api_key="test-key", insecure=True)
    assert client._client.api_key == "test-key"


def test_search_service_initialized():
    """Initialize the search service on construction."""
    client = Seltz(api_key="test-key")
    assert client._search is not None


def test_monitor_service_initialized():
    """Initialize the monitor service on construction and expose it."""
    client = Seltz(api_key="test-key")
    assert client._monitor is not None
    assert client.monitor is client._monitor
    assert isinstance(client.monitor, MonitorService)


@pytest.mark.parametrize("scope", ["news"])
def test_search_valid_scope_does_not_raise(scope, monkeypatch):
    """Accept valid scope values without raising."""
    monkeypatch.setattr(
        "seltz.services.search_service.SearchService.search", lambda *a, **kw: None
    )
    client = Seltz(api_key="test-key")
    client.search("query", scope=scope)


def test_search_omitted_scope_does_not_raise(monkeypatch):
    """Not passing scope should not raise."""
    monkeypatch.setattr(
        "seltz.services.search_service.SearchService.search", lambda *a, **kw: None
    )
    client = Seltz(api_key="test-key")
    client.search("query")


def test_search_forwards_filter_params(monkeypatch):
    """Filter parameters are forwarded from Seltz.search() to SearchService.search()."""
    captured = {}

    def fake_search(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.search_service.SearchService.search", fake_search
    )
    client = Seltz(api_key="test-key")
    client.search(
        "AI news",
        from_date="2026-01-01",
        to_date="2026-05-01",
        include_domains=["techcrunch.com", "wired.com"],
        exclude_domains=["wikipedia.org"],
    )

    assert captured["from_date"] == "2026-01-01"
    assert captured["to_date"] == "2026-05-01"
    assert captured["include_domains"] == ["techcrunch.com", "wired.com"]
    assert captured["exclude_domains"] == ["wikipedia.org"]


def test_search_omitted_filters_use_sentinel(monkeypatch):
    """Omitted filter parameters are passed as OMIT sentinel, not None."""
    from seltz._types import Omit

    captured = {}

    def fake_search(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.search_service.SearchService.search", fake_search
    )
    client = Seltz(api_key="test-key")
    client.search("query")

    assert isinstance(captured["include_domains"], Omit)
    assert isinstance(captured["exclude_domains"], Omit)
    assert isinstance(captured["from_date"], Omit)
    assert isinstance(captured["to_date"], Omit)


def test_answer_service_initialized():
    """Initialize the answer service on construction."""
    client = Seltz(api_key="test-key")
    assert client._answer is not None


def test_context_manager_closes_channel():
    """Exiting the context manager closes the underlying channel."""
    client = Seltz(api_key="test-key")
    closed = {"called": False}
    real_close = client._client.channel.close

    def tracking_close(*args, **kwargs):
        closed["called"] = True
        return real_close(*args, **kwargs)

    client._client.channel.close = tracking_close

    with client as entered:
        assert entered is client
        assert closed["called"] is False

    assert closed["called"] is True


def test_answer_builds_request_and_returns_response():
    """answer() builds an AnswerRequest with all fields and Bearer metadata, then returns the stub response."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        captured["metadata"] = metadata
        captured["timeout"] = timeout
        return AnswerResponse(
            answer="An answer.", citations=[Citation(url="https://example.com")]
        )

    service._stub.Answer = fake_answer

    response = service.answer("who is the CEO?", include_content=True)

    assert captured["req"].query == "who is the CEO?"
    assert captured["req"].api_key == "test-key"
    assert captured["req"].include_content is True
    assert ("authorization", "Bearer test-key") in captured["metadata"]
    assert captured["timeout"] == 30
    assert response.answer == "An answer."
    assert len(response.citations) == 1


def test_answer_maps_unauthenticated_to_auth_error():
    """A gRPC UNAUTHENTICATED status is surfaced as SeltzAuthenticationError."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="bad-key")

    class FakeRpcError(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNAUTHENTICATED

        def details(self):
            return "invalid api key"

    def fake_answer(req, metadata=None, timeout=None):
        raise FakeRpcError()

    service._stub.Answer = fake_answer

    with pytest.raises(SeltzAuthenticationError):
        service.answer("who is the CEO?")


def test_answer_forwards_params(monkeypatch):
    """query and include_content are forwarded from Seltz.answer() to AnswerService.answer()."""
    captured = {}

    def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer", fake_answer
    )
    client = Seltz(api_key="test-key")
    client.answer("AI news", include_content=True)

    assert captured["query"] == "AI news"
    assert captured["include_content"] is True


def test_answer_builds_request_with_scope():
    """A non-empty scope is forwarded verbatim onto the AnswerRequest."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news", scope="news")

    assert captured["req"].scope == "news"
    assert captured["req"].HasField("scope")


def test_answer_omits_scope_when_not_provided():
    """When scope is not provided, the field is left unset on the request
    (the server then falls back to the default scope)."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news")

    assert not captured["req"].HasField("scope")
    assert not captured["req"].HasField("model")


def test_answer_forwards_scope(monkeypatch):
    """scope is forwarded from Seltz.answer() to AnswerService.answer()."""
    captured = {}

    def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer", fake_answer
    )
    client = Seltz(api_key="test-key")
    client.answer("AI news", scope="news")

    assert captured["scope"] == "news"


def test_answer_builds_request_with_model():
    """A non-empty model (answer tier) is forwarded verbatim onto the AnswerRequest."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("who is the CEO?", model="seltz-pro")

    assert captured["req"].model == "seltz-pro"
    assert captured["req"].HasField("model")


def test_answer_forwards_model(monkeypatch):
    """model is forwarded from Seltz.answer() to AnswerService.answer()."""
    captured = {}

    def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer", fake_answer
    )
    client = Seltz(api_key="test-key")
    client.answer("who is the CEO?", model="seltz-pro")

    assert captured["model"] == "seltz-pro"


def test_answer_builds_request_with_response_format():
    """A response_format object is JSON-encoded into the request's string field."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer='{"summary": "x"}', citations=[])

    service._stub.Answer = fake_answer

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "summary_answer",
            "schema": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
                "additionalProperties": False,
            },
        },
    }
    service.answer("AI news", response_format=response_format)

    assert captured["req"].HasField("response_format")
    # The proto field is a JSON-encoded string; it round-trips to the object.
    assert json.loads(captured["req"].response_format) == response_format


def test_answer_omits_response_format_when_not_provided():
    """When response_format is not provided, the field is left unset (the answer
    stays Markdown)."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news")

    assert not captured["req"].HasField("response_format")


def test_answer_none_response_format_omitted():
    """Passing response_format=None leaves the field unset (like OMIT), rather
    than JSON-encoding to the string "null" — matches OpenAI-SDK callers that
    pass None to mean "no structured output"."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news", response_format=None)

    assert not captured["req"].HasField("response_format")


def test_answer_forwards_response_format(monkeypatch):
    """response_format is forwarded from Seltz.answer() to AnswerService.answer()."""
    captured = {}

    def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer", fake_answer
    )
    client = Seltz(api_key="test-key")
    response_format = {"type": "json_object"}
    client.answer("AI news", response_format=response_format)

    assert captured["response_format"] == response_format


def test_answer_stream_builds_request_with_response_format():
    """response_format is JSON-encoded onto the AnswerStreamRequest as well."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([AnswerStreamResponse(text_delta='{"summary": "x"}')])

    service._stub.AnswerStream = fake_answer_stream

    response_format = {"type": "json_object"}
    list(service.answer_stream("AI news", response_format=response_format))

    assert captured["req"].HasField("response_format")
    assert json.loads(captured["req"].response_format) == response_format


def test_answer_builds_request_with_system_prompt():
    """A system_prompt is set verbatim on the request (no encoding)."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    system_prompt = "Answer in British English.\n\nBe terse."
    service.answer("AI news", system_prompt=system_prompt)

    assert captured["req"].HasField("system_prompt")
    # Plain string field — forwarded byte-for-byte, interior formatting intact.
    assert captured["req"].system_prompt == system_prompt


def test_answer_omits_system_prompt_when_not_provided():
    """When system_prompt is not provided, the field is left unset (the system
    prompt stays exactly the operator's)."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news")

    assert not captured["req"].HasField("system_prompt")


def test_answer_leaves_system_prompt_unset_when_none():
    """system_prompt=None behaves like "not provided".

    Parity with the response_format nit: there the value is JSON-encoded, so
    None became the *string* "null" and set the field. system_prompt is passed
    through unencoded, so protobuf treats None as absent on its own — pinned
    here so a future encoding step cannot reintroduce the bug silently.
    """
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news", system_prompt=None)

    assert not captured["req"].HasField("system_prompt")


def test_answer_leaves_system_prompt_unset_when_whitespace_only():
    """A whitespace-only system_prompt is treated as absent.

    The docstring promises "empty or whitespace-only is treated as absent," so
    the builder guard drops it client-side rather than sending a present-but-
    empty field and relying on server normalization.
    """
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news", system_prompt="   \n\t ")

    assert not captured["req"].HasField("system_prompt")


def test_answer_leaves_system_prompt_unset_when_empty():
    """An empty-string system_prompt is treated as absent, like whitespace."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer="An answer.", citations=[])

    service._stub.Answer = fake_answer

    service.answer("AI news", system_prompt="")

    assert not captured["req"].HasField("system_prompt")


def test_answer_stream_leaves_system_prompt_unset_when_whitespace_only():
    """The streaming builder drops whitespace-only the same way."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([AnswerStreamResponse(text_delta="An ")])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("AI news", system_prompt="   "))

    assert not captured["req"].HasField("system_prompt")


def test_answer_stream_leaves_system_prompt_unset_when_none():
    """The streaming builder drops None the same way."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([AnswerStreamResponse(text_delta="An ")])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("AI news", system_prompt=None))

    assert not captured["req"].HasField("system_prompt")


def test_answer_forwards_system_prompt(monkeypatch):
    """system_prompt is forwarded from Seltz.answer() to AnswerService.answer()."""
    captured = {}

    def fake_answer(*args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer", fake_answer
    )
    client = Seltz(api_key="test-key")
    client.answer("AI news", system_prompt="Answer in British English.")

    assert captured["system_prompt"] == "Answer in British English."


def test_answer_builds_request_with_system_prompt_and_response_format():
    """system_prompt and response_format compose on the same request."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer(req, metadata=None, timeout=None):
        captured["req"] = req
        return AnswerResponse(answer='{"summary": "x"}', citations=[])

    service._stub.Answer = fake_answer

    response_format = {"type": "json_object"}
    service.answer(
        "AI news",
        system_prompt="Answer in British English.",
        response_format=response_format,
    )

    assert captured["req"].system_prompt == "Answer in British English."
    assert json.loads(captured["req"].response_format) == response_format


def test_answer_stream_builds_request_with_system_prompt():
    """system_prompt is set on the AnswerStreamRequest as well."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([AnswerStreamResponse(text_delta="An ")])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("AI news", system_prompt="Answer in British English."))

    assert captured["req"].HasField("system_prompt")
    assert captured["req"].system_prompt == "Answer in British English."


def test_answer_stream_builds_request_and_yields_events():
    """answer_stream() builds an AnswerStreamRequest with Bearer metadata and no
    deadline, then yields each event from the stub stream."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        captured["metadata"] = metadata
        return iter(
            [
                AnswerStreamResponse(
                    citations=Citations(citations=[Citation(url="https://example.com")])
                ),
                AnswerStreamResponse(text_delta="Hello"),
                AnswerStreamResponse(finish_reason="stop"),
            ]
        )

    service._stub.AnswerStream = fake_answer_stream

    events = list(service.answer_stream("who is the CEO?", include_content=True))

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


def test_answer_stream_maps_unauthenticated_to_auth_error():
    """A gRPC UNAUTHENTICATED status on the stream is surfaced as
    SeltzAuthenticationError when iteration begins."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="bad-key")

    class FakeRpcError(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNAUTHENTICATED

        def details(self):
            return "invalid api key"

    def fake_answer_stream(req, metadata=None):
        raise FakeRpcError()

    service._stub.AnswerStream = fake_answer_stream

    with pytest.raises(SeltzAuthenticationError):
        list(service.answer_stream("who is the CEO?"))


def test_answer_stream_builds_request_with_scope():
    """A non-empty scope is forwarded verbatim onto the AnswerStreamRequest."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("AI news", scope="news"))

    assert captured["req"].scope == "news"
    assert captured["req"].HasField("scope")


def test_answer_stream_omits_scope_when_not_provided():
    """When scope is not provided, the field is left unset on the stream request."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("AI news"))

    assert not captured["req"].HasField("scope")
    assert not captured["req"].HasField("model")


def test_answer_stream_builds_request_with_model():
    """A non-empty model (answer tier) is forwarded verbatim onto the AnswerStreamRequest."""
    channel = MagicMock()
    service = AnswerService(channel, api_key="test-key")

    captured = {}

    def fake_answer_stream(req, metadata=None):
        captured["req"] = req
        return iter([])

    service._stub.AnswerStream = fake_answer_stream

    list(service.answer_stream("who is the CEO?", model="seltz-pro"))

    assert captured["req"].model == "seltz-pro"
    assert captured["req"].HasField("model")


def test_answer_stream_forwards_params(monkeypatch):
    """query, include_content, scope, and model are forwarded from
    Seltz.answer_stream() to AnswerService.answer_stream()."""
    captured = {}

    def fake_answer_stream(*args, **kwargs):
        captured.update(kwargs)
        return iter([])

    monkeypatch.setattr(
        "seltz.services.answer_service.AnswerService.answer_stream", fake_answer_stream
    )
    client = Seltz(api_key="test-key")
    list(
        client.answer_stream(
            "AI news", include_content=True, scope="news", model="seltz-pro"
        )
    )

    assert captured["query"] == "AI news"
    assert captured["include_content"] is True
    assert captured["scope"] == "news"
    assert captured["model"] == "seltz-pro"


# ---------------------------------------------------------------------------
# Integration tests — require SELTZ_API_KEY
# ---------------------------------------------------------------------------


@pytest.mark.integration
@needs_api_key
def test_search_returns_response():
    """Return a SearchResponse instance for a standard query."""
    client = Seltz()
    response = client.search("best ai search engines")
    assert isinstance(response, SearchResponse)


@pytest.mark.integration
@needs_api_key
def test_search_returns_results():
    """Return at least one document for a non-empty query."""
    client = Seltz()
    response = client.search("best ai search engines", max_results=5)
    assert len(response.documents) > 0


@pytest.mark.integration
@needs_api_key
def test_search_max_results_respected():
    """Return no more documents than the requested max_results."""
    client = Seltz()
    response = client.search("best ai search engines", max_results=3)
    assert len(response.documents) <= 3


@pytest.mark.integration
@needs_api_key
def test_search_result_fields():
    """Each document in the response has url and content as strings."""
    client = Seltz()
    response = client.search("best ai search engines")
    for doc in response.documents:
        assert isinstance(doc.url, str)
        assert isinstance(doc.content, str)


@pytest.mark.integration
@needs_api_key
def test_search_empty_query():
    """Return a SearchResponse without raising for an empty query string."""
    client = Seltz()
    response = client.search("")
    assert isinstance(response, SearchResponse)
    assert len(response.documents) == 0


@pytest.mark.integration
@needs_api_key
def test_answer_returns_response():
    """Return an AnswerResponse with a non-empty markdown answer."""
    client = Seltz()
    response = client.answer("Who is Apple's next CEO?")
    assert isinstance(response, AnswerResponse)
    assert isinstance(response.answer, str)
    assert len(response.answer) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_returns_citations():
    """Return at least one citation, each carrying a URL string."""
    client = Seltz()
    response = client.answer("Who is Apple's next CEO?")
    assert len(response.citations) >= 1
    for citation in response.citations:
        assert isinstance(citation.url, str)


@pytest.mark.integration
@needs_api_key
def test_answer_with_scope_returns_response():
    """answer(scope="news") reaches the live API and returns a non-empty answer."""
    client = Seltz()
    response = client.answer("What is the latest news about AI?", scope="news")
    assert isinstance(response, AnswerResponse)
    assert isinstance(response.answer, str)
    assert len(response.answer) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_with_model_returns_response():
    """answer(model="seltz-pro") reaches the live API and returns a non-empty answer."""
    client = Seltz()
    response = client.answer("Who is Apple's next CEO?", model="seltz-pro")
    assert isinstance(response, AnswerResponse)
    assert isinstance(response.answer, str)
    assert len(response.answer) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_stream_yields_events():
    """Streaming answer yields a leading citations event, text deltas, and a
    terminal finish_reason, reconstructing a non-empty answer."""
    client = Seltz()
    kinds = []
    text = ""
    for event in client.answer_stream("Who is Apple's next CEO?"):
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
def test_answer_with_response_format_returns_json():
    """answer(response_format=...) reaches the live API and returns an answer
    that is a JSON string conforming to the requested schema; citations are
    still returned."""
    client = Seltz()
    response = client.answer(
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


@pytest.mark.integration
@needs_api_key
def test_answer_with_system_prompt_honours_the_instruction():
    """A system_prompt visibly steers presentation, and grounding survives.

    The instruction is a literal opening line rather than a stylistic ask so
    the assertion is mechanical. Citations are asserted alongside it: the
    customer section must not cost us the grounding contract.
    """
    client = Seltz()
    response = client.answer(
        "Who is Apple's next CEO?",
        system_prompt=(
            'Begin your reply with the exact line "BRIEFING:" before anything else.'
        ),
    )
    assert isinstance(response, AnswerResponse)
    assert response.answer.lstrip().upper().startswith("BRIEFING:")
    assert len(response.citations) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_without_system_prompt_is_unaffected():
    """The same query without a system_prompt carries no injected prefix.

    The contrast is what makes the test above meaningful — it proves the
    prefix came from the caller rather than from the shipped prompt.
    """
    client = Seltz()
    response = client.answer("Who is Apple's next CEO?")
    assert not response.answer.lstrip().upper().startswith("BRIEFING:")
    assert len(response.citations) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_stream_with_system_prompt_honours_the_instruction():
    """system_prompt applies on the streaming surface too."""
    client = Seltz()
    text = ""
    for event in client.answer_stream(
        "Who is Apple's next CEO?",
        system_prompt=(
            'Begin your reply with the exact line "BRIEFING:" before anything else.'
        ),
    ):
        if event.WhichOneof("event") == "text_delta":
            text += event.text_delta
    assert text.lstrip().upper().startswith("BRIEFING:")


@pytest.mark.integration
@needs_api_key
def test_answer_with_system_prompt_and_response_format_compose():
    """system_prompt and response_format apply together, schema still honoured."""
    client = Seltz()
    response = client.answer(
        "Who is Apple's next CEO?",
        system_prompt="Write the summary in British English.",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ceo_answer",
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
    payload = json.loads(response.answer)
    assert isinstance(payload["summary"], str) and payload["summary"]
    assert len(response.citations) > 0


@pytest.mark.integration
@needs_api_key
def test_answer_oversized_system_prompt_is_rejected():
    """Over the 8 KiB cap the server rejects before billing.

    INVALID_ARGUMENT is not specially mapped, so it surfaces as SeltzAPIError.
    """
    client = Seltz()
    with pytest.raises(SeltzAPIError) as excinfo:
        client.answer("Who is Apple's next CEO?", system_prompt="A" * 8193)
    assert "system_prompt" in str(excinfo.value)


@pytest.mark.integration
@needs_api_key
def test_answer_none_system_prompt_is_accepted_as_absent():
    """system_prompt=None reaches the server as an omitted field, not "None"."""
    client = Seltz()
    response = client.answer("Who is Apple's next CEO?", system_prompt=None)
    assert isinstance(response, AnswerResponse)
    assert len(response.citations) > 0
