r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnHardware", "DcnHardwareSchema"]
__pdoc__ = {
    "DcnHardwareSchema.resource": False,
    "DcnHardwareSchema.opts": False,
    "DcnHardware": False,
}

class DcnHardwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnHardware object"""

    board = marshmallow_fields.Str(data_key="board", allow_none=True)
    r""" Type of the system board, defined by the vendor.

Example: System Board XXVIII """

    cpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_hardware_cpu", "DcnHardwareCpuSchema"),
                unknown=EXCLUDE,
                data_key="cpu",
                allow_none=True
            )
    r""" CPU information. """

    frus = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.dcn_fru", "DcnFruSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="frus",
                allow_none=True
                )
    r""" The field replaceable units (FRUs) on the node. """

    gpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_hardware_gpu", "DcnHardwareGpuSchema"),
                unknown=EXCLUDE,
                data_key="gpu",
                allow_none=True
            )
    r""" GPU information. """

    @property
    def resource(self):
        return DcnHardware

    gettable_fields = [
        "board",
        "cpu",
        "frus",
        "gpu",
    ]
    """board,cpu,frus,gpu,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnHardware(Resource):

    _schema = DcnHardwareSchema
