from seshat.data_class.pandas import DFrame
from seshat.transformer import Transformer


class SFrameVectorizer(Transformer):
    ONLY_GROUP = False
    HANDLER_NAME = "vectorize"
    DEFAULT_FRAME = DFrame
