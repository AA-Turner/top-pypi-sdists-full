from algowalk.utils.tracker.algo_tracker import AlgoTracker
from algowalk.utils.strategy.algorithm_strategy import AlgorithmStrategy
from .tracker.sort_algorithm_tracker import StepTracker


class SortStrategy(AlgorithmStrategy):

    def search(self, data, target, tracker: AlgoTracker):
        raise NotImplementedError("Search method is not applicable for sorting strategies.")

    def pseudocode(self, tracker: StepTracker):
        pseudo = tracker.pseudocode_builder
        if pseudo:
            pseudo.bundle_generation(self.sort)

    def sort(self, data, tracker: AlgoTracker):
        pass
