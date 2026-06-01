from __future__ import annotations
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.scheduler import Scheduler


class EvaluationManager:
    def __init__(self, fs: Filesystem, config: Config):
        self._fs = fs
        self._cfg = config

    def calculate_average(self, reports: dict) -> float:
        scores = [r.get("total", 0) for r in reports.values()]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)

    def is_passing(self, score: float) -> bool:
        return score >= self._cfg.pass_threshold

    def should_run_parallel(self) -> bool:
        return True

    def eval_roles(self) -> list[dict]:
        return Scheduler.eval_roles()

    @staticmethod
    def round_score(score: float, ndigits: int = 2) -> float:
        return round(score, ndigits)
