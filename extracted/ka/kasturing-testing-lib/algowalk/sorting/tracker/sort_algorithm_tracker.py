import sys
from algowalk.utils.tracker.algo_tracker import AlgoTracker


class StepTracker(AlgoTracker):

    def __init__(self, visualizer=None, pseudocode_builder=None):
        super().__init__(visualizer, pseudocode_builder)
        self.total_swaps = 0

    def log_step(self, array_snapshot, i, j, did_swap):
        self.steps.append({
            'array': array_snapshot.copy(),
            'i': i,
            'j': j,
            'swap': did_swap
        })
        if did_swap:
            self.total_swaps += 1
            self.total_memory += sys.getsizeof(array_snapshot)

    def print_steps(self):
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: Compare index {step['i']} & {step['j']} → "
                  f"{'SWAP' if step['swap'] else 'NO SWAP'} → {step['array']}")

    def print_summary(self):
        total_time = self.end_time - self.start_time if self.end_time else 0
        print("\n\033[1;34m>>> Benchmark Summary <<<\033[0m")
        print("\033[1;33mSort → Execution → Metrics\033[0m\n")
        print(f"\033[1;32m✓ Total swaps:\033[0m {self.total_swaps}")
        print(f"\033[1;32m✓ Estimated space used:\033[0m {self.total_memory} bytes")
        print(f"\033[1;32m✓ Execution time:\033[0m {total_time:.6f} seconds")
        print(f"\033[1;35m⌛ Static Time Complexity:\033[0m O(n²)")
        print(f"\033[1;35m🧠 Static Space Complexity:\033[0m O(1)\n")

    def visualize(self):
        if self.visualizer:
            self.visualizer.visualize(self.steps)

    def print_pseudocode(self):
        if self.pseudocode_builder:
            self.pseudocode_builder.print_pseudocode()
