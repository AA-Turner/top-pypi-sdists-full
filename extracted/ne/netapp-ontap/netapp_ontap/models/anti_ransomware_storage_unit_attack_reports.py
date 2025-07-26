r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareStorageUnitAttackReports", "AntiRansomwareStorageUnitAttackReportsSchema"]
__pdoc__ = {
    "AntiRansomwareStorageUnitAttackReportsSchema.resource": False,
    "AntiRansomwareStorageUnitAttackReportsSchema.opts": False,
    "AntiRansomwareStorageUnitAttackReports": False,
}


class AntiRansomwareStorageUnitAttackReportsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareStorageUnitAttackReports object"""

    time = ImpreciseDateTime(data_key="time", allow_none=True)
    r""" Timestamp at which ransomware attack is observed.


Example: 2021-06-01T15:06:41.000+0000 """

    @property
    def resource(self):
        return AntiRansomwareStorageUnitAttackReports

    gettable_fields = [
        "time",
    ]
    """time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareStorageUnitAttackReports(Resource):

    _schema = AntiRansomwareStorageUnitAttackReportsSchema
