r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunConvert", "LunConvertSchema"]
__pdoc__ = {
    "LunConvertSchema.resource": False,
    "LunConvertSchema.opts": False,
    "LunConvert": False,
}


class LunConvertSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunConvert object"""

    namespace = marshmallow_fields.Nested("netapp_ontap.models.lun_convert_namespace.LunConvertNamespaceSchema", unknown=EXCLUDE, data_key="namespace", allow_none=True)
    r""" The source namespace for convert operation. This can be specified using property `convert.namespace.uuid` or `convert.namespace.name`. If both properties are supplied, they must refer to the same NVMe namespace.<br/>
Valid in POST. A convert request from NVMe namespace to LUN cannot be combined with setting any other LUN properties. All other properties of the converted LUN come from the source NVMe namespace.<br/> """

    @property
    def resource(self):
        return LunConvert

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "namespace",
    ]
    """namespace,"""


class LunConvert(Resource):

    _schema = LunConvertSchema
