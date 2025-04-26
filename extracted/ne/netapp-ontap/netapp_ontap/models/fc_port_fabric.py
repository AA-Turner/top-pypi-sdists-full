r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcPortFabric", "FcPortFabricSchema"]
__pdoc__ = {
    "FcPortFabricSchema.resource": False,
    "FcPortFabricSchema.opts": False,
    "FcPortFabric": False,
}


class FcPortFabricSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcPortFabric object"""

    connected = marshmallow_fields.Boolean(data_key="connected", allow_none=True)
    r""" Reports if the physical port has established a connection with the FC fabric. """

    connected_speed = Size(data_key="connected_speed", allow_none=True)
    r""" The negotiated data rate between the target FC port and the fabric in gigabits per second.


Example: 16 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the fabric to which the port is connected. This is only available when the FC port is connected to a fabric.<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more. """

    port_address = marshmallow_fields.Str(data_key="port_address", allow_none=True)
    r""" The FC port address of the host bus adapter (HBA) physical port.<br/>
Each FC port in an FC switched fabric has its own unique FC port address for routing purposes. The FC port address is assigned by a switch in the fabric when that port logs in to the fabric. This property refers to the FC port address given to the physical host bus adapter (HBA) port when the port performs a fabric login (FLOGI).<br/>
This is useful for obtaining statistics and diagnostic information from FC switches.<br/>
This is a six-digit hexadecimal encoded numeric value.


Example: 52100A """

    switch_port = marshmallow_fields.Str(data_key="switch_port", allow_none=True)
    r""" The switch port to which the FC port is connected.


Example: ssan-g620-03:33 """

    @property
    def resource(self):
        return FcPortFabric

    gettable_fields = [
        "connected",
        "connected_speed",
        "name",
        "port_address",
        "switch_port",
    ]
    """connected,connected_speed,name,port_address,switch_port,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FcPortFabric(Resource):

    _schema = FcPortFabricSchema
