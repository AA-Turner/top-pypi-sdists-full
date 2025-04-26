r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationProtectionGroupsRpoRemote", "ApplicationProtectionGroupsRpoRemoteSchema"]
__pdoc__ = {
    "ApplicationProtectionGroupsRpoRemoteSchema.resource": False,
    "ApplicationProtectionGroupsRpoRemoteSchema.opts": False,
    "ApplicationProtectionGroupsRpoRemote": False,
}


class ApplicationProtectionGroupsRpoRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationProtectionGroupsRpoRemote object"""

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" A detailed description of the remote RPO. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The remote RPO of the component. A remote RPO of zero indicates that the component is synchronously replicated to another cluster.

Valid choices:

* none
* zero
* hourly
* 6_hourly
* 15_minutely """

    @property
    def resource(self):
        return ApplicationProtectionGroupsRpoRemote

    gettable_fields = [
        "description",
        "name",
    ]
    """description,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationProtectionGroupsRpoRemote(Resource):

    _schema = ApplicationProtectionGroupsRpoRemoteSchema
