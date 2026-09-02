import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

from agentic_devtools.ai_providers.copilot_discovery import discover_copilot_models
from agentic_devtools.ai_providers.errors import ProviderError
from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.ai_providers.provider import ModelDiscovery

_ENTRY = {"modelId": "gpt-5-mini", "name": "GPT-5 mini"}


class _StubDiscovery(ModelDiscovery):
    def __init__(self, *, records: list[ModelRecord] | None = None, error: ProviderError | None = None) -> None:
        self._records = records or []
        self._error = error
        self.calls = 0

    def _discover_models(self) -> list[ModelRecord]:
        self.calls += 1
        if self._error is not None:
            raise self._error
        return self._records


def _record(model_id: str = "gpt-5-mini") -> ModelRecord:
    return ModelRecord(
        name="GPT-5 mini",
        model_id=model_id,
        provider="copilot",
        context_window=128000,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata=dict(_ENTRY, modelId=model_id),
        raw_metadata_verbatim=True,
    )


def _write_cache(cache_path: Path, fetched_at: float, model_id: str = "cached-model") -> None:
    cache_path.write_text(
        json.dumps({"version": 1, "fetchedAt": fetched_at, "models": [dict(_ENTRY, modelId=model_id)]}),
        encoding="utf-8",
    )


def test_live_discovery_wins_and_refreshes_the_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write_cache(cache_path, 0.0)
    discovery = _StubDiscovery(records=[_record("live-model")])

    records = discover_copilot_models(cache_path=cache_path, discovery=discovery)

    assert [record.model_id for record in records] == ["live-model"]
    assert json.loads(cache_path.read_text(encoding="utf-8"))["models"][0]["modelId"] == "live-model"


def test_warns_but_returns_records_when_the_cache_cannot_be_written(tmp_path: Path) -> None:
    warnings: list[str] = []
    discovery = _StubDiscovery(records=[_record()])

    with patch("agentic_devtools.ai_providers.copilot_discovery.write_model_cache", return_value=False):
        records = discover_copilot_models(
            cache_path=tmp_path / "copilot-models.json",
            discovery=discovery,
            warn=warnings.append,
        )

    assert [record.model_id for record in records] == ["gpt-5-mini"]
    assert any("Could not write" in warning for warning in warnings)


def test_falls_back_to_a_fresh_cache_when_discovery_fails(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    warnings: list[str] = []
    discovery = _StubDiscovery(error=ProviderError("copilot is offline", category="transport_error"))

    with patch("agentic_devtools.ai_providers.copilot_discovery.time.time", return_value=1000.0):
        _write_cache(cache_path, 900.0)
        records = discover_copilot_models(cache_path=cache_path, discovery=discovery, warn=warnings.append)

    assert [record.model_id for record in records] == ["cached-model"]
    assert any("discovery failed" in warning for warning in warnings)


def test_falls_back_to_a_stale_cache_when_the_refresh_fails(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    warnings: list[str] = []
    _write_cache(cache_path, 0.0, "stale-model")
    discovery = _StubDiscovery(error=ProviderError("copilot is offline", category="transport_error"))

    records = discover_copilot_models(cache_path=cache_path, discovery=discovery, warn=warnings.append)

    assert [record.model_id for record in records] == ["stale-model"]
    assert any("stale Copilot model cache" in warning for warning in warnings)


def test_can_disable_stale_cache_fallback(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    warnings: list[str] = []
    _write_cache(cache_path, 0.0, "stale-model")
    discovery = _StubDiscovery(error=ProviderError("copilot is offline", category="transport_error"))

    records = discover_copilot_models(
        cache_path=cache_path,
        discovery=discovery,
        allow_stale=False,
        warn=warnings.append,
    )

    assert records == []
    assert any("empty inventory" in warning for warning in warnings)


def test_returns_an_empty_inventory_when_nothing_is_available(tmp_path: Path) -> None:
    warnings: list[str] = []
    discovery = _StubDiscovery(error=ProviderError("copilot is offline", category="transport_error"))

    records = discover_copilot_models(
        cache_path=tmp_path / "missing.json",
        discovery=discovery,
        warn=warnings.append,
    )

    assert records == []
    assert any("empty inventory" in warning for warning in warnings)


def test_no_refresh_reads_the_cache_without_spawning_discovery(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    discovery = _StubDiscovery(records=[_record("live-model")])

    with patch("agentic_devtools.ai_providers.copilot_discovery.time.time", return_value=1000.0):
        _write_cache(cache_path, 1000.0)
        records = discover_copilot_models(refresh=False, cache_path=cache_path, discovery=discovery)

    assert [record.model_id for record in records] == ["cached-model"]
    assert discovery.calls == 0


def test_uses_the_acp_provider_and_shared_cache_path_by_default(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    created: list[Any] = []

    class _Provider(_StubDiscovery):
        def __init__(self) -> None:
            super().__init__(records=[_record("default-model")])
            created.append(self)

    with patch("agentic_devtools.ai_providers.copilot_discovery.get_cache_path", return_value=cache_path):
        with patch("agentic_devtools.ai_providers.copilot_discovery.CopilotACPDiscovery", _Provider):
            records = discover_copilot_models()

    assert [record.model_id for record in records] == ["default-model"]
    assert len(created) == 1
    assert cache_path.exists()


def test_warnings_default_to_stderr(tmp_path: Path, capsys) -> None:
    discovery = _StubDiscovery(error=ProviderError("copilot is offline", category="transport_error"))

    discover_copilot_models(cache_path=tmp_path / "missing.json", discovery=discovery)

    assert "copilot is offline" in capsys.readouterr().err
