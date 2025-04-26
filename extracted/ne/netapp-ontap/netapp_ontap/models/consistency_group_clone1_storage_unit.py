r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupClone1StorageUnit", "ConsistencyGroupClone1StorageUnitSchema"]
__pdoc__ = {
    "ConsistencyGroupClone1StorageUnitSchema.resource": False,
    "ConsistencyGroupClone1StorageUnitSchema.opts": False,
    "ConsistencyGroupClone1StorageUnit": False,
}


class ConsistencyGroupClone1StorageUnitSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupClone1StorageUnit object"""

    prefix = marshmallow_fields.Str(data_key="prefix", allow_none=True)
    r""" Storage unit name prefix for cloned volume blocks. """

    suffix = marshmallow_fields.Str(data_key="suffix", allow_none=True)
    r""" Storage unit name suffix for cloned volume blocks. """

    @property
    def resource(self):
        return ConsistencyGroupClone1StorageUnit

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


class ConsistencyGroupClone1StorageUnit(Resource):

    _schema = ConsistencyGroupClone1StorageUnitSchema
