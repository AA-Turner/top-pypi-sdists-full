r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DiskErrorInfo", "DiskErrorInfoSchema"]
__pdoc__ = {
    "DiskErrorInfoSchema.resource": False,
    "DiskErrorInfoSchema.opts": False,
    "DiskErrorInfo": False,
}


class DiskErrorInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DiskErrorInfo object"""

    reason = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="reason", allow_none=True)
    r""" The message and code detailing the error state of this disk. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Disk error type.

Valid choices:

* onepath
* onedomain
* control
* foreign
* toobig
* toosmall
* invalidblocksize
* targetasymmap
* deviceassymmap
* failovermisconfig
* unknown
* netapp
* fwdownrev
* qualfail
* diskfail
* notallflashdisk """

    @property
    def resource(self):
        return DiskErrorInfo

    gettable_fields = [
        "reason",
        "type",
    ]
    """reason,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DiskErrorInfo(Resource):

    _schema = DiskErrorInfoSchema
