r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsFilterResponseRecords", "EmsFilterResponseRecordsSchema"]
__pdoc__ = {
    "EmsFilterResponseRecordsSchema.resource": False,
    "EmsFilterResponseRecordsSchema.opts": False,
    "EmsFilterResponseRecords": False,
}


class EmsFilterResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsFilterResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_filter_response_records. """

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", unknown=EXCLUDE, data_key="access_control_role", allow_none=True)
    r""" The access_control_role field of the ems_filter_response_records. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Filter name

Example: wafl-critical-events """

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.ems_filter_rule.EmsFilterRuleSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Array of event filter rules on which to match. """

    system_defined = marshmallow_fields.Boolean(data_key="system_defined", allow_none=True)
    r""" Flag indicating system-defined filters.

Example: true """

    @property
    def resource(self):
        return EmsFilterResponseRecords

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "name",
        "rules",
        "system_defined",
    ]
    """links,access_control_role.links,access_control_role.name,name,rules,system_defined,"""

    patchable_fields = [
        "rules",
    ]
    """rules,"""

    postable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""


class EmsFilterResponseRecords(Resource):

    _schema = EmsFilterResponseRecordsSchema
