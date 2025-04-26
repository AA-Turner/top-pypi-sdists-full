r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationIpInterfacePlacementIpInterfaces", "SvmMigrationIpInterfacePlacementIpInterfacesSchema"]
__pdoc__ = {
    "SvmMigrationIpInterfacePlacementIpInterfacesSchema.resource": False,
    "SvmMigrationIpInterfacePlacementIpInterfacesSchema.opts": False,
    "SvmMigrationIpInterfacePlacementIpInterfaces": False,
}


class SvmMigrationIpInterfacePlacementIpInterfacesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationIpInterfacePlacementIpInterfaces object"""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, data_key="interface", allow_none=True)
    r""" The interface field of the svm_migration_ip_interface_placement_ip_interfaces. """

    port = marshmallow_fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the svm_migration_ip_interface_placement_ip_interfaces. """

    @property
    def resource(self):
        return SvmMigrationIpInterfacePlacementIpInterfaces

    gettable_fields = [
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "port.links",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """interface.links,interface.ip,interface.name,interface.uuid,port.links,port.name,port.node,port.uuid,"""

    patchable_fields = [
        "interface.name",
        "interface.uuid",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """interface.name,interface.uuid,port.name,port.node,port.uuid,"""

    postable_fields = [
        "interface.name",
        "interface.uuid",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """interface.name,interface.uuid,port.name,port.node,port.uuid,"""


class SvmMigrationIpInterfacePlacementIpInterfaces(Resource):

    _schema = SvmMigrationIpInterfacePlacementIpInterfacesSchema
