import logging
import os
import uuid

from orchestra_sdk.errors import (
    MissingEnvironmentKeysError,
    NoEnvironmentVariablesFoundError,
)

logger = logging.getLogger(__name__)


def _check_env_vars(env_keys: list[str], env_vars: os._Environ[str] | None) -> None:
    if env_vars is None or len(env_vars) == 0:
        raise NoEnvironmentVariablesFoundError

    missing_keys = set()

    for key in env_keys:
        if key not in env_vars:
            missing_keys.add(key)

    if missing_keys:
        raise MissingEnvironmentKeysError(missing_keys)


def validate_environment() -> uuid.UUID | None:
    required_env_keys = ["ORCHESTRA_TASK_RUN_ID"]
    env_vars = None

    try:
        # Read the environment
        env_vars = os.environ

        # Check the environment variables
        _check_env_vars(required_env_keys, env_vars)

        task_run_id = uuid.UUID(env_vars["ORCHESTRA_TASK_RUN_ID"])

        logger.debug("Environment configured correctly for Orchestra.")
        return task_run_id
    except MissingEnvironmentKeysError as e:
        logger.warning(f"Missing environment variables: {', '.join(e.missing_keys)}")
    except NoEnvironmentVariablesFoundError:
        logger.warning("No environment variables loaded")
    except Exception as e:
        logger.error(f"Error processing environment variables: {e}")

    return None
