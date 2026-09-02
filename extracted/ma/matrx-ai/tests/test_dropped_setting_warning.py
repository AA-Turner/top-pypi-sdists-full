"""An UNEXPECTED drop reaches the client as a WARNING; a conversion never does.

Arman, 2026-08-17: "a conversion does not need to be reported to the client,
but an unexpected drop definitely needs to be communicated to the client as a
warning, not as an error."
"""

from __future__ import annotations

from matrx_ai.catalog.models import Adjustment
from matrx_ai.providers.outbound_params import warn_client_about_dropped_settings


class _Emitter:
    def __init__(self) -> None:
        self.warnings: list = []

    async def send_warning(self, payload) -> None:  # noqa: ANN001
        self.warnings.append(payload)


def _collect(monkeypatch, adjustments: list[Adjustment]) -> list:
    import matrx_connect

    emitter = _Emitter()
    sent: list = []

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.emitter = emitter  # type: ignore[attr-defined]
    monkeypatch.setattr(matrx_connect, "get_app_context", lambda: ctx, raising=False)

    import asyncio

    def _capture(coro, **kwargs):
        # No event loop in this unit test — run the coroutine to completion so
        # the payload is observable, instead of scheduling it.
        # `**kwargs` because the caller passes `context=` (a real
        # `asyncio.create_task` keyword): a fake that is stricter than the API
        # it stands in for turns a WORKING code path into a red test, and the
        # swallowed TypeError made this read as "no warning was emitted".
        asyncio.run(coro)
        sent.append(True)

    monkeypatch.setattr(asyncio, "create_task", _capture)
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: None)
    warn_client_about_dropped_settings(adjustments, model="some-model")
    return emitter.warnings


def test_unexpected_drop_warns_the_user(monkeypatch):
    warnings = _collect(
        monkeypatch,
        [
            Adjustment(
                key="aspect_ratio",
                action="dropped",
                canonical_value="21:9",
                reason="'aspect_ratio'='21:9' is not mapped — dropped",
                expected=False,
            )
        ],
    )
    assert len(warnings) == 1
    assert warnings[0].code == "setting_not_supported"
    assert warnings[0].recoverable is True  # decorates the response, never invalidates it
    assert "aspect_ratio" in (warnings[0].user_message or "")


def test_a_conversion_is_silent_to_the_client(monkeypatch):
    # The system working as designed is not news.
    assert (
        _collect(
            monkeypatch,
            [
                Adjustment(
                    key="reasoning_effort",
                    action="mapped",
                    canonical_value="max",
                    sent_value="high",
                    reason="mapped",
                ),
                Adjustment(
                    key="tts_voice",
                    action="unsupported_value",
                    canonical_value="kore",
                    sent_value="aoede",
                    reason="reconciled",
                    expected=True,
                ),
            ],
        )
        == []
    )


def test_a_declared_capability_gap_is_silent(monkeypatch):
    # `supported: false` is someone's written-down decision, not a surprise.
    assert (
        _collect(
            monkeypatch,
            [
                Adjustment(
                    key="thinking_level",
                    action="dropped",
                    canonical_value="high",
                    reason="'thinking_level' is not supported by this api/offering",
                )
            ],
        )
        == []
    )


def test_one_event_covers_every_dropped_key(monkeypatch):
    warnings = _collect(
        monkeypatch,
        [
            Adjustment(key=k, action="dropped", canonical_value="x", reason="r", expected=False)
            for k in ("aspect_ratio", "resolution", "verbosity")
        ],
    )
    assert len(warnings) == 1  # not three toasts
    for key in ("aspect_ratio", "resolution", "verbosity"):
        assert key in (warnings[0].user_message or "")
