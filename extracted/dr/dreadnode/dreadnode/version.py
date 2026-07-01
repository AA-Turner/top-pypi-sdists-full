import os
from importlib.metadata import PackageNotFoundError, version

try:
    VERSION = version("dreadnode")
except PackageNotFoundError:
    VERSION = "0.0.0+local"

# Testing override — e.g. _DN_TEST_VERSION=1.0.0 to simulate an outdated install
VERSION = os.environ.get("_DN_TEST_VERSION", VERSION)
