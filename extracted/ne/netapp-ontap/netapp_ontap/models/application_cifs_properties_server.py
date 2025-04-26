r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationCifsPropertiesServer", "ApplicationCifsPropertiesServerSchema"]
__pdoc__ = {
    "ApplicationCifsPropertiesServerSchema.resource": False,
    "ApplicationCifsPropertiesServerSchema.opts": False,
    "ApplicationCifsPropertiesServer": False,
}


class ApplicationCifsPropertiesServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationCifsPropertiesServer object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Server name """

    @property
    def resource(self):
        return ApplicationCifsPropertiesServer

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationCifsPropertiesServer(Resource):

    _schema = ApplicationCifsPropertiesServerSchema
