r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CloudStoreUnavailableReason", "CloudStoreUnavailableReasonSchema"]
__pdoc__ = {
    "CloudStoreUnavailableReasonSchema.resource": False,
    "CloudStoreUnavailableReasonSchema.opts": False,
    "CloudStoreUnavailableReason": False,
}


class CloudStoreUnavailableReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CloudStoreUnavailableReason object"""

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Indicates why the object store is unavailable. """

    @property
    def resource(self):
        return CloudStoreUnavailableReason

    gettable_fields = [
        "message",
    ]
    """message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class CloudStoreUnavailableReason(Resource):

    _schema = CloudStoreUnavailableReasonSchema
