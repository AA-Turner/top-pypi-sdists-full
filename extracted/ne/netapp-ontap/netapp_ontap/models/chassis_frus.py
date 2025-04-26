r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ChassisFrus", "ChassisFrusSchema"]
__pdoc__ = {
    "ChassisFrusSchema.resource": False,
    "ChassisFrusSchema.opts": False,
    "ChassisFrus": False,
}


class ChassisFrusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ChassisFrus object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" The id field of the chassis_frus. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the chassis_frus.

Valid choices:

* ok
* error """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the chassis_frus.

Valid choices:

* fan
* psu """

    @property
    def resource(self):
        return ChassisFrus

    gettable_fields = [
        "id",
        "state",
        "type",
    ]
    """id,state,type,"""

    patchable_fields = [
        "id",
        "state",
        "type",
    ]
    """id,state,type,"""

    postable_fields = [
        "id",
        "state",
        "type",
    ]
    """id,state,type,"""


class ChassisFrus(Resource):

    _schema = ChassisFrusSchema
