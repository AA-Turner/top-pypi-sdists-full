r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerAuthentication", "ClusterPeerAuthenticationSchema"]
__pdoc__ = {
    "ClusterPeerAuthenticationSchema.resource": False,
    "ClusterPeerAuthenticationSchema.opts": False,
    "ClusterPeerAuthentication": False,
}


class ClusterPeerAuthenticationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerAuthentication object"""

    expiry_time = marshmallow_fields.Str(data_key="expiry_time", allow_none=True)
    r""" The time when the passphrase will expire, in ISO 8601 duration format or date and time format.  The default is 1 hour.

Example: P1DT2H3M4S or '2017-01-25T11:20:13Z' """

    generate_passphrase = marshmallow_fields.Boolean(data_key="generate_passphrase", allow_none=True)
    r""" Auto generate a passphrase when true. """

    in_use = marshmallow_fields.Str(data_key="in_use", allow_none=True)
    r""" The in_use field of the cluster_peer_authentication.

Valid choices:

* ok
* absent
* revoked """

    passphrase = marshmallow_fields.Str(data_key="passphrase", allow_none=True)
    r""" A password to authenticate the cluster peer relationship. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_peer_authentication.

Valid choices:

* ok
* absent
* pending
* problem """

    @property
    def resource(self):
        return ClusterPeerAuthentication

    gettable_fields = [
        "expiry_time",
        "in_use",
        "passphrase",
        "state",
    ]
    """expiry_time,in_use,passphrase,state,"""

    patchable_fields = [
        "expiry_time",
        "generate_passphrase",
        "in_use",
        "passphrase",
    ]
    """expiry_time,generate_passphrase,in_use,passphrase,"""

    postable_fields = [
        "expiry_time",
        "generate_passphrase",
        "in_use",
        "passphrase",
    ]
    """expiry_time,generate_passphrase,in_use,passphrase,"""


class ClusterPeerAuthentication(Resource):

    _schema = ClusterPeerAuthenticationSchema
