import pytest

from agentic_devtools.ai_providers.copilot_discovery import extract_available_models
from agentic_devtools.ai_providers.errors import ProviderError


def test_returns_the_authoritative_available_models_list() -> None:
    entries = [{"modelId": "auto"}, {"modelId": "gpt-5-mini"}]
    message = {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {"sessionId": "s-1", "models": {"availableModels": entries, "currentModelId": "gpt-5-mini"}},
    }

    assert extract_available_models(message) == entries


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ({"id": 2}, "no result object"),
        ({"id": 2, "result": "nope"}, "no result object"),
        ({"id": 2, "result": {}}, "no models object"),
        ({"id": 2, "result": {"models": []}}, "no models object"),
        ({"id": 2, "result": {"models": {}}}, "no availableModels list"),
        ({"id": 2, "result": {"models": {"availableModels": []}}}, "no availableModels list"),
        ({"id": 2, "result": {"models": {"availableModels": {}}}}, "no availableModels list"),
    ],
)
def test_rejects_responses_without_an_authoritative_list(message: dict[str, object], expected: str) -> None:
    with pytest.raises(ProviderError, match=expected):
        extract_available_models(message)
