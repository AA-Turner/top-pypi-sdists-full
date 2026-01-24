from .imports import *
import os, sys, inspect, logging
from logging.handlers import RotatingFileHandler
import logging
from pathlib import Path
PACKAGE_NAME = "abstract_utilities"   # ← update if needed


def _resolve_log_root():
    """
    Returns a safe writable logging directory depending on environment:
    - If running in a virtualenv → <venv>/.logs/<package>
    - Else if user writable → ~/.cache/<package>/logs
    - Else → /var/log/<package>
    """
    # 1) Virtualenv or Conda environment
    venv = os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")
    if venv:
        root = os.path.join(venv, ".logs", PACKAGE_NAME)
        os.makedirs(root, exist_ok=True)
        return root

    # 2) User home cache folder
    home = os.path.expanduser("~")
    user_cache_root = os.path.join(home, ".cache", PACKAGE_NAME, "logs")
    try:
        os.makedirs(user_cache_root, exist_ok=True)
        return user_cache_root
    except PermissionError:
        pass

    # 3) Last resort: system log dir (requires correct service user permissions)
    system_root = f"/var/log/{PACKAGE_NAME}"
    try:
        os.makedirs(system_root, exist_ok=True)
        return system_root
    except PermissionError:
        # Fail-safe fallback to /tmp
        fallback = f"/tmp/{PACKAGE_NAME}/logs"
        os.makedirs(fallback, exist_ok=True)
        return fallback


LOG_ROOT = _resolve_log_root()


##def get_logFile(bpName=None, maxBytes=100_000, backupCount=3):
##    """
##    A logger that always writes to a safe OS-appropriate path.
##    Works even when installed through pip.
##    """
##    if bpName is None:
##        frame_idx = _find_caller_frame_index()
##        frame_info = inspect.stack()[frame_idx]
##        caller_path = frame_info.filename
##        bpName = os.path.splitext(os.path.basename(caller_path))[0]
##        del frame_info
##
##    logger = logging.getLogger(f"{PACKAGE_NAME}.{bpName}")
##    logger.setLevel(logging.INFO)
##
##    if not logger.handlers:
##        log_file = os.path.join(LOG_ROOT, f"{bpName}.log")
##        handler = RotatingFileHandler(log_file, maxBytes=maxBytes, backupCount=backupCount)
##
##        fmt = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
##        formatter = logging.Formatter(fmt)
##        handler.setFormatter(formatter)
##
##        logger.addHandler(handler)
##
##        # Console handler (optional; can disable for gunicorn)
##        console = logging.StreamHandler(sys.stdout)
##        console.setFormatter(formatter)
##        logger.addHandler(console)
##
##    return logger
LOG_FORMAT = (
    "[%(asctime)s] "
    "%(levelname)-8s "
    "%(name)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"




def get_logFile(
    name: str,
    log_dir: str | Path = "logs",
    level: int = logging.INFO,
    console: bool = True,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    try:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except PermissionError:
        # 🔒 Import-safe fallback
        logger.addHandler(logging.NullHandler())

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger



def _find_caller_frame_index():
    """Find the correct caller module outside this logger."""
    for idx, frame_info in enumerate(inspect.stack()):
        if idx == 0:
            continue
        module = inspect.getmodule(frame_info.frame)
        if module and module.__name__ not in (__name__, "logging"):
            return idx
    return 1
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
