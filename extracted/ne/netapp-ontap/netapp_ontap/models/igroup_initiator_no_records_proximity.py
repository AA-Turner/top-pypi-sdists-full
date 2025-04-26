r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorNoRecordsProximity", "IgroupInitiatorNoRecordsProximitySchema"]
__pdoc__ = {
    "IgroupInitiatorNoRecordsProximitySchema.resource": False,
    "IgroupInitiatorNoRecordsProximitySchema.opts": False,
    "IgroupInitiatorNoRecordsProximity": False,
}


class IgroupInitiatorNoRecordsProximitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorNoRecordsProximity object"""

    local_svm = marshmallow_fields.Boolean(data_key="local_svm", allow_none=True)
    r""" A boolean that indicates if the initiator is proximal to the SVM of the containing initiator group. This is required for any POST or PATCH that includes the `proximity` sub-object. """

    peer_svms = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_list_item_proximity_peer_svms.IgroupInitiatorListItemProximityPeerSvmsSchema", unknown=EXCLUDE, allow_none=True), data_key="peer_svms", allow_none=True)
    r""" An array of remote peer SVMs to which the initiator is proximal. """

    @property
    def resource(self):
        return IgroupInitiatorNoRecordsProximity

    gettable_fields = [
        "local_svm",
        "peer_svms.links",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.links,peer_svms.name,peer_svms.uuid,"""

    patchable_fields = [
        "local_svm",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.name,peer_svms.uuid,"""

    postable_fields = [
        "local_svm",
        "peer_svms.name",
        "peer_svms.uuid",
    ]
    """local_svm,peer_svms.name,peer_svms.uuid,"""


class IgroupInitiatorNoRecordsProximity(Resource):

    _schema = IgroupInitiatorNoRecordsProximitySchema
