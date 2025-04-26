r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ReplicationErrorIgroup", "ReplicationErrorIgroupSchema"]
__pdoc__ = {
    "ReplicationErrorIgroupSchema.resource": False,
    "ReplicationErrorIgroupSchema.opts": False,
    "ReplicationErrorIgroup": False,
}


class ReplicationErrorIgroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ReplicationErrorIgroup object"""

    local_svm = marshmallow_fields.Boolean(data_key="local_svm", allow_none=True)
    r""" Indicates whether the reported igroup is on the local SVM or the peer SVM. When deleting a replicated igroup, the local copy is deleted first and then the peer copy is deleted. If the error is encountered between these two operations and only the peer igroup remains, the peer igroup is reported and the problem might need to be corrected on the peer cluster. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the initiator group.


Example: igroup1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ReplicationErrorIgroup

    gettable_fields = [
        "local_svm",
        "name",
        "uuid",
    ]
    """local_svm,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ReplicationErrorIgroup(Resource):

    _schema = ReplicationErrorIgroupSchema
