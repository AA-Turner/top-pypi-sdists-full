r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionVersionDiffVersion", "DatacollectionVersionDiffVersionSchema"]
__pdoc__ = {
    "DatacollectionVersionDiffVersionSchema.resource": False,
    "DatacollectionVersionDiffVersionSchema.opts": False,
    "DatacollectionVersionDiffVersion": False,
}

class DatacollectionVersionDiffVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionVersionDiffVersion object"""

    base = marshmallow_fields.Str(data_key="base", allow_none=True)
    r""" The unique identifier of the base version.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the version.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DatacollectionVersionDiffVersion

    gettable_fields = [
        "base",
        "uuid",
    ]
    """base,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "base",
    ]
    """base,"""


class DatacollectionVersionDiffVersion(Resource):

    _schema = DatacollectionVersionDiffVersionSchema
