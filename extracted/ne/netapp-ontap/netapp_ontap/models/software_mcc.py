r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareMcc", "SoftwareMccSchema"]
__pdoc__ = {
    "SoftwareMccSchema.resource": False,
    "SoftwareMccSchema.opts": False,
    "SoftwareMcc": False,
}


class SoftwareMccSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareMcc object"""

    elapsed_duration = Size(data_key="elapsed_duration", allow_none=True)
    r""" Elapsed duration of update time (in seconds) of MetroCluster.

Example: 2140 """

    estimated_duration = Size(data_key="estimated_duration", allow_none=True)
    r""" Estimated duration of update time (in seconds) of MetroCluster.

Example: 3480 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the site in MetroCluster.

Example: cluster_A """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Upgrade state of MetroCluster.

Valid choices:

* in_progress
* waiting
* paused_by_user
* paused_on_error
* completed
* canceled
* failed
* pause_pending
* cancel_pending """

    @property
    def resource(self):
        return SoftwareMcc

    gettable_fields = [
        "elapsed_duration",
        "estimated_duration",
        "name",
        "state",
    ]
    """elapsed_duration,estimated_duration,name,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SoftwareMcc(Resource):

    _schema = SoftwareMccSchema
