import logging
import time


class ThrottlingFilter(logging.Filter):
    """A logging filter that throttles repeated log messages."""

    def __init__(self, interval: float = 5):
        super().__init__()
        self.interval = interval
        self.last_logged: dict[tuple[int, object], float] = {}

    def filter(self, record: logging.LogRecord) -> bool:
        now = time.time()
        key = (record.levelno, record.msg)
        if now - self.last_logged.get(key, 0) > self.interval:
            self.last_logged[key] = now
            return True
        return False


logger = logging.getLogger("livekit_plugins_krisp_internal")
logger.addFilter(ThrottlingFilter())
