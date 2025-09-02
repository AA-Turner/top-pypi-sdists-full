"""Logger."""
import logging
import sys

log_format = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s")
log_level = logging.DEBUG

logger = logging.getLogger("t_nextgen")
if logger.hasHandlers():
    logger.handlers = []
logger.setLevel(log_level)
logger.propagate = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(log_format)
logger.addHandler(handler)
