import logging
import os
import inspect
from flask import jsonify
from .path_utils import mkdirs
from logging.handlers import RotatingFileHandler
from .abstract_classes import SingletonMeta


# from abstract_utilities import get_logFile  # Potential conflict - consider removing or renaming


        
class AbstractLogManager(metaclass=SingletonMeta):
    def __init__(self):
        # Create a logger; use __name__ to have a module-specific logger if desired.
        self.logger = logging.getLogger("AbstractLogManager")
        self.logger.setLevel(logging.DEBUG)  # Set to lowest level to let handlers filter as needed.

        # Create a console handler with a default level.
        self.console_handler = logging.StreamHandler()
        # Default level: show warnings and above.
        self.console_handler.setLevel(logging.WARNING)

        # Formatter for the logs.
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.console_handler.setFormatter(formatter)

        # If there are no handlers already attached, add our console handler.
        if not self.logger.hasHandlers():
            self.logger.addHandler(self.console_handler)

    def set_debug(self, enabled: bool) -> None:
        """
        Enable or disable DEBUG level messages.
        When enabled, the console handler will output DEBUG messages and above.
        When disabled, it falls back to INFO or WARNING (adjust as needed).
        """
        if enabled:
            self.console_handler.setLevel(logging.DEBUG)
            self.logger.debug("DEBUG logging enabled.")
        else:
            # For example, disable DEBUG by raising the level to INFO.
            self.console_handler.setLevel(logging.INFO)
            self.logger.info("DEBUG logging disabled; INFO level active.")

    def set_info(self, enabled: bool) -> None:
        """
        Enable or disable INFO level messages.
        When enabled, INFO and above are shown; when disabled, only WARNING and above.
        """
        if enabled:
            # Lower the handler level to INFO if currently higher.
            self.console_handler.setLevel(logging.INFO)
            self.logger.info("INFO logging enabled.")
        else:
            self.console_handler.setLevel(logging.WARNING)
            self.logger.warning("INFO logging disabled; only WARNING and above will be shown.")

    def set_warning(self, enabled: bool) -> None:
        """
        Enable or disable WARNING level messages.
        When disabled, only ERROR and CRITICAL messages are shown.
        """
        if enabled:
            # WARNING messages enabled means handler level is WARNING.
            self.console_handler.setLevel(logging.WARNING)
            self.logger.warning("WARNING logging enabled.")
        else:
            self.console_handler.setLevel(logging.ERROR)
            self.logger.error("WARNING logging disabled; only ERROR and CRITICAL messages will be shown.")

    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger


def get_logFile(bpName: str = None, maxBytes: int = 100_000, backupCount: int = 3) -> logging.Logger:
    """
    If bpName is None, use the “caller module’s basename” as the logger name.
    Otherwise, use the explicitly provided bpName.
    """
    if bpName is None:
        # Find the first frame outside logging_utils.py
        frame_idx = _find_caller_frame_index()
        frame_info = inspect.stack()[frame_idx]
        caller_path = frame_info.filename  # e.g. "/home/joe/project/app/routes.py"
        bpName = os.path.splitext(os.path.basename(caller_path))[0]
        del frame_info

    log_dir = mkdirs("logs")
    log_path = os.path.join(log_dir, f"{bpName}.log")

    logger = logging.getLogger(bpName)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
        handler.setLevel(logging.INFO)

        fmt = "%(asctime)s - %(levelname)s - %(pathname)s - %(message)s"
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

def _find_caller_frame_index():
    """
    Scan up the call stack until we find a frame whose module is NOT logging_utils.
    Return that index in inspect.stack().
    """
    for idx, frame_info in enumerate(inspect.stack()):
        # Ignore the very first frame (idx=0), which is this function itself.
        if idx == 0:
            continue
        module = inspect.getmodule(frame_info.frame)
        # If module is None (e.g. interactive), skip it;
        # else get module.__name__ and compare:
        module_name = module.__name__ if module else None

        # Replace 'yourpackage.logging_utils' with whatever your actual module path is:
        if module_name != __name__ and not module_name.startswith("logging"):
            # We found a frame that isn’t in this helper module or the stdlib logging.
            return idx
    # Fallback to 1 (the immediate caller) if nothing else matches:
    return 1


def get_logger_callable(logger, level="info"):
    if logger is None:
        return None
    elif isinstance(logger, logging.Logger):
        return getattr(logger, level.lower(), None)
    elif callable(logger) and hasattr(logger, "__self__") and isinstance(logger.__self__, logging.Logger):
        return logger
    else:
        return None


def print_or_log(message, logger=True, level="info"):
    """
    Print or log a message. If logger=True, find the first caller outside this module
    and name the logger after that caller’s basename. Then emit the log with a
    stacklevel that points directly at that same caller.
    """
    # 1) Find the first frame index outside logging_utils (and also outside the logging stdlib).
    caller_idx = _find_caller_frame_index()
    stack = inspect.stack()
    caller_frame = stack[caller_idx]
    caller_path = caller_frame.filename
    # e.g. "/home/joe/project/app/routes.py"
    bpName = os.path.splitext(os.path.basename(caller_path))[0]
    del caller_frame
    del stack

    if logger is True:
        # 2) Now get (or create) a logger named after the original caller’s basename:
        logger = get_logFile(bpName)

    log_callable = get_logger_callable(logger, level=level)
    if log_callable:
        # 3) Use the same index as stacklevel, so that the LogRecord’s pathname
        #    is exactly caller_path.
        log_callable(message, stacklevel=caller_idx + 1)
        # Explanation:
        #   - stacklevel=1 => log record’s pathname points to log_callable() itself
        #   - stacklevel=2 => pathname points to print_or_log()
        #   - stacklevel=3 => pathname points to initialize_call_log() (if called)
        #   - ...
        #   - stacklevel=caller_idx+1 => pathname points exactly to stack[caller_idx].filename
    else:
        print(message)

def initialize_call_log(value=None,
                        data=None,
                        logMsg=None,
                        log_level=None):
    """
    Inspect the stack to find the first caller *outside* this module,
    then log its function name and file path.
    """
    # Grab the current stack
    stack = inspect.stack()
    caller_name = "<unknown>"
    caller_path = "<unknown>"
    log_level = log_level or 'info'
    try:
        # Starting at index=1 to skip initialize_call_log itself
        for frame_info in stack[1:]:
            modname = frame_info.frame.f_globals.get("__name__", "")
            # Skip over frames in your logging modules:
            if not modname.startswith("abstract_utilities.log_utils") \
               and not modname.startswith("abstract_flask.request_utils") \
               and not modname.startswith("logging"):
                caller_name = frame_info.function
                caller_path = frame_info.filename
                break
    finally:
        # Avoid reference cycles
        del stack

    logMsg = logMsg or "initializing"
    full_message = (
        f"{logMsg}\n"
        f"calling_function: {caller_name}\n"
        f"path: {caller_path}\n"
        f"data: {data}"
    )

    print_or_log(full_message,level=log_level)
    
def get_json_call_response(value, status_code, data=None,logMsg=None,callLog = False):
    response_body = {}
    if status_code == 200:
        response_body["success"] = True
        response_body["result"] = value
        logMsg = logMsg or "success"
        if callLog:
            initialize_call_log(value=value,
                            data=data,
                            logMsg=logMsg,
                            log_level='info')
    else:
        response_body["success"] = False
        response_body["error"] = value
        logMsg = logMsg or f"ERROR: {logMsg}"
        initialize_call_log(value=value,
                            data=data,
                            logMsg=logMsg,
                            log_level='error')
    return jsonify(response_body), status_code


