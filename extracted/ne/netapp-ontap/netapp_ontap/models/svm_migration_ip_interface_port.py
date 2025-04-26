r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationIpInterfacePort", "SvmMigrationIpInterfacePortSchema"]
__pdoc__ = {
    "SvmMigrationIpInterfacePortSchema.resource": False,
    "SvmMigrationIpInterfacePortSchema.opts": False,
    "SvmMigrationIpInterfacePort": False,
}


class SvmMigrationIpInterfacePortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationIpInterfacePort object"""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, data_key="interface", allow_none=True)
    r""" The interface field of the svm_migration_ip_interface_port. """

    port = marshmallow_fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the svm_migration_ip_interface_port. """

    @property
    def resource(self):
        return SvmMigrationIpInterfacePort

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


class SvmMigrationIpInterfacePort(Resource):

    _schema = SvmMigrationIpInterfacePortSchema
