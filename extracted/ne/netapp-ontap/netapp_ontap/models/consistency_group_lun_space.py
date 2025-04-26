r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupLunSpace", "ConsistencyGroupLunSpaceSchema"]
__pdoc__ = {
    "ConsistencyGroupLunSpaceSchema.resource": False,
    "ConsistencyGroupLunSpaceSchema.opts": False,
    "ConsistencyGroupLunSpace": False,
}


class ConsistencyGroupLunSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupLunSpace object"""

    guarantee = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_lun_space_guarantee.ConsistencyGroupLunSpaceGuaranteeSchema", unknown=EXCLUDE, data_key="guarantee", allow_none=True)
    r""" Properties that request and report the space guarantee for the LUN. """

    size = Size(data_key="size", allow_none=True)
    r""" The total provisioned size of the LUN. The LUN size can be increased but not reduced using the REST interface.
The maximum and minimum sizes listed here are the absolute maximum and absolute minimum sizes, in bytes. The actual minimum and maximum sizes vary depending on the ONTAP version, ONTAP platform, and the available space in the containing volume and aggregate.
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation.


Example: 1073741824 """

    used = Size(data_key="used", allow_none=True)
    r""" The amount of space consumed by the main data stream of the LUN.<br/>
This value is the total space consumed in the volume by the LUN, including filesystem overhead, but excluding prefix and suffix streams. Due to internal filesystem overhead and the many ways SAN filesystems and applications utilize blocks within a LUN, this value does not necessarily reflect actual consumption/availability from the perspective of the filesystem or application. Without specific knowledge of how the LUN blocks are utilized outside of ONTAP, this property should not be used as an indicator for an out-of-space condition.<br/>
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation. """

    @property
    def resource(self):
        return ConsistencyGroupLunSpace

    gettable_fields = [
        "guarantee",
        "size",
        "used",
    ]
    """guarantee,size,used,"""

    patchable_fields = [
        "guarantee",
        "size",
    ]
    """guarantee,size,"""

    postable_fields = [
        "guarantee",
        "size",
    ]
    """guarantee,size,"""


class ConsistencyGroupLunSpace(Resource):

    _schema = ConsistencyGroupLunSpaceSchema
