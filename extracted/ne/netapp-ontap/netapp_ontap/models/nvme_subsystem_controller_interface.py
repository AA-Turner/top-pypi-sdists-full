r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemControllerInterface", "NvmeSubsystemControllerInterfaceSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerInterfaceSchema.resource": False,
    "NvmeSubsystemControllerInterfaceSchema.opts": False,
    "NvmeSubsystemControllerInterface": False,
}


class NvmeSubsystemControllerInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemControllerInterface object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the logical interface.


Example: lif1 """

    transport_address = marshmallow_fields.Str(data_key="transport_address", allow_none=True)
    r""" The transport address of the logical interface.


Example: nn-0x200400a0989a1c8d:pn-0x200500a0989a1c8d """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the logical interface.


Example: fa1c5941-2593-11e9-94c4-00a0989a1c8e """

    @property
    def resource(self):
        return NvmeSubsystemControllerInterface

    gettable_fields = [
        "name",
        "transport_address",
        "uuid",
    ]
    """name,transport_address,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeSubsystemControllerInterface(Resource):

    _schema = NvmeSubsystemControllerInterfaceSchema
