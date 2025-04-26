r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["S3AuditEventSelector", "S3AuditEventSelectorSchema"]
__pdoc__ = {
    "S3AuditEventSelectorSchema.resource": False,
    "S3AuditEventSelectorSchema.opts": False,
    "S3AuditEventSelector": False,
}


class S3AuditEventSelectorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3AuditEventSelector object"""

    access = marshmallow_fields.Str(data_key="access", allow_none=True)
    r""" Specifies read and write access types.


Valid choices:

* read
* write
* all
* none """

    permission = marshmallow_fields.Str(data_key="permission", allow_none=True)
    r""" Specifies allow and deny permission types.


Valid choices:

* deny
* allow
* all
* none """

    @property
    def resource(self):
        return S3AuditEventSelector

    gettable_fields = [
        "access",
        "permission",
    ]
    """access,permission,"""

    patchable_fields = [
        "access",
        "permission",
    ]
    """access,permission,"""

    postable_fields = [
        "access",
        "permission",
    ]
    """access,permission,"""


class S3AuditEventSelector(Resource):

    _schema = S3AuditEventSelectorSchema
