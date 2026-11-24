"""A media-generating model (image/audio/video, no structured output) answers with the
asset, so the declared JSON contract (kind ``media_asset``) is neither bound, injected into
its prompt, nor reported as dropped (false enforcement_dropped / answer_off_contract on the
podcast audio, video and feature-image mandates)."""

from types import SimpleNamespace

from matrx_ai.config import MessageList, UnifiedConfig
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
from matrx_ai.providers.unified_client import _downgrade_response_format
from matrx_ai.schema.answer_contract import (
    bind_declared_output_contract,
    declared_output_contract,
    release_declared_output_contract,
)

SCHEMA = {"type": "object", "properties": {"url": {"type": "string"}}}
RF = {"type": "json_schema", "json_schema": {"name": "media_asset", "schema": SCHEMA}}


def _caps(output, features=()):
    return resolve_model_capabilities(
        SimpleNamespace(name="m", capabilities={"input": ["text"], "output": output, "features": list(features)})
    )


def test_image_model_binds_no_contract_and_records_nothing(monkeypatch):
    recorded = []
    monkeypatch.setattr(
        "matrx_ai.providers.structured_output_findings.record_structured_output_finding_sync",
        lambda *a, **k: recorded.append(a),
    )
    caps = _caps(["image"])
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[]), response_format=dict(RF))
    tok = bind_declared_output_contract(config.response_format, caps)
    try:
        assert declared_output_contract() is None
        _downgrade_response_format(config, caps, "openai_chat")
        assert config.response_format == {"type": "text"}
        assert recorded == []
    finally:
        release_declared_output_contract(tok)


def test_structured_text_model_keeps_its_contract():
    caps = _caps(["text"], ["structured_output"])
    tok = bind_declared_output_contract(RF, caps)
    try:
        assert declared_output_contract() is not None
    finally:
        release_declared_output_contract(tok)
