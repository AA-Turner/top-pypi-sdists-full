r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Usm", "UsmSchema"]
__pdoc__ = {
    "UsmSchema.resource": False,
    "UsmSchema.opts": False,
    "Usm": False,
}


class UsmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Usm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the usm. """

    authentication_password = marshmallow_fields.Str(data_key="authentication_password", allow_none=True)
    r""" Authentication protocol password.

Example: humTdumt*@t0nAwa11 """

    authentication_protocol = marshmallow_fields.Str(data_key="authentication_protocol", allow_none=True)
    r""" Authentication protocol.

Valid choices:

* none
* md5
* sha
* sha2_256 """

    privacy_password = marshmallow_fields.Str(data_key="privacy_password", allow_none=True)
    r""" Privacy protocol password.

Example: p@**GOandCLCt*200 """

    privacy_protocol = marshmallow_fields.Str(data_key="privacy_protocol", allow_none=True)
    r""" Privacy protocol.

Valid choices:

* none
* des
* aes128 """

    @property
    def resource(self):
        return Usm

    gettable_fields = [
        "links",
        "authentication_protocol",
        "privacy_protocol",
    ]
    """links,authentication_protocol,privacy_protocol,"""

    patchable_fields = [
        "authentication_protocol",
        "privacy_protocol",
    ]
    """authentication_protocol,privacy_protocol,"""

    postable_fields = [
        "authentication_password",
        "authentication_protocol",
        "privacy_password",
        "privacy_protocol",
    ]
    """authentication_password,authentication_protocol,privacy_password,privacy_protocol,"""


class Usm(Resource):

    _schema = UsmSchema
