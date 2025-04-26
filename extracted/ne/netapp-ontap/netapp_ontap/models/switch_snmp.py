r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchSnmp", "SwitchSnmpSchema"]
__pdoc__ = {
    "SwitchSnmpSchema.resource": False,
    "SwitchSnmpSchema.opts": False,
    "SwitchSnmp": False,
}


class SwitchSnmpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchSnmp object"""

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" Community String or SNMPv3 Username. """

    version = marshmallow_fields.Str(data_key="version", allow_none=True)
    r""" SNMP Version.

Valid choices:

* snmpv1
* snmpv2c
* snmpv3 """

    @property
    def resource(self):
        return SwitchSnmp

    gettable_fields = [
        "user",
        "version",
    ]
    """user,version,"""

    patchable_fields = [
        "user",
        "version",
    ]
    """user,version,"""

    postable_fields = [
        "user",
        "version",
    ]
    """user,version,"""


class SwitchSnmp(Resource):

    _schema = SwitchSnmpSchema
