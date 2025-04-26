r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NfsServiceProtocol", "NfsServiceProtocolSchema"]
__pdoc__ = {
    "NfsServiceProtocolSchema.resource": False,
    "NfsServiceProtocolSchema.opts": False,
    "NfsServiceProtocol": False,
}


class NfsServiceProtocolSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsServiceProtocol object"""

    v3_64bit_identifiers_enabled = marshmallow_fields.Boolean(data_key="v3_64bit_identifiers_enabled", allow_none=True)
    r""" Specifies whether 64-bit support for NFSv3 FSIDs and file IDs is enabled. """

    v3_enabled = marshmallow_fields.Boolean(data_key="v3_enabled", allow_none=True)
    r""" Specifies whether NFSv3 protocol is enabled. """

    v3_features = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol_v3_features.NfsServiceProtocolV3FeaturesSchema", unknown=EXCLUDE, data_key="v3_features", allow_none=True)
    r""" The v3_features field of the nfs_service_protocol. """

    v40_enabled = marshmallow_fields.Boolean(data_key="v40_enabled", allow_none=True)
    r""" Specifies whether NFSv4.0 protocol is enabled. """

    v40_features = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol_v40_features.NfsServiceProtocolV40FeaturesSchema", unknown=EXCLUDE, data_key="v40_features", allow_none=True)
    r""" The v40_features field of the nfs_service_protocol. """

    v41_enabled = marshmallow_fields.Boolean(data_key="v41_enabled", allow_none=True)
    r""" Specifies whether NFSv4.1 or later protocol is enabled. """

    v41_features = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol_v41_features.NfsServiceProtocolV41FeaturesSchema", unknown=EXCLUDE, data_key="v41_features", allow_none=True)
    r""" The v41_features field of the nfs_service_protocol. """

    v42_features = marshmallow_fields.Nested("netapp_ontap.models.nfs_service_protocol_v42_features.NfsServiceProtocolV42FeaturesSchema", unknown=EXCLUDE, data_key="v42_features", allow_none=True)
    r""" The v42_features field of the nfs_service_protocol. """

    v4_64bit_identifiers_enabled = marshmallow_fields.Boolean(data_key="v4_64bit_identifiers_enabled", allow_none=True)
    r""" Specifies whether 64-bit support for NFSv4.x FSIDs and file IDs is enabled. """

    v4_fsid_change = marshmallow_fields.Boolean(data_key="v4_fsid_change", allow_none=True)
    r""" Specifies whether the change in FSID when NFSv4 clients traverse file systems is displayed. """

    v4_grace_seconds = Size(data_key="v4_grace_seconds", allow_none=True)
    r""" Specifies the grace period for clients to reclaim file locks after a server failure. """

    v4_id_domain = marshmallow_fields.Str(data_key="v4_id_domain", allow_none=True)
    r""" Specifies the domain portion of the string form of user and group
names as defined by the NFSv4 protocol. """

    v4_lease_seconds = Size(data_key="v4_lease_seconds", allow_none=True)
    r""" Specifies the lease seconds of the NFSv4 clients. If it is inactive for more than the time displayed, all of the file lock states on a node might be lost. """

    v4_session_slot_reply_cache_size = Size(data_key="v4_session_slot_reply_cache_size", allow_none=True)
    r""" Specifies the number of bytes of the reply that is cached in each NFSv4.x session slot. """

    v4_session_slots = Size(data_key="v4_session_slots", allow_none=True)
    r""" Specifies the number of entries in NFSv4.x session slot table. """

    @property
    def resource(self):
        return NfsServiceProtocol

    gettable_fields = [
        "v3_64bit_identifiers_enabled",
        "v3_enabled",
        "v3_features",
        "v40_enabled",
        "v40_features",
        "v41_enabled",
        "v41_features",
        "v42_features",
        "v4_64bit_identifiers_enabled",
        "v4_fsid_change",
        "v4_grace_seconds",
        "v4_id_domain",
        "v4_lease_seconds",
        "v4_session_slot_reply_cache_size",
        "v4_session_slots",
    ]
    """v3_64bit_identifiers_enabled,v3_enabled,v3_features,v40_enabled,v40_features,v41_enabled,v41_features,v42_features,v4_64bit_identifiers_enabled,v4_fsid_change,v4_grace_seconds,v4_id_domain,v4_lease_seconds,v4_session_slot_reply_cache_size,v4_session_slots,"""

    patchable_fields = [
        "v3_64bit_identifiers_enabled",
        "v3_enabled",
        "v3_features",
        "v40_enabled",
        "v40_features",
        "v41_enabled",
        "v41_features",
        "v42_features",
        "v4_64bit_identifiers_enabled",
        "v4_fsid_change",
        "v4_grace_seconds",
        "v4_id_domain",
        "v4_lease_seconds",
        "v4_session_slot_reply_cache_size",
        "v4_session_slots",
    ]
    """v3_64bit_identifiers_enabled,v3_enabled,v3_features,v40_enabled,v40_features,v41_enabled,v41_features,v42_features,v4_64bit_identifiers_enabled,v4_fsid_change,v4_grace_seconds,v4_id_domain,v4_lease_seconds,v4_session_slot_reply_cache_size,v4_session_slots,"""

    postable_fields = [
        "v3_64bit_identifiers_enabled",
        "v3_enabled",
        "v3_features",
        "v40_enabled",
        "v40_features",
        "v41_enabled",
        "v41_features",
        "v42_features",
        "v4_64bit_identifiers_enabled",
        "v4_fsid_change",
        "v4_grace_seconds",
        "v4_id_domain",
        "v4_lease_seconds",
        "v4_session_slot_reply_cache_size",
        "v4_session_slots",
    ]
    """v3_64bit_identifiers_enabled,v3_enabled,v3_features,v40_enabled,v40_features,v41_enabled,v41_features,v42_features,v4_64bit_identifiers_enabled,v4_fsid_change,v4_grace_seconds,v4_id_domain,v4_lease_seconds,v4_session_slot_reply_cache_size,v4_session_slots,"""


class NfsServiceProtocol(Resource):

    _schema = NfsServiceProtocolSchema
