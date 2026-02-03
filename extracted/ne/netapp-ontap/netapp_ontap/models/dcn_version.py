r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnVersion", "DcnVersionSchema"]
__pdoc__ = {
    "DcnVersionSchema.resource": False,
    "DcnVersionSchema.opts": False,
    "DcnVersion": False,
}

class DcnVersionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnVersion object"""

    full = marshmallow_fields.Str(data_key="full", allow_none=True)
    r""" The full version string.

Example: 9.18.1U0 Wed Jan 15 18:20:57 UTC 2026 """

    generation = Size(data_key="generation", allow_none=True)
    r""" The generation portion of the version.

Example: 9 """

    major = Size(data_key="major", allow_none=True)
    r""" The major portion of the version.

Example: 4 """

    minor = Size(data_key="minor", allow_none=True)
    r""" The minor portion of the version.

Example: 0 """

    patch = marshmallow_fields.Str(data_key="patch", allow_none=True)
    r""" The patch portion of the version.

Example: U2 """

    @property
    def resource(self):
        return DcnVersion

    gettable_fields = [
        "full",
        "generation",
        "major",
        "minor",
        "patch",
    ]
    """full,generation,major,minor,patch,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnVersion(Resource):

    _schema = DcnVersionSchema
