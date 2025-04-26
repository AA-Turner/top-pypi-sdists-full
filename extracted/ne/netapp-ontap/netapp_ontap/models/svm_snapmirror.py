r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SvmSnapmirror", "SvmSnapmirrorSchema"]
__pdoc__ = {
    "SvmSnapmirrorSchema.resource": False,
    "SvmSnapmirrorSchema.opts": False,
    "SvmSnapmirror": False,
}


class SvmSnapmirrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmSnapmirror object"""

    is_protected = marshmallow_fields.Boolean(data_key="is_protected", allow_none=True)
    r""" Specifies whether the SVM is a SnapMirror source SVM, using SnapMirror to protect its data. """

    protected_consistency_group_count = Size(data_key="protected_consistency_group_count", allow_none=True)
    r""" Specifies the number of SVM DR protected consistency groups in the SVM. """

    protected_volumes_count = Size(data_key="protected_volumes_count", allow_none=True)
    r""" Specifies the number of SVM DR protected volumes in the SVM. """

    @property
    def resource(self):
        return SvmSnapmirror

    gettable_fields = [
        "is_protected",
        "protected_consistency_group_count",
        "protected_volumes_count",
    ]
    """is_protected,protected_consistency_group_count,protected_volumes_count,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SvmSnapmirror(Resource):

    _schema = SvmSnapmirrorSchema
