from algowalk.sorting.tracker.sort_algorithm_tracker import StepTracker
from algowalk.shared.pseudocode.pseudocode_builder import PseudocodeBuilder


class SortContext:
    def __init__(self, strategy, visualizer=None):
        self.strategy = strategy
        self.visualizer = visualizer
        self.pseudocode_builder = PseudocodeBuilder()

    def execute_sort(self, data: list):
        # Initialize Step Tracker
        tracker = StepTracker(visualizer=self.visualizer, pseudocode_builder=self.pseudocode_builder)

        # Perform Sort
        sorted_data = self.strategy.sort(data, tracker)

        # Build Pseudocode
        self.strategy.pseudocode(tracker)

        # Print Summary and Steps
        tracker.print_steps()
        tracker.print_summary()

        # Print Pseudocode and Visualize
        tracker.print_pseudocode()
        tracker.visualize()

        print(f"\n✅ Final Sorted Output: {sorted_data}")
        return sorted_data
