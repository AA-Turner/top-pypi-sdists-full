r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfVendor", "ShelfVendorSchema"]
__pdoc__ = {
    "ShelfVendorSchema.resource": False,
    "ShelfVendorSchema.opts": False,
    "ShelfVendor": False,
}


class ShelfVendorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfVendor object"""

    manufacturer = marshmallow_fields.Str(data_key="manufacturer", allow_none=True)
    r""" Support for this field will be removed in a future release. Please use vendor.name for this field.

Example: XYZ """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the shelf_vendor.

Example: XYZ """

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" Part number

Example: A92831142733 """

    product = marshmallow_fields.Str(data_key="product", allow_none=True)
    r""" Product name

Example: LS2246 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Serial number

Example: 891234572210221 """

    @property
    def resource(self):
        return ShelfVendor

    gettable_fields = [
        "manufacturer",
        "name",
        "part_number",
        "product",
        "serial_number",
    ]
    """manufacturer,name,part_number,product,serial_number,"""

    patchable_fields = [
        "manufacturer",
        "name",
        "part_number",
        "product",
        "serial_number",
    ]
    """manufacturer,name,part_number,product,serial_number,"""

    postable_fields = [
        "manufacturer",
        "name",
        "part_number",
        "product",
        "serial_number",
    ]
    """manufacturer,name,part_number,product,serial_number,"""


class ShelfVendor(Resource):

    _schema = ShelfVendorSchema
