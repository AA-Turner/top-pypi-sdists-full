r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupExportPolicy", "ConsistencyGroupExportPolicySchema"]
__pdoc__ = {
    "ConsistencyGroupExportPolicySchema.resource": False,
    "ConsistencyGroupExportPolicySchema.opts": False,
    "ConsistencyGroupExportPolicy": False,
}


class ConsistencyGroupExportPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupExportPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_export_policy. """

    id = Size(data_key="id", allow_none=True)
    r""" Identifier for the export policy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the export policy. """

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.export_rules.ExportRulesSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" The set of rules that govern the export policy. """

    @property
    def resource(self):
        return ConsistencyGroupExportPolicy

    gettable_fields = [
        "links",
        "id",
        "name",
        "rules",
    ]
    """links,id,name,rules,"""

    patchable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""

    postable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""


class ConsistencyGroupExportPolicy(Resource):

    _schema = ConsistencyGroupExportPolicySchema
