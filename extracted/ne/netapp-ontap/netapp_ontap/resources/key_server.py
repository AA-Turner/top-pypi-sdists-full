r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["KeyServer", "KeyServerSchema"]
__pdoc__ = {
    "KeyServerSchema.resource": False,
    "KeyServerSchema.opts": False,
}


class KeyServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the key_server."""

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.key_server_state_array.KeyServerStateArraySchema", data_key="connectivity", unknown=EXCLUDE, allow_none=True)
    r""" A container for holding an array of the key server connectivity state for each node."""

    create_remove_timeout = Size(
        data_key="create_remove_timeout",
        validate=integer_validation(minimum=-1, maximum=60),
        allow_none=True,
    )
    r""" The key server timeout for create and remove operations.
-1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response.


Example: 60"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Password credentials for connecting with the key server. This is not audited.

Example: password"""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.key_server_no_records.KeyServerNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of key servers specified to add multiple key servers to a key manager in a single API call. Valid in POST only and not valid if `server` is provided."""

    secondary_key_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="secondary_key_servers", allow_none=True)
    r""" A list of the secondary key servers associated with the primary key server.

Example: ["secondary1.com","10.1.2.3"]"""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.

Example: keyserver1.com:5698"""

    timeout = Size(
        data_key="timeout",
        validate=integer_validation(minimum=-1, maximum=60),
        allow_none=True,
    )
    r""" I/O timeout in seconds for communicating with the key server.
-1 indicates that the server will wait indefinitely for the event to occur. 0 indicates that the server will not wait and will immediately timeout if it does not receive a response.


Example: 60"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" KMIP username credentials for connecting with the key server.

Example: username"""

    @property
    def resource(self):
        return KeyServer

    gettable_fields = [
        "links",
        "connectivity",
        "create_remove_timeout",
        "secondary_key_servers",
        "server",
        "timeout",
        "username",
    ]
    """links,connectivity,create_remove_timeout,secondary_key_servers,server,timeout,username,"""

    patchable_fields = [
        "create_remove_timeout",
        "password",
        "secondary_key_servers",
        "timeout",
        "username",
    ]
    """create_remove_timeout,password,secondary_key_servers,timeout,username,"""

    postable_fields = [
        "records",
        "server",
    ]
    """records,server,"""

class KeyServer(Resource):
    """Allows interaction with KeyServer objects on the host"""

    _schema = KeyServerSchema
    _path = "/api/security/key-managers/{security_key_manager[uuid]}/key-servers"
    _keys = ["security_key_manager.uuid", "server"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all KeyServer resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent KeyServer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["KeyServer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a primary key server.
### Related ONTAP commands
* `security key-manager external modify-server`
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["KeyServer"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["KeyServer"], NetAppResponse]:
        r"""Adds primary key servers to a configured external key manager.
### Required properties
* `uuid` - UUID of the external key manager.
* `server` - Primary Key server name.
### Related ONTAP commands
* `security key-manager external add-servers`
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["KeyServer"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a primary key server.
### Optional parameters:
* `force` - Bypass Out of Quorum checks when deleting a primary key server. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves key servers configured in an external key manager.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
### Related ONTAP commands
* `security key-manager external show`
* `security key-manager external show-status`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Adds primary key servers to a configured external key manager.
### Required properties
* `uuid` - UUID of the external key manager.
* `server` - Primary Key server name.
### Related ONTAP commands
* `security key-manager external add-servers`
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a primary key server.
### Related ONTAP commands
* `security key-manager external modify-server`
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a primary key server.
### Optional parameters:
* `force` - Bypass Out of Quorum checks when deleting a primary key server. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


