r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityKeyManagerRestoreKeys", "SecurityKeyManagerRestoreKeysSchema"]
__pdoc__ = {
    "SecurityKeyManagerRestoreKeysSchema.resource": False,
    "SecurityKeyManagerRestoreKeysSchema.opts": False,
    "SecurityKeyManagerRestoreKeys": False,
}


class SecurityKeyManagerRestoreKeysSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeyManagerRestoreKeys object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the security_key_manager_restore_keys. """

    key_id = marshmallow_fields.Str(data_key="key_id", allow_none=True)
    r""" Key identifier.

Example: 000000000000000002000000000001003aa8ce6a4fea3e466620134bea9510a10000000000000000 """

    key_server = marshmallow_fields.Str(data_key="key_server", allow_none=True)
    r""" External key server for key management.

Example: keyserver1.com:5698 """

    key_tag = marshmallow_fields.Str(data_key="key_tag", allow_none=True)
    r""" Additional information associated with the key.

Example: Authentication-Key-01 """

    node = marshmallow_fields.Nested("netapp_ontap.models.node_uuid.NodeUuidSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the security_key_manager_restore_keys. """

    @property
    def resource(self):
        return SecurityKeyManagerRestoreKeys

    gettable_fields = [
        "links",
        "key_id",
        "key_server",
        "key_tag",
        "node",
    ]
    """links,key_id,key_server,key_tag,node,"""

    patchable_fields = [
        "key_id",
        "key_server",
        "key_tag",
        "node",
    ]
    """key_id,key_server,key_tag,node,"""

    postable_fields = [
        "key_id",
        "key_server",
        "key_tag",
        "node",
    ]
    """key_id,key_server,key_tag,node,"""


class SecurityKeyManagerRestoreKeys(Resource):

    _schema = SecurityKeyManagerRestoreKeysSchema
