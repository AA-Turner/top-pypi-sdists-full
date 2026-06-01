from __future__ import annotations
from enum import Enum
from kanban_framework.infra.consts import Consts


class IterationAction(Enum):
    PASS = "retrospective"
    HOT = "hot_iteration"
    FULL = "full_iteration"
    MAX_ITER = "max_iterations"
    RETRY_PREV = "retry_previous"


class IterationDecider:
    @staticmethod
    def decide(
        avg_score: float,
        iteration: int,
        max_iter: int = Consts.MAX_ITERATIONS,
        pass_threshold: float = Consts.PASS_THRESHOLD,
        hot_min_score: float = Consts.HOT_ITERATION_MIN_SCORE,
    ) -> IterationAction:
        if iteration >= max_iter:
            return IterationAction.MAX_ITER
        if avg_score >= pass_threshold:
            return IterationAction.PASS
        if avg_score >= hot_min_score:
            return IterationAction.HOT
        return IterationAction.FULL

    @staticmethod
    def decide_quality_gate(
        score: float,
        round_num: int,
        max_rounds: int = 3,
        pass_threshold: float = 7.0,
    ) -> IterationAction:
        """Quality gate decision for plan_review and spec_review phases.

        Returns RETRY_PREV if score < threshold and rounds remain,
        PASS if score >= threshold, MAX_ITER if rounds exhausted.
        """
        if score >= pass_threshold:
            return IterationAction.PASS
        if round_num >= max_rounds:
            return IterationAction.MAX_ITER
        return IterationAction.RETRY_PREV
