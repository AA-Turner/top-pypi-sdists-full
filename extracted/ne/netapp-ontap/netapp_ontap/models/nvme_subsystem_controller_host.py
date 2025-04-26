r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemControllerHost", "NvmeSubsystemControllerHostSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerHostSchema.resource": False,
    "NvmeSubsystemControllerHostSchema.opts": False,
    "NvmeSubsystemControllerHost": False,
}


class NvmeSubsystemControllerHostSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemControllerHost object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" The host identifier registered with the controller.


Example: b8546ca6097349e5b1558dc154fc073b """

    nqn = marshmallow_fields.Str(data_key="nqn", allow_none=True)
    r""" The NVMe qualified name of the host.


Example: nqn.2014-08.org.nvmexpress:uuid:c2846cb1-89d2-4020-a3b0-71ce907b4eef """

    transport_address = marshmallow_fields.Str(data_key="transport_address", allow_none=True)
    r""" The transport address of the host.


Example: nn-0x20000090fae00806:pn-0x10000090fae00806 """

    @property
    def resource(self):
        return NvmeSubsystemControllerHost

    gettable_fields = [
        "id",
        "nqn",
        "transport_address",
    ]
    """id,nqn,transport_address,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeSubsystemControllerHost(Resource):

    _schema = NvmeSubsystemControllerHostSchema
