r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunLunMaps", "LunLunMapsSchema"]
__pdoc__ = {
    "LunLunMapsSchema.resource": False,
    "LunLunMapsSchema.opts": False,
    "LunLunMaps": False,
}


class LunLunMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunLunMaps object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_lun_maps. """

    igroup = marshmallow_fields.Nested("netapp_ontap.models.lun_lun_maps_igroup.LunLunMapsIgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The initiator group to which the LUN is mapped. """

    logical_unit_number = Size(data_key="logical_unit_number", allow_none=True)
    r""" The logical unit number assigned to the LUN when mapped to the specified initiator group. The number is used to identify the LUN to initiators in the initiator group when communicating through the Fibre Channel Protocol or iSCSI. Optional in POST; if no value is provided, ONTAP assigns the lowest available value. This property is not supported when the _provisioning_options.count_ property is 2 or more. """

    @property
    def resource(self):
        return LunLunMaps

    gettable_fields = [
        "links",
        "igroup",
        "logical_unit_number",
    ]
    """links,igroup,logical_unit_number,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "igroup",
        "logical_unit_number",
    ]
    """igroup,logical_unit_number,"""


class LunLunMaps(Resource):

    _schema = LunLunMapsSchema
