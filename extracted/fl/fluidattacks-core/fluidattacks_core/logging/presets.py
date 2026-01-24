from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging.config import _DictConfigArgs

# Main formats
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""
Default date format for logs.
"""


PRODUCT_LOGGING: _DictConfigArgs = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "production_handler": {
            "class": "fluidattacks_core.logging.handlers.ProductionSyncHandler",
            "stream": "ext://sys.stderr",
        },
        "debugging_handler": {
            "class": "fluidattacks_core.logging.handlers.DebuggingHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "handlers": ["production_handler", "debugging_handler"],
        "level": "INFO",
    },
}
"""
Default logging configuration dict for all the products.

Required environment variables:
- `PRODUCT_ID`
- `CI_COMMIT_REF_NAME`
- `CI_COMMIT_SHA`
"""
