""" mcli modify user functions """
import argparse
import logging
from typing import Optional

from mcli.api.users.api_get_users import get_users as api_get_users
from mcli.config import MCLIConfig
from mcli.utils.utils_interactive import choose_one
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def modify_user(
    user_identifier: Optional[str] = None,
    **kwargs,
) -> int:
    """Updates user for admin mode.

    Args:
        user_identifier: Either the user id or the email of the user to set.
                         If None, then the user is cleared.

    Returns:
        0 if succeeded, else 1 (e.g., if the user is not found)
    """
    del kwargs

    # Get the current user
    conf = MCLIConfig.load_config()

    # Unset operations can be completed immediately.
    if user_identifier is None:
        conf.user_id = None
        msg = f"{OK} Unset User"
        if conf.organization_id:
            msg += ' and Organization'
            conf.organization_id = None
        conf.save_config()
        logger.info(msg)
        return 0

    # Set operations requires a query of all users to find the user that
    # corresponds to the provided id or email.
    is_email = '@' in user_identifier
    users = api_get_users(user_emails=[user_identifier]) if is_email else api_get_users(users=[user_identifier])
    if len(users) == 0:
        logger.error(f"{FAIL} Unable to find User {user_identifier}")
        return 1

    user = users[0]

    org = None
    if len(user.organizations) == 0:
        logger.warning(f"{FAIL} User {user.name} ({user.email}) has no organizations. Will try making queries anyways")
    elif len(user.organizations) == 1:
        org = user.organizations[0]
    elif len(user.organizations) > 1:
        org = choose_one(
            'Which organization should be used for this user?',
            options=user.organizations,
        )

    conf.user_id = user.id
    msg = f'{OK} Updated User ID to {user.id} ({user.name} | {user.email})'
    if org:
        conf.organization_id = org.id
        msg += f' and Organization ID to {org.id} ({org.name})'
    conf.save_config()
    logger.info(msg)
    return 0


def configure_user_argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("user_identifier", help="user id or email")
