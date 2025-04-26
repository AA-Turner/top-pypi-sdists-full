r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationComponentApplication", "ApplicationComponentApplicationSchema"]
__pdoc__ = {
    "ApplicationComponentApplicationSchema.resource": False,
    "ApplicationComponentApplicationSchema.opts": False,
    "ApplicationComponentApplication": False,
}


class ApplicationComponentApplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponentApplication object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_component_application. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Application name """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The application UUID. Valid in URL. """

    @property
    def resource(self):
        return ApplicationComponentApplication

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationComponentApplication(Resource):

    _schema = ApplicationComponentApplicationSchema
