from fluidattacks_core.logging.filters import BatchOnlyFilter, NoBatchFilter
from fluidattacks_core.logging.formatters import ColorfulFormatter
from fluidattacks_core.logging.handlers import DebuggingHandler, ProductionSyncHandler
from fluidattacks_core.logging.utils import get_environment_metadata, get_job_metadata

# Main formats
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""
Default date format for logs.
"""


# Configuration for logging in batch environments
_JOB_METADATA = get_job_metadata()
_ENVIRONMENT_METADATA = get_environment_metadata()

BATCH_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "batch_only": {"()": BatchOnlyFilter},
        "no_batch": {"()": NoBatchFilter},
    },
    "formatters": {
        "one_line_format": {
            "class": "logging.Formatter",
            "format": (
                "{asctime} {levelname} [{name}] [{filename}:{lineno}] "
                "[trace_id=None span_id=None "
                f"service.name=batch/{_JOB_METADATA.job_queue} "
                f"service.version={_ENVIRONMENT_METADATA.version} "
                f"deployment.environment={_ENVIRONMENT_METADATA.environment} "
                "trace_sampled=False]"
                " - {message}, extra=None"
            ),
            "datefmt": DATE_FORMAT,
            "style": "{",
        },
        "simple_format": {
            "class": "logging.Formatter",
            "format": "{asctime} [{levelname}] [{name}] {message}",
            "datefmt": DATE_FORMAT,
            "style": "{",
        },
        "colorful_format": {
            "()": ColorfulFormatter,
            "datefmt": DATE_FORMAT,
            "style": "{",
        },
    },
    "handlers": {
        "batch_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "one_line_format",
            "filters": ["batch_only"],
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "colorful_format",
            "filters": ["no_batch"],
        },
    },
    "root": {
        "handlers": ["batch_handler", "console_handler"],
        "level": "INFO",
    },
}
"""
Logging configuration dict for batch environments.

Root logger will have two handlers for batch and non-batch environments.
"""

PRODUCT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "production_handler": {"()": ProductionSyncHandler},
        "debugging_handler": {"()": DebuggingHandler},
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
