"""Shared sample trio configuration documents for trio_config symbol tests."""

from __future__ import annotations

from agentic_devtools.ai_providers.tier_selector import TIER_LADDER
from agentic_devtools.cli.azure_devops.review_attribution import get_model_family

_DOER_MODELS = {
    "tier-1": ("mai-code-1.1-flash", "gpt-5.6-luna"),
    "tier-2": ("claude-sonnet-5", "gemini-3.1-pro-preview"),
    "tier-3": ("claude-opus-5", "claude-opus-4.8"),
}


def document(*, doer_tier: str = "tier-1") -> dict:
    doer_preference, doer_fallback = _DOER_MODELS[doer_tier]
    roles = {
        "doer": {"tier": doer_tier, "modelPreference": doer_preference, "fallbackModels": [doer_fallback]},
        "duckA": {
            "tier": "tier-2",
            "modelPreference": "claude-sonnet-5",
            "fallbackModels": ["gemini-3.1-pro-preview"],
        },
        "duckB": {"tier": "tier-1", "modelPreference": "gpt-5.6-luna", "fallbackModels": ["mai-code-1.1-flash"]},
        "adjudicator": {
            "tier": "tier-3",
            "modelPreference": "claude-opus-5",
            "fallbackModels": ["claude-opus-4.8"],
        },
        "heavyweightDuckA": {
            "tier": "tier-3",
            "modelPreference": "claude-opus-4.8",
            "fallbackModels": ["claude-opus-5"],
        },
        "heavyweightDuckB": {
            "tier": "tier-3",
            "modelPreference": "claude-opus-4.6",
            "fallbackModels": ["claude-opus-5"],
        },
        "heavyweightAdjudicator": {
            "tier": "tier-3",
            "modelPreference": "claude-opus-5",
            "fallbackModels": ["claude-opus-4.8"],
        },
    }
    return {
        "schemaVersion": "1.0",
        "trioRef": "example-trio",
        "roles": roles,
        "reviewCap": {
            "mode": "standard",
            "maxRounds": 5,
            "maxPointsPerReview": 20,
            "timeBudgetMinutes": 30,
        },
        "rotationPolicy": {
            "requireDistinctModels": True,
            "requireDistinctReviewerFamilies": True,
            "onExhaustion": "rotate_then_escalate",
        },
        "adjudicationPolicy": {
            "allowOverturn": True,
            "requireEvidentiaryReasoning": True,
            "failClosedOnDispute": True,
        },
    }


def metadata(*models: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for model in models:
        for tier, tier_models in TIER_LADDER.items():
            if model in tier_models:
                result[model] = {
                    "tier": tier,
                    "modelFamily": get_model_family(model) or model.lower(),
                    "status": "available",
                }
                break
    return result


def canonical_metadata(*models: str) -> dict[str, dict[str, object]]:
    return {
        model: {
            "modelId": model,
            "surfaces": {
                "copilot": {"modelId": model},
                "vscode": {"displayName": model},
                "docs": {"displayName": model},
            },
        }
        for model in models
    }


def availability(*models: str, unavailable: tuple[str, ...] = ()) -> dict[str, str]:
    unavailable_set = set(unavailable)
    return {model: ("unavailable" if model in unavailable_set else "available") for model in models}
