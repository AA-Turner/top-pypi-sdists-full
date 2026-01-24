from typing import Dict, Optional

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.schemas.base_config import GalileoConfig


def healthcheck(config: Optional[GalileoConfig] = None) -> Dict:
    """
    Check the health of the Galileo API.

    Returns
    -------
    Dict
        Health check response from the Galileo API.
    """
    config = config or GalileoConfig.get()
    logger.debug("Checking the health of the Galileo API...")
    response_dict = config.api_client.request(RequestMethod.GET, Routes.healthcheck)
    logger.debug("Galileo API is reachable.")
    return response_dict
