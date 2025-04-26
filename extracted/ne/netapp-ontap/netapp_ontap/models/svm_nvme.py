r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmNvme", "SvmNvmeSchema"]
__pdoc__ = {
    "SvmNvmeSchema.resource": False,
    "SvmNvmeSchema.opts": False,
    "SvmNvme": False,
}


class SvmNvmeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmNvme object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_nvme. """

    allowed = marshmallow_fields.Boolean(data_key="allowed", allow_none=True)
    r""" If this is set to true, an SVM administrator can manage the NVMe service. If it is false, only the cluster administrator can manage the service. """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" If allowed, setting to true enables the NVMe service. """

    @property
    def resource(self):
        return SvmNvme

    gettable_fields = [
        "links",
        "allowed",
        "enabled",
    ]
    """links,allowed,enabled,"""

    patchable_fields = [
        "allowed",
    ]
    """allowed,"""

    postable_fields = [
        "allowed",
        "enabled",
    ]
    """allowed,enabled,"""


class SvmNvme(Resource):

    _schema = SvmNvmeSchema
