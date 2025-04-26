r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunCopy", "LunCopySchema"]
__pdoc__ = {
    "LunCopySchema.resource": False,
    "LunCopySchema.opts": False,
    "LunCopy": False,
}


class LunCopySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunCopy object"""

    destinations = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.lun_copy_destinations.LunCopyDestinationsSchema", unknown=EXCLUDE, allow_none=True), data_key="destinations", allow_none=True)
    r""" An array of destination LUNs of LUN copy operations in which the containing LUN is the source of the copy. """

    source = marshmallow_fields.Nested("netapp_ontap.models.lun_copy_source.LunCopySourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source LUN of a LUN copy operation in which the containing LUN is the destination of the copy.<br/>
Valid in POST except when creating a LUN clone. A LUN copy request cannot be combined with setting any other LUN properties except the destination location. All other properties of the destination LUN come from the source LUN. """

    @property
    def resource(self):
        return LunCopy

    gettable_fields = [
        "destinations",
        "source",
    ]
    """destinations,source,"""

    patchable_fields = [
        "source",
    ]
    """source,"""

    postable_fields = [
        "source",
    ]
    """source,"""


class LunCopy(Resource):

    _schema = LunCopySchema
