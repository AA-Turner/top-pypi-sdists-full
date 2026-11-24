"""A spoken (audio-only) answer is never verified against the bound JSON contract
(false answer_off_contract, event f257f0c5, flashcards.spoken_front_tts)."""

from types import SimpleNamespace

from matrx_ai.schema.answer_contract import (
    bind_declared_output_contract,
    declared_output_contract,
    is_audio_only_output,
    release_declared_output_contract,
)

RF = {"type": "json_schema", "json_schema": {"name": "x", "schema": {"type": "object"}}}


def test_audio_only_binds_no_contract():
    tts = SimpleNamespace(produces_audio=True, produces_text=False)
    assert is_audio_only_output(tts)
    tok = bind_declared_output_contract(RF, tts)
    try:
        assert declared_output_contract() is None
    finally:
        release_declared_output_contract(tok)


def test_text_model_still_binds():
    chat = SimpleNamespace(produces_audio=False, produces_text=True)
    tok = bind_declared_output_contract(RF, chat)
    try:
        assert declared_output_contract() is not None
    finally:
        release_declared_output_contract(tok)
