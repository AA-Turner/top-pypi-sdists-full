"""Declarative reward recipes for hosted training runtimes.

These recipes are intentionally lightweight and runtime-focused so they can be
used from sandboxes and API workers without importing the heavier reward
aggregation stack.
"""

from __future__ import annotations

import hashlib
import math
import re
import typing as t
from dataclasses import dataclass, field


@dataclass(slots=True)
class RewardPromptRow:
    """Minimal prompt-row information needed by declarative reward recipes."""

    expected_output: str | None = None
    reward: float | None = None
    metadata: dict[str, t.Any] = field(default_factory=dict)
    template_context: dict[str, str | int | None] = field(default_factory=dict)


@dataclass(slots=True)
class RewardTaskDefinition:
    """Minimal task metadata needed by declarative reward recipes."""

    reference: str
    verification: dict[str, t.Any] | None = None


@dataclass(slots=True)
class RewardEvaluationContext:
    """Inputs available to a reward recipe during rollout scoring."""

    completion: str
    prompt_row: RewardPromptRow
    task: RewardTaskDefinition | None = None
    recipe_params: dict[str, t.Any] = field(default_factory=dict)


@dataclass(slots=True)
class RewardEvaluationResult:
    """Normalized reward output from a declarative recipe."""

    reward: float
    metrics: dict[str, t.Any] = field(default_factory=dict)


class RewardRecipeRegistry:
    """Resolve declarative reward recipes into executable scorers."""

    def __init__(self) -> None:
        self._recipes: dict[
            str, t.Callable[[RewardEvaluationContext], RewardEvaluationResult]
        ] = {
            "contains_v1": self._contains_v1,
            "exact_match_v1": self._exact_match_v1,
            "trajectory_imitation_v1": self._trajectory_imitation_v1,
            "row_reward_v1": self._row_reward_v1,
            "task_verifier_v1": self._task_verifier_v1,
            "gsm8k_v1": self._gsm8k_v1,
        }

    def evaluate(
        self,
        *,
        reward_recipe: dict[str, t.Any] | None,
        completion: str,
        prompt_row: RewardPromptRow,
        task: RewardTaskDefinition | None,
    ) -> RewardEvaluationResult:
        recipe_name = "row_reward_v1"
        recipe_params: dict[str, t.Any] = {}
        if reward_recipe is not None:
            recipe_name = str(reward_recipe.get("name") or recipe_name)
            params = reward_recipe.get("params")
            if isinstance(params, dict):
                recipe_params = params

        recipe = self._recipes.get(recipe_name)
        if recipe is None:
            raise ValueError(f"Unknown reward recipe: {recipe_name}")

        return recipe(
            RewardEvaluationContext(
                completion=completion,
                prompt_row=prompt_row,
                task=task,
                recipe_params=recipe_params,
            )
        )

    def _contains_v1(self, context: RewardEvaluationContext) -> RewardEvaluationResult:
        needle = context.recipe_params.get("needle")
        if not isinstance(needle, str) or not needle:
            raise ValueError("contains_v1 requires params.needle")

        passed = needle in context.completion
        reward = float(
            context.recipe_params.get("reward_if_true", 1.0 if passed else 0.0)
        )
        if not passed:
            reward = float(context.recipe_params.get("reward_if_false", 0.0))

        return RewardEvaluationResult(
            reward=reward,
            metrics={"reward/passed": passed, "reward/recipe": "contains_v1"},
        )

    def _exact_match_v1(self, context: RewardEvaluationContext) -> RewardEvaluationResult:
        expected = context.recipe_params.get("expected")
        if not isinstance(expected, str) or not expected:
            expected = context.prompt_row.expected_output
        if not expected:
            raise ValueError("exact_match_v1 requires an expected output")

        passed = context.completion.strip() == expected.strip()
        reward = 1.0 if passed else 0.0
        return RewardEvaluationResult(
            reward=reward,
            metrics={"reward/passed": passed, "reward/recipe": "exact_match_v1"},
        )

    def _row_reward_v1(self, context: RewardEvaluationContext) -> RewardEvaluationResult:
        reward = context.prompt_row.reward
        if reward is None:
            reward = float(context.recipe_params.get("default", 0.0))
        return RewardEvaluationResult(
            reward=reward,
            metrics={"reward/recipe": "row_reward_v1"},
        )

    def _trajectory_imitation_v1(
        self,
        context: RewardEvaluationContext,
    ) -> RewardEvaluationResult:
        expected = context.recipe_params.get("expected")
        if not isinstance(expected, str) or not expected:
            expected = context.prompt_row.expected_output
        if not expected:
            raise ValueError("trajectory_imitation_v1 requires an expected output")

        passed = context.completion.strip() == expected.strip()
        if passed:
            reward = context.prompt_row.reward
            if reward is None:
                reward = float(context.recipe_params.get("reward_if_true", 1.0))
        else:
            reward = float(context.recipe_params.get("reward_if_false", 0.0))

        return RewardEvaluationResult(
            reward=float(reward),
            metrics={
                "reward/passed": passed,
                "reward/recipe": "trajectory_imitation_v1",
                "reward/base_reward": context.prompt_row.reward,
            },
        )

    def _task_verifier_v1(self, context: RewardEvaluationContext) -> RewardEvaluationResult:
        verification = context.task.verification if context.task is not None else None
        if not isinstance(verification, dict):
            raise TypeError("task_verifier_v1 requires a task with verification config")

        method = verification.get("method")
        if method != "flag":
            raise ValueError(
                "task_verifier_v1 currently supports only flag-based task verification"
            )

        # Accept new `hash` key first, fall back to legacy `flag_hash` for
        # pre-migration task definitions.
        expected_hash = verification.get("hash") or verification.get("flag_hash")
        if not isinstance(expected_hash, str) or not expected_hash.startswith("sha256:"):
            raise ValueError("task_verifier_v1 requires verification.hash")

        normalized = context.completion.strip()
        computed_hash = f"sha256:{hashlib.sha256(normalized.encode()).hexdigest()}"
        passed = computed_hash == expected_hash
        reward = float(
            context.recipe_params.get("reward_if_true", 1.0 if passed else 0.0)
        )
        if not passed:
            reward = float(context.recipe_params.get("reward_if_false", 0.0))

        return RewardEvaluationResult(
            reward=reward,
            metrics={
                "reward/passed": passed,
                "reward/recipe": "task_verifier_v1",
                "reward/computed_hash": computed_hash,
            },
        )

    def _gsm8k_v1(self, context: RewardEvaluationContext) -> RewardEvaluationResult:
        """Score a GSM8K-style completion against a numeric ground truth.

        Pairs naturally with prompt rows whose ``expected_output`` is the
        original gsm8k ``answer`` field (which already ends with
        ``#### <number>``). The recipe extracts the trailing number from
        both sides, normalizes commas/whitespace, and compares with float
        tolerance — ``1,000``, ``1000.0`` and ``1000`` all match.
        """

        expected_raw = context.recipe_params.get("expected") or context.prompt_row.expected_output
        if not isinstance(expected_raw, str) or not expected_raw:
            raise ValueError(
                "gsm8k_v1 requires expected_output (or params.expected)"
            )

        expected_value = _extract_gsm8k_final_answer(expected_raw)
        if expected_value is None:
            raise ValueError(
                "gsm8k_v1 expected_output did not contain a parseable answer "
                "(`#### <n>` or a bare number)"
            )

        actual_value = _extract_gsm8k_final_answer(context.completion)
        extraction_failed = actual_value is None

        reward_if_true = float(context.recipe_params.get("reward_if_true", 1.0))
        reward_if_false = float(context.recipe_params.get("reward_if_false", 0.0))

        if extraction_failed or not math.isclose(
            actual_value,  # type: ignore[arg-type]
            expected_value,
            rel_tol=1e-6,
            abs_tol=1e-6,
        ):
            passed = False
        else:
            passed = True

        return RewardEvaluationResult(
            reward=reward_if_true if passed else reward_if_false,
            metrics={
                "reward/recipe": "gsm8k_v1",
                "reward/passed": passed,
                "reward/expected": expected_value,
                "reward/actual": actual_value,
                "reward/extraction_failed": extraction_failed,
            },
        )


_GSM8K_FINAL_ANSWER_PATTERN = re.compile(r"####\s*([-+]?[\d,]+(?:\.\d+)?)")
_BARE_NUMBER_PATTERN = re.compile(r"[-+]?[\d,]*\d(?:\.\d+)?")


def _extract_gsm8k_final_answer(text: str) -> float | None:
    """Extract the final numeric answer from a GSM8K-style string.

    Prefers the explicit ``#### <n>`` marker (canonical gsm8k format). When
    multiple markers appear (intermediate calculations), the last one wins.
    Falls back to the last bare number in the text — handles cases where
    the model emits the answer without the delimiter. Returns ``None`` when
    nothing parseable is found, which the recipe treats as extraction
    failure (reward = ``reward_if_false``).
    """

    matches = list(_GSM8K_FINAL_ANSWER_PATTERN.finditer(text))
    if matches:
        return _normalize_number(matches[-1].group(1))

    bare = list(_BARE_NUMBER_PATTERN.finditer(text))
    if bare:
        return _normalize_number(bare[-1].group(0))

    return None


def _normalize_number(raw: str) -> float | None:
    """Strip commas/whitespace/trailing-period and parse as float."""

    cleaned = raw.strip().rstrip(".").replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


__all__ = [
    "RewardEvaluationContext",
    "RewardEvaluationResult",
    "RewardPromptRow",
    "RewardRecipeRegistry",
    "RewardTaskDefinition",
]
