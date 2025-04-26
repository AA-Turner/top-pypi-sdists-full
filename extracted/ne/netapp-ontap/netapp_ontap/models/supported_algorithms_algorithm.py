r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SupportedAlgorithmsAlgorithm", "SupportedAlgorithmsAlgorithmSchema"]
__pdoc__ = {
    "SupportedAlgorithmsAlgorithmSchema.resource": False,
    "SupportedAlgorithmsAlgorithmSchema.opts": False,
    "SupportedAlgorithmsAlgorithm": False,
}


class SupportedAlgorithmsAlgorithmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SupportedAlgorithmsAlgorithm object"""

    id = Size(data_key="id", allow_none=True)
    r""" Algorithm ID.

Example: -7 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Algorithm name.

Example: ES-256 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Algorithm type.

Valid choices:

* public_key """

    @property
    def resource(self):
        return SupportedAlgorithmsAlgorithm

    gettable_fields = [
        "id",
        "name",
        "type",
    ]
    """id,name,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SupportedAlgorithmsAlgorithm(Resource):

    _schema = SupportedAlgorithmsAlgorithmSchema
