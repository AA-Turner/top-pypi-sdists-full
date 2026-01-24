#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import logging
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent / "includes/python"))

from .server import get_session  # noqa: E402, F401
from .server import init_spark_session  # noqa: E402, F401
from .server import start_session  # noqa: E402, F401
from .utils.session import skip_session_configuration  # noqa: E402, F401

# Turn off catalog warning for Snowpark
sp_logger = logging.getLogger("snowflake.snowpark")


class NoCatalogExperimentalFilter(logging.Filter):
    def filter(self, record):
        return "Session.catalog() is experimental" not in record.getMessage()


sp_logger.addFilter(NoCatalogExperimentalFilter())
