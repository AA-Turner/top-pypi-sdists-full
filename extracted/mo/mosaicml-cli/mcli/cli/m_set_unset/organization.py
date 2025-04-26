""" mcli modify organization functions """
import argparse
import logging
from typing import Optional

from mcli.config import MCLIConfig
from mcli.utils.utils_logging import OK

logger = logging.getLogger(__name__)


def modify_organization(
    organization_id: Optional[str] = None,
    **kwargs,
) -> int:
    """Sets organization for admin mode

    Returns:
        0 if succeeded, else 1
    """
    del kwargs

    # Get the current org
    conf = MCLIConfig.load_config()
    conf.organization_id = organization_id
    conf.user_id = None
    conf.save_config()

    if organization_id:
        logger.info(f"{OK} Updated Organization to {organization_id}")
    else:
        logger.info(f"{OK} Unset Organization and User")
    return 0


def configure_organization_argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('organization_id')
