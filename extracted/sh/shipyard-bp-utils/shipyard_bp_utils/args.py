import os
import re
from urllib import parse
from shipyard_templates import ShipyardLogger

logger = ShipyardLogger.get_logger()


def convert_to_boolean(string: str, default: bool = False) -> bool:
    """
    Convert a string to a boolean.

    Args:
    string (str): A string to convert to a boolean.
    default (bool): The default value to return if the string is None or does not match "TRUE" or "FALSE"

    Returns:
    bool: True if string is TRUE, False if string is FALSE, else default.
    """
    logger.debug(f"Converting {string} to boolean...")
    result = None

    if string:
        bool_string = string.upper().strip()
        if bool_string == "FALSE":
            result = False
        elif bool_string == "TRUE":
            result = True
    if result is None:
        result = default
        if string is None:
            logger.warning(f"Argument was not set. Using default: {result}.")
        else:
            logger.warning(
                f'Input "{string}" did not match expected "TRUE" or "FALSE" (case-insensitive) formats.'
                f"Using default: {result}."
            )
    logger.debug(f"Converted {string} to {result} boolean.")
    return result


def create_shipyard_link() -> str:
    """
    Create a link back to the Shipyard log page for the currently running voyage.

    This function generates a URL that links to the Shipyard log page. It uses
    environment variables to construct this link. If all required environment variables
    are not set, a generic Shipyard URL is returned.

    Returns:
    str: A URL string that links to the Shipyard log page for the current voyage,
         or a generic Shipyard URL if the necessary details are not available.
    """
    logger.debug("Creating Shipyard link...")

    base_url = "https://app.shipyardapp.com/"
    org_name = os.getenv("SHIPYARD_ORG_NAME")
    project_id = os.getenv("SHIPYARD_PROJECT_ID")
    fleet_id = os.getenv("SHIPYARD_FLEET_ID")
    vessel_id = os.getenv("SHIPYARD_VESSEL_ID")
    fleet_log_id = os.getenv("SHIPYARD_FLEET_LOG_ID")
    vessel_log_id = os.getenv("SHIPYARD_LOG_ID")

    if project_id and fleet_id and fleet_log_id:
        logger.debug("Detecting project_id, fleet_id, and fleet_log_id...")
        dynamic_link_section = f"{org_name}/projects/{project_id}/fleets/{fleet_id}/logs/{fleet_log_id}/{vessel_log_id}"
    elif project_id and vessel_id and vessel_log_id:
        logger.debug("Detecting project_id, vessel_id, and vessel_log_id...")
        dynamic_link_section = (
            f"{org_name}/projects/{project_id}/vessels/{vessel_id}/logs/{vessel_log_id}"
        )
    else:
        logger.debug(
            "No project_id, fleet_id, fleet_log_id, vessel_id, or vessel_log_id detected. Using generic link..."
        )
        return "www.shipyardapp.com"
    shipyard_link = base_url + parse.quote(dynamic_link_section)

    logger.debug(f"Created Shipyard link: {shipyard_link}")

    return shipyard_link
