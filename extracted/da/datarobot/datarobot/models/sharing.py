#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.enums import SHARING_RECIPIENT_TYPE, SHARING_ROLE, TARGET_SHARING_ROLE
from datarobot.errors import InvalidUsageError
from datarobot.models.api_object import APIObject
from datarobot.models.user_blueprints.models import HumanReadable

if TYPE_CHECKING:
    from datarobot._compat import TypedDict

    class SharingAccessPayload(TypedDict, total=False):
        username: str
        role: str
        can_share: bool
        can_use_data: bool

    class SharingRolePayload(TypedDict, total=False):
        id: Optional[str]
        role: SHARING_ROLE
        share_recipient_type: SHARING_RECIPIENT_TYPE
        username: Optional[str]
        can_share: Optional[bool]


class SharingAccess(APIObject):
    """Represents metadata about whom a entity (e.g., a data store) has been shared with

    .. versionadded:: v2.14

    Currently :py:class:`DataStores <datarobot.DataStore>`,
    :py:class:`DataSources <datarobot.DataSource>`,
    :py:class:`Datasets <datarobot.models.Dataset>`,
    :py:class:`Projects <datarobot.models.Project>` (new in version v2.15) and
    :py:class:`CalendarFiles <datarobot.CalendarFile>` (new in version 2.15) can be shared.

    This class can represent either access that has already been granted, or be used to grant access
    to additional users.

    Attributes
    ----------
    username : str
        A particular user.
    role : str or None
        If a string, represents a particular level of access and should be one of
        ``datarobot.enums.SHARING_ROLE``. For more information on the specific access levels, see
        the :ref:`sharing <sharing>` documentation. If None, can be passed to a ``share``
        function to revoke access for a specific user.
    can_share : bool or None
        If a ``bool``, indicates whether this user is permitted to further share. When False, the
        user has access to the entity, but can only revoke their own access but not modify any
        user's access role. When True, the user can share with any other user at an access role up
        to their own. May be None if the SharingAccess was not retrieved from the DataRobot server
        but intended to be passed into a ``share`` function; this will be equivalent to passing True.
    can_use_data : bool or None
        If a ``bool``, indicates whether this user should be able to view, download, and process data
        (use to create projects, predictions, etc.). For OWNER ``can_use_data`` is always True. If role
        is empty ``canUseData`` is ignored.
    user_id : str or None
        The ID of the user.
    """

    _converter = t.Dict({
        t.Key("username"): String,
        t.Key("role"): String,
        t.Key("can_share", default=None): t.Or(t.Bool, t.Null),
        t.Key("can_use_data", default=None): t.Or(t.Bool, t.Null),
        t.Key("user_id", default=None): t.Or(String, t.Null),
    }).ignore_extra("*")

    def __init__(
        self,
        username: str,
        role: str,
        can_share: Optional[bool] = None,
        can_use_data: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> None:
        self.username = username
        self.role = role
        self.can_share = can_share
        self.can_use_data = can_use_data
        self.user_id = user_id

    def __repr__(self) -> str:
        return (
            "{cls}(username: {username}, role: {role}, "
            "can_share: {can_share}, can_use_data: {can_use_data}, user_id: {user_id})"
        ).format(
            cls=self.__class__.__name__,
            username=self.username,
            role=self.role,
            can_share=self.can_share,
            can_use_data=self.can_use_data,
            user_id=self.user_id,
        )

    def collect_payload(self) -> SharingAccessPayload:
        """Set up the dict that should be sent to the server in order to share this

        Returns
        -------
        payload : dict
        """
        payload: SharingAccessPayload = {"username": self.username, "role": self.role}
        if self.can_share is not None:
            payload["can_share"] = self.can_share
        if self.can_use_data is not None:
            payload["can_use_data"] = self.can_use_data
        return payload


class SharingRole(APIObject):
    """
    Represents metadata about a user who has been granted access to an entity.
    At least one of `id` or `username` must be set.

    Attributes
    ----------
    id : str or None
        The ID of the user.
    role : str
        Represents a particular level of access. Should be one of
        ``datarobot.enums.SHARING_ROLE``.
    share_recipient_type : SHARING_RECIPIENT_TYPE
        The type of user for the object of the method. Can be ``user`` or ``organization``.
    user_full_name : str or None
        The full name of the user.
    username : str or None
        The username (usually the email) of the user.
    can_share : bool or None
        Indicates whether this user is permitted to share with other users. When False, the
        user has access to the entity, but can only revoke their own access. They cannot not modify
        any user's access role. When True, the user can share with any other user at an access
        role up to their own.
    """

    _converter = t.Dict({
        t.Key("id", optional=True): t.String,
        t.Key("user_full_name", optional=True): t.String,
        t.Key("name", optional=True) >> "username": t.String,
        t.Key("role"): t.String,
        t.Key("share_recipient_type"): t.String,
        t.Key("can_share", optional=True, default=None): t.Or(t.Bool, t.Null),
    }).ignore_extra("*")

    def __init__(
        self,
        role: SHARING_ROLE,
        share_recipient_type: SHARING_RECIPIENT_TYPE,
        can_share: Optional[bool] = None,
        id: Optional[str] = None,
        user_full_name: Optional[str] = None,
        username: Optional[str] = None,
    ):
        if not id and not username:
            raise InvalidUsageError("Please include either a username or an ID of a user.")
        self.id = id
        self.user_full_name = user_full_name
        self.role = SHARING_ROLE[role]
        self.share_recipient_type = share_recipient_type
        self.username = username
        self.can_share = can_share

    def collect_payload(self) -> SharingRolePayload:
        """
        Generate a dictionary representation of this SharingRole.

        Returns
        -------
        formatted_role : SharingRolePayload
            A dictionary representation of this SharingRole ready for sending to DataRobot.
        """
        formatted_role: SharingRolePayload = {
            "role": self.role,
            "share_recipient_type": self.share_recipient_type,
            "can_share": self.can_share,
        }
        if self.id:
            formatted_role["id"] = self.id
        if self.username:
            formatted_role["username"] = self.username
        return formatted_role


class CatalogSharedRole(APIObject, HumanReadable):
    """Represents a role/access entry returned from the sharing API for a catalog item.

    Attributes
    ----------
    can_share : bool
        True if this user can share with other users.
    can_use_data : bool
        True if the user can view, download and process data
        (use to create projects, predictions, etc).
    id : str
        The ID of the recipient organization, group, or user.
    name : str
        The name of the recipient organization, group, or user.
    role : str
        The role of the org/group/user on this catalog entry or ``NO_ROLE``
        or removing access when used with route to modify access. One of
        ``datarobot.enums.TARGET_SHARING_ROLE``.
    share_recipient_type : str
        The recipient type.
    user_full_name : str or None
        If the recipient type is a user, the full name of the user if available.
    """

    _converter = t.Dict({
        t.Key("can_share"): t.Bool,
        t.Key("can_use_data"): t.Bool,
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("role"): t.Enum(*list(TARGET_SHARING_ROLE)),
        t.Key("share_recipient_type"): t.Enum(*list(SHARING_RECIPIENT_TYPE)),
        t.Key("user_full_name", optional=True): t.String,
    }).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        role: str,
        share_recipient_type: SHARING_RECIPIENT_TYPE,
        can_share: Optional[bool] = None,
        can_use_data: Optional[bool] = None,
        user_full_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.role = TARGET_SHARING_ROLE[role]
        self.share_recipient_type = share_recipient_type
        self.user_full_name = user_full_name
        self.can_share = can_share
        self.can_use_data = can_use_data


class CatalogSharedRoleRequest(APIObject, HumanReadable):
    """A single recipient/role entry used in a catalog sharing modification request.

    Exactly one of ``id`` or ``name`` must be provided to identify the recipient.

    Attributes
    ----------
    role : str
        The role of the org/group/user on this catalog entity or ``NO_ROLE`` for removing
        access when used with route to modify access. One of
        ``datarobot.enums.TARGET_SHARING_ROLE``.
    share_recipient_type : str
        The recipient type. One of ``datarobot.enums.SHARING_RECIPIENT_TYPE``.
    id : str or None
        The org/group/user ID. Required if ``name`` is not provided.
    name : str or None
        Name of the user/group/org to update the access role for. Required if ``id`` is
        not provided.
    can_share : bool
        Whether the org/group/user should be able to share with others. If ``True``, the
        org/group/user will be able to grant any role (up to and including their own) to
        other orgs/groups/user. If ``role`` is ``NO_ROLE``, ``can_share`` is ignored.
    can_use_data : bool or None
        Whether the user/group/org should be able to view, download, and process (e.g.,
        use it to create projects, predictions, etc) data. For ``OWNER``, ``can_use_data``
        is always ``True``.
    """

    _converter = t.Dict({
        t.Key("can_share", optional=True, default=False): t.Bool,
        t.Key("can_use_data", optional=True): t.Bool,
        t.Key("id", optional=True): t.String,
        t.Key("name", optional=True): t.String,
        t.Key("role"): t.Enum(*list(TARGET_SHARING_ROLE)),
        t.Key("share_recipient_type"): t.Enum(*list(SHARING_RECIPIENT_TYPE)),
    }).ignore_extra("*")

    def __init__(
        self,
        role: str,
        share_recipient_type: SHARING_RECIPIENT_TYPE,
        id: Optional[str] = None,
        name: Optional[str] = None,
        can_share: bool = False,
        can_use_data: Optional[bool] = None,
    ) -> None:
        if bool(id) == bool(name):
            raise InvalidUsageError("RoleRequest requires exactly one of `id` or `name` to identify the recipient.")
        self.role = role
        self.share_recipient_type = share_recipient_type
        self.id = id
        self.name = name
        self.can_share = can_share
        self.can_use_data = can_use_data


class ModifyCatalogSharedRolePayload(APIObject, HumanReadable):
    """Payload used to modify the sharing roles on an entity.

    Attributes
    ----------
    operation : str
        The name of the action being taken. The only supported operation is ``updateRoles``.
    roles : list of RoleRequest
        A list of role-request entries (1-100 items).
    apply_grant_to_linked_objects : bool
        If ``True``, grant the user read access to any linked objects (e.g., ``DataSources`` and
        ``DataStores``) used by this entity. Defaults to ``False``.
    """

    _converter = t.Dict({
        t.Key("operation", default="updateRoles"): t.Enum("updateRoles"),
        t.Key("roles"): t.List(CatalogSharedRoleRequest._converter, min_length=1, max_length=100),
        t.Key("apply_grant_to_linked_objects", optional=True, default=False): t.Bool,
    }).ignore_extra("*")

    def __init__(
        self,
        roles: List[CatalogSharedRoleRequest],
        operation: str = "updateRoles",
        apply_grant_to_linked_objects: bool = False,
    ) -> None:
        self.operation = operation
        self.roles = roles
        self.apply_grant_to_linked_objects = apply_grant_to_linked_objects
