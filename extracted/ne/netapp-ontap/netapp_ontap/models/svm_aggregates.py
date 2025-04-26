r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmAggregates", "SvmAggregatesSchema"]
__pdoc__ = {
    "SvmAggregatesSchema.resource": False,
    "SvmAggregatesSchema.opts": False,
    "SvmAggregates": False,
}


class SvmAggregatesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmAggregates object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the svm_aggregates. """

    available_size = Size(data_key="available_size", allow_none=True)
    r""" Space available, in bytes.

Example: 10156560384 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the svm_aggregates.

Example: aggr1 """

    snaplock_type = marshmallow_fields.Str(data_key="snaplock_type", allow_none=True)
    r""" SnapLock type.

Valid choices:

* non_snaplock
* compliance
* enterprise """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Aggregate state.

Valid choices:

* online
* offline
* unknown """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Type of aggregate.

Valid choices:

* hdd
* hybrid
* lun
* ssd
* vmdisk """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the svm_aggregates.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SvmAggregates

    gettable_fields = [
        "links",
        "available_size",
        "name",
        "snaplock_type",
        "state",
        "type",
        "uuid",
    ]
    """links,available_size,name,snaplock_type,state,type,uuid,"""

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


class SvmAggregates(Resource):

    _schema = SvmAggregatesSchema
