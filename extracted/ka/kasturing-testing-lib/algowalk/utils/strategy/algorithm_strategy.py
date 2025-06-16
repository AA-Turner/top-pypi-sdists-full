from abc import ABC, abstractmethod
from algowalk.utils.tracker.algo_tracker import AlgoTracker


class AlgorithmStrategy(ABC):

    @abstractmethod
    def search(self, data, target, tracker: AlgoTracker):
        pass

    @abstractmethod
    def pseudocode(self, tracker: AlgoTracker):
        pass

    @abstractmethod
    def sort(self, data, tracker: AlgoTracker):
        pass
