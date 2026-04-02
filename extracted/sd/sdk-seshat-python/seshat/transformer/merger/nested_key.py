from typing import Optional, List, Union

from seshat.data_class import SFrame, GroupSFrame, DFrame, SPFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.merger import SFrameMerger


class NestedKeyMerger(SFrameMerger):
    """
    A merger that searches for a specific key in a nested GroupSFrame structure
    and merges the frames found with this key using the built-in extend functionality.

    This merger supports both pandas (DFrame) and PySpark (SPFrame) DataFrames and is designed
    to work with the output of a Branch transformer where:
    - The input is a GroupSFrame
    - The children of the input are also GroupSFrames
    - The children of the children are dictionaries mapping strings to frames

    Parameters
    ----------
    group_key : str
        The key to search for in the nested structure
    result_key : str, optional
        The key to use for the result in the output GroupSFrame.
        If not provided, the group_key will be used.

    Examples
    --------
    >>> branch = Branch(pipe_map=pipe_map)
    >>> result = branch(sf_input)  # result is a GroupSFrame with GroupSFrame children
    >>> merger = NestedKeyMerger(group_key="user_data")
    >>> merged_result = merger(result)  # merged_result is a GroupSFrame with a single frame
    """

    def __init__(
        self, group_key: str, result_key: Optional[str] = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.group_key = group_key
        self.result_key = result_key or group_key

    def _find_nested_frames(
        self, sf_input: GroupSFrame
    ) -> List[Union[DFrame, SPFrame]]:
        frames = []

        for child_key, child_sf in sf_input.children.items():
            # Look for the group_key in the children of the child
            frame = child_sf.get(self.group_key)
            if frame is not None:
                frames.append(frame)

        return frames

    def __call__(self, sf_input: SFrame, *args, **kwargs) -> SFrame:
        if not isinstance(sf_input, GroupSFrame):
            return sf_input

        # Find all frames with the group_key
        frames = self._find_nested_frames(sf_input)

        if not frames:
            return sf_input

        # Merge frames - start with a deep copy of the first frame
        result_frame = frames[0].__deepcopy__(None)

        # Extend with the rest using the built-in extend method
        for frame in frames[1:]:
            result_frame.extend(frame.data)

        if result_frame is None:
            return sf_input

        # Create a new GroupSFrame with the result
        result = GroupSFrame()
        result[self.result_key] = result_frame

        return result

    def calculate_complexity(self):
        return 15


class NestedKeyMergerScenario(TransformerScenario):
    def as_json(self):
        sf_input_dict = {}
        if self.sf_input is not None:
            group = self.sf_input.make_group()
            if (
                group is not None
                and hasattr(group, "children")
                and group.children is not None
            ):
                for k, sf in group.children.items():
                    if sf is not None and isinstance(sf, GroupSFrame):
                        sf_input_dict[k] = {
                            nested_k: nested_sf.to_dict()
                            for nested_k, nested_sf in sf.children.items()
                            if nested_sf is not None
                        }
        return {
            "description": self.description,
            "sf_input": sf_input_dict,
            "attributes": self.get_attributes(self.transformer),
            "result": self.format_result(),
        }


class NestedKeyMergerStory(BaseTransformerStory):
    transformer = NestedKeyMerger
    tags = ["merger", "multi-sf-operation", "nested-structure"]
    use_cases = [
        "Merge results from Branch transformer that creates nested GroupSFrame structures.",
        "Combine data from multiple groups processed separately by Branch into a single SFrame.",
        "Flatten nested GroupSFrame outputs after processing different data segments.",
    ]
    logic_overview = (
        "Searches for a specific key in nested GroupSFrame structures and merges all frames "
        "found with that key. Designed to work with Branch transformer outputs where each group's "
        "result is itself a GroupSFrame containing frames under specific keys."
    )
    steps = [
        "Receive a GroupSFrame where each child is also a GroupSFrame (nested structure).",
        "For each child GroupSFrame, search for the specified `group_key`.",
        "Collect all frames found with the `group_key` from all nested children.",
        "Merge the collected frames using the extend method (vertically concatenate).",
        "Return a GroupSFrame with the merged result under `result_key` (defaults to `group_key`).",
    ]

    def get_scenarios(self):
        from test.transformer.merger import NestedKeyMergerDFTestCase

        return NestedKeyMergerScenario.from_testcase(
            NestedKeyMergerDFTestCase, transformer=self.transformer
        )

    interactions = [
        (
            "Branch",
            "NestedKeyMerger is designed to work with Branch outputs. "
            "After Branch processes multiple groups separately, each group's output is a GroupSFrame. "
            "NestedKeyMerger extracts frames with a specific key from all groups and merges them together.",
        )
    ]
