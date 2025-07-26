r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortIdentity", "SwitchPortIdentitySchema"]
__pdoc__ = {
    "SwitchPortIdentitySchema.resource": False,
    "SwitchPortIdentitySchema.opts": False,
    "SwitchPortIdentity": False,
}


class SwitchPortIdentitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortIdentity object"""

    breakout = marshmallow_fields.Nested("netapp_ontap.models.switch_port_identity_breakout.SwitchPortIdentityBreakoutSchema", unknown=EXCLUDE, data_key="breakout", allow_none=True)
    r""" The breakout field of the switch_port_identity. """

    index = Size(data_key="index", allow_none=True)
    r""" Interface Index. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Interface Name. """

    number = Size(data_key="number", allow_none=True)
    r""" Interface Number. """

    @property
    def resource(self):
        return SwitchPortIdentity

    gettable_fields = [
        "breakout",
        "index",
        "name",
        "number",
    ]
    """breakout,index,name,number,"""

    patchable_fields = [
        "breakout",
    ]
    """breakout,"""

    postable_fields = [
        "breakout",
    ]
    """breakout,"""


class SwitchPortIdentity(Resource):

    _schema = SwitchPortIdentitySchema
