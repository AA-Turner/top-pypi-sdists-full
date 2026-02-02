# dslighting/benchmark/native/grader.py

import logging
from typing import Dict, Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# A registry of metric functions
METRIC_FUNCTIONS = {}

def register_metric(name):
    """Decorator to register a new metric function."""
    def decorator(func):
        METRIC_FUNCTIONS[name] = func
        return func
    return decorator

@register_metric("rmsle")
def root_mean_squared_log_error(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Calculates Root Mean Squared Logarithmic Error."""
    return np.sqrt(np.mean(np.power(np.log1p(y_pred) - np.log1p(y_true), 2)))

@register_metric("accuracy")
def accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Calculates accuracy score."""
    return np.mean(y_true == y_pred)

def grade_submission(
    submission_df: pd.DataFrame,
    ground_truth_df: pd.DataFrame,
    metric: str,
    id_column: str = "id",
    target_column: str = "target",
) -> float:
    """
    Grades a submission dataframe against a ground truth dataframe using a specified metric.

    Args:
        submission_df: DataFrame of the agent's submission.
        ground_truth_df: DataFrame of the ground truth answers.
        metric: The name of the metric to use (e.g., 'rmsle', 'accuracy').
        id_column: The name of the ID column to join on.
        target_column: The name of the target column to score.

    Returns:
        The calculated score as a float.
    """
    if metric not in METRIC_FUNCTIONS:
        raise ValueError(f"Unknown metric: '{metric}'. Available metrics are: {list(METRIC_FUNCTIONS.keys())}")

    # Merge submission and ground truth
    merged_df = pd.merge(submission_df, ground_truth_df, on=id_column, how="left")

    # Handle cases where the merge adds suffixes
    pred_col_name = f"{target_column}_x" if f"{target_column}_x" in merged_df.columns else target_column
    true_col_name = f"{target_column}_y" if f"{target_column}_y" in merged_df.columns else target_column

    if pred_col_name not in merged_df.columns:
        raise ValueError(f"Target column '{target_column}' not found in submission after merge.")
    if true_col_name not in merged_df.columns:
        raise ValueError(f"Target column '{target_column}' not found in ground truth after merge.")

    y_pred = merged_df[pred_col_name]
    y_true = merged_df[true_col_name]

    # Drop rows where ground truth is missing
    valid_indices = y_true.notna()
    if valid_indices.sum() == 0:
        logger.warning("No valid ground truth values found after merging. Score is 0.")
        return 0.0
    
    if valid_indices.sum() < len(y_true):
        logger.warning(
            f"Submission contains {len(y_true) - valid_indices.sum()} predictions "
            "for which there is no ground truth. These will be ignored."
        )
        y_pred = y_pred[valid_indices]
        y_true = y_true[valid_indices]

    # Calculate score
    metric_fn = METRIC_FUNCTIONS[metric]
    score = metric_fn(y_true, y_pred)
    
    logger.info(f"Grading successful. Metric '{metric}': {score:.4f}")
    return score
