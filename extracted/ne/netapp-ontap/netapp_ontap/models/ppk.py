r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Ppk", "PpkSchema"]
__pdoc__ = {
    "PpkSchema.resource": False,
    "PpkSchema.opts": False,
    "Ppk": False,
}


class PpkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Ppk object"""

    identity = marshmallow_fields.Str(data_key="identity", allow_none=True)
    r""" Post-quantum pre-shared key identity. """

    shared_key = marshmallow_fields.Str(data_key="shared_key", allow_none=True)
    r""" Post-quantum pre-shared key. """

    @property
    def resource(self):
        return Ppk

    gettable_fields = [
        "identity",
    ]
    """identity,"""

    patchable_fields = [
        "identity",
    ]
    """identity,"""

    postable_fields = [
        "identity",
        "shared_key",
    ]
    """identity,shared_key,"""


class Ppk(Resource):

    _schema = PpkSchema
