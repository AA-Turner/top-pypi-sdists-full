r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesServiceProcessorApiService", "ClusterNodesServiceProcessorApiServiceSchema"]
__pdoc__ = {
    "ClusterNodesServiceProcessorApiServiceSchema.resource": False,
    "ClusterNodesServiceProcessorApiServiceSchema.opts": False,
    "ClusterNodesServiceProcessorApiService": False,
}


class ClusterNodesServiceProcessorApiServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesServiceProcessorApiService object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the SP API service of the SP or BMC is enabled or disabled. When the SP API service is disabled, features such as network-based firmware updates and network-based down node log collection are not available, and the slower serial-interface is used for firmware updates and down node log collection. """

    limit_access = marshmallow_fields.Boolean(data_key="limit_access", allow_none=True)
    r""" Restricts SP API service access to cluster nodes only. By default, limit_access is set to true. """

    port = Size(data_key="port", allow_none=True)
    r""" Specifies the port number on the SP or BMC used for the SP API service. By default, port 50000 is used. """

    @property
    def resource(self):
        return ClusterNodesServiceProcessorApiService

    gettable_fields = [
        "enabled",
        "limit_access",
        "port",
    ]
    """enabled,limit_access,port,"""

    patchable_fields = [
        "enabled",
        "limit_access",
        "port",
    ]
    """enabled,limit_access,port,"""

    postable_fields = [
        "enabled",
        "limit_access",
        "port",
    ]
    """enabled,limit_access,port,"""


class ClusterNodesServiceProcessorApiService(Resource):

    _schema = ClusterNodesServiceProcessorApiServiceSchema
