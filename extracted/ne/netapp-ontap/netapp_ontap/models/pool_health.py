r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PoolHealth", "PoolHealthSchema"]
__pdoc__ = {
    "PoolHealthSchema.resource": False,
    "PoolHealthSchema.opts": False,
    "PoolHealth": False,
}


class PoolHealthSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PoolHealth object"""

    is_healthy = marshmallow_fields.Boolean(data_key="is_healthy", allow_none=True)
    r""" Indicates whether the storage pool is able to participate in provisioning operations. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the shared storage pool.

Valid choices:

* normal
* degraded
* creating
* deleting
* reassigning
* growing """

    unhealthy_reason = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="unhealthy_reason", allow_none=True)
    r""" Indicates why the storage pool is unhealthy. This property is not returned for healthy storage pools. """

    @property
    def resource(self):
        return PoolHealth

    gettable_fields = [
        "is_healthy",
        "state",
        "unhealthy_reason",
    ]
    """is_healthy,state,unhealthy_reason,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PoolHealth(Resource):

    _schema = PoolHealthSchema
