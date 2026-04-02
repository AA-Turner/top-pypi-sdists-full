from copy import deepcopy
from typing import List, Dict

from seshat.data_class import SFrame, GroupSFrame
from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.transformer.splitter import Splitter, SplitterScenario


class MultiSplitter(Splitter):
    """
    Applies multiple splitters sequentially to an SFrame.

    This allows for complex splitting strategies by combining different splitter types.

    Parameters
    ----------
    splitters : List[Splitter]
        A list of Splitter instances to apply.
    """

    splitters: List[Splitter]

    def __init__(self, splitters: List[Splitter], group_keys=None, *args, **kwargs):
        super().__init__(group_keys=group_keys, *args, **kwargs)
        self.splitters = splitters

    def __call__(self, input_sf: SFrame, *args, **kwargs) -> Dict[str, SFrame]:
        empty_sf = (
            GroupSFrame()
            if isinstance(input_sf, GroupSFrame)
            else input_sf.from_raw(None)
        )

        partition = {
            self.train_key: empty_sf,
            self.test_key: deepcopy(empty_sf),
        }
        for splitter in self.splitters:
            splitter.clear_input = False
            result = splitter(input_sf)
            partition[self.test_key][splitter.default_sf_key] = result[
                splitter.test_key
            ]
            partition[self.train_key][splitter.default_sf_key] = result[
                splitter.train_key
            ]

        return partition


class MultiSplitterStory(BaseTransformerStory):
    transformer = MultiSplitter
    use_cases = [
        "To apply multiple splitting strategies simultaneously to different parts of a "
        "grouped SFrame.",
        "To build complex train/test splits that involve different criteria for "
        "different datasets within a single SFrame structure.",
    ]
    logic_overview = (
        "The MultiSplitter takes a list of individual Splitter instances and applies "
        "each of them to the input SFrame. It iterates through the provided splitters "
        "and combines their results into a single output dictionary containing 'train' "
        "and 'test' SFrames. Each inner splitter's result is assigned to the output "
        "SFrame using its `default_sf_key`."
    )
    steps = [
        "Initialize the MultiSplitter with a list of configured Splitter instances.",
        "Create an empty grouped SFrame structure for the 'train' and 'test' outputs.",
        "Iterate through each splitter in the provided list:",
        "Apply the current splitter to the input SFrame.",
        "Place the 'train' and 'test' results from the current splitter into the "
        "corresponding sections of the main 'train' and 'test' output SFrames, using "
        "the inner splitter's `default_sf_key`.",
        "Return the final dictionary containing the combined 'train' and 'test' SFrames.",
    ]
    tags = ["splitter", "multi", "group-sf-operation"]

    outputs = [
        "A dictionary containing 'test' and 'train' keys, where each key maps to a "
        "GroupSFrame containing the respective data."
    ]
    find_outputs = False

    def get_scenarios(self):
        from test.transformer.splitter import MultiSplitterDFTestCase

        return SplitterScenario.from_testcase(
            MultiSplitterDFTestCase, transformer=self.transformer
        )
