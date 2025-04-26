r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VdiOnSanNewIgroups", "VdiOnSanNewIgroupsSchema"]
__pdoc__ = {
    "VdiOnSanNewIgroupsSchema.resource": False,
    "VdiOnSanNewIgroupsSchema.opts": False,
    "VdiOnSanNewIgroups": False,
}


class VdiOnSanNewIgroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VdiOnSanNewIgroups object"""

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A comment available for use by the administrator. """

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_new_igroups_igroups.MongoDbOnSanNewIgroupsIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" The igroups field of the vdi_on_san_new_igroups. """

    initiator_objects = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_new_igroups_initiator_objects.MongoDbOnSanNewIgroupsInitiatorObjectsSchema", unknown=EXCLUDE, allow_none=True), data_key="initiator_objects", allow_none=True)
    r""" The initiator_objects field of the vdi_on_san_new_igroups. """

    initiators = marshmallow_fields.List(marshmallow_fields.Str, data_key="initiators", allow_none=True)
    r""" The initiators field of the vdi_on_san_new_igroups. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the new initiator group. """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" The protocol of the new initiator group.

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return VdiOnSanNewIgroups

    gettable_fields = [
        "initiators",
    ]
    """initiators,"""

    patchable_fields = [
        "comment",
        "igroups",
        "initiator_objects",
        "initiators",
        "name",
        "protocol",
    ]
    """comment,igroups,initiator_objects,initiators,name,protocol,"""

    postable_fields = [
        "comment",
        "igroups",
        "initiator_objects",
        "initiators",
        "name",
        "protocol",
    ]
    """comment,igroups,initiator_objects,initiators,name,protocol,"""


class VdiOnSanNewIgroups(Resource):

    _schema = VdiOnSanNewIgroupsSchema
