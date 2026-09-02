from .imports import *
from .log_file import *
def get_logger_callable(logger, level="info"):
    if logger is None:
        return None
    elif isinstance(logger, logging.Logger):
        return getattr(logger, level.lower(), None)
    elif callable(logger) and hasattr(logger, "__self__") and isinstance(logger.__self__, logging.Logger):
        return logger
    else:
        return None


def _find_caller_frame_index():
    """
    Return the index in inspect.stack() of the first frame
    that’s not in this module or the logging stdlib.
    """
    for idx, frame_info in enumerate(inspect.stack()):
        fn = frame_info.filename
        if not fn.endswith("logging_utils.py") and "logging" not in os.path.basename(fn):
            return idx
    return 0  # fallback

def get_caller_info():
    """
    Returns (caller_path, caller_idx).
    caller_idx is the index into inspect.stack() where the call came from.
    """
    idx = _find_caller_frame_index()
    frame = inspect.stack()[idx]
    return frame.filename, idx

def print_or_log(message, logger=True, level="info"):
    # 1) grab both the path and the numeric index
    caller_path, caller_idx = get_caller_info()

    # 2) decide which logger object to use
    if logger is True:
        bpName = os.path.splitext(os.path.basename(caller_path))[0]
        logger = get_logFile(bpName)

    # 3) pick the right logging method
    log_callable = get_logger_callable(logger, level=level)
    if log_callable:
        # pass the integer stacklevel = caller_idx + 1
        log_callable(message, stacklevel=caller_idx + 1)
    else:
        print(message)
