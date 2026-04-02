from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame

from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.deriver.base import SFrameDeriver


class DuplicatedSFrameDeriver(SFrameDeriver):
    """
    Duplicate an SFrame and add it to the group sframe with a new key.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "duplicated": configs.DUPLICATED_SF_KEY,
    }

    def derive_df(self, default: DataFrame, *args, **kwargs):
        return {"default": default, "duplicated": default.copy()}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        return {"default": default, "duplicated": default.select("*")}


class DuplicatedSFrameDeriverStory(BaseTransformerStory):
    transformer = DuplicatedSFrameDeriver
    use_cases = [
        "To create a duplicate copy of an existing SFrame within a grouped SFrame.",
        (
            "When a transformation pipeline requires an identical copy of the input SFrame "
            "for parallel processing or alternative transformations."
        ),
    ]
    logic_overview = (
        "Creates a shallow copy of the default SFrame and adds it to the grouped "
        "SFrame under a new key, typically 'duplicated'."
    )
    steps = [
        "The default SFrame is copied.",
        "The copied SFrame is added to the output dictionary with the key 'duplicated'.",
        "The original default SFrame is also returned in the output dictionary under its original key.",
    ]
    tags = ["deriver", "single-sf-operation", "group-sf-manipulation"]

    def get_scenarios(self):
        from test.transformer.deriver.test_duplicated_sframe import (
            DuplicatedSFrameDFTestCase,
        )

        return TransformerScenario.from_testcase(
            DuplicatedSFrameDFTestCase, transformer=self.transformer
        )
