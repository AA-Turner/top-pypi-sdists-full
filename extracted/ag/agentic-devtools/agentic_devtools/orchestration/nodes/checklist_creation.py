"""Checklist creation node: generate structured checklist from plan.

Calls the LLM to decompose the implementation plan into discrete,
actionable checklist items with acceptance criteria.
"""

from __future__ import annotations

import json
from typing import Any

from agentic_devtools.orchestration.execution.context_factory import _run_async
from agentic_devtools.orchestration.nodes._helpers import _to_nonneg_int, utc_now
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


def checklist_creation_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Generate structured checklist from the implementation plan.

    Calls LLM with plan context to produce a list of ChecklistItem entries.
    """
    plan = state.get("plan", "")
    issue_key = state.get("issue_key", "")

    if not plan:
        return {
            "step": "checklist_creation",
            "error": "No plan available to generate checklist from.",
            "events": [
                {
                    "event": "checklist_creation_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "no_plan"},
                }
            ],
        }

    try:
        checklist_result = _generate_checklist(issue_key, plan)
    except Exception as exc:
        return {
            "step": "checklist_creation",
            "error": f"Checklist generation failed: {exc}",
            "events": [
                {
                    "event": "checklist_creation_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": str(exc)},
                }
            ],
        }

    checklist_items = checklist_result.get("items", [])
    token_usage = checklist_result.get("token_usage", {})

    return {
        "step": "checklist_creation",
        "error": None,
        "checklist_items": checklist_items,
        "checklist_created": True,
        "token_usage_prompt": _to_nonneg_int(state.get("token_usage_prompt"))
        + _to_nonneg_int(token_usage.get("prompt_tokens")),
        "token_usage_completion": _to_nonneg_int(state.get("token_usage_completion"))
        + _to_nonneg_int(token_usage.get("completion_tokens")),
        "events": [
            {
                "event": "checklist_creation_completed",
                "timestamp": utc_now(),
                "signals": {"item_count": len(checklist_items)},
            }
        ],
    }


def _generate_checklist(issue_key: str, plan: str) -> dict[str, Any]:
    """Generate checklist items via LLM provider.

    Returns dict with keys: items (list of dicts), token_usage.
    """
    from agentic_devtools.orchestration.llm.factory import ProviderFactory

    factory = ProviderFactory()
    provider = factory.get_provider("checklist_creation", "work_on_issue")

    system_prompt = (
        "You are an implementation checklist generator. Given an implementation plan, "
        "break it down into discrete, actionable checklist items. Each item should be "
        "small enough to implement in a single TDD cycle (write test, implement, verify).\n\n"
        "Respond with a JSON object containing:\n"
        '- "items": list of objects, each with:\n'
        '  - "description": what needs to be done\n'
        '  - "acceptance_criteria": how to verify completion\n'
        '  - "estimated_complexity": "low", "medium", or "high"\n'
        '  - "is_complete": false\n'
    )

    user_prompt = f"Issue: {issue_key}\n\nImplementation Plan:\n{plan}"

    async def _call_llm():
        from agentic_devtools.orchestration.llm.types import LLMMessage

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt),
        ]
        response = await provider.complete(messages)
        return response

    response = _run_async(_call_llm())

    token_usage = {}
    if response.usage:
        token_usage = {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
        }

    _FALLBACK_ITEM = [
        {
            "description": "Implement the plan as described",
            "acceptance_criteria": "All tests pass",
            "estimated_complexity": "medium",
            "is_complete": False,
        }
    ]

    try:
        parsed = json.loads(response.text)
        if isinstance(parsed, dict):
            items = parsed.get("items", [])
            if not (isinstance(items, list) and items):
                items = _FALLBACK_ITEM
        else:
            items = _FALLBACK_ITEM
    except (json.JSONDecodeError, TypeError):
        # Fallback: create a single item from the plan
        items = _FALLBACK_ITEM

    return {"items": items, "token_usage": token_usage}
