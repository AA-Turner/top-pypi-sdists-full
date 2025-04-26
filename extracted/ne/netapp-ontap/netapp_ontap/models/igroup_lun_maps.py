r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupLunMaps", "IgroupLunMapsSchema"]
__pdoc__ = {
    "IgroupLunMapsSchema.resource": False,
    "IgroupLunMapsSchema.opts": False,
    "IgroupLunMaps": False,
}


class IgroupLunMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupLunMaps object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_lun_maps. """

    logical_unit_number = Size(data_key="logical_unit_number", allow_none=True)
    r""" The logical unit number assigned to the LUN for initiators in the initiator group. """

    lun = marshmallow_fields.Nested("netapp_ontap.models.igroup_lun_maps_lun.IgroupLunMapsLunSchema", unknown=EXCLUDE, data_key="lun", allow_none=True)
    r""" The LUN to which the initiator group is mapped. """

    @property
    def resource(self):
        return IgroupLunMaps

    gettable_fields = [
        "links",
        "logical_unit_number",
        "lun",
    ]
    """links,logical_unit_number,lun,"""

    patchable_fields = [
        "lun",
    ]
    """lun,"""

    postable_fields = [
        "lun",
    ]
    """lun,"""


class IgroupLunMaps(Resource):

    _schema = IgroupLunMapsSchema
