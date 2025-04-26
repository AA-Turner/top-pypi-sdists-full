r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KeyServerState", "KeyServerStateSchema"]
__pdoc__ = {
    "KeyServerStateSchema.resource": False,
    "KeyServerStateSchema.opts": False,
    "KeyServerState": False,
}


class KeyServerStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServerState object"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the key_server_state. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Key server connectivity state

Valid choices:

* available
* not_responding
* unknown """

    @property
    def resource(self):
        return KeyServerState

    gettable_fields = [
        "node.links",
        "node.name",
        "node.uuid",
        "state",
    ]
    """node.links,node.name,node.uuid,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class KeyServerState(Resource):

    _schema = KeyServerStateSchema
