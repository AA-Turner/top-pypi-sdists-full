r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KeyServerStateArray", "KeyServerStateArraySchema"]
__pdoc__ = {
    "KeyServerStateArraySchema.resource": False,
    "KeyServerStateArraySchema.opts": False,
    "KeyServerStateArray": False,
}


class KeyServerStateArraySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServerStateArray object"""

    cluster_availability = marshmallow_fields.Boolean(data_key="cluster_availability", allow_none=True)
    r""" Set to true when key server connectivity state is available on all nodes of the cluster. """

    node_states = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.key_server_state.KeyServerStateSchema", unknown=EXCLUDE, allow_none=True), data_key="node_states", allow_none=True)
    r""" An array of key server connectivity states for each node. """

    @property
    def resource(self):
        return KeyServerStateArray

    gettable_fields = [
        "cluster_availability",
        "node_states",
    ]
    """cluster_availability,node_states,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class KeyServerStateArray(Resource):

    _schema = KeyServerStateArraySchema
