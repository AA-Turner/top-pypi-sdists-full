r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VsiOnSan", "VsiOnSanSchema"]
__pdoc__ = {
    "VsiOnSanSchema.resource": False,
    "VsiOnSanSchema.opts": False,
    "VsiOnSan": False,
}


class VsiOnSanSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VsiOnSan object"""

    datastore = marshmallow_fields.Nested("netapp_ontap.models.vsi_on_nas_datastore.VsiOnNasDatastoreSchema", unknown=EXCLUDE, data_key="datastore", allow_none=True)
    r""" The datastore field of the vsi_on_san. """

    hypervisor = marshmallow_fields.Str(data_key="hypervisor", allow_none=True)
    r""" The name of the hypervisor hosting the application.

Valid choices:

* hyper_v
* vmware
* xen """

    igroup_name = marshmallow_fields.Str(data_key="igroup_name", allow_none=True)
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. """

    new_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.vsi_on_san_new_igroups.VsiOnSanNewIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="new_igroups", allow_none=True)
    r""" The list of initiator groups to create. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the vsi_on_san. """

    @property
    def resource(self):
        return VsiOnSan

    gettable_fields = [
        "datastore",
        "hypervisor",
        "igroup_name",
        "protection_type",
    ]
    """datastore,hypervisor,igroup_name,protection_type,"""

    patchable_fields = [
        "datastore",
        "igroup_name",
        "new_igroups",
        "protection_type",
    ]
    """datastore,igroup_name,new_igroups,protection_type,"""

    postable_fields = [
        "datastore",
        "hypervisor",
        "igroup_name",
        "new_igroups",
        "protection_type",
    ]
    """datastore,hypervisor,igroup_name,new_igroups,protection_type,"""


class VsiOnSan(Resource):

    _schema = VsiOnSanSchema
