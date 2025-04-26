r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmMigrationDestination", "SvmMigrationDestinationSchema"]
__pdoc__ = {
    "SvmMigrationDestinationSchema.resource": False,
    "SvmMigrationDestinationSchema.opts": False,
    "SvmMigrationDestination": False,
}


class SvmMigrationDestinationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationDestination object"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", unknown=EXCLUDE, data_key="ipspace", allow_none=True)
    r""" The ipspace field of the svm_migration_destination. """

    volume_placement = marshmallow_fields.Nested("netapp_ontap.models.svm_migration_volume_placement.SvmMigrationVolumePlacementSchema", unknown=EXCLUDE, data_key="volume_placement", allow_none=True)
    r""" Volume selection information """

    @property
    def resource(self):
        return SvmMigrationDestination

    gettable_fields = [
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
    ]
    """ipspace.links,ipspace.name,ipspace.uuid,"""

    patchable_fields = [
        "volume_placement",
    ]
    """volume_placement,"""

    postable_fields = [
        "ipspace.name",
        "ipspace.uuid",
        "volume_placement",
    ]
    """ipspace.name,ipspace.uuid,volume_placement,"""


class SvmMigrationDestination(Resource):

    _schema = SvmMigrationDestinationSchema
