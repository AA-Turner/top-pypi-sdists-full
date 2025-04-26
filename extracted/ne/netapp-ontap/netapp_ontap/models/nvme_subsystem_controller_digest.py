r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemControllerDigest", "NvmeSubsystemControllerDigestSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerDigestSchema.resource": False,
    "NvmeSubsystemControllerDigestSchema.opts": False,
    "NvmeSubsystemControllerDigest": False,
}


class NvmeSubsystemControllerDigestSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemControllerDigest object"""

    data = marshmallow_fields.Boolean(data_key="data", allow_none=True)
    r""" Reports if digests are enabled for the data portion of the PDU. """

    header = marshmallow_fields.Boolean(data_key="header", allow_none=True)
    r""" Reports if digests are enabled for the header portion of the PDU. """

    @property
    def resource(self):
        return NvmeSubsystemControllerDigest

    gettable_fields = [
        "data",
        "header",
    ]
    """data,header,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeSubsystemControllerDigest(Resource):

    _schema = NvmeSubsystemControllerDigestSchema
