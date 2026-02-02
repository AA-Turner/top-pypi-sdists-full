"""
DSLighting Grading System

Unified grading helpers and evaluators.
Includes a generic Evaluator, Task model, and metric utilities.
"""

from dslighting.benchmark.grading.evaluator import Evaluator
from dslighting.benchmark.grading.task import Task
from dslighting.benchmark.grading.metrics import grade_submission, METRIC_FUNCTIONS

# Compatibility aliases.
UniversalEvaluator = Evaluator
KaggleEvaluator = Evaluator

__all__ = [
    "Evaluator",
    "UniversalEvaluator",  # Alias for Evaluator
    "KaggleEvaluator",     # Alias for Evaluator
    "Task",
    "grade_submission",
    "METRIC_FUNCTIONS",
]
