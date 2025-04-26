r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupIgroup", "ConsistencyGroupIgroupSchema"]
__pdoc__ = {
    "ConsistencyGroupIgroupSchema.resource": False,
    "ConsistencyGroupIgroupSchema.opts": False,
    "ConsistencyGroupIgroup": False,
}


class ConsistencyGroupIgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupIgroup object"""

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. Valid in POST and PATCH. """

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_child_luns_lun_maps_igroup_igroups.ConsistencyGroupChildLunsLunMapsIgroupIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" The existing initiator groups that are members of the group. Optional in POST.<br/>
This property is mutually exclusive with the _initiators_ property during POST.<br/>
This array contains only the direct children of the initiator group. If the member initiator groups have further nested initiator groups, those are reported in the `igroups` property of the child initiator group.<br/>
Zero or more nested initiator groups can be supplied when the initiator group is created. The initiator group will act as if it contains the aggregation of all initiators in any nested initiator groups.<br/>
After creation, nested initiator groups can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/igroups` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/igroups`](#/SAN/igroup_nested_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/igroups/{uuid}`](#/SAN/igroup_nested_delete) for more details. """

    initiators = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_child_luns_lun_maps_igroup_initiators.ConsistencyGroupChildLunsLunMapsIgroupInitiatorsSchema", unknown=EXCLUDE, allow_none=True), data_key="initiators", allow_none=True)
    r""" The initiators that are members of the group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group. Required in POST; optional in PATCH.


Example: igroup1 """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/>
The protocol of an initiator group cannot be changed after creation of the group.


Valid choices:

* fcp
* iscsi
* mixed """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupIgroup

    gettable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
        "protocol",
        "uuid",
    ]
    """comment,igroups,initiators,name,os_type,protocol,uuid,"""

    patchable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
    ]
    """comment,igroups,initiators,name,os_type,"""

    postable_fields = [
        "comment",
        "igroups",
        "initiators",
        "name",
        "os_type",
        "protocol",
    ]
    """comment,igroups,initiators,name,os_type,protocol,"""


class ConsistencyGroupIgroup(Resource):

    _schema = ConsistencyGroupIgroupSchema
