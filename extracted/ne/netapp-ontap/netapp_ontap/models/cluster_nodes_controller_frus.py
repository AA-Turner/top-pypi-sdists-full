r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesControllerFrus", "ClusterNodesControllerFrusSchema"]
__pdoc__ = {
    "ClusterNodesControllerFrusSchema.resource": False,
    "ClusterNodesControllerFrusSchema.opts": False,
    "ClusterNodesControllerFrus": False,
}


class ClusterNodesControllerFrusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesControllerFrus object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" The id field of the cluster_nodes_controller_frus. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_nodes_controller_frus.

Valid choices:

* ok
* error """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the cluster_nodes_controller_frus.

Valid choices:

* fan
* psu
* pcie
* disk
* nvs
* dimm
* controller """

    @property
    def resource(self):
        return ClusterNodesControllerFrus

    gettable_fields = [
        "id",
        "state",
        "type",
    ]
    """id,state,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesControllerFrus(Resource):

    _schema = ClusterNodesControllerFrusSchema
