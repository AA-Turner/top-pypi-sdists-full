r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupClone1Volume", "ConsistencyGroupClone1VolumeSchema"]
__pdoc__ = {
    "ConsistencyGroupClone1VolumeSchema.resource": False,
    "ConsistencyGroupClone1VolumeSchema.opts": False,
    "ConsistencyGroupClone1Volume": False,
}


class ConsistencyGroupClone1VolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupClone1Volume object"""

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" Volume name prefix for cloned volumes. """

    suffix = marshmallow_fields.Str(data_key="suffix", allow_none=True)
    r""" Volume name suffix for cloned volumes. """

    @property
    def resource(self):
        return ConsistencyGroupClone1Volume

    gettable_fields = [
        "prefix",
        "suffix",
    ]
    """prefix,suffix,"""

    patchable_fields = [
        "prefix",
        "suffix",
    ]
    """prefix,suffix,"""

    postable_fields = [
        "prefix",
        "suffix",
    ]
    """prefix,suffix,"""


class ConsistencyGroupClone1Volume(Resource):

    _schema = ConsistencyGroupClone1VolumeSchema
