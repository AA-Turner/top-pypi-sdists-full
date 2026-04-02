from typing import Dict

from seshat.data_class.base import GroupSFrame, SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    TransformerScenario,
)
from seshat.transformer import Transformer


class Splitter(Transformer):
    """
    A data transformer class that splits a dataset into training and testing subsets
    based on a specified percentage. This class functions as a transformer by taking
    a dataset as input, processing it to a group sframe contains test and train data.
    """

    train_key: str
    test_key: str

    percent: float
    HANDLER_NAME = "split"
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "train": configs.TRAIN_SF_KEY,
        "test": configs.TEST_SF_KEY,
    }

    def __init__(self, clear_input: bool = True, group_keys=None, *args, **kwargs):
        super().__init__(group_keys, *args, **kwargs)
        self.clear_input = clear_input
        self.test_key = self.group_keys["test"]
        self.train_key = self.group_keys["train"]

    def calculate_complexity(self):
        return 2

    def __call__(self, *args, **kwargs) -> Dict["str", SFrame]:
        return super().__call__(*args, **kwargs).make_group().children

    def set_raw(self, sf: GroupSFrame, result: Dict[str, object]):
        if self.clear_input:
            sf.children.clear()
        super().set_raw(sf, result)


class SplitterScenario(TransformerScenario):
    def format_result(self):
        # Because the output of splitters differs from other transformers.
        test = self.get_result()["test"]
        train = self.get_result()["train"]

        return {
            "test": {k: sf.to_dict() for k, sf in test.make_group().children.items()},
            "train": {k: sf.to_dict() for k, sf in train.make_group().children.items()},
        }
