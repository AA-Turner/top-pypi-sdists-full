from typing import Dict

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql.functions import col, min, max

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.transformer.splitter import Splitter
from seshat.transformer.splitter import SplitterScenario
from seshat.utils.validation import NumericColumnValidator


class BlockSplitter(Splitter):
    """
    Splits a sframe into train and test sets based on a block number column.

    The split is determined by a specified percentage of the range of block numbers.
    Data with block numbers below the calculated cutoff go into the training set,
    and data with block numbers at or above the cutoff go into the test set.

    Parameters
    ----------
    percent : float, optional
        The percentage of the block number range to allocate to the training set, by default 0.8.
    block_num_col : str, optional
        The name of the column containing block numbers, by default `configs.BLOCK_NUM_COL`.
    """

    def __init__(
        self,
        percent=0.8,
        block_num_col=configs.BLOCK_NUM_COL,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys=group_keys, *args, **kwargs)
        self.block_num_col = block_num_col
        self.percent = percent

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.block_num_col)

    def split_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, object]:
        default = NumericColumnValidator().validate(default, self.block_num_col)
        cutoff_block_number = int(
            default[self.block_num_col].min()
            + (
                (default[self.block_num_col].max() - default[self.block_num_col].min())
                * self.percent
            )
        )
        df_train = default[default[self.block_num_col] < cutoff_block_number]
        df_test = default[default[self.block_num_col] >= cutoff_block_number]

        return {"train": df_train, "test": df_test}

    def split_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, object]:

        default = NumericColumnValidator().validate(default, self.block_num_col)

        min_block, max_block = default.agg(
            min(col(self.block_num_col)), max(col(self.block_num_col))
        ).first()
        cutoff_block_number = int(min_block + ((max_block - min_block) * self.percent))
        df_train = default.filter(col(self.block_num_col) < cutoff_block_number)
        df_test = default.filter(col(self.block_num_col) >= cutoff_block_number)

        return {"train": df_train, "test": df_test}


class BlockSplitterStory(BaseTransformerStory):
    transformer = BlockSplitter
    use_cases = [
        "To split time series or panel data while keeping observations within the same "
        "block (e.g., time period, group) together.",
        "To create train/test splits that respect the natural grouping or ordering in "
        "the data.",
    ]
    logic_overview = (
        "The BlockSplitter splits an SFrame based on the values in a specified block "
        "number column. It calculates a cutoff value based on the 'percent' parameter "
        "and the range of block numbers. Data rows with block numbers below the cutoff "
        "go to the training set, and those at or above the cutoff go to the test set."
    )
    steps = [
        "Initialize the transformer with the 'percent' for the training set size and "
        "the 'block_num_col'.",
        "Validate that the 'block_num_col' exists and is numeric.",
        "Find the minimum and maximum values in the 'block_num_col'.",
        "Calculate the cutoff block number based on the percentage.",
        "Filter the SFrame to create the train set (block numbers < cutoff) and the "
        "test set (block numbers >= cutoff).",
        "Return a dictionary containing the 'train' and 'test' SFrames.",
    ]
    tags = ["splitter", "ethereum", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.splitter.test_block_splitter import (
            BlockSplitterDFTestCase,
        )

        return SplitterScenario.from_testcase(
            BlockSplitterDFTestCase, transformer=self.transformer
        )

    outputs = [
        "A dictionary containing 'test' and 'train' keys, where each key maps to an "
        "SFrame containing the respective data."
    ]
    find_outputs = False
