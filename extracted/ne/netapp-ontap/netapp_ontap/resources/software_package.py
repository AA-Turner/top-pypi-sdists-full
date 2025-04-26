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


__all__ = ["SoftwarePackage", "SoftwarePackageSchema"]
__pdoc__ = {
    "SoftwarePackageSchema.resource": False,
    "SoftwarePackageSchema.opts": False,
}


class SoftwarePackageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwarePackage object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the software_package."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Indicates when this package was loaded

Example: 2019-02-04T19:00:00.000+0000"""

    version = marshmallow_fields.Str(
        data_key="version",
        allow_none=True,
    )
    r""" Version of this package

Example: ONTAP_X"""

    @property
    def resource(self):
        return SoftwarePackage

    gettable_fields = [
        "links",
        "create_time",
        "version",
    ]
    """links,create_time,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SoftwarePackage(Resource):
    """Allows interaction with SoftwarePackage objects on the host"""

    _schema = SoftwarePackageSchema
    _path = "/api/cluster/software/packages"
    _keys = ["version"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
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
        """Returns a count of all SoftwarePackage resources that match the provided query"""
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
        """Returns a list of RawResources that represent SoftwarePackage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SoftwarePackage"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the software package information.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


