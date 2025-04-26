r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitQosPolicy", "StorageUnitQosPolicySchema"]
__pdoc__ = {
    "StorageUnitQosPolicySchema.resource": False,
    "StorageUnitQosPolicySchema.opts": False,
    "StorageUnitQosPolicy": False,
}


class StorageUnitQosPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitQosPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the storage_unit_qos_policy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the QoS policy.


Example: qos1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the QoS policy.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return StorageUnitQosPolicy

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageUnitQosPolicy(Resource):

    _schema = StorageUnitQosPolicySchema
