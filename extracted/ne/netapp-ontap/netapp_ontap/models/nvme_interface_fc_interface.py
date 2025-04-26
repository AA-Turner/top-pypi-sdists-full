r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeInterfaceFcInterface", "NvmeInterfaceFcInterfaceSchema"]
__pdoc__ = {
    "NvmeInterfaceFcInterfaceSchema.resource": False,
    "NvmeInterfaceFcInterfaceSchema.opts": False,
    "NvmeInterfaceFcInterface": False,
}


class NvmeInterfaceFcInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeInterfaceFcInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the nvme_interface_fc_interface. """

    port = marshmallow_fields.Nested("netapp_ontap.resources.fc_port.FcPortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the nvme_interface_fc_interface. """

    wwnn = marshmallow_fields.Str(data_key="wwnn", allow_none=True)
    r""" The WWNN (world wide node name) of the Fibre Channel NVMe interface.


Example: 20:00:00:50:56:b4:13:a9 """

    wwpn = marshmallow_fields.Str(data_key="wwpn", allow_none=True)
    r""" The WWPN (world wide port name) of the Fibre Channel NVMe interface.


Example: 20:00:00:50:56:b4:13:a8 """

    @property
    def resource(self):
        return NvmeInterfaceFcInterface

    gettable_fields = [
        "links",
        "port.links",
        "port.name",
        "port.node",
        "port.uuid",
        "wwnn",
        "wwpn",
    ]
    """links,port.links,port.name,port.node,port.uuid,wwnn,wwpn,"""

    patchable_fields = [
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """port.name,port.node,port.uuid,"""

    postable_fields = [
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """port.name,port.node,port.uuid,"""


class NvmeInterfaceFcInterface(Resource):

    _schema = NvmeInterfaceFcInterfaceSchema
