from typing import List

import seshat.transformer
from seshat.data_class import GroupSFrame, SFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.merger import SFrameMerger
from seshat.transformer.merger.common import Merger


class MultiMerger(SFrameMerger):
    """
    This merger applies multiple `Merger` instances sequentially to an input `GroupSFrame`.
    It iterates through a list of pre-configured `Merger` objects, applying each one
    to the current state of the `GroupSFrame`.

    Parameters
    ----------
    mergers : List[seshat.transformer.merger.Merger]
        A list of `Merger` instances to be applied in sequence.
    """

    mergers = List[Merger]
    ONLY_GROUP = True

    def __init__(self, mergers, group_keys=None, *args, **kwargs):
        super().__init__(group_keys, *args, **kwargs)
        self.mergers = mergers

    def __call__(
        self, sf_input: GroupSFrame, *args: object, **kwargs: object
    ) -> SFrame:
        for merger in self.mergers:
            sf_input = merger(sf_input)
        return sf_input

    def calculate_complexity(self):
        return sum([m.calculate_complexity() for m in self.mergers])


class MultiMergerStory(BaseTransformerStory):
    transformer = MultiMerger
    tags = ["merger", "multi-sf-operation"]
    use_cases = [
        (
            "Apply a sequence of complex merge operations to a dataset, where each merge "
            "depends on the output of the previous one."
        ),
        "Build a multi-stage data integration workflow that combines data from various sources iteratively.",
    ]
    logic_overview = (
        "Applies a list of `Merger` instances sequentially to an input GroupSFrame. Each merger processes the SFrame "
        "and passes its output to the next merger in the sequence, allowing for chained merge operations."
    )
    steps = [
        "Receive an initial GroupSFrame as input.",
        "Iterate through the list of `mergers` provided during initialization.",
        "For each `merger` in the list, apply it to the current state of the input SFrame. "
        "The output of the current merger becomes the input for the next merger.",
        "After all mergers have been applied, return the final resulting SFrame.",
    ]

    def get_scenarios(self):
        from test.transformer.merger.test_multi import MultiMergerDFTestcase

        return TransformerScenario.from_testcase(
            MultiMergerDFTestcase, transformer=self.transformer
        )
