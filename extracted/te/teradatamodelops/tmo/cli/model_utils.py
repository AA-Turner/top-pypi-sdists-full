import logging
import os
import shutil

ARTIFACTS_PATH = "./artifacts"
MODELS_PATH = "./models"

logger = logging.getLogger(__name__)


def cleanup_artifacts():
    """
    Clean up artifacts and models directories.

    Removes the artifacts directory if it exists and the models
    file/directory if it exists.
    """
    if os.path.exists(ARTIFACTS_PATH):
        # Handle symlinks separately as shutil.rmtree fails on them
        if os.path.islink(ARTIFACTS_PATH):
            os.unlink(ARTIFACTS_PATH)
        else:
            shutil.rmtree(ARTIFACTS_PATH)
    try:
        os.remove(MODELS_PATH)
    except OSError:
        logger.debug(f"Nothing to remove, folder '{MODELS_PATH}' does not exists.")
