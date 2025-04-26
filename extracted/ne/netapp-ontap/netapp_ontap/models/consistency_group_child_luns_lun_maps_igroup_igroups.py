r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupChildLunsLunMapsIgroupIgroups", "ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema"]
__pdoc__ = {
    "ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema.resource": False,
    "ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema.opts": False,
    "ConsistencyGroupChildLunsLunMapsIgroupIgroups": False,
}


class ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupChildLunsLunMapsIgroupIgroups object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_child_luns_lun_maps_igroup_igroups. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group.


Example: igroup1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupChildLunsLunMapsIgroupIgroups

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ConsistencyGroupChildLunsLunMapsIgroupIgroups(Resource):

    _schema = ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema
