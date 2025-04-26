r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupNvmeSubsystem", "ConsistencyGroupNvmeSubsystemSchema"]
__pdoc__ = {
    "ConsistencyGroupNvmeSubsystemSchema.resource": False,
    "ConsistencyGroupNvmeSubsystemSchema.opts": False,
    "ConsistencyGroupNvmeSubsystem": False,
}


class ConsistencyGroupNvmeSubsystemSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupNvmeSubsystem object"""

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" A configurable comment for the NVMe subsystem. Optional in POST and PATCH. """

    hosts = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_nvme_host.ConsistencyGroupNvmeHostSchema", unknown=EXCLUDE, allow_none=True), data_key="hosts", allow_none=True)
    r""" The NVMe hosts configured for access to the NVMe subsystem.
Optional in POST. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the NVMe subsystem. Once created, an NVMe subsystem cannot be renamed. Required in POST.


Example: subsystem1 """

    os_type = marshmallow_fields.Str(data_key="os_type", allow_none=True)
    r""" The host operating system of the NVMe subsystem's hosts. Required in POST.


Valid choices:

* aix
* linux
* vmware
* windows """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the NVMe subsystem.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupNvmeSubsystem

    gettable_fields = [
        "comment",
        "hosts",
        "name",
        "os_type",
        "uuid",
    ]
    """comment,hosts,name,os_type,uuid,"""

    patchable_fields = [
        "comment",
    ]
    """comment,"""

    postable_fields = [
        "comment",
        "hosts",
        "name",
        "os_type",
    ]
    """comment,hosts,name,os_type,"""


class ConsistencyGroupNvmeSubsystem(Resource):

    _schema = ConsistencyGroupNvmeSubsystemSchema
