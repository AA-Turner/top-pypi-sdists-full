r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorRelationshipPolicy", "SnapmirrorRelationshipPolicySchema"]
__pdoc__ = {
    "SnapmirrorRelationshipPolicySchema.resource": False,
    "SnapmirrorRelationshipPolicySchema.opts": False,
    "SnapmirrorRelationshipPolicy": False,
}


class SnapmirrorRelationshipPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorRelationshipPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snapmirror_relationship_policy. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the SnapMirror policy.

Example: Asynchronous """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the snapmirror_relationship_policy.

Valid choices:

* async
* sync
* continuous """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the SnapMirror policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SnapmirrorRelationshipPolicy

    gettable_fields = [
        "links",
        "name",
        "type",
        "uuid",
    ]
    """links,name,type,uuid,"""

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


class SnapmirrorRelationshipPolicy(Resource):

    _schema = SnapmirrorRelationshipPolicySchema
