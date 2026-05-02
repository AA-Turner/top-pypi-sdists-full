from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections

from .logger import Logger
from .persona import Persona
from .themerating import ThemeRating


class DataGenerator:
    """Implementation of a generator based on a persona rating."""

    colors = ["g", "b", "r", "k", "orange"]

    def __init__(self, startdate: datetime, rating: ThemeRating, samples: int):
        """Initialisation of the class.

        Parameters
        ----------
        startdate : datetime
            The date of the first sample.
        rating: ThemeRating
            How a person would react to a theme.
        samples: int
            Length of the data to generate.
        """

        self.startdate = startdate
        self.rating = rating
        self.samples = samples
        self.data = np.ones([2, samples]) * (-1)

    @property
    def mean(self) -> float:
        """Return the mean of the generated data."""

        return np.nanmean(self.data[1, :])

    @property
    def rate(self) -> float:
        """Return the fill rate of the generated data."""

        return np.sum(~np.isnan(self.data[1, :])) / self.data.shape[1]

    def fill(self):
        """Fill the data in the correct order."""

        self._respect_pattern()
        self._respect_mean()
        self._respect_factor_rate()
        self._respect_fill_rate()

    def show(self, person: Persona):
        """Show the generated data."""

        if not Logger.verbose:
            return

        Logger.write(
            f"[{'GENERATOR':10s}]     Generated average: {self.mean:.2f} (req {self.rating.average:.2f})"
        )

        Logger.write(
            f"[{'GENERATOR':10s}]     Generated fill-rate: {self.rate:.2f} (req {self.rating.rate:.2f})"
        )

        n_factors = len(self.rating.factors)

        _, ax = plt.subplots(figsize=(12, 5))

        for factor in range(n_factors):

            factor_indexes = np.where(self.data[0, :] == factor)[0]
            factor_data = self.data[1, factor_indexes]

            lines = [
                [(idx, 0), (idx, value)]
                for idx, value in zip(factor_indexes, factor_data)
            ]

            linecoll = collections.LineCollection(
                lines, linewidths=1, color=DataGenerator._get_color(factor)
            )
            ax.add_collection(linecoll)

            plt.scatter(
                factor_indexes,
                factor_data,
                s=6,
                color=DataGenerator._get_color(factor),
                label=f"factor {factor} ({self.rating.factors[factor].rate:.0%})",
            )

        plt.axhline(y=self.mean, color="r", linestyle="--", label="data mean")
        plt.axhline(
            y=self.rating.average, color="g", linestyle="--", label="required mean"
        )
        plt.yticks(self.rating.possible_values + [0])
        plt.xticks(np.arange(0, np.ceil(self.samples / 10) * 10 + 1, 10))
        plt.grid()

        plt.title(f"Data generated for {person.name} (theme {self.rating.id})")
        plt.legend()

        plt.show()

    @classmethod
    def _get_color(cls, index: int):
        """Get a color in a cyclic maner."""

        return DataGenerator.colors[index % len(DataGenerator.colors)]

    def _respect_pattern(self):
        """Fill the data according to the patterns specified by the rating."""

        for factor_idx, factor in enumerate(self.rating.factors):
            for pattern in factor.patterns:
                indexes = np.arange(pattern.start, self.samples, pattern.step)
                self.data[0, indexes] = factor_idx
                self.data[1, indexes] = pattern.value

    def _respect_mean(self):
        """Fill the remaining data so that the average value equals the one in the rating."""

        patterns = [p for factor in self.rating.factors for p in factor.patterns]
        mean = (self.rating.average - np.sum([p.value / p.step for p in patterns])) / (
            1 - np.sum([1 / p.step for p in patterns])
        )

        indexes = np.where(self.data[0, :] == -1)[0]

        self.data[1, indexes] = self._get_randoms(mean, indexes.shape[0])

    def _respect_factor_rate(self):
        """Fill the data according to the patterns specified by the rating."""

        splits_counts = [
            int(factor.rate * self.data.shape[1]) for factor in self.rating.factors
        ]

        for idx, split_count in enumerate(splits_counts):
            remaining_indexes = np.where(self.data[0, :] == -1)[0]

            n_to_pick = split_count - np.count_nonzero(self.data[0, :] == idx)
            indexes = np.random.choice(remaining_indexes, n_to_pick, replace=False)

            self.data[0, indexes] = idx

    def _respect_fill_rate(self):
        """Fill the data so that the filling rate is respected."""

        n_to_remove = round(self.samples * (1 - self.rating.rate))
        indexes = np.random.choice(np.arange(self.samples), n_to_remove, replace=False)

        self.data[0, indexes] = None
        self.data[1, indexes] = None

    def _get_randoms(self, mean: float, size: int = 0) -> np.ndarray:
        """Get random values with a given mean."""

        computed_mean: float = None

        while not computed_mean or not (mean + 0.01 >= computed_mean >= mean - 0.01):
            rand = np.random.choice(self.rating.possible_values, size)
            computed_mean = rand.mean()

        return rand

    def __str__(self):
        return
