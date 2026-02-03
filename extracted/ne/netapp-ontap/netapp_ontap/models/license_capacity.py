r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["LicenseCapacity", "LicenseCapacitySchema"]
__pdoc__ = {
    "LicenseCapacitySchema.resource": False,
    "LicenseCapacitySchema.opts": False,
    "LicenseCapacity": False,
}

class LicenseCapacitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LicenseCapacity object"""

    disabled_size = Size(data_key="disabled_size", allow_none=True)
    r""" Capacity that is currently disabled due to license limits. Its unit of measure is specified in the measurement_unit field. """

    maximum_size = Size(data_key="maximum_size", allow_none=True)
    r""" Licensed capacity size that can be used. Its unit of measure is specified in the measurement_unit field. """

    measurement_unit = marshmallow_fields.Str(data_key="measurement_unit", allow_none=True)
    r""" Unit of measure for capacity based licenses.

Valid choices:

* bytes
* gpu_count """

    used_size = Size(data_key="used_size", allow_none=True)
    r""" Specifies the total number of GPUs in the system when measurement_unit is GPUs, else specifies the bytes used. """

    @property
    def resource(self):
        return LicenseCapacity

    gettable_fields = [
        "disabled_size",
        "maximum_size",
        "measurement_unit",
        "used_size",
    ]
    """disabled_size,maximum_size,measurement_unit,used_size,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LicenseCapacity(Resource):

    _schema = LicenseCapacitySchema
