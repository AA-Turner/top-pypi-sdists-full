"""CGU-M3 W3 (P-177 live walk 2026-11-04): the swap note showed for ~1.6 s and vanished when the saved answer took
over — the saved row never said which model answered. The executor now stamps the swap sentence on the answer."""

from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters import SilentEmitter

from matrx_ai.orchestrator.executor import _model_swap_stamp
from matrx_ai.providers.free_tier_models import MODEL_SWAP_NOTE_KEY


def test_the_answer_carries_the_swap_sentence() -> None:
    token = set_app_context(AppContext(user_id="g-1", emitter=SilentEmitter(), metadata={MODEL_SWAP_NOTE_KEY: "Ran on Claude Haiku. Sign up free for Claude Opus."}))
    try:
        assert _model_swap_stamp() == {"model_swap": "Ran on Claude Haiku. Sign up free for Claude Opus."}
    finally:
        clear_app_context(token)


def test_no_swap_stamps_nothing() -> None:
    token = set_app_context(AppContext(user_id="u-1", emitter=SilentEmitter(), metadata={}))
    try:
        assert _model_swap_stamp() == {}
    finally:
        clear_app_context(token)
