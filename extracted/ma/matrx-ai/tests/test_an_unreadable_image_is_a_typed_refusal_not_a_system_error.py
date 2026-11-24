"""A provider 400 "Unable to process input image" is the input's refusal: typed, user-facing, never filed.

Live 2026-11-18: Google's 400 landed as a ``provider_request_failed`` system error. The executor now
types it (``input_refusal_info``) and treats it as a caller refusal, so ``_capture_terminal_provider_failure``
is skipped. Any other 400 stays an ordinary failure.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_ai.providers.caller_refusal import caller_refusal_codes
from matrx_ai.providers.errors import PROVIDER_INPUT_REFUSED, input_refusal_info


def test_unreadable_image_400_is_typed_and_final() -> None:
    exc = RuntimeError("400 INVALID_ARGUMENT. {'error': {'message': 'Unable to process input image.'}}")
    info = input_refusal_info(exc, "Google")
    assert info is not None
    assert info.error_type == PROVIDER_INPUT_REFUSED
    assert info.is_retryable is False
    assert info.status_code == 400
    assert "image" in info.user_message.lower()
    assert "Unable to process" not in info.user_message  # the provider's words stay server-side
    assert PROVIDER_INPUT_REFUSED in caller_refusal_codes()


def test_any_other_failure_is_not_an_input_refusal() -> None:
    assert input_refusal_info(RuntimeError("400 Request contains an invalid argument."), "google") is None
    assert input_refusal_info(RuntimeError("provider outage"), "google") is None


def test_executor_skips_the_system_error_for_the_refusal() -> None:

    from matrx_ai.orchestrator import executor

    src = stable_source(executor)
    assert "_input_refusal = input_refusal_info(e, provider)" in src
    assert "or _input_refusal is not None" in src
