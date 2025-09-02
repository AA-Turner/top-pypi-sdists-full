from ..imports import *
# — UI helpers —
def emit(self, record):
    try:
        msg = self.format(record)
        self.widget.append(msg)
        self.widget.ensureCursorVisible()
    except Exception as e:
        logger.info(f"{e}")
