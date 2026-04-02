from seshat.data_class.pandas import DFrame
from seshat.transformer import Transformer


class SFrameDeriver(Transformer):
    """
    Interface for deriver, specially set handler name to `derive` for all other derivers.
    """

    ONLY_GROUP = False
    HANDLER_NAME = "derive"
    DEFAULT_FRAME = DFrame
