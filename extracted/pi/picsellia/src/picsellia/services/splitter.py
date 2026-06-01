import logging
import random
from typing import Any

logger = logging.getLogger("picsellia")


class Splitter:
    @staticmethod
    def normalize_ratios(ratios: list[float]):
        return [ratio / sum(ratios) for ratio in ratios]

    @staticmethod
    def shuffle_items(items: list[Any], random_seed: Any | None):
        if random_seed is not None:
            random.seed(random_seed)
        random.shuffle(items)

    @staticmethod
    def split_with_ratios(
        items: list[Any], normalized_ratios: list[float]
    ) -> list[list[Any]]:
        n = len(items)

        # Find split points from ratios
        split_points = [0] + [
            int(sum(normalized_ratios[:i]) * n)
            for i in range(1, len(normalized_ratios) + 1)
        ]

        # Return a list of group of item split with ratios
        return [
            items[split_points[i] : split_points[i + 1]]
            for i in range(len(split_points) - 1)
        ]
