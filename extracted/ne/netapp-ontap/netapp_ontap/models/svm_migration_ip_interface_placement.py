r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationIpInterfacePlacement", "SvmMigrationIpInterfacePlacementSchema"]
__pdoc__ = {
    "SvmMigrationIpInterfacePlacementSchema.resource": False,
    "SvmMigrationIpInterfacePlacementSchema.opts": False,
    "SvmMigrationIpInterfacePlacement": False,
}


class SvmMigrationIpInterfacePlacementSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationIpInterfacePlacement object"""

    ip_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_ip_interface_port.SvmMigrationIpInterfacePortSchema", unknown=EXCLUDE, allow_none=True), data_key="ip_interfaces", allow_none=True)
    r""" List of source SVM's IP interface and port pairs on the destination for migrating the source SVM's IP interfaces. """

    @property
    def resource(self):
        return SvmMigrationIpInterfacePlacement

    gettable_fields = [
        "ip_interfaces",
    ]
    """ip_interfaces,"""

    patchable_fields = [
        "ip_interfaces",
    ]
    """ip_interfaces,"""

    postable_fields = [
        "ip_interfaces",
    ]
    """ip_interfaces,"""


class SvmMigrationIpInterfacePlacement(Resource):

    _schema = SvmMigrationIpInterfacePlacementSchema
