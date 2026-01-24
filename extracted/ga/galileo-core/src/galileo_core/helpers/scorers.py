"""
Scorer utility functions and constants.

This module contains utility functions for working with scorer names and metric names,
including mappings between metric names and their corresponding scorer names.
"""

from re import match
from typing import Optional

from galileo_core.schemas.shared.scorers.scorer_name import ScorerName

# Used to validate custom scorer names.
SCORER_NAME_REGEX = r"^[\w -]+$"


METRIC_TO_SCORER_NAME = {
    # The luna/plus mess.
    "groundedness": ScorerName.context_adherence,
    "completeness_gpt": ScorerName.completeness,
    "retriever_attribution": ScorerName.chunk_attribution_utilization,
    "retriever_utilization": ScorerName.chunk_attribution_utilization,
    "rag_nli_adherence": ScorerName.context_adherence_luna,
    "context_adherence_luna": ScorerName.context_adherence_luna,
    "rag_nli_completeness": ScorerName.completeness_luna,
    "rag_nli_retriever_attribution": ScorerName.chunk_attribution_utilization_luna,
    "rag_nli_retriever_utilization": ScorerName.chunk_attribution_utilization_luna,
    "rag_nli_retriever_relevance": ScorerName.chunk_attribution_utilization_luna,
    # The output scorers.
    "pii": ScorerName.output_pii,
    "sexist": ScorerName.output_sexist_luna,
    "tone": ScorerName.output_tone,
    "toxicity": ScorerName.output_toxicity_luna,
    "input_toxicity": ScorerName.input_toxicity_luna,
    "input_sexist": ScorerName.input_sexist_luna,
    # Others.
    "factuality": ScorerName.correctness,
    "prompt_injection_gpt": ScorerName.prompt_injection,
    "prompt_injection": ScorerName.prompt_injection_luna,
    "sexist_gpt": ScorerName.output_sexist,
    "input_sexist_gpt": ScorerName.input_sexist,
    "toxicity_gpt": ScorerName.output_toxicity,
    "input_toxicity_gpt": ScorerName.input_toxicity,
}


# Reverse mapping from scorer names to all associated metric names.
SCORER_TO_ALL_METRICS = {}
for scorer in ScorerName:
    # Find all metrics that map to this scorer
    mapped_metrics = [
        metric_name for metric_name, scorer_name in METRIC_TO_SCORER_NAME.items() if scorer_name == scorer
    ]

    # If no metrics map to this scorer, use the scorer's own value as the metric
    if not mapped_metrics:
        mapped_metrics = [scorer.value]

    SCORER_TO_ALL_METRICS[scorer.value] = mapped_metrics


def check_scorer_name(name: str) -> str:
    """
    Check if name contains only letters, numbers, space, - and _.

    Parameters
    ----------
    name : str
        The scorer name to validate.

    Returns
    -------
    str
        The validated scorer name.

    Raises
    ------
    ValueError
        If the scorer name contains invalid characters.
    """
    if not bool(match(SCORER_NAME_REGEX, name)):
        raise ValueError("Scorer name cannot contain special characters, only letters, numbers, space, - and _.")
    return name


def get_scorer_name_from_metric_name(metric_name: str) -> Optional[ScorerName]:
    """
    Get the scorer name from the metric name and return None if no scorer matches.

    This function first checks the METRIC_TO_SCORER_NAME mapping for special cases
    where the metric name doesn't directly correspond to the scorer name. If not found,
    it tries to match the metric name directly to a ScorerName enum value.

    Parameters
    ----------
    metric_name : str
        The metric name to look up. Leading underscores will be stripped.

    Returns
    -------
    Optional[ScorerName]
        The corresponding ScorerName enum value, or None if no match is found.
    """
    metric_name = metric_name.lstrip("_")

    # For metrics that don't match their scorer name.
    scorer_name = METRIC_TO_SCORER_NAME.get(metric_name)
    if scorer_name is None:
        try:
            # For metrics that do match their scorer name.
            scorer_name = ScorerName(metric_name)
        except ValueError:
            # Return None if metric name not in ScorerName enum.
            return None
    return scorer_name
