from typing import Dict

from pandas import DataFrame
from pyspark.sql.dataframe import DataFrame as PySparkDataFrame
from sklearn.model_selection import train_test_split

from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.transformer.splitter import Splitter
from seshat.transformer.splitter import SplitterScenario


class RandomSplitter(Splitter):
    """
    Splits a sframe into train and test sets randomly.

    The split is performed using random sampling, with a specified percentage
    allocated to the training set.

    Parameters
    ----------
    percent : float, optional
        The percentage of the data to allocate to the training set, by default 0.8 (or 80 if > 1).
    seed : int, optional
        The random seed for reproducibility, by default 42.
    """

    def __init__(self, percent=0.8, seed=42, group_keys=None, *args, **kwargs):
        super().__init__(group_keys=group_keys, *args, **kwargs)
        self.percent = percent
        if self.percent > 1:
            self.percent /= 100
        self.seed = seed

    def split_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, object]:
        train, test = train_test_split(
            default, train_size=self.percent, random_state=self.seed
        )
        return {"train": train, "test": test}

    def split_spf(self, default: PySparkDataFrame, *args, **kwargs):
        train, test = default.randomSplit(
            [self.percent, 1 - self.percent], seed=self.seed
        )
        return {"train": train, "test": test}


class RandomSplitterStory(BaseTransformerStory):
    transformer = RandomSplitter
    use_cases = [
        "To randomly partition a dataset into training and testing subsets for model "
        "development and evaluation.",
    ]
    logic_overview = (
        "The RandomSplitter divides an SFrame into two parts (train and test) using "
        "random sampling. The split size is determined by the 'percent' parameter. "
        "It handles both pandas DataFrames (using scikit-learn's `train_test_split`) "
        "and PySpark DataFrames (using `randomSplit`)."
    )
    steps = [
        "Initialize the transformer with the desired 'percent' for the training set "
        "size and an optional 'seed' for reproducibility.",
        "If the input is a pandas DataFrame, use `sklearn.model_selection.train_test_split` "
        "with the specified percentage and seed.",
        "If the input is a PySpark DataFrame, use the `randomSplit` method with the "
        "specified percentages ([percent, 1 - percent]) and seed.",
        "Return a dictionary containing the 'train' and 'test' SFrames.",
    ]
    tags = ["splitter", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.splitter.test_random_splitter import (
            RandomSplitterDFTestCase,
        )

        return SplitterScenario.from_testcase(
            RandomSplitterDFTestCase, transformer=self.transformer
        )

    outputs = [
        "A dictionary containing 'test' and 'train' keys, where each key maps to an "
        "SFrame containing the respective data."
    ]
    find_outputs = False
