from typing import Literal

from matrx_utils import vcprint

from matrx_ai.config.finish_reason import FinishReason
from matrx_ai.config.unified_config import (
    UnifiedResponse,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest


#: A provider refusal with nothing written is re-asked ONCE (see
#: ``handle_finish_reason``) before the run fails. Live 2026-10-18: Claude Opus 5.5 declined the Studio Debrief
#: (stop_reason=refusal, 0 output tokens, a blank assistant turn) in about 4 of 6
#: tries and answered the other 2 — the classifier is not deterministic, and a
#: zero-token refusal costs nothing to ask again.


def response_has_no_output(response: UnifiedResponse) -> bool:
    """True when the turn holds nothing a person can see and no tool call."""
    from matrx_ai.config import TextContent, ThinkingContent

    messages = response.messages
    if not isinstance(messages, (list, tuple)):
        messages = [messages]
    for message in messages:
        for content in getattr(message, "content", None) or []:
            if isinstance(content, ThinkingContent):
                continue
            if isinstance(content, TextContent) and not (content.text or "").strip():
                continue
            return False
    return True


def handle_finish_reason(
    response: UnifiedResponse,
    request: AIMatrixRequest,
    retry_attempt: int,
    max_retries: int,
    debug: bool = False,
) -> Literal["continue", "truncated", "retry", "stop"]:
    """
    Handle finish reason and prepare for retry if needed.

    Returns:
        - "continue": Clean completion, proceed with normal flow.
        - "truncated": Response hit the token limit. Partial output was returned.
                       Caller must notify the UI and stop the loop.
        - "retry": Retryable error prepared, retry the request.
        - "stop": Fatal error, stop execution.
    """
    finish_reason = response.finish_reason

    if not finish_reason:
        return "continue"

    if isinstance(finish_reason, str):
        try:
            finish_reason = FinishReason(finish_reason)
        except ValueError:
            vcprint(
                f"⚠️  Unknown finish reason '{finish_reason}', continuing anyway",
                color="yellow",
            )
            return "continue"

    if finish_reason.is_success():
        return "continue"

    # ── TRUNCATION ────────────────────────────────────────────────────────────
    if finish_reason.is_truncated():
        model = request.config.model or "unknown model"
        max_tokens = request.config.max_output_tokens

        print("\n")
        print("=" * 70)
        print("🚨  TOKEN LIMIT HIT — RESPONSE TRUNCATED")
        print("=" * 70)
        print(f"  Model      : {model}")
        print(f"  max_tokens : {max_tokens if max_tokens is not None else '(none set — model default used)'}")
        print("  finish_reason = max_tokens")
        print("  The model stopped mid-response because it ran out of output tokens.")
        print("  The response the user received is INCOMPLETE.")
        print("=" * 70)
        print("\n")

        # The executor records this operational condition through the structured
        # error boundary.  Never dump the provider payload here: besides making
        # an expected diagnostic look like an unstructured ERROR, it can contain
        # the user's complete generated response.
        vcprint(
            {
                "finish_reason": str(finish_reason),
                "model": model,
                "max_output_tokens": max_tokens,
            },
            "Truncated provider response",
            color="yellow",
            verbose=debug,
        )
        return "truncated"

    # ── LOG ALL OTHER NON-SUCCESS REASONS ─────────────────────────────────────
    print("\n")
    print("=" * 70)
    print(f"⚠️  NON-SUCCESS FINISH REASON: {finish_reason}")
    print("=" * 70)
    vcprint(
        response.raw_response,
        f"Full Response (finish_reason={finish_reason})",
        color="yellow",
        verbose=True,
    )

    # ── EMPTY REFUSAL: ask again once, nothing is added to the conversation ──
    if (
        finish_reason == FinishReason.REFUSAL
        and retry_attempt < min(max_retries, 1)
        and response_has_no_output(response)
    ):
        return "retry"

    # ── RETRYABLE ─────────────────────────────────────────────────────────────
    if finish_reason.is_retryable():
        if retry_attempt < max_retries:
            vcprint(
                f"↻ Retry {retry_attempt + 1}/{max_retries} due to {finish_reason}",
                color="cyan",
            )

            for msg in response.messages:
                request.config.messages.append(msg)

            if request.config.tools:
                tool_names = [
                    tool if isinstance(tool, str) else tool.get("name", "unknown")
                    for tool in request.config.tools
                ]
                tools_message = (
                    f"The previous function call failed. The following tools are the only "
                    f"ones available: {tool_names}. Please use only these tools. If you do "
                    f"not have the resources you need, do not guess. Inform the user and "
                    f"avoid further complication."
                )
            else:
                tools_message = (
                    "The previous function call failed. No tools/functions are available "
                    "in this conversation. Please respond directly without attempting to "
                    "call any functions. If you do not have the resources you need, do not "
                    "guess. Inform the user and avoid further complication."
                )

            # A HOST-authored turn (census C7, 2026-10-17): stamped so it is never stored or
            # read back as something the person said (guard: test_host_authored_user_turns.py).
            from matrx_ai.config.message_config import host_authored_user_turn

            request.config.messages.append(
                host_authored_user_turn(tools_message, reason="retry_after_failed_call")
            )
            vcprint(f"📝 Added retry context: {tools_message}", color="cyan", verbose=debug)
            return "retry"
        else:
            print("\n")
            print("=" * 70)
            print(f"✗ MAX RETRIES ({max_retries}) EXCEEDED for finish_reason={finish_reason}")
            print("=" * 70)
            print("\n")

    # ── FATAL ERROR ───────────────────────────────────────────────────────────
    if finish_reason.is_error():
        print("\n")
        print("=" * 70)
        print(f"✗ FATAL FINISH REASON — stopping execution: {finish_reason}")
        print("=" * 70)
        print("\n")
        return "stop"

    vcprint(
        f"⚠️  Unhandled finish reason '{finish_reason}', continuing anyway",
        color="yellow",
    )
    return "continue"
