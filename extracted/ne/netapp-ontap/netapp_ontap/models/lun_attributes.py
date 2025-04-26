r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunAttributes", "LunAttributesSchema"]
__pdoc__ = {
    "LunAttributesSchema.resource": False,
    "LunAttributesSchema.opts": False,
    "LunAttributes": False,
}


class LunAttributesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunAttributes object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_attributes. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The attribute name.


Example: name1 """

    value = marshmallow_fields.Str(data_key="value", allow_none=True)
    r""" The attribute value.


Example: value1 """

    @property
    def resource(self):
        return LunAttributes

    gettable_fields = [
        "links",
        "name",
        "value",
    ]
    """links,name,value,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "value",
    ]
    """name,value,"""


class LunAttributes(Resource):

    _schema = LunAttributesSchema
