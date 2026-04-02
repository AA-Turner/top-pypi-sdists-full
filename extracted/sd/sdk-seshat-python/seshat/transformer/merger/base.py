from seshat.transformer import Transformer


class SFrameMerger(Transformer):
    HANDLER_NAME = "merge"
    ONLY_GROUP = True
