import importlib
from typing import Any, Dict

from spready.config import getEnvURL
from .parser import SpreadyDecoratorParser
import os, sys
from loguru import logger
import requests

 
parser = SpreadyDecoratorParser(os.environ["SPREADY_MODULES"])
spreadyModules = parser.spreadyRouts

logger.info(f"Spready moduels found: {spreadyModules}")

from .dto import SPRequest


def updateStatus(statusURL, res, headers):
    logger.info("Updating status")
    try:
        statusUpdate = requests.post(statusURL, headers=headers, json=res)
        if statusUpdate.status_code != 200:
            logger.warning(
                f"Failed to update status: {statusUpdate.status_code}"
            )
        else:
            logger.debug(f"Updated status successfully!")
    except Exception as _e:
        logger.warning(f"Failed to update status: {_e}")


def runjob(routePath: str, params: Dict[str, Any], requestType: str, headers: Dict[str, Any] = {}):
    logger.info(f"Running function with {routePath} and {params}")
    statusURL = f"{getEnvURL()}/status/{headers['x-spready-job-id']}"
    result = {}
    try:
        if routePath in spreadyModules:
            function_string = spreadyModules[routePath]
        else:
            logger.error(f"Route not found {routePath}")
            raise Exception("Route not found")
        mod_name, func_name = function_string.rsplit('.',1)
        logger.debug(f"Module name: {mod_name}")
        logger.debug(f"Function name: {func_name}")
        sys.path.append(os.getcwd())
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        req = SPRequest(json=params, requestType=requestType, headers=headers)
        result = func(req)
        logger.debug(f"Output: {result}")
        return result
    except Exception as _e:
        result = {"error": str(_e)}
    finally:
        updateStatus(statusURL=statusURL, res=result, headers=headers)
        return result

        
