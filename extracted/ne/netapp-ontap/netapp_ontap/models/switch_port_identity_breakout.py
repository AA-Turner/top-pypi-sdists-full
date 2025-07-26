r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortIdentityBreakout", "SwitchPortIdentityBreakoutSchema"]
__pdoc__ = {
    "SwitchPortIdentityBreakoutSchema.resource": False,
    "SwitchPortIdentityBreakoutSchema.opts": False,
    "SwitchPortIdentityBreakout": False,
}


class SwitchPortIdentityBreakoutSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortIdentityBreakout object"""

    number = Size(data_key="number", allow_none=True)
    r""" Breakout port sub-interface number.

Example: 1 """

    physical_port = marshmallow_fields.Str(data_key="physical_port", allow_none=True)
    r""" Breakout physical port name.

Example: Ethernet1/9 """

    @property
    def resource(self):
        return SwitchPortIdentityBreakout

    gettable_fields = [
        "number",
        "physical_port",
    ]
    """number,physical_port,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SwitchPortIdentityBreakout(Resource):

    _schema = SwitchPortIdentityBreakoutSchema
