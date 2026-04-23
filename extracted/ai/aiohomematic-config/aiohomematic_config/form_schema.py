"""
Form schema generator for Homematic device configuration.

Transforms ParameterData descriptions and current values into a
JSON-serializable form schema that any frontend can render.

Public API of this module is defined by __all__.
"""

from collections.abc import Mapping
import inspect
from typing import Any

from aiohomematic.ccu_translations import (
    get_channel_type_translation,
    get_device_icon,
    get_device_model_description,
    get_parameter_help,
    get_parameter_value_translation,
    get_ui_label_translation,
    resolve_channel_type,
)
from aiohomematic.const import SCHEDULE_PATTERN, ParameterData, ParameterType
from aiohomematic.easymode_data import (
    MASTER_SENDER_TYPE,
    SenderTypeMetadata,
    get_channel_metadata,
    get_cross_validation_rules,
    get_option_preset,
)
from aiohomematic.parameter_tools import (
    get_parameter_step,
    is_parameter_internal,
    is_parameter_readable,
    is_parameter_visible,
    is_parameter_writable,
)
from pydantic import BaseModel

from aiohomematic_config.const import DEFAULT_LOCALE
from aiohomematic_config.grouping import ParameterGrouper
from aiohomematic_config.labels import LabelResolver
from aiohomematic_config.link_param_metadata import classify_link_parameter, get_time_presets
from aiohomematic_config.widgets import WidgetType, determine_widget


class FormParameter(BaseModel):
    """A single parameter in a form schema."""

    id: str
    label: str
    description: str | None = None
    type: str
    widget: WidgetType
    min: float | int | None = None
    max: float | int | None = None
    step: float | None = None
    unit: str = ""
    default: Any = None
    current_value: Any = None
    writable: bool = True
    modified: bool = False
    operations: int = 0  # Raw OPERATIONS bitfield from paramset description
    options: list[str] | None = None
    option_labels: dict[str, str] | None = None

    # Link parameter metadata (optional, enriched for LINK paramsets):
    keypress_group: str | None = None
    category: str | None = None
    display_as_percent: bool = False
    has_last_value: bool = False
    hidden_by_default: bool = False
    time_pair_id: str | None = None
    time_selector_type: str | None = None
    time_presets: list[dict[str, int | str]] | None = None

    # Easymode metadata (UC2: conditional visibility):
    visible_when: dict[str, Any] | None = None
    # Easymode metadata (UC5: option presets):
    presets: list[dict[str, Any]] | None = None
    allow_custom_value: bool = False
    # Easymode metadata (UC6: subset membership):
    subset_group_id: str | None = None


class FormSection(BaseModel):
    """A logical group of parameters in a form."""

    id: str
    title: str
    parameters: list[FormParameter]


class CrossValidationConstraint(BaseModel):
    """A cross-parameter validation constraint for the form UI."""

    rule_id: str
    rule: str  # "gte", "lte", "between", "not_equal"
    applies_to_params: list[str]
    error_key: str
    param_a: str | None = None
    param_b: str | None = None
    param: str | None = None
    min_param: str | None = None
    max_param: str | None = None


class SubsetOption(BaseModel):
    """A single option in a subset group."""

    id: int
    label: str
    values: dict[str, int | float | str]


class SubsetGroup(BaseModel):
    """A group of parameters that form a combined selection."""

    id: str
    label: str
    member_params: list[str]
    options: list[SubsetOption]
    current_option_id: int | None = None


class FormSchema(BaseModel):
    """Complete form schema for a channel's paramset configuration."""

    channel_address: str
    channel_type: str
    model_description: str = ""
    channel_type_label: str = ""
    device_icon: str | None = None
    sections: list[FormSection]
    total_parameters: int
    writable_parameters: int
    # Easymode metadata (UC6: subset groups):
    subset_groups: list[SubsetGroup] | None = None
    # Easymode metadata (cross-parameter validation constraints):
    cross_validation: list[CrossValidationConstraint] | None = None


class FormSchemaGenerator:
    """
    Generate form schemas from paramset descriptions.

    Combines widget determination, parameter grouping, and label resolution
    to produce a complete, frontend-agnostic form schema.
    """

    __slots__ = ("_grouper", "_label_resolver")

    def __init__(
        self,
        *,
        locale: str = DEFAULT_LOCALE,
        label_resolver: LabelResolver | None = None,
        grouper: ParameterGrouper | None = None,
    ) -> None:
        """Initialize the form schema generator."""
        self._label_resolver = label_resolver or LabelResolver(locale=locale)
        self._grouper = grouper or ParameterGrouper(locale=locale)

    def generate(  # noqa: C901
        self,
        *,
        descriptions: Mapping[str, ParameterData],
        current_values: dict[str, Any],
        channel_address: str = "",
        channel_type: str = "",
        sender_type: str = "",
        model: str = "",
        sub_model: str | None = None,
        require_translation: bool = True,
        enrich_link_metadata: bool = False,
        is_hmip: bool = False,
    ) -> FormSchema:
        """
        Generate a complete form schema for the given paramset.

        Args:
            descriptions: Parameter descriptions (from get_paramset_description).
            current_values: Current parameter values (from get_paramset).
            channel_address: Channel address for context.
            channel_type: Channel type for grouping hints.
            sender_type: Sender channel type for easymode metadata lookup.
            model: Device model ID for description lookup.
            sub_model: Optional sub-model for description fallback.
            require_translation: If True, only include parameters with CCU translations.
                Set to False for LINK paramsets where translations are often unavailable.
            enrich_link_metadata: If True, classify each parameter and attach
                link metadata (keypress group, category, time presets, etc.).
            is_hmip: If True, resolve channel type to HmIP-specific variant
                for correct translation lookups (e.g., SHUTTER_CONTACT → SHUTTER_CONTACT_HMIP).

        Returns:
            A FormSchema ready for JSON serialization.

        """
        # Resolve channel type for HmIP devices (e.g., SHUTTER_CONTACT → SHUTTER_CONTACT_HMIP)
        channel_type = resolve_channel_type(channel_type=channel_type, is_hmip=is_hmip)

        # Filter parameters using CCU-compatible rules:
        # 1. FLAGS & VISIBLE must be set
        # 2. FLAGS & INTERNAL must NOT be set
        # 3. OPERATIONS must include READ or WRITE
        # 4. Schedule parameters (XX_WP_*, WEEK_PROGRAM_*) are excluded
        # 5. Only parameters with CCU translations are included (matches CCU WebUI easymode behavior)
        #    unless require_translation is False (e.g. for LINK paramsets)
        visible_params: dict[str, ParameterData] = {
            param_id: pd
            for param_id, pd in descriptions.items()
            if is_parameter_visible(parameter_data=pd)
            and not is_parameter_internal(parameter_data=pd)
            and (is_parameter_readable(parameter_data=pd) or is_parameter_writable(parameter_data=pd))
            and not SCHEDULE_PATTERN.match(param_id)
            and not param_id.startswith("WEEK_PROGRAM")
            and (
                not require_translation
                or self._label_resolver.has_translation(parameter_id=param_id, channel_type=channel_type)
            )
        }

        # Load easymode metadata for enrichment
        st_meta: SenderTypeMetadata | None = None
        if channel_type and (ch_meta := get_channel_metadata(channel_type=channel_type)):
            if sender_type:
                st_meta = ch_meta.sender_types.get(sender_type)
            # Fall back to _MASTER metadata for MASTER/VALUES paramsets (no sender_type)
            if st_meta is None:
                st_meta = ch_meta.sender_types.get(MASTER_SENDER_TYPE)

        # Group parameters (with metadata-based ordering when available)
        groups = self._grouper.group(
            descriptions=visible_params,
            channel_type=channel_type,
            sender_type=sender_type,
        )

        # Build sections
        sections: list[FormSection] = []
        total_params = 0
        writable_params = 0

        for group in groups:
            form_params: list[FormParameter] = []
            for param_id in group.parameters:
                if (pd := visible_params.get(param_id)) is None:
                    continue

                writable = is_parameter_writable(parameter_data=pd)
                current = current_values.get(param_id)
                default = pd.get("DEFAULT")
                modified = current is not None and default is not None and current != default
                param_type = pd.get("TYPE", ParameterType.EMPTY)

                widget = determine_widget(parameter_data=pd)
                if not writable:
                    widget = WidgetType.READ_ONLY

                # Only include min/max for numeric types
                p_min = pd.get("MIN")
                p_max = pd.get("MAX")
                has_numeric_range = isinstance(p_min, (int, float)) and isinstance(p_max, (int, float))

                # Build option_labels for VALUE_LIST parameters
                options: list[str] | None = None
                option_labels: dict[str, str] | None = None
                if "VALUE_LIST" in pd:
                    options = list(pd["VALUE_LIST"])
                    resolved_labels: dict[str, str] = {}
                    for i, value in enumerate(options):
                        translated = get_parameter_value_translation(
                            parameter=param_id,
                            value=value,
                            channel_type=channel_type or None,
                            locale=self._label_resolver.locale,
                        )
                        # Fall back to index-based lookup (easymode TCL option values
                        # are stored as parameter=N since VALUE_LIST strings are not
                        # available at extraction time). Skip value-only fallback to
                        # avoid generic matches for numeric indices like "0" or "1".
                        if translated is None:
                            translated = get_parameter_value_translation(
                                parameter=param_id,
                                value=str(i),
                                channel_type=channel_type or None,
                                locale=self._label_resolver.locale,
                                use_fallback=False,
                            )
                        resolved_labels[value] = translated or _humanize_value(value=value)
                    option_labels = resolved_labels

                form_param = FormParameter(
                    id=param_id,
                    label=self._label_resolver.resolve(
                        parameter_id=param_id,
                        channel_type=channel_type,
                    ),
                    description=get_parameter_help(
                        parameter=param_id,
                        locale=self._label_resolver.locale,
                    ),
                    type=str(param_type),
                    widget=widget,
                    min=p_min if has_numeric_range else None,
                    max=p_max if has_numeric_range else None,
                    step=get_parameter_step(parameter_data=pd) if has_numeric_range else None,
                    unit=pd.get("UNIT", ""),
                    default=default,
                    current_value=current,
                    writable=writable,
                    modified=modified,
                    operations=pd.get("OPERATIONS", 0),
                    options=options,
                    option_labels=option_labels,
                )
                if enrich_link_metadata:
                    meta = classify_link_parameter(parameter_id=param_id)
                    form_param.keypress_group = meta.keypress_group.value
                    form_param.category = meta.category.value
                    form_param.display_as_percent = meta.display_as_percent
                    form_param.hidden_by_default = meta.hidden_by_default
                    form_param.time_pair_id = meta.time_pair_id
                    if meta.time_selector_type:
                        form_param.time_selector_type = meta.time_selector_type.value
                        form_param.time_presets = get_time_presets(
                            selector_type=meta.time_selector_type,
                            locale=self._label_resolver.locale,
                        )
                    # LEVEL: has_last_value when max > 1.0
                    if meta.display_as_percent and isinstance(p_max, (int, float)) and p_max > 1.0:
                        form_param.has_last_value = True
                    else:
                        form_param.has_last_value = meta.has_last_value

                # Enrich with easymode metadata (presets, visibility, subsets)
                if st_meta:
                    self._enrich_easymode(
                        form_param=form_param,
                        st_meta=st_meta,
                        current_values=current_values,
                    )

                form_params.append(form_param)
                total_params += 1
                if writable:
                    writable_params += 1

            if form_params:
                sections.append(
                    FormSection(
                        id=group.id,
                        title=group.title,
                        parameters=form_params,
                    )
                )

        # Resolve channel type label
        channel_type_label = ""
        if channel_type:
            channel_type_label = (
                get_channel_type_translation(
                    channel_type=channel_type,
                    locale=self._label_resolver.locale,
                )
                or channel_type
            )

        # Resolve model description
        model_description = ""
        if model:
            model_description = (
                get_device_model_description(
                    model=model,
                    sub_model=sub_model,
                    locale=self._label_resolver.locale,
                )
                or ""
            )

        # Resolve device icon
        device_icon: str | None = None
        if model:
            device_icon = get_device_icon(model=model)

        # Build subset groups from easymode metadata
        subset_groups: list[SubsetGroup] | None = None
        if st_meta and st_meta.subsets:
            subset_groups = self._build_subset_groups(
                st_meta=st_meta,
                current_values=current_values,
            )

        # Build cross-validation constraints from easymode metadata
        cross_validation: list[CrossValidationConstraint] | None = None
        if st_meta and st_meta.cross_validation_rule_ids:
            all_rules = {r.id: r for r in get_cross_validation_rules()}
            constraints = [
                CrossValidationConstraint(
                    rule_id=rule.id,
                    rule=rule.rule,
                    applies_to_params=list(rule.applies_to_params),
                    error_key=rule.error_key,
                    param_a=rule.param_a,
                    param_b=rule.param_b,
                    param=rule.param,
                    min_param=rule.min_param,
                    max_param=rule.max_param,
                )
                for rule_id in st_meta.cross_validation_rule_ids
                if (rule := all_rules.get(rule_id))
            ]
            if constraints:
                cross_validation = constraints

        return FormSchema(
            channel_address=channel_address,
            channel_type=channel_type,
            model_description=model_description,
            channel_type_label=channel_type_label,
            device_icon=device_icon,
            sections=sections,
            total_parameters=total_params,
            writable_parameters=writable_params,
            subset_groups=subset_groups,
            cross_validation=cross_validation,
        )

    def _build_subset_groups(
        self,
        *,
        st_meta: SenderTypeMetadata,
        current_values: dict[str, Any],
    ) -> list[SubsetGroup]:
        """Build subset group definitions for the form schema."""
        groups: list[SubsetGroup] = []
        for subset in st_meta.subsets:
            # Check if current values match this subset
            all_match = all(current_values.get(p) == v for p, v in subset.values.items())

            options = [
                SubsetOption(
                    id=subset.id,
                    label=subset.name_key,
                    values=subset.values,
                )
            ]

            # Check if a group for these member_params already exists
            existing = next(
                (g for g in groups if set(g.member_params) == set(subset.member_params)),
                None,
            )
            if existing:
                existing.options.append(options[0])
                if all_match:
                    existing.current_option_id = subset.id
            else:
                groups.append(
                    SubsetGroup(
                        id=f"subset_{subset.member_params[0]}",
                        label=subset.name_key,
                        member_params=list(subset.member_params),
                        options=options,
                        current_option_id=subset.id if all_match else None,
                    )
                )

        return groups

    def _enrich_easymode(
        self,
        *,
        form_param: FormParameter,
        st_meta: SenderTypeMetadata,
        current_values: dict[str, Any],
    ) -> None:
        """Enrich a FormParameter with easymode metadata (presets, visibility, subsets)."""
        param_id = form_param.id

        # UC5: Option presets
        if (preset_type := st_meta.option_presets.get(param_id)) and (
            preset_def := get_option_preset(preset_type=preset_type)
        ):
            form_param.presets = [
                {
                    "value": entry.value,
                    "label": (
                        entry.label
                        or (
                            get_ui_label_translation(
                                label_key=entry.label_key,
                                locale=self._label_resolver.locale,
                            )
                            if entry.label_key
                            else None
                        )
                        or str(entry.value)
                    ),
                }
                for entry in preset_def.presets
            ]
            form_param.allow_custom_value = preset_def.allow_custom

        # UC6: Subset membership
        for subset in st_meta.subsets:
            if param_id in subset.member_params:
                form_param.subset_group_id = f"subset_{subset.id}"
                break

        # UC2: Conditional visibility
        for cv_rule in getattr(st_meta, "conditional_visibility", ()):
            if param_id in cv_rule.show:
                form_param.visible_when = {
                    "trigger_param": cv_rule.trigger,
                    "trigger_value": cv_rule.trigger_value,
                    "invert": False,
                }
                break
            if param_id in cv_rule.hide:
                form_param.visible_when = {
                    "trigger_param": cv_rule.trigger,
                    "trigger_value": cv_rule.trigger_value,
                    "invert": True,
                }
                break


def _humanize_value(*, value: str) -> str:
    """Convert a VALUE_LIST entry to a human-readable label."""
    return value.replace("_", " ").title()


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
