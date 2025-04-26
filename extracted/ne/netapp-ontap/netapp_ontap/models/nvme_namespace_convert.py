r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceConvert", "NvmeNamespaceConvertSchema"]
__pdoc__ = {
    "NvmeNamespaceConvertSchema.resource": False,
    "NvmeNamespaceConvertSchema.opts": False,
    "NvmeNamespaceConvert": False,
}


class NvmeNamespaceConvertSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespaceConvert object"""

    lun = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_convert_lun.NvmeNamespaceConvertLunSchema", unknown=EXCLUDE, data_key="lun", allow_none=True)
    r""" The source LUN for convert operation. This can be specified using property `convert.lun.uuid` or `convert.lun.name`. If both properties are supplied, they must refer to the same LUN.<br/>
Valid in POST. A convert request from LUN to NVMe namespace cannot be combined with setting any other namespace properties. All other properties of the converted NVMe namespace come from the source LUN.<br/> """

    @property
    def resource(self):
        return NvmeNamespaceConvert

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "lun",
    ]
    """lun,"""


class NvmeNamespaceConvert(Resource):

    _schema = NvmeNamespaceConvertSchema
