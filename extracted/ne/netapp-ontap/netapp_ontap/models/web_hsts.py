r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["WebHsts", "WebHstsSchema"]
__pdoc__ = {
    "WebHstsSchema.resource": False,
    "WebHstsSchema.opts": False,
    "WebHsts": False,
}


class WebHstsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebHsts object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether HTTP Strict Transport Security (HSTS) is enabled. """

    max_age = Size(data_key="max_age", allow_none=True)
    r""" HTTPS Strict Transport Security (HSTS) max-age value in seconds. The maximum time, in seconds, that the browser should remember that a site is only to be accessed using HTTPS.

Example: 31536000 """

    @property
    def resource(self):
        return WebHsts

    gettable_fields = [
        "enabled",
        "max_age",
    ]
    """enabled,max_age,"""

    patchable_fields = [
        "enabled",
        "max_age",
    ]
    """enabled,max_age,"""

    postable_fields = [
        "enabled",
        "max_age",
    ]
    """enabled,max_age,"""


class WebHsts(Resource):

    _schema = WebHstsSchema
