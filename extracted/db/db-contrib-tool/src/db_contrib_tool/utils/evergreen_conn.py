"""Helper functions to interact with evergreen."""

from typing import Optional

import structlog
from evergreen import EvergreenApi, RetryingEvergreenApi

EVERGREEN_HOST = "https://evergreen.mongodb.com"

LOGGER = structlog.getLogger(__name__)


def get_evergreen_api(evergreen_config: Optional[str] = None) -> EvergreenApi:
    """
    Return evergreen API.

    :param evergreen_config: Path to Evergreen auth config.
    :return: Evergreen API client.
    """
    if evergreen_config:
        return RetryingEvergreenApi.get_api(config_file=evergreen_config, log_on_error=True)
    else:
        # use_config_file=True will search for configs in the common locations
        return RetryingEvergreenApi.get_api(use_config_file=True, log_on_error=True)
