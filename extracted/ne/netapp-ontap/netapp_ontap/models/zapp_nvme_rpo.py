r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeRpo", "ZappNvmeRpoSchema"]
__pdoc__ = {
    "ZappNvmeRpoSchema.resource": False,
    "ZappNvmeRpoSchema.opts": False,
    "ZappNvmeRpo": False,
}


class ZappNvmeRpoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeRpo object"""

    local = marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_rpo_local.ZappNvmeRpoLocalSchema", unknown=EXCLUDE, data_key="local", allow_none=True)
    r""" The local field of the zapp_nvme_rpo. """

    remote = marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme_rpo_remote.ZappNvmeRpoRemoteSchema", unknown=EXCLUDE, data_key="remote", allow_none=True)
    r""" The remote field of the zapp_nvme_rpo. """

    @property
    def resource(self):
        return ZappNvmeRpo

    gettable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""

    patchable_fields = [
        "local",
    ]
    """local,"""

    postable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""


class ZappNvmeRpo(Resource):

    _schema = ZappNvmeRpoSchema
