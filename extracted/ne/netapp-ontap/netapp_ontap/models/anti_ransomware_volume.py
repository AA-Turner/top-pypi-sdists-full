r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolume", "AntiRansomwareVolumeSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeSchema.resource": False,
    "AntiRansomwareVolumeSchema.opts": False,
    "AntiRansomwareVolume": False,
}


class AntiRansomwareVolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolume object"""

    attack_detected_by = marshmallow_fields.Str(data_key="attack_detected_by", allow_none=True)
    r""" This field specifies whether the attack was reported by `File Analysis` or `Encrypted data percentage analysis`.

Valid choices:

* file_analysis
* encryption_percentage_analysis """

    attack_detection_parameters = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_attack_detection_parameters.AntiRansomwareVolumeAttackDetectionParametersSchema", unknown=EXCLUDE, data_key="attack_detection_parameters", allow_none=True)
    r""" The attack_detection_parameters field of the anti_ransomware_volume. """

    attack_probability = marshmallow_fields.Str(data_key="attack_probability", allow_none=True)
    r""" Probability of a ransomware attack.<br>`none` No suspected ransomware activity.<br>`low` Minimally suspected ransomware activity.<br>`moderate` Moderately suspected ransomware activity.<br>`high` Significantly suspected ransomware activity.

Valid choices:

* none
* low
* moderate
* high """

    attack_reports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_attack_report.AntiRansomwareAttackReportSchema", unknown=EXCLUDE, allow_none=True), data_key="attack_reports", allow_none=True)
    r""" The attack_reports field of the anti_ransomware_volume. """

    block_device_detection_start_time = ImpreciseDateTime(data_key="block_device_detection_start_time", allow_none=True)
    r""" This field specifies the block device evaluation start time. """

    block_device_detection_state = marshmallow_fields.Str(data_key="block_device_detection_state", allow_none=True)
    r""" This field specifies the block device attack detection status. <br> `evaluation_period` Attack detection is currently in its evaluation phase. <br> `active_unsuitable_workload` Attack detection is active, but the current workload is not suitable for Anti-ransomware protection. <br> `active_suitable_workload` Attack detection is active, and the current workload is appropriate for Anti-ransomware protection.

Valid choices:

* evaluation_period
* active_unsuitable_workload
* active_suitable_workload """

    dry_run_start_time = ImpreciseDateTime(data_key="dry_run_start_time", allow_none=True)
    r""" Time when Anti-ransomware monitoring `state` is set to dry-run value for starting evaluation mode. """

    event_log = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_event_log.AntiRansomwareVolumeEventLogSchema", unknown=EXCLUDE, data_key="event_log", allow_none=True)
    r""" The event_log field of the anti_ransomware_volume. """

    space = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_space.AntiRansomwareVolumeSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the anti_ransomware_volume. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Anti-ransomware state.<br>`disabled` Anti-ransomware monitoring is disabled on the volume. This is the default state in a POST operation.<br>`disable_in_progress` Anti-ransomware monitoring is being disabled and a cleanup operation is in effect. Valid in GET operation.<br>`dry_run` Anti-ransomware monitoring is enabled in the evaluation mode.<br>`enabled` Anti-ransomware monitoring is active on the volume.<br>`paused` Anti-ransomware monitoring is paused on the volume.<br>`enable_paused` Anti-ransomware monitoring is paused on the volume from its earlier enabled state. Valid in GET operation. <br>`dry_run_paused` Anti-ransomware monitoring is paused on the volume from its earlier dry_run state. Valid in GET operation. <br>For POST, the valid Anti-ransomware states are only `disabled`, `enabled` and `dry_run`, whereas for PATCH, `paused` is also valid along with the three valid states for POST.

Valid choices:

* disabled
* disable_in_progress
* dry_run
* enabled
* paused
* enable_paused
* dry_run_paused """

    surge_as_normal = marshmallow_fields.Boolean(data_key="surge_as_normal", allow_none=True)
    r""" Indicates whether or not to set the surge values as historical values. This field is no longer supported. Use update_baseline_from_surge instead. """

    surge_usage = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_surge_usage.AntiRansomwareVolumeSurgeUsageSchema", unknown=EXCLUDE, data_key="surge_usage", allow_none=True)
    r""" Usage values of the volume's workload during surge. This object is no longer supported use surge_statistics instead. """

    suspect_files = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_suspect_files.AntiRansomwareVolumeSuspectFilesSchema", unknown=EXCLUDE, allow_none=True), data_key="suspect_files", allow_none=True)
    r""" The suspect_files field of the anti_ransomware_volume. """

    typical_usage = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_typical_usage.AntiRansomwareVolumeTypicalUsageSchema", unknown=EXCLUDE, data_key="typical_usage", allow_none=True)
    r""" Typical usage values of volume workload. This object is no longer supported use historical_statistics instead. """

    update_baseline_from_surge = marshmallow_fields.Boolean(data_key="update_baseline_from_surge", allow_none=True)
    r""" Sets the observed surge value as the new baseline on a volume. """

    workload = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_workload.AntiRansomwareVolumeWorkloadSchema", unknown=EXCLUDE, data_key="workload", allow_none=True)
    r""" The workload field of the anti_ransomware_volume. """

    @property
    def resource(self):
        return AntiRansomwareVolume

    gettable_fields = [
        "attack_detected_by",
        "attack_detection_parameters",
        "attack_probability",
        "attack_reports",
        "block_device_detection_start_time",
        "block_device_detection_state",
        "dry_run_start_time",
        "event_log",
        "space",
        "state",
        "surge_as_normal",
        "surge_usage",
        "suspect_files",
        "typical_usage",
        "update_baseline_from_surge",
        "workload",
    ]
    """attack_detected_by,attack_detection_parameters,attack_probability,attack_reports,block_device_detection_start_time,block_device_detection_state,dry_run_start_time,event_log,space,state,surge_as_normal,surge_usage,suspect_files,typical_usage,update_baseline_from_surge,workload,"""

    patchable_fields = [
        "attack_detection_parameters",
        "event_log",
        "state",
        "surge_as_normal",
        "update_baseline_from_surge",
        "workload",
    ]
    """attack_detection_parameters,event_log,state,surge_as_normal,update_baseline_from_surge,workload,"""

    postable_fields = [
        "attack_detection_parameters",
        "event_log",
        "state",
        "surge_as_normal",
        "update_baseline_from_surge",
        "workload",
    ]
    """attack_detection_parameters,event_log,state,surge_as_normal,update_baseline_from_surge,workload,"""


class AntiRansomwareVolume(Resource):

    _schema = AntiRansomwareVolumeSchema
