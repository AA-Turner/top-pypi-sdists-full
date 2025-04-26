r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockLitigationGet", "SnaplockLitigationGetSchema"]
__pdoc__ = {
    "SnaplockLitigationGetSchema.resource": False,
    "SnaplockLitigationGetSchema.opts": False,
    "SnaplockLitigationGet": False,
}


class SnaplockLitigationGetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLitigationGet object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snaplock_litigation_get. """

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" Specifies the litigation ID. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the legal-hold litigation name.

Example: lit1 """

    operations = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snaplock_litigation_get_operations.SnaplockLitigationGetOperationsSchema", unknown=EXCLUDE, allow_none=True), data_key="operations", allow_none=True)
    r""" The operations field of the snaplock_litigation_get. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the snaplock_litigation_get. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the snaplock_litigation_get. """

    @property
    def resource(self):
        return SnaplockLitigationGet

    gettable_fields = [
        "links",
        "id",
        "name",
        "operations",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,id,name,operations,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class SnaplockLitigationGet(Resource):

    _schema = SnaplockLitigationGetSchema
