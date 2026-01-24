
import logging


class UdfLogger(logging.Logger):

    def __init__(self, name: str):
        super().__init__(name)

    def error(self, msg, *args, **kwargs):
        msg = f"Python Worker: {msg}"
        super().error(msg, *args, **kwargs)
