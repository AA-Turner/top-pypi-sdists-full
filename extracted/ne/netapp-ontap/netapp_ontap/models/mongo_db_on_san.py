r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MongoDbOnSan", "MongoDbOnSanSchema"]
__pdoc__ = {
    "MongoDbOnSanSchema.resource": False,
    "MongoDbOnSanSchema.opts": False,
    "MongoDbOnSan": False,
}


class MongoDbOnSanSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MongoDbOnSan object"""

    dataset = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_dataset.MongoDbOnSanDatasetSchema", unknown=EXCLUDE, data_key="dataset", allow_none=True)
    r""" The dataset field of the mongo_db_on_san. """

    new_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_new_igroups.MongoDbOnSanNewIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="new_igroups", allow_none=True)
    r""" The list of initiator groups to create. """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The name of the host OS running the application.

Valid choices:

* hyper_v
* linux
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen """

    primary_igroup_name = marshmallow_fields.Str(data_key="primary_igroup_name", allow_none=True)
    r""" The initiator group for the primary. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the mongo_db_on_san. """

    secondary_igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_secondary_igroups.MongoDbOnSanSecondaryIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="secondary_igroups", allow_none=True)
    r""" The secondary_igroups field of the mongo_db_on_san. """

    @property
    def resource(self):
        return MongoDbOnSan

    gettable_fields = [
        "dataset",
        "os_type",
        "primary_igroup_name",
        "protection_type",
        "secondary_igroups",
    ]
    """dataset,os_type,primary_igroup_name,protection_type,secondary_igroups,"""

    patchable_fields = [
        "dataset",
        "new_igroups",
        "primary_igroup_name",
        "protection_type",
        "secondary_igroups",
    ]
    """dataset,new_igroups,primary_igroup_name,protection_type,secondary_igroups,"""

    postable_fields = [
        "dataset",
        "new_igroups",
        "os_type",
        "primary_igroup_name",
        "protection_type",
        "secondary_igroups",
    ]
    """dataset,new_igroups,os_type,primary_igroup_name,protection_type,secondary_igroups,"""


class MongoDbOnSan(Resource):

    _schema = MongoDbOnSanSchema
