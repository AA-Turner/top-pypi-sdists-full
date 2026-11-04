from __future__ import annotations

from typing import TYPE_CHECKING

from seeq.base.seeq_names import SeeqNames
from seeq.sdk import ApiClient
from seeq.sdk.api import ItemsApi, UsersApi, UserGroupsApi, FormulasApi
from seeq.sdk.models import PutScalarsInputV1, UserOutputV1, UserGroupOutputV1, AddOnToolInputV1, WorkbookOutputV1
from seeq.spy import _version

if TYPE_CHECKING:
    # Imported for type checking only, because importing it at runtime would cycle back through _login.
    from seeq.spy._session import Session


def is_continuation_token_used() -> bool:
    """
    Check if compute API endpoints should use the continuation_token field for pagination. On false, should use the
    old start key increment and deduplicate capsules scheme.

    Returns
    -------
    True if the SDK version is equal to or greater than 63.
    """
    return _version.is_sdk_module_version_at_least(63)


def is_force_calculated_scalars_available() -> bool:
    """
    Check if the force_calculated_scalars parameter is available on the PutScalars endpoint.

    Returns
    -------
    True if the force_calculated_scalars parameter is available on the PutScalars endpoint.
    """
    return 'force_calculated_scalars' in PutScalarsInputV1.attribute_map


def is_launch_location_available() -> bool:
    """
    Check if the launch_location parameter is available on the AddOnTools endpoint.

    Returns
    -------
    True if the launch_location parameter is available on the AddOnTools endpoint.
    """
    return 'launch_location' in AddOnToolInputV1.attribute_map


def is_compile_formula_and_parameters_available() -> bool:
    """
    Check if the compile_formula_and_parameters method is available in the FormulasApi.

    Returns
    -------
    True if the compile_formula_and_parameters method is available in the FormulasApi.
    """
    return hasattr(FormulasApi, 'compile_formula_and_parameters')


def is_vantage_supported() -> bool:
    """
    Check if Vantage is available in this server.

    Returns
    -------
    True if Vantage is supported.
    """
    return _version.is_sdk_module_version_at_least(66, 30, 0)


def are_vantage_rooms_as_workbooks_supported() -> bool:
    """
    Vantage Rooms used to be in their own weird database. Now they look like workbooks in the backend and have
    an evidence_table_definition_id field.

    Returns
    -------
    True if Vantage Rooms are backed by workbooks.
    """
    return 'evidence_table_definition_id' in WorkbookOutputV1.attribute_map


def is_user_in_early_access(session: Session) -> bool:
    """
    Check if the acting user is a member of the Early Access capability group.

    Returns
    -------
    True if the logged-in user has been granted the Early Access capability.
    """
    user = getattr(session, 'user', None)
    if user is None:
        return False

    # The Early Access Capability was added in R66.64 (2025-10-14); older servers cannot have Early Access users.
    capability_grants = getattr(user, 'capability_grants', None)
    if not capability_grants:
        return False

    return any(grant.capability == SeeqNames.Capabilities.EarlyAccess.data_id for grant in capability_grants)


def is_item_finder_sdk_available() -> bool:
    """
    Returns
    -------
    True if the ItemFinder search endpoint is present in the installed SDK.
    """
    return hasattr(ItemsApi, 'execute_item_finder_searches_v2')


def is_item_finder_search_available(session: Session) -> bool:
    """
    Check if item searches should go through the ItemFinder search endpoint instead of the legacy
    ItemsApi.search_items and TreesApi endpoints.

    Gated on Early Access membership for the initial rollout. Once the endpoint ships broadly this becomes a
    server version check, and callers do not have to change.

    Also gated on spy.options.compatibility >= 203. An untyped ItemFinder search returns fewer types than legacy
    search by default so this would be considered a breaking behavior change.

    Returns
    -------
    True if ItemFinder search should be used.
    """
    if not is_item_finder_sdk_available():
        return False

    ITEM_FINDER_SPY_VERSION = 203
    if session.options.wants_compatibility_with(ITEM_FINDER_SPY_VERSION - 1):
        return False

    return is_user_in_early_access(session)


def get_user(client: ApiClient, user_id: str, *, include_groups: bool = True) -> UserOutputV1:
    """
    Get a user

    Parameters
    ----------
    client : ApiClient
        The api_client to use for the SDK call.
    user_id : str
        ID of the user to get (required)
    include_groups : bool
        Include the groups of which the user is a member. Note that, depending on the version of Seeq, this parameter
        may not be supported.
    """
    users_api = UsersApi(client)
    try:
        return users_api.get_user(id=user_id, include_groups=include_groups)
    except TypeError:
        return users_api.get_user(id=user_id)


def get_user_group(client: ApiClient, user_group_id: str, *, include_members: bool = True) -> UserGroupOutputV1:
    """
    Get a user group.

    client : ApiClient
        The session to use for the request (required)
    user_group_id : str
        ID of the user group to get (required)
    include_members : bool
        Include the members (users) of the user group. Note that, depending on the version of Seeq, this parameter may
        not be supported.
    """
    usergroups_api = UserGroupsApi(client)
    try:
        return usergroups_api.get_user_group(user_group_id=user_group_id, include_members=include_members)
    except TypeError:
        return usergroups_api.get_user_group(user_group_id=user_group_id)
