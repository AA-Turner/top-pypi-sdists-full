from abc import ABC, abstractmethod


class StepVisualizer(ABC):
    @abstractmethod
    def visualize(self, steps):
        pass
