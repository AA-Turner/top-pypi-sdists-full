r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StoragePortCable", "StoragePortCableSchema"]
__pdoc__ = {
    "StoragePortCableSchema.resource": False,
    "StoragePortCableSchema.opts": False,
    "StoragePortCable": False,
}


class StoragePortCableSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StoragePortCable object"""

    identifier = marshmallow_fields.Str(data_key="identifier", allow_none=True)
    r""" The identifier field of the storage_port_cable.

Example: 500a0980000b6c3f-50000d1703544b80 """

    length = marshmallow_fields.Str(data_key="length", allow_none=True)
    r""" The length field of the storage_port_cable.

Example: 2m """

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" The part_number field of the storage_port_cable.

Example: 112-00431+A0 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial_number field of the storage_port_cable.

Example: 616930439 """

    transceiver = marshmallow_fields.Str(data_key="transceiver", allow_none=True)
    r""" The transceiver field of the storage_port_cable.

Valid choices:

* qsfp
* qsfp_plus
* qsfp28
* mini_sas_hd
* sfp """

    vendor = marshmallow_fields.Str(data_key="vendor", allow_none=True)
    r""" The vendor field of the storage_port_cable.

Example: Molex Inc. """

    @property
    def resource(self):
        return StoragePortCable

    gettable_fields = [
        "identifier",
        "length",
        "part_number",
        "serial_number",
        "transceiver",
        "vendor",
    ]
    """identifier,length,part_number,serial_number,transceiver,vendor,"""

    patchable_fields = [
        "identifier",
        "length",
        "part_number",
        "serial_number",
        "transceiver",
        "vendor",
    ]
    """identifier,length,part_number,serial_number,transceiver,vendor,"""

    postable_fields = [
        "identifier",
        "length",
        "part_number",
        "serial_number",
        "transceiver",
        "vendor",
    ]
    """identifier,length,part_number,serial_number,transceiver,vendor,"""


class StoragePortCable(Resource):

    _schema = StoragePortCableSchema
