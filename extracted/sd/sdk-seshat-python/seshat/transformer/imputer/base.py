from seshat.transformer import Transformer


class Imputer(Transformer):
    def impute(self):
        pass


class SFrameImputer(Transformer):
    HANDLER_NAME = "impute"
