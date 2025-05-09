r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiServiceTarget", "IscsiServiceTargetSchema"]
__pdoc__ = {
    "IscsiServiceTargetSchema.resource": False,
    "IscsiServiceTargetSchema.opts": False,
    "IscsiServiceTarget": False,
}


class IscsiServiceTargetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiServiceTarget object"""

    alias = marshmallow_fields.Str(data_key="alias", allow_none=True)
    r""" The iSCSI target alias of the iSCSI service.<br/>
The target alias can contain one (1) to 128 characters and feature any printable character except space (" "). A PATCH request with an empty alias ("") clears the alias.<br/>
Optional in POST and PATCH. In POST, this defaults to the name of the SVM.


Example: svm1 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The iSCSI target name of the iSCSI service. This is generated for the SVM during POST.<br/>
If required, the target name can be modified using the ONTAP command line.


Example: iqn.1992-08.com.netapp:sn.574caf71890911e8a6b7005056b4ea79:vs.2 """

    @property
    def resource(self):
        return IscsiServiceTarget

    gettable_fields = [
        "alias",
        "name",
    ]
    """alias,name,"""

    patchable_fields = [
        "alias",
    ]
    """alias,"""

    postable_fields = [
        "alias",
    ]
    """alias,"""


class IscsiServiceTarget(Resource):

    _schema = IscsiServiceTargetSchema
