r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesHaInterconnect", "ClusterNodesHaInterconnectSchema"]
__pdoc__ = {
    "ClusterNodesHaInterconnectSchema.resource": False,
    "ClusterNodesHaInterconnectSchema.opts": False,
    "ClusterNodesHaInterconnect": False,
}


class ClusterNodesHaInterconnectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaInterconnect object"""

    adapter = marshmallow_fields.Str(data_key="adapter", allow_none=True)
    r""" HA interconnect device name.

Example: MVIA-RDMA """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Indicates the HA interconnect status.

Valid choices:

* down
* up """

    @property
    def resource(self):
        return ClusterNodesHaInterconnect

    gettable_fields = [
        "adapter",
        "state",
    ]
    """adapter,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesHaInterconnect(Resource):

    _schema = ClusterNodesHaInterconnectSchema
