r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["WebauthnCredentialsPublicKey", "WebauthnCredentialsPublicKeySchema"]
__pdoc__ = {
    "WebauthnCredentialsPublicKeySchema.resource": False,
    "WebauthnCredentialsPublicKeySchema.opts": False,
    "WebauthnCredentialsPublicKey": False,
}


class WebauthnCredentialsPublicKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebauthnCredentialsPublicKey object"""

    algorithm = marshmallow_fields.Str(data_key="algorithm", allow_none=True)
    r""" Public key algorithm.

Example: ES-256 """

    value = marshmallow_fields.Str(data_key="value", allow_none=True)
    r""" Public key value.

Example: xxxxxxxxxxxxxxxxxxxxxe5sZohRRv2B10JjjALXmGRmEfFIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxYr2+w== """

    @property
    def resource(self):
        return WebauthnCredentialsPublicKey

    gettable_fields = [
        "algorithm",
        "value",
    ]
    """algorithm,value,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WebauthnCredentialsPublicKey(Resource):

    _schema = WebauthnCredentialsPublicKeySchema
