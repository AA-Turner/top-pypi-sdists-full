from typing import Iterable, List, Dict, Type

from pyspark.sql import DataFrame, DataFrame as PySparkDataFrame

from seshat.data_class import GroupSFrame, DFrame, SPFrame, SFrame
from seshat.general import configs
from seshat.general.exceptions import InvalidArgumentsError
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.merger import SFrameMerger
from seshat.transformer.schema import Schema


class Merger(SFrameMerger):
    """
    This transformer merge two sframe based on columns names.

    Parameters:
    ----------
    axis: int, optional
        Show that merging operation should operate on which axis. Default is 1.
    left_on: str, optional
        Column name that is base of merging for default sf
    right_on: str, optional
        Column name that is base of merging for right sf
    on: str, optional
        Column name that is base of merging for both default & right sf.
        This is same when left_on and right_on are same.
    right_schema: Schema, optional
        This schema will be ran on right sf before merging happened.
        Useful when keep only some columns of right sf in default sf is required.
    inplace: bool, optional
        Show that weather default sf should changed or merged result save on new sf.
        Default is False.
    merge_how: str, optional
        Show how to merge two sframes. For example: left, right, inner.
        Default is left.
    drop_unmerged: bool, optional
        If true, two sframe that used for merging will drop from result.
    group_key
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "other": configs.OTHER_SF_KEY,
        "merged": configs.MERGED_SF_KEY,
    }
    on: str | Iterable[str]
    axis: int

    def __init__(
        self,
        axis: int = 1,
        left_on: str | List[str] = None,
        right_on: str | List[str] = None,
        on: str | List[str] = None,
        right_schema: Schema = None,
        inplace: bool = False,
        group_keys=None,
        merge_how: str = "left",
        drop_unmerged: bool = False,
        *args,
        **kwargs,
    ):
        if isinstance(left_on, list) != isinstance(right_on, list):
            raise InvalidArgumentsError(
                "left_on and right_on must both be either lists or strings and cannot be of different types."
            )
        if isinstance(left_on, list) and len(left_on) != len(right_on):
            raise InvalidArgumentsError("len(right_on) must equal len(left_on)")

        super().__init__(group_keys, *args, **kwargs)
        self.axis = axis
        self.left_on = left_on
        self.right_on = right_on
        self.on = on
        self.right_schema = right_schema
        self.inplace = inplace
        self.merge_how = merge_how
        self.drop_unmerged = drop_unmerged

    def calculate_complexity(self):
        return 10

    def set_raw(self, sf: GroupSFrame, result: Dict[str, object]):
        if self.drop_unmerged:
            for _, v in self.group_keys.items():
                sf.children.pop(v, None)
        return super().set_raw(sf, result)

    def merge_df(self, default: DataFrame, other: DataFrame, *args, **kwargs):
        merging_kwargs = self.get_merging_kwargs()
        merged = self.merge(default, other, DFrame, merging_kwargs)
        if self.axis == 1 and "right_on" in merging_kwargs:
            merged = merged.drop(self.get_drop_cols(), axis=1)
        merged = merged.drop_duplicates().reset_index(drop=True)
        return self.choose_return_result(default, other, merged)

    def merge_spf(
        self, default: PySparkDataFrame, other: PySparkDataFrame, *args, **kwargs
    ):
        merging_kwargs = self.get_merging_kwargs()
        merged = self.merge(default, other, SPFrame, merging_kwargs)
        if self.axis == 1 and "right_on" in merging_kwargs:
            merged: PySparkDataFrame = merged.drop(*self.get_drop_cols())
        merged = merged.dropDuplicates()
        return self.choose_return_result(default, other, merged)

    def merge(
        self,
        default: object,
        other: object,
        sf_class: Type[SFrame],
        merging_kwargs: dict,
    ) -> object:
        default_sf = sf_class.from_raw(default)
        other_sf = sf_class.from_raw(other)
        if self.right_schema:
            other_sf = self.right_schema(other_sf)
        result = default_sf.extend(other_sf.to_raw(), axis=self.axis, **merging_kwargs)
        return result

    def get_merging_kwargs(self):
        if self.on:
            return {"on": self.on, "how": self.merge_how}
        return {
            "left_on": self.left_on,
            "right_on": self.right_on,
            "how": self.merge_how,
        }

    def choose_return_result(self, default, other, merged):
        if self.drop_unmerged:
            result_kwargs = {}
        else:
            result_kwargs = {"default": default, "other": other}

        if self.inplace:
            result_kwargs["default"] = merged
        else:
            result_kwargs["merged"] = merged
        return result_kwargs

    def get_drop_cols(self):
        left_on_set = (
            {self.left_on} if isinstance(self.left_on, str) else set(self.left_on)
        )
        right_on_set = (
            {self.right_on} if isinstance(self.right_on, str) else set(self.right_on)
        )
        return right_on_set - left_on_set


class MergerStory(BaseTransformerStory):
    transformer = Merger
    tags = ["merger", "multi-sf-operation"]
    use_cases = [
        "Combine transaction data with address information by joining on common address columns.",
        "Join two datasets horizontally (adding columns) or vertically (stacking rows).",
    ]
    logic_overview = (
        "Combines two SFrames (a 'default' SFrame and an 'other' SFrame) based on specified "
        "columns and a merge strategy, producing a single SFrame containing the combined data. "
        "It supports various join types (left, right, inner) and can operate horizontally or vertically."
    )
    steps = [
        "Identify the default SFrame and the 'other' SFrame from the input GroupSFrame.",
        "If a `right_schema` is provided, apply it to the 'other' SFrame to preprocess its columns before merging.",
        "Determine the merge keys (`left_on`, `right_on`, or `on`) and the merge strategy (`how`).",
        (
            "Perform the merge operation (horizontal for `axis=1` or vertical for `axis=0`) "
            "based on the specified parameters."
        ),
        "Handle potential duplicate rows in the merged SFrame by dropping them and resetting the index.",
        (
            "Based on the `inplace` and `drop_unmerged` parameters, return the merged SFrame. "
            "If `inplace` is True, the default SFrame is updated; otherwise, a new 'merged' SFrame is created. "
            "If `drop_unmerged` is True, the original default and other SFrames are removed from the result."
        ),
    ]

    def get_scenarios(self):
        from test.transformer.merger.test_common import MergerDFTestCase

        return TransformerScenario.from_testcase(
            MergerDFTestCase, transformer=self.transformer
        )
