"""Initialize logging with good defaults"""

from typing import Dict, Any, cast
import logging
import logging.config
import copy
import os
import json


from .common import DEFAULT_LOGGING_CONFIG, UTCISOFormatter, DEFAULT_LOG_FORMAT, log_metrics, AddExtrasFilter


def init_logging(level: int = logging.INFO) -> None:
    """Initialize logging, call this if you don't know any better logging arrangements"""
    labels_json = os.environ.get("LOG_GLOBAL_LABELS_JSON")
    if os.environ.get("LOG_HTTP_TARGET_URI"):
        from .httpmulti import HTTP_LOGGING_CONFIG  # pylint: disable=C0415

        config = copy.deepcopy(HTTP_LOGGING_CONFIG)
    else:
        config = cast(Dict[str, Any], copy.deepcopy(DEFAULT_LOGGING_CONFIG))
    # If we have the labels env set, apply filter that sets these labels to all log records
    if labels_json:
        config["filters"] = {
            "global_labels": {
                "()": AddExtrasFilter,
                "extras": json.loads(labels_json),
            },
        }
        for key in config["handlers"]:
            if "filters" not in config["handlers"][key]:
                config["handlers"][key]["filters"] = []
            config["handlers"][key]["filters"].append("global_labels")
    # Set root loglevel to desired
    config["root"]["level"] = level
    logging.config.dictConfig(config)


# export the common names here too for backwards compatibility
__all__ = ["DEFAULT_LOG_FORMAT", "UTCISOFormatter", "DEFAULT_LOGGING_CONFIG", "log_metrics", "init_logging"]
