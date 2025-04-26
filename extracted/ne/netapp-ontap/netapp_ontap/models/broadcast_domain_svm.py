r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BroadcastDomainSvm", "BroadcastDomainSvmSchema"]
__pdoc__ = {
    "BroadcastDomainSvmSchema.resource": False,
    "BroadcastDomainSvmSchema.opts": False,
    "BroadcastDomainSvm": False,
}


class BroadcastDomainSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BroadcastDomainSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the broadcast_domain_svm. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the broadcast domain, scoped to its IPspace

Example: bd1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Broadcast domain UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return BroadcastDomainSvm

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


class BroadcastDomainSvm(Resource):

    _schema = BroadcastDomainSvmSchema
