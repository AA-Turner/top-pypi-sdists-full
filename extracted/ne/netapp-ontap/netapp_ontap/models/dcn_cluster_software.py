r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnClusterSoftware", "DcnClusterSoftwareSchema"]
__pdoc__ = {
    "DcnClusterSoftwareSchema.resource": False,
    "DcnClusterSoftwareSchema.opts": False,
    "DcnClusterSoftware": False,
}

class DcnClusterSoftwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnClusterSoftware object"""

    version = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_version", "DcnVersionSchema"),
                unknown=EXCLUDE,
                data_key="version",
                allow_none=True
            )
    r""" This contains DCN version information. """

    @property
    def resource(self):
        return DcnClusterSoftware

    gettable_fields = [
        "version",
    ]
    """version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnClusterSoftware(Resource):

    _schema = DcnClusterSoftwareSchema
