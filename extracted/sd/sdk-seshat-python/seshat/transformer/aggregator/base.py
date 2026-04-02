from seshat.data_class import DFrame
from seshat.general import configs
from seshat.transformer import Transformer


class Aggregator(Transformer):
    ONLY_GROUP = False
    HANDLER_NAME = "aggregate"
    DEFAULT_FRAME = DFrame
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}
