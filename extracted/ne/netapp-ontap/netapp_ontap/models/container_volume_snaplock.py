r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumeSnaplock", "ContainerVolumeSnaplockSchema"]
__pdoc__ = {
    "ContainerVolumeSnaplockSchema.resource": False,
    "ContainerVolumeSnaplockSchema.opts": False,
    "ContainerVolumeSnaplock": False,
}


class ContainerVolumeSnaplockSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumeSnaplock object"""

    append_mode_enabled = marshmallow_fields.Boolean(data_key="append_mode_enabled", allow_none=True)
    r""" Specifies if the volume append mode is enabled or disabled. When it is enabled, all the files created with write permissions on the volume are, by default, WORM appendable files. The user can append the data to a WORM appendable file but cannot modify the existing contents of the file nor delete the file until it expires.

Example: false """

    autocommit_period = marshmallow_fields.Str(data_key="autocommit_period", allow_none=True)
    r""" Specifies the autocommit period for SnapLock volume. All files which are not modified for a period greater than the autocommit period of the volume are committed to the WORM state. The autocommit period value represents a duration and must be specified in the ISO-8601 duration format. The autocommit period can be in years, months, days, hours, and minutes. A period specified for years, months, and days is represented in the ISO-8601 format as "P<num>Y", "P<num>M", "P<num>D" respectively, for example "P10Y" represents a duration of 10 years. A duration in hours and minutes is represented by "PT<num>H" and "PT<num>M" respectively. The period string must contain only a single time element that is, either years, months, days, hours, or minutes. A duration which combines different periods is not supported, for example "P1Y10M" is not supported. Apart from the duration specified in the ISO-8601 format, the autocommit field also accepts the string "none".

Example: P30M """

    retention = marshmallow_fields.Nested("netapp_ontap.models.volume_snaplock_retention.VolumeSnaplockRetentionSchema", unknown=EXCLUDE, data_key="retention", allow_none=True)
    r""" The retention field of the container_volume_snaplock. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The SnapLock type of the volume. <br>compliance &dash; A SnapLock Compliance(SLC) volume provides the highest level of WORM protection and an administrator cannot destroy a SLC volume if it contains unexpired WORM files. <br> enterprise &dash; An administrator can delete a SnapLock Enterprise(SLE) volume.<br> non_snaplock &dash; Indicates the volume is non-snaplock.

Valid choices:

* compliance
* enterprise
* non_snaplock """

    @property
    def resource(self):
        return ContainerVolumeSnaplock

    gettable_fields = [
        "append_mode_enabled",
        "autocommit_period",
        "retention",
        "type",
    ]
    """append_mode_enabled,autocommit_period,retention,type,"""

    patchable_fields = [
        "append_mode_enabled",
        "autocommit_period",
        "retention",
    ]
    """append_mode_enabled,autocommit_period,retention,"""

    postable_fields = [
        "append_mode_enabled",
        "autocommit_period",
        "retention",
        "type",
    ]
    """append_mode_enabled,autocommit_period,retention,type,"""


class ContainerVolumeSnaplock(Resource):

    _schema = ContainerVolumeSnaplockSchema
