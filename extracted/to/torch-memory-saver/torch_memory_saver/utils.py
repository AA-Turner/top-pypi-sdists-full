import logging
import os
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)


def get_binary_path_from_package(stem: str):
    dir_package = Path(__file__).parent
    candidates = [p for d in [dir_package, dir_package.parent] for p in d.glob(f"{stem}.*.so")]
    assert len(candidates) == 1, f"Expected exactly one torch_memory_saver_cpp library, found: {candidates}"
    return candidates[0]


# private utils, not to be used by end users
@contextmanager
def change_env(key: str, value: str):
    old_value = os.environ.get(key, "")
    os.environ[key] = value
    logger.debug(f"change_env set key={key} value={value}")
    try:
        yield
    finally:
        assert os.environ[key] == value
        os.environ[key] = old_value
        logger.debug(f"change_env restore key={key} value={old_value}")
