from seshat.data_class.pandas import DFrame
from seshat.general import configs
from seshat.transformer import Transformer


class SFrameTrimmer(Transformer):
    """
    Interface for trimmer, specially set handler name to `trim` for all other trimmers.
    """

    HANDLER_NAME = "trim"
    DEFAULT_FRAME = DFrame
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}

    def __init__(self, group_keys=None, address_cols=None):
        super().__init__(group_keys)
        self.address_cols = address_cols
