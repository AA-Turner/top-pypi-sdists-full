import os

from loguru import logger


def get_local_sca_path() -> str:
    """Returns the path to the local asset-detector bundle.

    Uses GABLE_ASSET_DETECTOR_PATH environment variable.

    Raises:
        ValueError: If GABLE_ASSET_DETECTOR_PATH is not set.
    """
    path = os.path.expanduser(os.environ.get("GABLE_ASSET_DETECTOR_PATH", ""))
    if not path:
        logger.warning("GABLE_ASSET_DETECTOR_PATH environment variable not set")
        raise ValueError(
            "GABLE_ASSET_DETECTOR_PATH environment variable is not set. "
            "Please set it to the path of the asset-detector bundle."
        )
    return path


def get_local_kotlin_script() -> str:
    """Returns the path to the local Kotlin reflection based "SCA" script.

    Uses GABLE_KOTLIN_SCRIPT_PATH environment variable.

    Raises:
        ValueError: If GABLE_KOTLIN_SCRIPT_PATH is not set.
    """
    path = os.environ.get("GABLE_KOTLIN_SCRIPT_PATH")
    if not path:
        logger.warning("GABLE_KOTLIN_SCRIPT_PATH environment variable not set")
        raise ValueError(
            "GABLE_KOTLIN_SCRIPT_PATH environment variable is not set. "
            "Please set it to the path of the Kotlin reflection script."
        )
    return path


def get_local_sca_prime() -> str:
    """Returns the path to the local SCA Prime binary.

    Uses GABLE_SCA_PRIME_PATH environment variable.

    Raises:
        ValueError: If GABLE_SCA_PRIME_PATH is not set.
    """
    path = os.environ.get("GABLE_SCA_PRIME_PATH")
    if not path:
        logger.warning("GABLE_SCA_PRIME_PATH environment variable not set")
        raise ValueError(
            "GABLE_SCA_PRIME_PATH environment variable is not set. "
            "Please set it to the path of the SCA Prime binary."
        )
    return path
