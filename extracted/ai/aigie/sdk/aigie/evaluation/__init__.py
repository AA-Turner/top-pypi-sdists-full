"""
Aigie Evaluation Framework for Kytte Production Runtime.

Implements the EVALUATE step in Kytte's Detect → Evaluate → Fix flow:

    Detect → [EVALUATE] → Fix
                ↑
           (this module)

Features:
- Runtime agent evaluation for instant error identification
- LLM-as-Judge scoring for remediation decisions
- Reinforcement learning compatible output format
- Integration with backend's UnifiedLLMJudgeService

Usage:
    from aigie.evaluation import LLMJudge

    judge = LLMJudge()

    # For remediation decisions (Detect → Evaluate → Fix)
    result = await judge.evaluate_for_remediation(
        input="User query",
        output="Agent response",
        error=detected_error,  # From DETECT step
    )

    if result["needs_remediation"]:
        # Trigger FIX step via RemediationService
        trigger = result["remediation_trigger"]
"""

from .llm_judge import (
    CriterionScore,
    EvaluationCriteria,
    EvaluationResult,
    JudgeConfig,
    LLMJudge,
)
from .scorers import (
    BaseScorer,
    CoherenceScorer,
    FactualityScorer,
    HelpfulnessScorer,
    RelevanceScorer,
    SafetyScorer,
)

__all__ = [
    # LLM Judge (EVALUATE step)
    "LLMJudge",
    "EvaluationResult",
    "EvaluationCriteria",
    "JudgeConfig",
    "CriterionScore",
    # Specialized Scorers
    "BaseScorer",
    "RelevanceScorer",
    "CoherenceScorer",
    "FactualityScorer",
    "HelpfulnessScorer",
    "SafetyScorer",
]
