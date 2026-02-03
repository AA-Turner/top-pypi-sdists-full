r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeSoftware", "DcnNodeSoftwareSchema"]
__pdoc__ = {
    "DcnNodeSoftwareSchema.resource": False,
    "DcnNodeSoftwareSchema.opts": False,
    "DcnNodeSoftware": False,
}

class DcnNodeSoftwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeSoftware object"""

    compatibility = marshmallow_fields.Str(data_key="compatibility", allow_none=True)
    r""" Indicates whether the node's software version is compatible with the ONTAP cluster. A node is considered compatible if its software release is not newer than the ONTAP cluster's release, and not more than four major versions older. This field helps determine if the node can join or be used to form the DCN cluster.


Valid choices:

* full
* incompatible """

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_version", "DcnVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" This contains DCN version information. """

    @property
    def resource(self):
        return DcnNodeSoftware

    gettable_fields = [
        "compatibility",
        "version",
    ]
    """compatibility,version,"""

    patchable_fields = [
        "compatibility",
    ]
    """compatibility,"""

    postable_fields = [
        "compatibility",
    ]
    """compatibility,"""


class DcnNodeSoftware(Resource):

    _schema = DcnNodeSoftwareSchema
