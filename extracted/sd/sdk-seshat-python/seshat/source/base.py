from typing import Type, List

from seshat.data_class import SF_MAP, GroupSFrame
from seshat.data_class.base import SFrame
from seshat.general import configs
from seshat.general.exceptions import InvalidModeError
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer import Transformer
from seshat.transformer.merger import Merger
from seshat.transformer.schema import Schema


class Source(Transformer):
    """
    An interface class for data retrieval that allows querying and optional schema transformation.
    This class reads data based on a provided query, modifies the data's schema
    if a schema is provided, and returns the result in a specified SFrame format.

    Parameters
    ----------
    query : str, optional
        Query string or identifier for data retrieval (implementation-specific).
    schema : Schema, optional
        Schema for transforming fetched data before returning.
    mode : str, optional
        SFrame mode determining the data class type (default: configs.DEFAULT_MODE).
        Must be a valid key in SF_MAP (e.g., "df" for DFrame, "spf" for SPFrame).
    group_keys : dict, optional
        Group keys for SFrame grouping. Default: {"default": DEFAULT_SF_KEY, "result": "result"}.
    merger : Merger, optional
        Merger instance for combining fetched data with input SFrame.
        If provided, merger will be set to work inplace.
    """

    query: str
    data_class: Type[SFrame]
    schema: Schema
    mode: str

    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY, "result": "result"}

    def __init__(
        self,
        query=None,
        schema=None,
        mode=configs.DEFAULT_MODE,
        group_keys=None,
        merger: Merger = None,
        *args,
        **kwargs
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.query = query
        self.schema = schema
        self.mode = mode
        try:
            self.data_class = SF_MAP[mode]
        except KeyError:
            raise InvalidModeError()

        self.merger = merger
        if self.merger:
            # ensure merger works inplace
            self.merger.inplace = True

    def __call__(self, sf_input: SFrame = None, *args, **kwargs) -> SFrame:
        fetched_sf = self.fetch(sf_input, *args, **kwargs)
        if self.schema and not fetched_sf.empty:
            fetched_sf = self.schema(fetched_sf)
        if sf_input is None:
            return fetched_sf

        if isinstance(sf_input, GroupSFrame):
            group_sf = sf_input
        else:
            group_sf = sf_input.make_group(
                self.merger_default_key if self.merger else self.default_sf_key
            )

        if self.merger:
            group_sf[self.merger_other_key] = fetched_sf
            group_sf = self.merger(group_sf)
            group_sf.children.pop(self.merger_other_key, None)
            group_sf[self.default_sf_key] = group_sf.children.pop(
                self.merger_default_key
            )
        else:
            group_sf[self.result_key] = fetched_sf

        return group_sf

    def calculate_complexity(self):
        return NotImplementedError()

    def fetch(self, *args, **kwargs) -> SFrame:
        pass

    def get_query(self):
        return self.query

    def convert_data_type(self, data) -> SFrame:
        return self.data_class.from_raw(data)

    @property
    def merger_default_key(self):
        return self.merger.group_keys["default"]

    @property
    def merger_other_key(self):
        return self.merger.group_keys["other"]

    @property
    def result_key(self):
        return self.group_keys["result"]


class SourceStory(BaseTransformerStory):
    transformer = Source

    use_cases = [
        "Fetch data from external sources (databases, APIs, files) and integrate into pipeline",
        "Apply schema transformation to fetched data before processing",
        "Merge fetched data with existing SFrame using custom merger logic",
        "Convert raw data into appropriate SFrame format based on mode configuration",
    ]

    logic_overview = (
        "Sources fetch data from external systems, optionally transform it with a schema, "
        "and either return it as a new SFrame or merge it with existing input data."
    )

    steps = [
        "Fetch data from the source using the fetch() method",
        "Apply schema transformation if schema is provided and data is not empty",
        "If no input SFrame provided, return the fetched data directly",
        "If input SFrame exists, convert it to GroupSFrame if needed",
        "If merger is configured, merge fetched data with input using the merger",
        "Otherwise, add fetched data as a new SFrame with the result key",
        "Return the resulting GroupSFrame",
    ]

    tags = ["source", "data-fetching"]

    def get_scenarios(self) -> List[TransformerScenario]:
        from test.transformer.source import SourceTestCase

        return TransformerScenario.from_testcase(
            SourceTestCase, transformer=self.transformer
        )
