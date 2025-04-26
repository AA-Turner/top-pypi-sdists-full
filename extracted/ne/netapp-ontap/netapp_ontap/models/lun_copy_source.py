r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunCopySource", "LunCopySourceSchema"]
__pdoc__ = {
    "LunCopySourceSchema.resource": False,
    "LunCopySourceSchema.opts": False,
    "LunCopySource": False,
}


class LunCopySourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunCopySource object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the lun_copy_source. """

    max_throughput = Size(data_key="max_throughput", allow_none=True)
    r""" The maximum data throughput, in bytes per second, that should be utilized in support of the LUN copy. This property can be used to throttle a transfer and limit its impact on the performance of the source and destination nodes. The specified value will be rounded up to the nearest megabyte.<br/>
If this property is not specified in a POST that begins a LUN copy, throttling is not applied to the data transfer.<br/>
For more information, see _Size properties_ in the _docs_ section of the ONTAP REST API documentation.<br/>
Valid only in a POST that begins a LUN copy or a PATCH when a LUN copy is already in process. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The fully qualified path of the LUN copy source composed of a "/vol" prefix, the volume name, the optional qtree name, and base name of the LUN.<br/>
Set this property in POST to specify the source for a LUN copy operation.


Example: /vol/vol2/lun1 """

    peer = marshmallow_fields.Nested("netapp_ontap.resources.svm_peer.SvmPeerSchema", unknown=EXCLUDE, data_key="peer", allow_none=True)
    r""" The peer field of the lun_copy_source. """

    progress = marshmallow_fields.Nested("netapp_ontap.models.lun_copy_source_progress.LunCopySourceProgressSchema", unknown=EXCLUDE, data_key="progress", allow_none=True)
    r""" Properties related to the progress of an active or recently completed LUN copy. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the LUN copy source.<br/>
Set this property in POST to specify the source for a LUN copy operation.


Example: 03c05019-40d9-3945-c767-dca4c3be5e90 """

    @property
    def resource(self):
        return LunCopySource

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
        "max_throughput",
        "peer.name",
        "peer.uuid",
        "progress",
    ]
    """max_throughput,peer.name,peer.uuid,progress,"""

    postable_fields = [
        "max_throughput",
        "name",
        "peer.name",
        "peer.uuid",
        "uuid",
    ]
    """max_throughput,name,peer.name,peer.uuid,uuid,"""


class LunCopySource(Resource):

    _schema = LunCopySourceSchema
