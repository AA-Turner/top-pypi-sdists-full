"""THE TRUNCATION NOTICE TELLS THE TRUTH ABOUT WHERE THE READER IS.

THE DEFECT THIS GUARDS (live 2026-09-12, workflow run
2cf711eb-1a15-49ed-baf7-ddb166dba129, step "Montessori asks"): a prose step was
cut at 1,200 tokens and the platform said so honestly — then offered *"Ask me to
continue and I'll pick up where it cut off"* to a parent sitting inside a
workflow run, where there is no me to ask and no way to ask it. A remedy nobody
can perform is a dead control wearing a helpful sentence (root ``CLAUDE.md``: *a
screen never lies*).

What is being proven:

* ``matrx_ai.config.finish_reason.truncation_notice`` offers "ask me to
  continue" ONLY where a person can actually say it, and otherwise names the
  step's output limit and who can raise it — on BOTH branches (a plain cut-off
  reply and an interrupted tool call).
* ``matrx_ai.orchestrator.executor._caller_can_continue`` — which decides that
  at the truncation site — reads ``continuable`` off the request metadata and
  treats every historical caller (no key, no metadata) as a conversation.

Why it is a forcing test: the assertions are on the sentence a person reads and
on the routing decision, not on a constant. Replacing ``_caller_can_continue``
with the pre-fix behaviour (``lambda request: True`` — everyone can continue) or
dropping the ``continuable`` branch from ``truncation_notice`` turns these red.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.finish_reason import CONTINUABLE_METADATA_KEY, truncation_notice
from matrx_ai.orchestrator.executor import _caller_can_continue

#: The live incident's authored ceiling.
INCIDENT_CEILING = 1_200

CONTINUE_OFFER = "Ask me to continue"


# --------------------------------------------------------------------------
# The plain cut-off reply
# --------------------------------------------------------------------------
def test_a_conversation_is_told_to_ask_for_the_rest() -> None:
    notice = truncation_notice(max_output_tokens=INCIDENT_CEILING, continuable=True)

    assert CONTINUE_OFFER in notice
    assert "1,200" in notice


def test_a_workflow_step_is_never_offered_a_remedy_nobody_can_perform() -> None:
    notice = truncation_notice(max_output_tokens=INCIDENT_CEILING, continuable=False)

    assert "ask me to continue" not in notice.lower()
    assert "1,200" in notice, "the number the workflow's author has to raise"
    assert "output limit" in notice.lower(), "and the remedy names raising it"


# --------------------------------------------------------------------------
# The interrupted-tool-call branch
# --------------------------------------------------------------------------
def test_a_conversation_whose_tool_call_died_is_told_a_retry_is_coming() -> None:
    notice = truncation_notice(
        max_output_tokens=INCIDENT_CEILING,
        interrupted_tool_calls=["workflow_author"],
        continuable=True,
    )

    assert "workflow_author" in notice
    assert "try again" in notice.lower(), "a retry is a real remedy in a conversation"
    assert "output limit" not in notice.lower()


def test_a_workflow_step_whose_tool_call_died_is_told_it_cannot_retry_itself() -> None:
    notice = truncation_notice(
        max_output_tokens=INCIDENT_CEILING,
        interrupted_tool_calls=["workflow_author"],
        continuable=False,
    )

    assert "workflow_author" in notice
    assert "ask me to continue" not in notice.lower()
    assert "cannot retry itself" in notice.lower()
    assert "output limit" in notice.lower()


# --------------------------------------------------------------------------
# The routing decision at the truncation site
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "case, request_obj, expected",
    [
        ("a request carrying empty metadata is a conversation", SimpleNamespace(metadata={}), True),
        ("a request with no metadata attribute at all", SimpleNamespace(), True),
        (
            "a caller that declared itself continuable",
            SimpleNamespace(metadata={CONTINUABLE_METADATA_KEY: True}),
            True,
        ),
        (
            "a workflow step, which declares there is nowhere to continue",
            SimpleNamespace(metadata={CONTINUABLE_METADATA_KEY: False}),
            False,
        ),
    ],
)
def test_the_truncation_site_reads_continuable_off_the_request(
    case: str, request_obj: object, expected: bool
) -> None:
    assert _caller_can_continue(request_obj) is expected, case


# ---------------------------------------------------------------------------
# THE ARITHMETIC LEG — the second, independent layer of "was this truncated?"
#
# Live 2026-09-12, run 2cf711eb…, step `read_case`: the provider's reason was
# lost crossing a seam, so the only surviving evidence was that the completion
# produced exactly the 2,500 tokens it was permitted. `completion_truncation`
# must read that; and it must NOT overrule a provider that declared `stop`,
# because a model may legitimately finish exactly on its cap.
# ---------------------------------------------------------------------------


def _completion(*, permitted, produced, finish=None, metadata=None):
    """The smallest object carrying the facts the classifier reads."""
    config = SimpleNamespace(max_output_tokens=permitted, model="claude-opus-5")
    return SimpleNamespace(
        metadata=dict(metadata or {}),
        request=SimpleNamespace(config=config),
        final_response=SimpleNamespace(finish_reason=finish) if finish else None,
        finish_reason=None,
        total_usage=SimpleNamespace(output_tokens=produced),
    )


def test_a_silent_provider_that_spent_every_permitted_token_is_truncated():
    from matrx_ai.config.finish_reason import completion_truncation

    ceiling = completion_truncation(_completion(permitted=2500, produced=2500))
    assert ceiling is not None, "the read_case incident: 2500 of 2500 tokens, no finish reason"
    assert ceiling.max_output_tokens == 2500
    assert ceiling.output_tokens == 2500


def test_a_declared_stop_is_never_overruled_by_arithmetic():
    from matrx_ai.config.finish_reason import completion_truncation

    # A model asked for 32,000 may legitimately finish on its own at exactly
    # 32,000. Inventing a truncation here is the mirror of the masked-cause bug.
    assert completion_truncation(_completion(permitted=32000, produced=32000, finish="stop")) is None
    assert completion_truncation(_completion(permitted=32000, produced=32000, finish="end_turn")) is None


def test_a_completion_well_under_its_ceiling_is_never_truncated():
    from matrx_ai.config.finish_reason import completion_truncation

    assert completion_truncation(_completion(permitted=2500, produced=900)) is None
