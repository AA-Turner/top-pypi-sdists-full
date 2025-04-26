r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsRoleConfigResponseRecords", "EmsRoleConfigResponseRecordsSchema"]
__pdoc__ = {
    "EmsRoleConfigResponseRecordsSchema.resource": False,
    "EmsRoleConfigResponseRecordsSchema.opts": False,
    "EmsRoleConfigResponseRecords": False,
}


class EmsRoleConfigResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsRoleConfigResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_role_config_response_records. """

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", unknown=EXCLUDE, data_key="access_control_role", allow_none=True)
    r""" The access_control_role field of the ems_role_config_response_records. """

    event_filter = marshmallow_fields.Nested("netapp_ontap.resources.ems_filter.EmsFilterSchema", unknown=EXCLUDE, data_key="event_filter", allow_none=True)
    r""" The event_filter field of the ems_role_config_response_records. """

    limit_access_to_global_configs = marshmallow_fields.Boolean(data_key="limit_access_to_global_configs", allow_none=True)
    r""" Indicates whether the access control has limited access to global EMS configurations. """

    @property
    def resource(self):
        return EmsRoleConfigResponseRecords

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "event_filter.links",
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """links,access_control_role.links,access_control_role.name,event_filter.links,event_filter.name,limit_access_to_global_configs,"""

    patchable_fields = [
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """event_filter.name,limit_access_to_global_configs,"""

    postable_fields = [
        "access_control_role.name",
        "event_filter.name",
        "limit_access_to_global_configs",
    ]
    """access_control_role.name,event_filter.name,limit_access_to_global_configs,"""


class EmsRoleConfigResponseRecords(Resource):

    _schema = EmsRoleConfigResponseRecordsSchema
