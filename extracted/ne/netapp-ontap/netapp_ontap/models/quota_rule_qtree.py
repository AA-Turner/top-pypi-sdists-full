r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QuotaRuleQtree", "QuotaRuleQtreeSchema"]
__pdoc__ = {
    "QuotaRuleQtreeSchema.resource": False,
    "QuotaRuleQtreeSchema.opts": False,
    "QuotaRuleQtree": False,
}


class QuotaRuleQtreeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QuotaRuleQtree object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the quota_rule_qtree. """

    id = Size(data_key="id", allow_none=True)
    r""" The unique identifier for a qtree.

Example: 1 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the qtree.

Example: qt1 """

    @property
    def resource(self):
        return QuotaRuleQtree

    gettable_fields = [
        "links",
        "id",
        "name",
    ]
    """links,id,name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class QuotaRuleQtree(Resource):

    _schema = QuotaRuleQtreeSchema
