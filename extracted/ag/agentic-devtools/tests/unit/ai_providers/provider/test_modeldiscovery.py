import pytest

from agentic_devtools.ai_providers.errors import ProviderError
from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.ai_providers.provider import ModelDiscovery


class DummyDiscovery(ModelDiscovery):
    def __init__(self, *, bad_result: object = None, use_bad_result: bool = False) -> None:
        self._bad_result = bad_result
        self._use_bad_result = use_bad_result

    def _discover_models(self) -> list[ModelRecord]:
        if self._use_bad_result:
            return self._bad_result  # type: ignore[return-value]
        return [
            ModelRecord(
                name="Test Model",
                model_id="test-model",
                provider="dummy",
                context_window=1024,
                max_output_tokens=256,
                supports_tools=False,
                raw_metadata={},
            )
        ]


def test_discover_models_returns_model_records() -> None:
    discovery = DummyDiscovery()

    records = discovery.discover_models()

    assert [record.model_id for record in records] == ["test-model"]


@pytest.mark.parametrize("bad_result", [None, "not-a-list", 42, {"model_id": "m"}])
def test_discover_models_rejects_non_list_result(bad_result: object) -> None:
    discovery = DummyDiscovery(bad_result=bad_result, use_bad_result=True)

    with pytest.raises(
        ProviderError,
        match=r"_discover_models\(\) must return a list; got ",
    ):
        discovery.discover_models()


def test_discover_models_rejects_non_model_record_items() -> None:
    discovery = DummyDiscovery(bad_result=["not-a-model-record"], use_bad_result=True)

    with pytest.raises(
        ProviderError,
        match=r"_discover_models\(\) must return a list of ModelRecord instances; item at index 0 is ",
    ):
        discovery.discover_models()


def test_model_discovery_rejects_overridden_discover_models() -> None:
    with pytest.raises(
        TypeError,
        match="ModelDiscovery subclasses must implement _discover_models\\(\\) "
        "instead of overriding discover_models\\(\\)\\.",
    ):

        class InvalidDiscovery(ModelDiscovery):
            def discover_models(self) -> list[ModelRecord]:  # type: ignore[misc]
                return []
