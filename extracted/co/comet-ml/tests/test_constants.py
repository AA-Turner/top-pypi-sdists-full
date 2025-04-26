import os
import sys
from os.path import dirname, join

# there is no ydata_profile yet exists for 3.13+
YDATA_PROFILE_SKIP = sys.version_info[:2] > (3, 12)
# there is no Ray yet exists for 3.13
RAY_SKIP = sys.version_info[:2] > (3, 12)

DUMMY_BACKEND_ADDRESS = "https://localhost/clientlib/"

TEST_LOGO_IMAGE_PATH = join(dirname(__file__), "logo.png")
TEST_AUDIO_SAMPLE_PATH = join(dirname(__file__), "test.wav")
TEST_VIDEO_SAMPLE_PATH = join(dirname(__file__), "video.mp4")
TEST_SVG_IMAGE_PATH = join(dirname(__file__), "test.svg")
BINARY_ARTIFACT_FILE_PATH = join(dirname(__file__), "bin_artifact")
TEST_TABLE_CSV_PATH = join(dirname(__file__), "test_table.csv")
TEST_NOTEBOOK_PATH = join(dirname(__file__), "Notebook.ipynb")

MAIN_PID = os.getpid()
MAX_TRY_SECONDS = 20

FLUSH_INITIAL_DATA_LOGGER_TIMEOUT = 10

OS_PACKAGES_AVAILABLE = os.path.isfile("/var/lib/dpkg/status")

DUMMY_FEATURE_TOGGLE = "dummy_feature_toggle"

# The dummy values for testing
SOME_KEY = "some key"
SOME_VALUE = "some value"
SOME_API_KEY = "some api key"
SOME_RUN_ID = "some run id"
SOME_PROJECT_ID = "some project id"
SOME_PROJECT_NAME = "some  project name"
SOME_EXPERIMENT_KEY = "some experiment id"
SOME_WORKSPACE_ID = "some-workspace-id"
SOME_WORKSPACE = "WORKSPACE NAME"
