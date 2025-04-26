r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesServiceProcessorBackup", "ClusterNodesServiceProcessorBackupSchema"]
__pdoc__ = {
    "ClusterNodesServiceProcessorBackupSchema.resource": False,
    "ClusterNodesServiceProcessorBackupSchema.opts": False,
    "ClusterNodesServiceProcessorBackup": False,
}


class ClusterNodesServiceProcessorBackupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesServiceProcessorBackup object"""

    is_current = marshmallow_fields.Boolean(data_key="is_current", allow_none=True)
    r""" Indicates whether the service processor is currently booted from the backup partition. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Status of the backup partition.

Valid choices:

* installed
* corrupt
* updating
* auto_updating
* none """

    version = marshmallow_fields.Str(data_key="version", allow_none=True)
    r""" Firmware version of the backup partition.

Example: 11.6 """

    @property
    def resource(self):
        return ClusterNodesServiceProcessorBackup

    gettable_fields = [
        "is_current",
        "state",
        "version",
    ]
    """is_current,state,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesServiceProcessorBackup(Resource):

    _schema = ClusterNodesServiceProcessorBackupSchema
