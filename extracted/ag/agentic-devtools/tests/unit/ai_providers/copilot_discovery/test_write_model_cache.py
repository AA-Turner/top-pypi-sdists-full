import json
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

from agentic_devtools.ai_providers.copilot_discovery import write_model_cache
from agentic_devtools.ai_providers.models import ModelRecord

_ENTRY = {
    "modelId": "gpt-5-mini",
    "name": "GPT-5 mini",
    "_meta": {"copilotUsage": "0x", "copilotPriceCategory": "low", "copilotEnablement": "enabled"},
}


def _record() -> ModelRecord:
    return ModelRecord(
        name="GPT-5 mini",
        model_id="gpt-5-mini",
        provider="copilot",
        context_window=128000,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata=cast("dict[str, Any]", dict(_ENTRY)),
        raw_metadata_verbatim=True,
    )


def test_writes_the_raw_acp_entries_and_a_timestamp(tmp_path: Path) -> None:
    cache_path = tmp_path / "caches" / "copilot-models.json"

    assert write_model_cache([_record()], cache_path=cache_path, now=1234.0) is True

    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert payload["fetchedAt"] == 1234.0
    assert payload["models"] == [_ENTRY]


def test_redacts_credentials_in_persisted_acp_entries(tmp_path: Path) -> None:
    cache_path = tmp_path / "caches" / "copilot-models.json"
    record = ModelRecord(
        name="GPT-5 mini",
        model_id="gpt-5-mini",
        provider="copilot",
        context_window=128000,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata=cast(
            "dict[str, Any]",
            dict(_ENTRY, token="secret-value", nested={"apiKey": "nested-secret"}),
        ),
        raw_metadata_verbatim=True,
    )

    assert write_model_cache([record], cache_path=cache_path, now=1234.0) is True

    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    assert payload["models"][0]["token"] == "<redacted>"
    assert payload["models"][0]["nested"]["apiKey"] == "<redacted>"


def test_defaults_to_the_shared_cache_path(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"

    with patch("agentic_devtools.ai_providers.copilot_discovery.get_cache_path", return_value=cache_path):
        assert write_model_cache([_record()]) is True

    assert cache_path.exists()


def test_replaces_an_existing_cache_atomically(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    cache_path.write_text("stale", encoding="utf-8")

    with patch("agentic_devtools.ai_providers.copilot_discovery.os.replace") as mock_replace:
        assert write_model_cache([_record()], cache_path=cache_path) is True

    assert mock_replace.call_count == 1
    assert Path(mock_replace.call_args[0][0]).parent == tmp_path
    assert mock_replace.call_args[0][1] == cache_path


def test_returns_false_when_the_cache_cannot_be_written(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"

    with patch(
        "agentic_devtools.ai_providers.copilot_discovery.tempfile.mkstemp",
        side_effect=OSError("read-only"),
    ):
        assert write_model_cache([_record()], cache_path=cache_path) is False


def test_removes_the_temp_file_when_the_replace_fails(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"

    with patch(
        "agentic_devtools.ai_providers.copilot_discovery.os.replace",
        side_effect=OSError("cross-device"),
    ):
        assert write_model_cache([_record()], cache_path=cache_path) is False

    assert list(tmp_path.iterdir()) == []
