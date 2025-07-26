r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareStorageUnit", "AntiRansomwareStorageUnitSchema"]
__pdoc__ = {
    "AntiRansomwareStorageUnitSchema.resource": False,
    "AntiRansomwareStorageUnitSchema.opts": False,
    "AntiRansomwareStorageUnit": False,
}


class AntiRansomwareStorageUnitSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareStorageUnit object"""

    attack_probability = marshmallow_fields.Str(data_key="attack_probability", allow_none=True)
    r""" The probability of a ransomware attack.<br/>
Possible values:

* `none` No suspected ransomware activity.
* `moderate` Suspected ransomware activity.


Valid choices:

* none
* moderate """

    attack_reports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_storage_unit_attack_reports.AntiRansomwareStorageUnitAttackReportsSchema", unknown=EXCLUDE, allow_none=True), data_key="attack_reports", allow_none=True)
    r""" The attack_reports field of the anti_ransomware_storage_unit. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The anti-ransomware state for the storage unit.<br/>
Possible values:

* `disabled` Anti-ransomware monitoring is disabled for the storage unit. Valid in PATCH and GET.
* `disable_in_progress` Anti-ransomware monitoring is being disabled and a clean-up operation is in progress. Valid in GET.
* `enabled` Anti-ransomware monitoring is active for the storage unit. Valid in PATCH and GET.
* `paused` Anti-ransomware monitoring is paused for the storage unit from its earlier enabled state. Valid in PATCH and GET.


Valid choices:

* disabled
* disable_in_progress
* enabled
* paused """

    @property
    def resource(self):
        return AntiRansomwareStorageUnit

    gettable_fields = [
        "attack_probability",
        "attack_reports",
        "state",
    ]
    """attack_probability,attack_reports,state,"""

    patchable_fields = [
        "state",
    ]
    """state,"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareStorageUnit(Resource):

    _schema = AntiRansomwareStorageUnitSchema
