r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnaplockFileFingerprintGet", "SnaplockFileFingerprintGetSchema"]
__pdoc__ = {
    "SnaplockFileFingerprintGetSchema.resource": False,
    "SnaplockFileFingerprintGetSchema.opts": False,
    "SnaplockFileFingerprintGet": False,
}


class SnaplockFileFingerprintGetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockFileFingerprintGet object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snaplock_file_fingerprint_get. """

    id = Size(data_key="id", allow_none=True)
    r""" A unique identifier for the fingerprint operation.

Example: 17039367 """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the snaplock_file_fingerprint_get. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the snaplock_file_fingerprint_get. """

    @property
    def resource(self):
        return SnaplockFileFingerprintGet

    gettable_fields = [
        "links",
        "id",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,id,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """svm.name,svm.uuid,volume.name,volume.uuid,"""


class SnaplockFileFingerprintGet(Resource):

    _schema = SnaplockFileFingerprintGetSchema
