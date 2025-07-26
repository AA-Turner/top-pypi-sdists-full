r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesNvlog", "ClusterNodesNvlogSchema"]
__pdoc__ = {
    "ClusterNodesNvlogSchema.resource": False,
    "ClusterNodesNvlogSchema.opts": False,
    "ClusterNodesNvlog": False,
}


class ClusterNodesNvlogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesNvlog object"""

    backing_type = marshmallow_fields.Str(data_key="backing_type", allow_none=True)
    r""" Indicates the current NVLog journal backing type.

Valid choices:

* ephemeral_memory
* ephemeral_disk """

    swap_mode = marshmallow_fields.Str(data_key="swap_mode", allow_none=True)
    r""" Indicates the current NVLog journal swap mode.

Valid choices:

* dynamic
* manual """

    @property
    def resource(self):
        return ClusterNodesNvlog

    gettable_fields = [
        "backing_type",
        "swap_mode",
    ]
    """backing_type,swap_mode,"""

    patchable_fields = [
        "backing_type",
        "swap_mode",
    ]
    """backing_type,swap_mode,"""

    postable_fields = [
        "backing_type",
        "swap_mode",
    ]
    """backing_type,swap_mode,"""


class ClusterNodesNvlog(Resource):

    _schema = ClusterNodesNvlogSchema
