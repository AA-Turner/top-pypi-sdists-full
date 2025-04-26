r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationRpoComponentsRpo", "ApplicationRpoComponentsRpoSchema"]
__pdoc__ = {
    "ApplicationRpoComponentsRpoSchema.resource": False,
    "ApplicationRpoComponentsRpoSchema.opts": False,
    "ApplicationRpoComponentsRpo": False,
}


class ApplicationRpoComponentsRpoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationRpoComponentsRpo object"""

    local = marshmallow_fields.Nested("netapp_ontap.models.application_rpo_components_rpo_local.ApplicationRpoComponentsRpoLocalSchema", unknown=EXCLUDE, data_key="local", allow_none=True)
    r""" The local field of the application_rpo_components_rpo. """

    remote = marshmallow_fields.Nested("netapp_ontap.models.application_rpo_components_rpo_remote.ApplicationRpoComponentsRpoRemoteSchema", unknown=EXCLUDE, data_key="remote", allow_none=True)
    r""" The remote field of the application_rpo_components_rpo. """

    @property
    def resource(self):
        return ApplicationRpoComponentsRpo

    gettable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""

    patchable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""

    postable_fields = [
        "local",
        "remote",
    ]
    """local,remote,"""


class ApplicationRpoComponentsRpo(Resource):

    _schema = ApplicationRpoComponentsRpoSchema
