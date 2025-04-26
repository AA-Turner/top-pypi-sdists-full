r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupQosPolicy", "ConsistencyGroupQosPolicySchema"]
__pdoc__ = {
    "ConsistencyGroupQosPolicySchema.resource": False,
    "ConsistencyGroupQosPolicySchema.opts": False,
    "ConsistencyGroupQosPolicy": False,
}


class ConsistencyGroupQosPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupQosPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_qos_policy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The QoS policy group name. This is mutually exclusive with UUID and other QoS attributes during POST and PATCH.

Example: performance """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The QoS policy group UUID. This is mutually exclusive with name and other QoS attributes during POST and PATCH.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupQosPolicy

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

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


class ConsistencyGroupQosPolicy(Resource):

    _schema = ConsistencyGroupQosPolicySchema
