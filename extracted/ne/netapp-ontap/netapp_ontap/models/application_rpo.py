r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationRpo", "ApplicationRpoSchema"]
__pdoc__ = {
    "ApplicationRpoSchema.resource": False,
    "ApplicationRpoSchema.opts": False,
    "ApplicationRpo": False,
}


class ApplicationRpoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationRpo object"""

    components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_rpo_components.ApplicationRpoComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="components", allow_none=True)
    r""" The components field of the application_rpo. """

    is_supported = marshmallow_fields.Boolean(data_key="is_supported", allow_none=True)
    r""" Is RPO supported for this application? Generation 1 applications did not support Snapshot copies or MetroCluster. """

    local = marshmallow_fields.Nested("netapp_ontap.models.application_rpo_local.ApplicationRpoLocalSchema", unknown=EXCLUDE, data_key="local", allow_none=True)
    r""" The local field of the application_rpo. """

    remote = marshmallow_fields.Nested("netapp_ontap.models.application_rpo_remote.ApplicationRpoRemoteSchema", unknown=EXCLUDE, data_key="remote", allow_none=True)
    r""" The remote field of the application_rpo. """

    @property
    def resource(self):
        return ApplicationRpo

    gettable_fields = [
        "components",
        "is_supported",
        "local",
        "remote",
    ]
    """components,is_supported,local,remote,"""

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


class ApplicationRpo(Resource):

    _schema = ApplicationRpoSchema
