r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TotpPost", "TotpPostSchema"]
__pdoc__ = {
    "TotpPostSchema.resource": False,
    "TotpPostSchema.opts": False,
    "TotpPost": False,
}


class TotpPostSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TotpPost object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the totp_post. """

    account = marshmallow_fields.Nested("netapp_ontap.resources.account.AccountSchema", unknown=EXCLUDE, data_key="account", allow_none=True)
    r""" The account field of the totp_post. """

    comment = marshmallow_fields.Str(data_key="comment", allow_none=True)
    r""" Optional comment for the TOTP profile. """

    emergency_codes = marshmallow_fields.List(marshmallow_fields.Str, data_key="emergency_codes", allow_none=True)
    r""" TOTP profile emergency codes for a user. These codes are for emergency use when a user cannot access 2FA codes through other means.

Example: "17503785" """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Status of the TOTP profile.

Example: true """

    install_url = marshmallow_fields.Str(data_key="install_url", allow_none=True)
    r""" TOTP profile installation URL for a user. """

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="owner", allow_none=True)
    r""" The owner field of the totp_post. """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm """

    secret_key = marshmallow_fields.Str(data_key="secret_key", allow_none=True)
    r""" TOTP profile secret key for a user. """

    sha_fingerprint = marshmallow_fields.Str(data_key="sha_fingerprint", allow_none=True)
    r""" SHA fingerprint for the TOTP secret key. """

    verification_code = marshmallow_fields.Str(data_key="verification_code", allow_none=True)
    r""" TOTP profile verification code for a user. """

    @property
    def resource(self):
        return TotpPost

    gettable_fields = [
        "links",
        "account.links",
        "account.name",
        "comment",
        "emergency_codes",
        "enabled",
        "install_url",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "scope",
        "secret_key",
        "sha_fingerprint",
        "verification_code",
    ]
    """links,account.links,account.name,comment,emergency_codes,enabled,install_url,owner.links,owner.name,owner.uuid,scope,secret_key,sha_fingerprint,verification_code,"""

    patchable_fields = [
        "account.name",
        "comment",
        "enabled",
    ]
    """account.name,comment,enabled,"""

    postable_fields = [
        "account.name",
        "comment",
        "owner.name",
        "owner.uuid",
    ]
    """account.name,comment,owner.name,owner.uuid,"""


class TotpPost(Resource):

    _schema = TotpPostSchema
