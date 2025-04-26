r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VsiOnNas", "VsiOnNasSchema"]
__pdoc__ = {
    "VsiOnNasSchema.resource": False,
    "VsiOnNasSchema.opts": False,
    "VsiOnNas": False,
}


class VsiOnNasSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VsiOnNas object"""

    datastore = marshmallow_fields.Nested("netapp_ontap.models.vsi_on_nas_datastore.VsiOnNasDatastoreSchema", unknown=EXCLUDE, data_key="datastore", allow_none=True)
    r""" The datastore field of the vsi_on_nas. """

    hyper_v_access = marshmallow_fields.Nested("netapp_ontap.models.vdi_on_nas_hyper_v_access.VdiOnNasHyperVAccessSchema", unknown=EXCLUDE, data_key="hyper_v_access", allow_none=True)
    r""" The hyper_v_access field of the vsi_on_nas. """

    nfs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.app_nfs_access.AppNfsAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="nfs_access", allow_none=True)
    r""" The list of NFS access controls. You must provide either 'host' or 'access' to enable NFS access. """

    protection_type = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san_protection_type.MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE, data_key="protection_type", allow_none=True)
    r""" The protection_type field of the vsi_on_nas. """

    @property
    def resource(self):
        return VsiOnNas

    gettable_fields = [
        "datastore",
        "hyper_v_access",
        "nfs_access",
        "protection_type",
    ]
    """datastore,hyper_v_access,nfs_access,protection_type,"""

    patchable_fields = [
        "datastore",
        "protection_type",
    ]
    """datastore,protection_type,"""

    postable_fields = [
        "datastore",
        "hyper_v_access",
        "nfs_access",
        "protection_type",
    ]
    """datastore,hyper_v_access,nfs_access,protection_type,"""


class VsiOnNas(Resource):

    _schema = VsiOnNasSchema
