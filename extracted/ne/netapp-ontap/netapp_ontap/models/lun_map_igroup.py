r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMapIgroup", "LunMapIgroupSchema"]
__pdoc__ = {
    "LunMapIgroupSchema.resource": False,
    "LunMapIgroupSchema.opts": False,
    "LunMapIgroup": False,
}


class LunMapIgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMapIgroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_map_igroup. """

    initiators = marshmallow_fields.List(marshmallow_fields.Str, data_key="initiators", allow_none=True)
    r""" The initiators that are members of the initiator group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group. Valid in POST.


Example: igroup1 """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system.


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
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group.


Valid choices:

* fcp
* iscsi
* mixed """

    replicated = marshmallow_fields.Boolean(data_key="replicated", allow_none=True)
    r""" This property reports if the initiator group is replicated. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group. Valid in POST.


Example: 1ad8544d-8cd1-91e0-9e1c-723478563412 """

    @property
    def resource(self):
        return LunMapIgroup

    gettable_fields = [
        "links",
        "initiators",
        "name",
        "os_type",
        "protocol",
        "replicated",
        "uuid",
    ]
    """links,initiators,name,os_type,protocol,replicated,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class LunMapIgroup(Resource):

    _schema = LunMapIgroupSchema
