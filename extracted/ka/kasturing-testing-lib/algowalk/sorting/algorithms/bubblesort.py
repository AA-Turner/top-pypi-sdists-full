from algowalk.sorting.sort_strategy import SortStrategy
from algowalk.sorting.tracker.sort_algorithm_tracker import StepTracker


class BubbleSortStrategy(SortStrategy):
    def sort(self, data: list, tracker: StepTracker) -> list:
        tracker.start(data)
        n = len(data)
        arr = data.copy()

        for i in range(n):
            for j in range(0, n - i - 1):
                match = arr[j] > arr[j + 1]
                tracker.log_step(arr, j, j + 1, match)

                if match:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        tracker.end()
        return arr
