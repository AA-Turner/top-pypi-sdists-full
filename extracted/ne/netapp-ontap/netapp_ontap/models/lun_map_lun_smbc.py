r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMapLunSmbc", "LunMapLunSmbcSchema"]
__pdoc__ = {
    "LunMapLunSmbcSchema.resource": False,
    "LunMapLunSmbcSchema.opts": False,
    "LunMapLunSmbc": False,
}


class LunMapLunSmbcSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMapLunSmbc object"""

    replicated = marshmallow_fields.Boolean(data_key="replicated", allow_none=True)
    r""" This property reports if the LUN is replicated via SM-BC. """

    @property
    def resource(self):
        return LunMapLunSmbc

    gettable_fields = [
        "replicated",
    ]
    """replicated,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LunMapLunSmbc(Resource):

    _schema = LunMapLunSmbcSchema
