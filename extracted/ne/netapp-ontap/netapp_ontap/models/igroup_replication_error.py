r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupReplicationError", "IgroupReplicationErrorSchema"]
__pdoc__ = {
    "IgroupReplicationErrorSchema.resource": False,
    "IgroupReplicationErrorSchema.opts": False,
    "IgroupReplicationError": False,
}


class IgroupReplicationErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupReplicationError object"""

    igroup = marshmallow_fields.Nested("netapp_ontap.models.replication_error_igroup.ReplicationErrorIgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The igroup field of the igroup_replication_error. """

    summary = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="summary", allow_none=True)
    r""" The summary field of the igroup_replication_error. """

    @property
    def resource(self):
        return IgroupReplicationError

    gettable_fields = [
        "igroup",
        "summary",
    ]
    """igroup,summary,"""

    patchable_fields = [
        "igroup",
    ]
    """igroup,"""

    postable_fields = [
        "igroup",
    ]
    """igroup,"""


class IgroupReplicationError(Resource):

    _schema = IgroupReplicationErrorSchema
