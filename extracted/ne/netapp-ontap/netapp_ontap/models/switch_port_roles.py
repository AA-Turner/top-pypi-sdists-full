r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortRoles", "SwitchPortRolesSchema"]
__pdoc__ = {
    "SwitchPortRolesSchema.resource": False,
    "SwitchPortRolesSchema.opts": False,
    "SwitchPortRoles": False,
}


class SwitchPortRolesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortRoles object"""

    dr_group = marshmallow_fields.Str(data_key="dr_group", allow_none=True)
    r""" DR group. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Allowed use type.

Valid choices:

* cluster
* storage
* metrocluster
* local_isl
* remote_isl
* vpc_peer_link """

    zone = Size(data_key="zone", allow_none=True)
    r""" Zone ID to differentiate between roles with the same type. """

    @property
    def resource(self):
        return SwitchPortRoles

    gettable_fields = [
        "dr_group",
        "type",
        "zone",
    ]
    """dr_group,type,zone,"""

    patchable_fields = [
        "dr_group",
        "type",
        "zone",
    ]
    """dr_group,type,zone,"""

    postable_fields = [
        "dr_group",
        "type",
        "zone",
    ]
    """dr_group,type,zone,"""


class SwitchPortRoles(Resource):

    _schema = SwitchPortRolesSchema
