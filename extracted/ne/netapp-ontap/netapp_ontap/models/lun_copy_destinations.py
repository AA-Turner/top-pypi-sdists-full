r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunCopyDestinations", "LunCopyDestinationsSchema"]
__pdoc__ = {
    "LunCopyDestinationsSchema.resource": False,
    "LunCopyDestinationsSchema.opts": False,
    "LunCopyDestinations": False,
}


class LunCopyDestinationsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunCopyDestinations object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_copy_destinations. """

    max_throughput = Size(data_key="max_throughput", allow_none=True)
    r""" The maximum data throughput, in bytes per second, that should be utilized in support of the LUN copy. See property `copy.source.max_throughput` for further details. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The fully qualified path of the LUN copy destination composed of a "/vol" prefix, the volume name, the optional qtree name, and base name of the LUN.


Example: /vol/vol1/lun1 """

    peer = marshmallow_fields.Nested("netapp_ontap.resources.svm_peer.SvmPeerSchema", unknown=EXCLUDE, data_key="peer", allow_none=True)
    r""" The peer field of the lun_copy_destinations. """

    progress = marshmallow_fields.Nested("netapp_ontap.models.lun_copy_destinations_progress.LunCopyDestinationsProgressSchema", unknown=EXCLUDE, data_key="progress", allow_none=True)
    r""" Properties related to the progress of an active or recently completed LUN copy. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the LUN copy destination.


Example: 1bc327d5-4654-5284-a116-f182282240b4 """

    @property
    def resource(self):
        return LunCopyDestinations

    gettable_fields = [
        "links",
        "max_throughput",
        "name",
        "peer.links",
        "peer.name",
        "peer.uuid",
        "progress",
        "uuid",
    ]
    """links,max_throughput,name,peer.links,peer.name,peer.uuid,progress,uuid,"""

    patchable_fields = [
        "peer.name",
        "peer.uuid",
        "progress",
    ]
    """peer.name,peer.uuid,progress,"""

    postable_fields = [
        "peer.name",
        "peer.uuid",
        "progress",
    ]
    """peer.name,peer.uuid,progress,"""


class LunCopyDestinations(Resource):

    _schema = LunCopyDestinationsSchema
