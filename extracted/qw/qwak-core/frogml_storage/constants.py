import os

home_dir = os.path.expanduser("~")

JFROG_CLI_CONFIG_FILE_PATH = os.path.join(home_dir, ".jfrog", "jfrog-cli.conf.v6")
CONFIG_FILE_PATH = os.path.join(home_dir, ".frogml", "config.json")

FROG_ML_CONFIG_USER = "user"
FROG_ML_CONFIG_ARTIFACTORY_URL = "artifactory_url"
FROG_ML_CONFIG_PASSWORD = "password"  # nosec B105
FROG_ML_CONFIG_ACCESS_TOKEN = "access_token"  # nosec B105
FROG_ML_DEFAULT_HTTP_THREADS_COUNT = 5
FROG_ML_MAX_CHARS_FOR_NAME = 60

SERVER_ID = "server_id"

JFROG_CLI_CONFIG_ARTIFACTORY_URL = "artifactoryUrl"
JFROG_CLI_CONFIG_URL = "url"
JFROG_CLI_CONFIG_USER = "user"
JFROG_CLI_CONFIG_PASSWORD = "password"  # nosec B105
JFROG_CLI_CONFIG_ACCESS_TOKEN = "accessToken"  # nosec B105

MODEL = "model"
ROOT_FROGML_MODEL_UI_DIRECTORY = "models"
MODEL_UI_DIRECTORY = "model"
MODEL_METADATA_FILE_NAME = "model-manifest.json"
BODY_PART_MODEL_MANIFEST_STREAM = "modelManifest"

DATASET = "dataset"
ROOT_FROGML_DATASET_UI_DIRECTORY = "datasets"
DATASET_UI_DIRECTORY = "dataset"
DATASET_METADATA_FILE_NAME = "dataset-manifest.json"
BODY_PART_DATASET_MANIFEST_STREAM = "datasetManifest"

CHECKSUM_SHA2_HEADER = "X-Checksum-Sha256"

JFML_THREAD_COUNT = "JFML_THREAD_COUNT"
JF_URL = "JF_URL"
JF_ACCESS_TOKEN = "JF_ACCESS_TOKEN"  # nosec B105

FROG_ML_IGNORED_FILES = [
    ".DS_Store",
    "CVS",
    ".cvsignore",
    "SCCS",
    "vssver.scc",
    ".svn",
    ".git",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".gitkeep",
    ".gitconfig",
    MODEL_METADATA_FILE_NAME,
    DATASET_METADATA_FILE_NAME,
]
