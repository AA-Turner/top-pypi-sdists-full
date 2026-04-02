from seshat.data_class import SFrame, GroupSFrame
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.trimmer import SFrameTrimmer


class GroupTrimmer(SFrameTrimmer):
    """
    This trimmer will remove the default sf from the group sframe.

    Parameters
    ----------
    auto_unwrap_single_child : bool, default=False
        Whether to automatically unwrap the GroupSFrame to a single SFrame
        when only one child remains after removing the default sf.
    """

    ONLY_GROUP = True

    def __init__(self, auto_unwrap_single_child: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.auto_unwrap_single_child = auto_unwrap_single_child

    def calculate_complexity(self):
        return 1

    def __call__(self, sf_input: SFrame, *args: object, **kwargs: object) -> SFrame:
        sf_output: GroupSFrame = sf_input.from_raw(**self.get_from_raw_kwargs(sf_input))
        sf_output.children.pop(self.default_sf_key)

        if self.auto_unwrap_single_child and len(sf_output.children) == 1:
            return next(iter(sf_output.children.values()))

        return sf_output


class GroupTrimmerStory(BaseTransformerStory):
    transformer = GroupTrimmer
    use_cases = [
        "Sometimes during the pipeline, it's necessary to remove an SFrame from "
        "the group—either to reduce data size during transfer or for other "
        "processing reasons."
    ]
    logic_overview = (
        "Removes the entry associated with the `default` key in `group_keys` from the "
        "input grouped SFrame."
    )
    steps = []
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "GroupTrimmerDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
