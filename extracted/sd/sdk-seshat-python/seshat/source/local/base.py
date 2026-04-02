from typing import List

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.source import Source
from seshat.transformer.merger import Merger


class LocalSource(Source):
    """
    LocalSource is a data source that can read from local CSV files or in-memory data structures.
    Supports both file paths and in-memory DataFrames/dicts/lists as data sources.

    Parameters
    ----------
    data_source : str or DataFrame or dict or list
        Either a file path string to a CSV file, or an in-memory data structure
        (pandas DataFrame, dict, list) to be converted to SFrame.
    schema : Schema, optional
        Schema for data transformation after loading.
    mode : str, optional
        SFrame mode for data conversion (default: configs.DEFAULT_MODE).
    group_keys : dict, optional
        Group keys for SFrame grouping.
    merge_result : bool, optional
        Whether to merge results with input SFrame (default: False).
    merger : Merger, optional
        Merger instance for combining results.
    """

    def __init__(
        self,
        data_source,
        schema=None,
        mode=configs.DEFAULT_MODE,
        group_keys=None,
        merge_result=False,
        merger: Merger = Merger,
        *args,
        **kwargs
    ):
        super().__init__(
            schema=schema,
            mode=mode,
            group_keys=group_keys,
            merge_result=merge_result,
            merger=merger,
            *args,
            **kwargs
        )
        self.data_source = data_source

    def convert_data_type(self, data) -> SFrame:
        return self.data_class.from_raw(data)

    def fetch(self, *args, **kwargs) -> SFrame:
        d = (
            self.data_class.read_csv(path=self.data_source)
            if isinstance(self.data_source, str)
            else self.data_source
        )

        return self.convert_data_type(d)

    def calculate_complexity(self):
        return 10


class LocalSourceStory(BaseTransformerStory):
    transformer = LocalSource

    use_cases = [
        "Read data from local CSV files into SFrame pipelines",
        "Load in-memory data structures (DataFrames, lists, dicts) into pipelines",
        "Quickly prototype and test pipelines with local data",
        "Process local files with schema transformation and data merging",
    ]

    logic_overview = (
        "LocalSource reads data from local files (CSV) or in-memory sources (DataFrames, raw data). "
        "It inherits from Source, using the standard Source.__call__() method for integration with SFrame pipelines. "
        "The data_source can be either a file path string or an in-memory data structure."
    )

    steps = [
        "Check if data_source is a string (file path) or in-memory data",
        "If string, use data_class.read_csv() to load the file",
        "If in-memory, use the data directly",
        "Convert loaded data to appropriate SFrame format using convert_data_type()",
        "Follow standard Source logic: apply schema if provided, merge or add to GroupSFrame as needed",
    ]

    tags = ["source", "local", "file", "csv", "data-loading"]

    def get_scenarios(self) -> List[TransformerScenario]:
        from test.transformer.source.test_local_source import LocalSourceTestCase

        return TransformerScenario.from_testcase(
            LocalSourceTestCase, transformer=self.transformer
        )
