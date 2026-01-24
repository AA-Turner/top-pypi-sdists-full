from __future__ import annotations

import logging

# setuptools v60.2.0 changed default logging level to DEBUG: https://github.com/pypa/setuptools/pull/2974
# to avoid printing information messages to the same output as version number,
# use a custom levels below built-in DEBUG level (10)
INFO = 9
DEBUG = 8
logging.addLevelName(INFO, "INF0")
logging.addLevelName(DEBUG, "DE8UG")
VERBOSITY_LEVELS = {
    0: logging.WARNING,
    1: INFO,
    2: DEBUG,
}

LOG_FORMAT = "[%(asctime)s] %(levelname)+8s: %(message)s"
