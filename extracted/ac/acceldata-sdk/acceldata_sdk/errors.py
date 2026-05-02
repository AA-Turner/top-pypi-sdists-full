class TorchError(Exception):
    pass


class APIError(TorchError):
    def __init__(self, text):
        self.message = text


class TorchSdkException(Exception):
    pass