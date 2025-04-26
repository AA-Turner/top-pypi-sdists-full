r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnaplockRetention", "ConsistencyGroupSnaplockRetentionSchema"]
__pdoc__ = {
    "ConsistencyGroupSnaplockRetentionSchema.resource": False,
    "ConsistencyGroupSnaplockRetentionSchema.opts": False,
    "ConsistencyGroupSnaplockRetention": False,
}


class ConsistencyGroupSnaplockRetentionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnaplockRetention object"""

    default = marshmallow_fields.Str(data_key="default", allow_none=True)
    r""" Specifies the default retention period that is applied to objects within a consistency group while committing them to the WORM state without an associated retention period.

Example: P6M """

    maximum = marshmallow_fields.Str(data_key="maximum", allow_none=True)
    r""" Specifies the maximum allowed retention period for objects committed to the WORM state on the consistency group.

Example: P30Y """

    minimum = marshmallow_fields.Str(data_key="minimum", allow_none=True)
    r""" Specifies the minimum allowed retention period for objects within a consistency group committed to the WORM state on the consistency group.

Example: P30Y """

    @property
    def resource(self):
        return ConsistencyGroupSnaplockRetention

    gettable_fields = [
        "default",
        "maximum",
        "minimum",
    ]
    """default,maximum,minimum,"""

    patchable_fields = [
        "default",
        "maximum",
        "minimum",
    ]
    """default,maximum,minimum,"""

    postable_fields = [
        "default",
        "maximum",
        "minimum",
    ]
    """default,maximum,minimum,"""


class ConsistencyGroupSnaplockRetention(Resource):

    _schema = ConsistencyGroupSnaplockRetentionSchema
