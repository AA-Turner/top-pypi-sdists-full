from abc import abstractmethod
import time
import sys


class AlgoTracker:
    def __init__(self, visualizer=None, pseudocode_builder=None):
        self.steps = []
        self.visualizer = visualizer
        self.pseudocode_builder = pseudocode_builder
        self.start_time = None
        self.end_time = None
        self.total_memory = 0

    def start(self, data):
        self.start_time = time.perf_counter()
        self.total_memory += sys.getsizeof(data)

    def end(self):
        self.end_time = time.perf_counter()

    @abstractmethod
    def log_step(self, *args, **kwargs):
        pass

    @abstractmethod
    def print_steps(self):
        pass

    @abstractmethod
    def print_summary(self):
        # shared summary logic
        pass

    @abstractmethod
    def visualize(self):
        pass

    @abstractmethod
    def print_pseudocode(self):
        pass