from copy import deepcopy
from typing import List

from seshat.data_class import SFrame, GroupSFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.merger import SFrameMerger


class ListMerger(SFrameMerger):
    """
    Get the list of sframe either they are group or non-group and at last return
    only one group with all input sf.
    To avoid duplication in sf keys in result group sf, this format have been used:
    If sf is group, then key is prefix + index of sf in input sf_list + child key
    Otherwise key is prefix + index of sf in input sf_list

    Parameters:
    ----------
    sf_prefix: str
        The prefix that all sf keys in output starts with it.
    sf_list: List[SFrame]
        The List of sframes, each one can be group or non-group. The merging operation
        is performed on this list.

    Examples
    --------
    >>> sf1: SFrame, sf2: GroupSFrame
    >>> list(sf2.keys)
    ['default', 'address']

    >>> merger = ListMerger(sf_prefix="sf_")
    >>> result_sf = merger(sf_list=[sf1, sf2])
    >>> list(result_sf.keys)
    ['sf_0', 'sf_1_default', 'sf_1_address']
    """

    def __init__(self, sf_prefix="sf", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sf_prefix = sf_prefix

    def __call__(self, sf_list: List[SFrame], *args, **kwargs):
        result_sf = GroupSFrame()
        for i, sf in enumerate(sf_list):
            if isinstance(sf, GroupSFrame):
                for child_key, child_sf in sf.children.items():
                    result_sf[f"{self.sf_prefix}{i}_{child_key}"] = child_sf
            else:
                result_sf[f"{self.sf_prefix}{i}"] = sf
        return result_sf

    def calculate_complexity(self):
        return 15


class ListMergerScenario(TransformerScenario):
    """
    Custom TransformerScenario for list merger, because it has different
    __call__ method from default transformers.
    """

    def as_json(self):
        return {
            "description": self.description,
            "sf_list": [
                {k: s.to_dict() for k, s in sf_item.make_group().children.items()}
                for sf_item in self.sf_input
            ],
            "attributes": self.get_attributes(self.transformer),
            "result": {
                k: sf.to_dict()
                for k, sf in self.get_result().make_group().children.items()
            },
        }

    @classmethod
    def get_call_wrapper(cls, transformer, description, scenarios):
        def call_wrapper(call):
            def inner(self, *args, **kwargs):
                sf_list = kwargs.get("sf_list")
                if sf_list is None:
                    sf_list = args[0]

                copied_sf_list = deepcopy(sf_list)
                result = call(self, sf_list)
                if isinstance(self, transformer):
                    scenario = cls(
                        sf_input=copied_sf_list,
                        transformer=self,
                        description=description[0],
                    )
                    scenario._result = result
                    scenarios.append(scenario)
                return result

            return inner

        return call_wrapper


class ListMergerStory(BaseTransformerStory):
    transformer = ListMerger
    tags = ["merger", "multi-sf-operation"]
    use_cases = [
        (
            "Consolidate multiple individual SFrames or GroupSFrames into a single GroupSFrame "
            "for unified processing."
        ),
        (
            "Prepare a collection of diverse datasets for a subsequent transformer that expects "
            "a single GroupSFrame input."
        ),
    ]
    logic_overview = (
        "Takes a list of SFrames (which can be individual SFrames or GroupSFrames) and combines them into a single "
        "GroupSFrame, ensuring unique keys by prefixing them with an index and an optional user-defined prefix."
    )
    steps = [
        "Initialize an empty GroupSFrame to store the combined results.",
        "Iterate through each SFrame in the input `sf_list` along with its index.",
        (
            "If an SFrame is a GroupSFrame, iterate through its children and add each child to the result GroupSFrame, "
            "using a key composed of `sf_prefix`, the SFrame's index, and the child's original key "
            "(e.g., `sf_0_default`, `sf_0_address`)."
        ),
        "If an SFrame is a regular SFrame, add it directly to the result GroupSFrame, "
        "using a key composed of `sf_prefix` and the SFrame's index (e.g., `sf_1`).",
        "Return the consolidated GroupSFrame.",
    ]

    def get_scenarios(self):
        from test.transformer.merger.test_list import ListMergerDFTestCase

        return ListMergerScenario.from_testcase(
            ListMergerDFTestCase, transformer=self.transformer
        )
