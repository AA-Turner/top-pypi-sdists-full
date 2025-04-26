"""
Admin functionality helpers
"""
from contextlib import contextmanager
from typing import Dict, Optional

from mcli import config
from mcli.api.users.api_get_users import User, get_users

EMAIL_CACHE: Dict[str, User] = {}


def _populate_email_to_id_cache(email: Optional[str] = None):
    if email and email in EMAIL_CACHE:
        return  # already populated

    for user in get_users():
        EMAIL_CACHE[user.email] = user

    if email and email not in EMAIL_CACHE:
        raise ValueError(f'User with email {email} not found')


def is_user_part_of_org(email: str, org_name: str) -> bool:
    """
    Checks if a user is part of an organization
    """
    _populate_email_to_id_cache(email)

    user = EMAIL_CACHE[email]
    orgs = {org.name for org in user.organizations}
    return org_name in orgs


@contextmanager
def as_user(
    *,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
):
    """
    Context manager to temporarily override the current user
    """
    if not user_id and not email:
        raise ValueError('Must specify either user_id or email')

    config.ADMIN_MODE = True
    mcli_config = config.MCLIConfig.load_config()

    previous_user_id = mcli_config.user_id
    previous_org_id = mcli_config.organization_id

    if email:
        _populate_email_to_id_cache(email)
        user = EMAIL_CACHE[email]
        user_id = user.id

    mcli_config.user_id = user_id
    mcli_config.organization_id = None
    mcli_config.save_config()

    yield mcli_config.user_id

    config.ADMIN_MODE = False
    mcli_config.user_id = previous_user_id
    mcli_config.organization_id = previous_org_id
    mcli_config.save_config()


@contextmanager
def as_organization(*, org_id: str):
    """
    Context manager to temporarily override the current org
    """
    config.ADMIN_MODE = True
    mcli_config = config.MCLIConfig.load_config()

    previous_user_id = mcli_config.user_id
    previous_org_id = mcli_config.organization_id

    mcli_config.organization_id = org_id
    mcli_config.user_id = None
    mcli_config.save_config()

    yield mcli_config.organization_id

    config.ADMIN_MODE = False
    mcli_config.user_id = previous_user_id
    mcli_config.organization_id = previous_org_id
    mcli_config.save_config()
