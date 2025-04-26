r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationTemplate1", "ApplicationTemplate1Schema"]
__pdoc__ = {
    "ApplicationTemplate1Schema.resource": False,
    "ApplicationTemplate1Schema.opts": False,
    "ApplicationTemplate1": False,
}


class ApplicationTemplate1Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationTemplate1 object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the application_template1. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the template that was used to provision this application. """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" The protocol access of the template that was used to provision this application.

Valid choices:

* nas
* nvme
* s3
* san """

    version = Size(data_key="version", allow_none=True)
    r""" The version of the template that was used to provision this application. The template version changes only if the layout of the application changes over time. For example, redo logs in Oracle RAC templates were updated and provisioned differently in DATA ONTAP 9.3.0 compared to prior releases, so the version number was increased. If layouts change in the future, the changes will be documented along with the corresponding version numbers. """

    @property
    def resource(self):
        return ApplicationTemplate1

    gettable_fields = [
        "links",
        "name",
        "protocol",
        "version",
    ]
    """links,name,protocol,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ApplicationTemplate1(Resource):

    _schema = ApplicationTemplate1Schema
