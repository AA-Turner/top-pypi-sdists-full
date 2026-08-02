"""Unit tests for Layer 2 compaction / continuation prompt contract.

Covers template-level assertions only — no LLM call, no message flow changes.
The prompts were rewritten to a state-capture XML contract; these tests guard
the public shape so future edits don't silently regress it.
"""

from __future__ import annotations

from xpander_sdk.core.context_optimizer.context_optimizer import (
    AUTO_COMPACT_USER_PROMPT_TEMPLATE,
    CONTINUATION_MESSAGE_TEMPLATE,
    PARTIAL_COMPACT_USER_PROMPT_TEMPLATE,
)

REQUIRED_STATE_TAGS = [
    "<work_completed>",
    "<decisions_made>",
    "<data_gathered>",
    "<user_requests_verbatim>",
    "<open_questions>",
    "<current_focus>",
    "<next_action>",
]


def test_compaction_prompt_contains_state_tags():
    for tag in REQUIRED_STATE_TAGS:
        assert tag in AUTO_COMPACT_USER_PROMPT_TEMPLATE


def test_compaction_prompt_includes_hard_rules():
    for must in [
        "MUST preserve all opaque identifiers",
        "MUST NOT attribute assistant suggestions",
        "MUST NOT include speculative next steps",
        "MUST output XML-tagged sections",
        "MUST treat work in <work_completed> as DONE",
        "MUST NOT use any tools",
    ]:
        assert must in AUTO_COMPACT_USER_PROMPT_TEMPLATE


def test_compaction_prompt_renders_with_placeholders():
    rendered = AUTO_COMPACT_USER_PROMPT_TEMPLATE.format(
        conversation="[]",
        plan_section="",
        custom_instructions_section="",
    )
    assert "<work_completed>" in rendered
    assert "[]" in rendered


def test_partial_compact_prompt_uses_same_xml_contract():
    for tag in [
        "<work_completed>",
        "<decisions_made>",
        "<data_gathered>",
        "<user_requests_verbatim>",
        "<open_questions>",
    ]:
        assert tag in PARTIAL_COMPACT_USER_PROMPT_TEMPLATE


def test_continuation_message_contains_binding_rules():
    sample_block = "<recent_actions>TEST_ACTION</recent_actions>"
    rendered = CONTINUATION_MESSAGE_TEMPLATE.format(
        summary="<state>X</state>",
        backup_pointer="",
        recent_actions_block=sample_block,
        authoritative_ledger_block="",
    )
    assert "<session_resume>" in rendered
    assert "<binding_rules>" in rendered
    assert "Treat <work_completed> as DONE" in rendered
    assert "Do NOT relitigate" in rendered
    assert "Do NOT ask the user any questions" in rendered
    assert "<authoritative_ledger>" in rendered  # binding-rule body references it
    # Strong contract — sample block must appear verbatim.
    assert sample_block in rendered
    # No stray placeholder.
    assert "{recent_actions_block}" not in rendered
    assert "{authoritative_ledger_block}" not in rendered


def test_continuation_message_omits_recent_actions_when_block_empty():
    """Empty recent_actions_block must not leave dangling references in the
    template. Guidance for <recent_actions> lives inside the block itself, so
    when no block is rendered the continuation must not mention it."""
    rendered = CONTINUATION_MESSAGE_TEMPLATE.format(
        summary="<state>X</state>",
        backup_pointer="",
        recent_actions_block="",
        authoritative_ledger_block="",
    )
    # The binding-rule body mentions <authoritative_ledger> — that's the
    # static reference. The actual entry block is what must be missing.
    assert "<entry " not in rendered
    assert "{recent_actions_block}" not in rendered
    assert "{authoritative_ledger_block}" not in rendered
