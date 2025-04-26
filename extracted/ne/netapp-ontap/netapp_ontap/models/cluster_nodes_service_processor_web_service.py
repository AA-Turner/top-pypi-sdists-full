r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesServiceProcessorWebService", "ClusterNodesServiceProcessorWebServiceSchema"]
__pdoc__ = {
    "ClusterNodesServiceProcessorWebServiceSchema.resource": False,
    "ClusterNodesServiceProcessorWebServiceSchema.opts": False,
    "ClusterNodesServiceProcessorWebService": False,
}


class ClusterNodesServiceProcessorWebServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesServiceProcessorWebService object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the web service of the SP or BMC is enabled or disabled. When the web service is disabled, features such as network-based firmware updates and network-based down node log collection are not available, and the slower serial-interface is used for firmware updates and down node log collection. """

    limit_access = marshmallow_fields.Boolean(data_key="limit_access", allow_none=True)
    r""" Restricts web service access to cluster nodes only. By default, limit_access is set to true. """

    @property
    def resource(self):
        return ClusterNodesServiceProcessorWebService

    gettable_fields = [
        "enabled",
        "limit_access",
    ]
    """enabled,limit_access,"""

    patchable_fields = [
        "enabled",
        "limit_access",
    ]
    """enabled,limit_access,"""

    postable_fields = [
        "enabled",
        "limit_access",
    ]
    """enabled,limit_access,"""


class ClusterNodesServiceProcessorWebService(Resource):

    _schema = ClusterNodesServiceProcessorWebServiceSchema
