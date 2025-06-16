class UnauthorizedRequestError(RuntimeError):
    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
