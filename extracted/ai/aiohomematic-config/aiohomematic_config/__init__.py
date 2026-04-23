"""
aiohomematic-config: Presentation layer for Homematic device configuration.

Transforms Homematic device paramset descriptions into UI-optimized
structures. No RPC knowledge, no CCU access -- operates purely on data
structures from aiohomematic.

Key components:

- ``FormSchemaGenerator``: ParameterData + values -> JSON form schemas
- ``ParameterGrouper``: Flat parameter list -> grouped sections
- ``LabelResolver``: Technical IDs -> human-readable labels (i18n)
- ``ConfigSession``: Change tracking, undo/redo, dirty state
- ``ConfigExporter``: Serialize/deserialize configurations

Quick start::

    from aiohomematic_config import FormSchemaGenerator

    generator = FormSchemaGenerator(locale="en")
    schema = generator.generate(
        descriptions=descriptions,
        current_values=current_values,
        channel_type="HEATING_CLIMATECONTROL_TRANSCEIVER",
    )
    # schema is a Pydantic model, JSON-serializable
"""

from aiohomematic_config.change_log import ConfigChangeEntry, ConfigChangeLog, build_change_diff
from aiohomematic_config.const import VERSION
from aiohomematic_config.exporter import ExportedConfiguration, export_configuration, import_configuration
from aiohomematic_config.form_schema import FormParameter, FormSchema, FormSchemaGenerator, FormSection
from aiohomematic_config.grouping import ParameterGroup, ParameterGrouper
from aiohomematic_config.labels import LabelResolver
from aiohomematic_config.link_param_metadata import (
    PRESETS_BY_TYPE,
    KeypressGroup,
    LinkParamCategory,
    LinkParamMeta,
    TimePreset,
    TimeSelectorType,
    classify_link_parameter,
    decode_time_value,
    encode_time_value,
    get_time_presets,
)
from aiohomematic_config.profile_data import ChannelProfileSet, ProfileDef, ProfileParamConstraint, ResolvedProfile
from aiohomematic_config.profile_store import ProfileStore
from aiohomematic_config.schedule_facade import (
    ClimateScheduleData,
    DeviceScheduleData,
    ScheduleDeviceInfo,
    get_climate_schedule,
    get_device_schedule,
    list_schedule_devices,
    set_climate_active_profile,
    set_climate_schedule_weekday,
    set_device_schedule,
    set_schedule_enabled,
)
from aiohomematic_config.session import ConfigSession
from aiohomematic_config.widgets import WidgetType, determine_widget

__all__ = [  # noqa: RUF022
    # change_log
    "ConfigChangeEntry",
    "ConfigChangeLog",
    "build_change_diff",
    # const
    "VERSION",
    # exporter
    "ExportedConfiguration",
    "export_configuration",
    "import_configuration",
    # form_schema
    "FormParameter",
    "FormSchema",
    "FormSchemaGenerator",
    "FormSection",
    # grouping
    "ParameterGroup",
    "ParameterGrouper",
    # labels
    "LabelResolver",
    # link_param_metadata
    "KeypressGroup",
    "LinkParamCategory",
    "LinkParamMeta",
    "PRESETS_BY_TYPE",
    "TimePreset",
    "TimeSelectorType",
    "classify_link_parameter",
    "decode_time_value",
    "encode_time_value",
    "get_time_presets",
    # profile_data
    "ChannelProfileSet",
    "ProfileDef",
    "ProfileParamConstraint",
    "ResolvedProfile",
    # profile_store
    "ProfileStore",
    # schedule_facade
    "ClimateScheduleData",
    "DeviceScheduleData",
    "ScheduleDeviceInfo",
    "get_climate_schedule",
    "get_device_schedule",
    "list_schedule_devices",
    "set_climate_active_profile",
    "set_climate_schedule_weekday",
    "set_device_schedule",
    "set_schedule_enabled",
    # session
    "ConfigSession",
    # widgets
    "WidgetType",
    "determine_widget",
]
