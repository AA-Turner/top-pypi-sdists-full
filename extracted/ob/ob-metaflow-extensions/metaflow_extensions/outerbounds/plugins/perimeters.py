import os
import fcntl
from os import path
import json
from metaflow.exception import MetaflowException
from typing import Union

CURRENT_PERIMETER_KEY = "OB_CURRENT_PERIMETER"
CURRENT_PERIMETER_URL = "OB_CURRENT_PERIMETER_MF_CONFIG_URL"
CURRENT_PERIMETER_URL_LEGACY_KEY = (
    "OB_CURRENT_PERIMETER_URL"  # For backwards compatibility with workstations.
)


def get_perimeter_config_url_if_set_in_ob_config() -> Union[str, None]:
    # If OBP_CONFIG_DIR is set, use that, otherwise use METAFLOW_HOME
    # If neither are set, use ~/.metaflowconfig
    obp_config_dir = path.expanduser(
        os.environ.get(
            "OBP_CONFIG_DIR", os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")
        )
    )

    profile = os.environ.get("METAFLOW_PROFILE")
    file_path = (
        os.path.join(obp_config_dir, "ob_config.json")
        if not profile
        else os.path.join(obp_config_dir, f"ob_config_{profile}.json")
    )

    if os.path.exists(file_path):
        # Acquire a shared read lock on the file
        # This is important! Any process that is using metaflow at the moment will hold this lock
        # disallowing the outerbounds CLI from changing the perimeter mid process.
        # Note that this is an advisory lock, the file can still be edited by any process should it choose to.
        # The lock is released when the metaflow process finishes, whether gracefully or not.
        fd = os.open(file_path, os.O_RDONLY)
        fcntl.flock(fd, fcntl.LOCK_SH)

        with open(file_path, "r") as f:
            ob_config = json.loads(f.read())

        if CURRENT_PERIMETER_KEY in ob_config and (
            CURRENT_PERIMETER_URL in ob_config
            or CURRENT_PERIMETER_URL_LEGACY_KEY in ob_config
        ):
            os.environ[CURRENT_PERIMETER_KEY] = ob_config[CURRENT_PERIMETER_KEY]
            if CURRENT_PERIMETER_URL in ob_config:
                os.environ[CURRENT_PERIMETER_URL] = ob_config[CURRENT_PERIMETER_URL]
            elif CURRENT_PERIMETER_URL_LEGACY_KEY in ob_config:
                os.environ[CURRENT_PERIMETER_URL] = ob_config[
                    CURRENT_PERIMETER_URL_LEGACY_KEY
                ]
            return os.environ[CURRENT_PERIMETER_URL]
        else:
            raise MetaflowException(
                "{} does not contain the key {}".format(
                    file_path, CURRENT_PERIMETER_KEY
                )
            )
    elif "OBP_CONFIG_DIR" in os.environ:
        raise MetaflowException(
            "Environment variable OBP_CONFIG_DIR is set to {} but this directory does not contain an ob_config.json file.".format(
                os.environ["OBP_CONFIG_DIR"]
            )
        )
    return None
