from enum import Enum


class ChainAggregationStrategy(str, Enum):
    sum = "sum"
    average = "average"
    first = "first"
    last = "last"
