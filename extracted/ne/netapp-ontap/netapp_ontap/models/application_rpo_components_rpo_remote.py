r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationRpoComponentsRpoRemote", "ApplicationRpoComponentsRpoRemoteSchema"]
__pdoc__ = {
    "ApplicationRpoComponentsRpoRemoteSchema.resource": False,
    "ApplicationRpoComponentsRpoRemoteSchema.opts": False,
    "ApplicationRpoComponentsRpoRemote": False,
}


class ApplicationRpoComponentsRpoRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationRpoComponentsRpoRemote object"""

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" A detailed description of the remote RPO. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The remote RPO of the component. A remote RPO of zero indicates that the component is synchronously replicated to another cluster.

Valid choices:

* 6_hourly
* 15_minutely
* hourly
* none
* zero """

    @property
    def resource(self):
        return ApplicationRpoComponentsRpoRemote

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


class ApplicationRpoComponentsRpoRemote(Resource):

    _schema = ApplicationRpoComponentsRpoRemoteSchema
