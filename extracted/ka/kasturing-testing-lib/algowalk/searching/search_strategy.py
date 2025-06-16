from algowalk.searching.tracker.search_algo_tracker import StepTracker
from abc import abstractmethod
from algowalk.utils.tracker.algo_tracker import AlgoTracker
from algowalk.utils.strategy.algorithm_strategy import AlgorithmStrategy


class SearchStrategy(AlgorithmStrategy):

    def sort(self, data, tracker: AlgoTracker):
        raise NotImplementedError('Sort method is not applicable for search strategies.')

    @abstractmethod
    def search(self, data, target, tracker: StepTracker):
        pass

    def pseudocode(self, tracker: StepTracker):
        pseudo = tracker.pseudocode_builder
        if pseudo:
            pseudo.bundle_generation(self.search)
