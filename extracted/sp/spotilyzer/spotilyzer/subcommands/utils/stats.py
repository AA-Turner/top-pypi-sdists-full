"""
spotilyzer stats utilities
"""

# system imports
import math


class StatCollector:
    """
    Class to collect data for statistical analysis.
    """

    def __init__(self):
        self.count = 0
        self.total = 0.0
        self.square_total = 0.0

    def add(self, value):
        """
        Add data point to population.
        :param value: data value
        :return: None
        """
        self.count += 1
        self.total += value
        self.square_total += value * value

    def weighted_add(self, value, weight):
        """
        Add data point with weight to population
        :param value: data value
        :param weight: weight to apply to data value
        :return: None
        """
        self.count += weight
        self.total += weight * value
        self.square_total += weight * value * value

    def eval(self, sampled=True):
        """
        Compute average and standard deviation. Values are cached so any data
        added with subsequent add() calls are not used.
        :param sampled: Flag to indicate if data is sampled. A True value
        computes standard deviation with an n-1 denominator. A False value
        computes standard deviation with an n denominator.
        :return: tuple with average, standard deviation
        """
        if not hasattr(self, 'stats'):
            if self.count == 0:
                raise ZeroDivisionError("no data")
            avg = self.total / self.count
            if sampled:
                if self.count == 1:
                    raise ZeroDivisionError("insufficient data")
                variance = (self.square_total - self.total * avg) \
                           / (self.count - 1)
            else:
                variance = self.square_total / self.count - avg * avg
            if variance < 0.0:
                variance = 0.0
            self.stats = (avg, math.sqrt(variance))
        return self.stats


def quality(stat_collector, cov_level):
    """
    Determine if variance is within an acceptable level.
    :param stat_collector: StatCollector object
    :param cov_level: acceptable limit for coefficient of variation
    :return: True if coefficient of variation is within acceptable limit
    """
    avg, stddev = stat_collector.eval(sampled=False)
    return stddev / avg < cov_level
