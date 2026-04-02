from seshat.general import configs
from seshat.transformer import Transformer


class SFrameReducer(Transformer):
    """
    Base class for reducers operating on SFrame-like data.
    """

    HANDLER_NAME = "reduce"
    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}
