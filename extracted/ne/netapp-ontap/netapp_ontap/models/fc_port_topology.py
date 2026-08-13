r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FcPortTopology", "FcPortTopologySchema"]
__pdoc__ = {
    "FcPortTopologySchema.resource": False,
    "FcPortTopologySchema.opts": False,
    "FcPortTopology": False,
}

class FcPortTopologySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcPortTopology object"""

    configured = marshmallow_fields.Str(data_key="configured", allow_none=True)
    r""" The configured topology of the FC port.


Valid choices:

* direct
* fabric """

    supported = marshmallow_fields.List(marshmallow_fields.Str, data_key="supported", allow_none=True)
    r""" The supported topologies of the FC port. """

    @property
    def resource(self):
        return FcPortTopology

    gettable_fields = [
        "configured",
        "supported",
    ]
    """configured,supported,"""

    patchable_fields = [
        "configured",
    ]
    """configured,"""

    postable_fields = [
    ]
    """"""


class FcPortTopology(Resource):

    _schema = FcPortTopologySchema
