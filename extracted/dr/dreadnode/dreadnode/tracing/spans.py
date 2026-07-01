"""Span factories for type-safe tracing.

Only study_span and trial_span are actively used by Study.
All other span creation should use dreadnode.task_span() directly.
"""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from dreadnode.tracing.span import TaskSpan


def study_span(
    name: str,
    *,
    label: str | None = None,
    tags: list[str] | None = None,
    airt_assessment_id: str | None = None,
    airt_attack_name: str | None = None,
    airt_goal: str | None = None,
    airt_goal_category: str | None = None,
    airt_category: str | None = None,
    airt_sub_category: str | None = None,
    airt_transforms: list[str] | None = None,
    airt_target_model: str | None = None,
    airt_attacker_model: str | None = None,
    airt_evaluator_model: str | None = None,
    airt_attack_domain: str | None = None,
    airt_distance_norm: str | None = None,
    airt_input_modality: str | None = None,
    airt_perturbation_budget: float | None = None,
    airt_original_class: str | None = None,
) -> TaskSpan[t.Any]:
    """
    Create a bare span for optimization study execution.

    Events populate all attributes via emit().

    Args:
        name: The study name.
        label: Human-readable label.
        tags: Additional tags.
        airt_assessment_id: AIRT assessment ID (for platform linking).
        airt_attack_name: AIRT attack name.
        airt_goal: AIRT attack goal.
        airt_goal_category: AIRT goal category.
        airt_transforms: AIRT transforms applied.
        airt_target_model: Target model identifier.
        airt_attacker_model: Attacker model identifier.
        airt_evaluator_model: Evaluator model identifier.

    Returns:
        A bare TaskSpan for study execution.
    """
    from dreadnode import task_span

    # Inherit assessment_id from context if not explicitly passed
    if airt_assessment_id is None:
        try:
            from dreadnode.airt.assessment import _current_assessment

            current = _current_assessment.get()
            if current is not None and current.assessment_id is not None:
                airt_assessment_id = current.assessment_id
        except ImportError:
            pass

    airt_attrs: dict[str, str | float | list[str]] = {}
    if any(
        [
            airt_assessment_id,
            airt_attack_name,
            airt_goal,
            airt_goal_category,
            airt_transforms,
            airt_attack_domain,
        ]
    ):
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_ASSESSMENT_ID,
            AIRT_ATTRIBUTE_ATTACK_DOMAIN,
            AIRT_ATTRIBUTE_ATTACK_NAME,
            AIRT_ATTRIBUTE_ATTACKER_MODEL,
            AIRT_ATTRIBUTE_CATEGORY,
            AIRT_ATTRIBUTE_DISTANCE_NORM,
            AIRT_ATTRIBUTE_EVALUATOR_MODEL,
            AIRT_ATTRIBUTE_GOAL,
            AIRT_ATTRIBUTE_GOAL_CATEGORY,
            AIRT_ATTRIBUTE_INPUT_MODALITY,
            AIRT_ATTRIBUTE_ORIGINAL_CLASS,
            AIRT_ATTRIBUTE_PERTURBATION_BUDGET,
            AIRT_ATTRIBUTE_SUB_CATEGORY,
            AIRT_ATTRIBUTE_TARGET_MODEL,
            AIRT_ATTRIBUTE_TRANSFORMS,
        )

        if airt_assessment_id:
            airt_attrs[AIRT_ATTRIBUTE_ASSESSMENT_ID] = airt_assessment_id
        if airt_attack_name:
            airt_attrs[AIRT_ATTRIBUTE_ATTACK_NAME] = airt_attack_name
        if airt_goal:
            airt_attrs[AIRT_ATTRIBUTE_GOAL] = airt_goal
        if airt_goal_category:
            airt_attrs[AIRT_ATTRIBUTE_GOAL_CATEGORY] = airt_goal_category
        if airt_category:
            airt_attrs[AIRT_ATTRIBUTE_CATEGORY] = airt_category
        if airt_sub_category:
            airt_attrs[AIRT_ATTRIBUTE_SUB_CATEGORY] = airt_sub_category
        if airt_transforms:
            airt_attrs[AIRT_ATTRIBUTE_TRANSFORMS] = airt_transforms
        if airt_target_model:
            airt_attrs[AIRT_ATTRIBUTE_TARGET_MODEL] = airt_target_model
        if airt_attacker_model:
            airt_attrs[AIRT_ATTRIBUTE_ATTACKER_MODEL] = airt_attacker_model
        if airt_evaluator_model:
            airt_attrs[AIRT_ATTRIBUTE_EVALUATOR_MODEL] = airt_evaluator_model
        if airt_attack_domain:
            airt_attrs[AIRT_ATTRIBUTE_ATTACK_DOMAIN] = airt_attack_domain
        if airt_distance_norm:
            airt_attrs[AIRT_ATTRIBUTE_DISTANCE_NORM] = airt_distance_norm
        if airt_input_modality:
            airt_attrs[AIRT_ATTRIBUTE_INPUT_MODALITY] = airt_input_modality
        if airt_perturbation_budget is not None:
            airt_attrs[AIRT_ATTRIBUTE_PERTURBATION_BUDGET] = airt_perturbation_budget
        if airt_original_class:
            airt_attrs[AIRT_ATTRIBUTE_ORIGINAL_CLASS] = airt_original_class

    transforms_suffix = ""
    if airt_transforms:
        transforms_suffix = f" [{', '.join(airt_transforms)}]"

    return task_span(
        name=f"study:{name}{transforms_suffix}",
        type="study",
        label=(label or name) + transforms_suffix,
        tags=["study", "optimization", *(tags or [])],
        attributes=airt_attrs or None,
    )


def trial_span(
    trial_id: str,
    *,
    step: int,
    task_name: str | None = None,
    label: str | None = None,
    tags: list[str] | None = None,
    airt_assessment_id: str | None = None,
    airt_trial_index: int | None = None,
    airt_attack_name: str | None = None,
    airt_goal: str | None = None,
    airt_goal_category: str | None = None,
    airt_category: str | None = None,
    airt_sub_category: str | None = None,
    airt_transforms: list[str] | None = None,
    airt_target_model: str | None = None,
    airt_attacker_model: str | None = None,
    airt_evaluator_model: str | None = None,
    airt_attack_domain: str | None = None,
    airt_distance_norm: str | None = None,
    airt_input_modality: str | None = None,
) -> TaskSpan[t.Any]:
    """
    Create a bare span for optimization trial.

    Events populate all attributes via emit().

    Args:
        trial_id: Unique trial identifier.
        step: Trial number in the study.
        task_name: Name of the task being evaluated (for label).
        label: Human-readable label.
        tags: Additional tags.
        airt_assessment_id: AIRT assessment ID (for linking trial to assessment).
        airt_trial_index: AIRT trial index within the attack.
        airt_attack_name: AIRT attack name.
        airt_goal: AIRT attack goal.
        airt_goal_category: AIRT goal category.
        airt_transforms: AIRT transforms applied.
        airt_target_model: Target model identifier.
        airt_attacker_model: Attacker model identifier.
        airt_evaluator_model: Evaluator/judge model identifier.

    Returns:
        A bare TaskSpan for trial execution.
    """
    from dreadnode import task_span

    airt_attrs: dict[str, str | int | list[str]] = {}
    if any(
        [
            airt_assessment_id,
            airt_trial_index is not None,
            airt_attack_name,
            airt_goal_category,
            airt_attack_domain,
        ]
    ):
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_ASSESSMENT_ID,
            AIRT_ATTRIBUTE_ATTACK_DOMAIN,
            AIRT_ATTRIBUTE_ATTACK_NAME,
            AIRT_ATTRIBUTE_CATEGORY,
            AIRT_ATTRIBUTE_DISTANCE_NORM,
            AIRT_ATTRIBUTE_GOAL,
            AIRT_ATTRIBUTE_GOAL_CATEGORY,
            AIRT_ATTRIBUTE_INPUT_MODALITY,
            AIRT_ATTRIBUTE_SUB_CATEGORY,
            AIRT_ATTRIBUTE_TARGET_MODEL,
            AIRT_ATTRIBUTE_TRANSFORMS,
            AIRT_ATTRIBUTE_TRIAL_INDEX,
        )

        if airt_assessment_id:
            airt_attrs[AIRT_ATTRIBUTE_ASSESSMENT_ID] = airt_assessment_id
        if airt_trial_index is not None:
            airt_attrs[AIRT_ATTRIBUTE_TRIAL_INDEX] = airt_trial_index
        if airt_attack_name:
            airt_attrs[AIRT_ATTRIBUTE_ATTACK_NAME] = airt_attack_name
        if airt_goal:
            airt_attrs[AIRT_ATTRIBUTE_GOAL] = airt_goal
        if airt_goal_category:
            airt_attrs[AIRT_ATTRIBUTE_GOAL_CATEGORY] = airt_goal_category
        if airt_category:
            airt_attrs[AIRT_ATTRIBUTE_CATEGORY] = airt_category
        if airt_sub_category:
            airt_attrs[AIRT_ATTRIBUTE_SUB_CATEGORY] = airt_sub_category
        if airt_transforms is not None:
            airt_attrs[AIRT_ATTRIBUTE_TRANSFORMS] = airt_transforms
        if airt_target_model:
            airt_attrs[AIRT_ATTRIBUTE_TARGET_MODEL] = airt_target_model
        if airt_attacker_model:
            from dreadnode.tracing.constants import AIRT_ATTRIBUTE_ATTACKER_MODEL

            airt_attrs[AIRT_ATTRIBUTE_ATTACKER_MODEL] = airt_attacker_model
        if airt_evaluator_model:
            from dreadnode.tracing.constants import AIRT_ATTRIBUTE_EVALUATOR_MODEL

            airt_attrs[AIRT_ATTRIBUTE_EVALUATOR_MODEL] = airt_evaluator_model
        if airt_attack_domain:
            airt_attrs[AIRT_ATTRIBUTE_ATTACK_DOMAIN] = airt_attack_domain
        if airt_distance_norm:
            airt_attrs[AIRT_ATTRIBUTE_DISTANCE_NORM] = airt_distance_norm
        if airt_input_modality:
            airt_attrs[AIRT_ATTRIBUTE_INPUT_MODALITY] = airt_input_modality

    return task_span(
        name=f"trial:{trial_id[:8]}",
        type="trial",
        label=label or (f"{task_name} [{step}]" if task_name else f"trial_{step}"),
        tags=["trial", *(tags or [])],
        attributes=airt_attrs or None,
    )
