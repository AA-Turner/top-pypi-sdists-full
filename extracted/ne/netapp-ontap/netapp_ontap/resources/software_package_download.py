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


__all__ = ["SoftwarePackageDownload", "SoftwarePackageDownloadSchema"]
__pdoc__ = {
    "SoftwarePackageDownloadSchema.resource": False,
    "SoftwarePackageDownloadSchema.opts": False,
}


class SoftwarePackageDownloadSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwarePackageDownload object"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Password for download

Example: admin_password"""

    url = marshmallow_fields.Str(
        data_key="url",
        allow_none=True,
    )
    r""" HTTP or FTP URL of the package through a server

Example: http://server/package"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" Username for download

Example: admin"""

    @property
    def resource(self):
        return SoftwarePackageDownload

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "password",
        "url",
        "username",
    ]
    """password,url,username,"""

class SoftwarePackageDownload(Resource):
    """Allows interaction with SoftwarePackageDownload objects on the host"""

    _schema = SoftwarePackageDownloadSchema
    _path = "/api/cluster/software/download"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the software or firmware download status.
### Related ONTAP commands
* `cluster image package check-download-progress`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
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
        r"""Downloads a software or firmware package from the server.
### Required properties
* `url` - URL location of the software package
### Recommended optional parameters
* `username` - Username of HTTPS/FTP server
* `password` - Password of HTTPS/FTP server
### Related ONTAP commands
* `cluster image package get`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




