import os
from pathlib import Path, PosixPath

FROGML_DIR_PATH: PosixPath = Path.home() / ".frogml"
CONFIG_FILE_PATH: str = os.path.join(FROGML_DIR_PATH, "config.json")
FROG_ML_CONFIG_USER = "user"
FROG_ML_CONFIG_ARTIFACTORY_URL = "artifactory_url"
SERVER_ID = "server_id"
JF_URL = "JF_URL"
JF_ACCESS_TOKEN = "JF_ACCESS_TOKEN"  # nosec B105
FROG_ML_CONFIG_PASSWORD = "password"  # nosec B105
FROG_ML_CONFIG_ACCESS_TOKEN = "access_token"  # nosec B105
