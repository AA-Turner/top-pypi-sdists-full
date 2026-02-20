from typing import Dict, List


class ClickStrategyLearner:
    STRATEGIES = ["bbox", "text", "selector", "force", "js"]

    def __init__(self) -> None:
        self.stats: Dict[str, Dict[str, Dict[str, int]]] = {}
        self.global_stats: Dict[str, Dict[str, int]] = {
            s: {"success": 0, "failure": 0} for s in self.STRATEGIES
        }

    def record_result(self, element_type: str, strategy: str, success: bool) -> None:
        if element_type not in self.stats:
            self.stats[element_type] = {
                s: {"success": 0, "failure": 0} for s in self.STRATEGIES
            }
        key = "success" if success else "failure"
        self.stats[element_type][strategy][key] += 1
        self.global_stats[strategy][key] += 1

    def get_ordered_strategies(self, element_type: str) -> List[str]:
        stats = self.stats.get(element_type, self.global_stats)

        def success_rate(strategy: str) -> float:
            s = stats[strategy]
            total = s["success"] + s["failure"]
            if total == 0:
                return 0.5
            return s["success"] / total

        ordered = sorted(self.STRATEGIES, key=success_rate, reverse=True)

        filtered = []
        for strategy in ordered:
            s = stats[strategy]
            total = s["success"] + s["failure"]
            rate = success_rate(strategy)
            if total < 3 or rate >= 0.1:
                filtered.append(strategy)

        return filtered if filtered else self.STRATEGIES
