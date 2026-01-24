from datetime import date, datetime, timedelta

import pytz
from django.core.exceptions import ValidationError
from psycopg.types.range import DateRange, TimestampRange, TimestamptzRange
from rest_framework import serializers
from rest_framework.settings import api_settings
from timezone_field.choices import standard, with_gmt_offset
from timezone_field.rest_framework import TimeZoneSerializerField

from .mixins import RangeMixin, WBCoreSerializerFieldMixin
from .number import NumberFieldMixin
from .types import WBCoreType


class DateTimeField(WBCoreSerializerFieldMixin, serializers.DateTimeField):
    field_type = WBCoreType.DATETIME.value


class DateField(WBCoreSerializerFieldMixin, serializers.DateField):
    field_type = WBCoreType.DATE.value


class TimeField(WBCoreSerializerFieldMixin, serializers.TimeField):
    field_type = WBCoreType.TIME.value


class ShortcutMixin(WBCoreSerializerFieldMixin):
    def __init__(self, shortcuts: list | None = None, *args, **kwargs):
        self.shortcuts = shortcuts
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        if self.shortcuts is not None:
            representation["shortcuts"] = self.shortcuts
        return key, representation


class DateRangeBoundedValidator:
    """
    Ensure a psycopg DateRange has both lower and upper bounds set (no None).
    """

    def __call__(self, value):
        # Accept empty values the usual DRF way; let `required` handle presence.
        if value is None:
            return

        # DateRange / DateTimeTZRange objects expose .lower and .upper. [web:30][web:44]
        lower = getattr(value, "lower", None)
        upper = getattr(value, "upper", None)

        if lower is None or upper is None:
            raise ValidationError("This range must have both a lower and an upper bound.")


class DateRangeField(RangeMixin, ShortcutMixin, serializers.DateField):
    field_type = WBCoreType.DATERANGE.value
    internal_field = DateRange
    default_validators = [DateRangeBoundedValidator()]

    def __init__(
        self,
        *args,
        outward_bounds_transform="[)",
        inward_bounds_transform="[)",
        **kwargs,
    ):
        self.outward_bounds_transform = outward_bounds_transform  # Allow to specify another bound representation than the default and used for db (]. If specified, will switch the range around to and from the serializer
        self.inward_bounds_transform = inward_bounds_transform
        if self.outward_bounds_transform not in ["[]", "[)", "()", "(]"]:
            raise ValueError(f"Outward bound transform {self.outward_bounds_transform} is not a valid choice")
        if self.inward_bounds_transform not in ["[]", "[)", "()", "(]"]:
            raise ValueError(f"Inward bound transform {self.inward_bounds_transform} is not a valid choice")

        super().__init__(*args, **kwargs)

    def _transform_range(self, lower, upper, inward=False):
        """
        Private utility function that shift the range by one operator
        Args:
            lower: Lower bound
            upper: Upper bound
            inverse: If True, the transform is back to its original bound transform

        Returns:
            The shifted bound
        """
        bound_transform = self.inward_bounds_transform if inward else self.outward_bounds_transform
        if lower and bound_transform[0] == "(":
            lower = lower + timedelta(days=1) if inward else lower - timedelta(days=1)
        if upper and bound_transform[1] == "]":
            upper = upper + timedelta(days=1) if inward else upper - timedelta(days=1)
        return lower, upper


class DateTimeRangeField(RangeMixin, ShortcutMixin, serializers.DateTimeField):
    field_type = WBCoreType.DATETIMERANGE.value
    internal_field = TimestamptzRange
    default_validators = [DateRangeBoundedValidator()]

    def __init__(self, *args, lower_time_choices=None, upper_time_choices=None, **kwargs):
        self.lower_time_choices = lower_time_choices
        if (
            self.lower_time_choices
            and not isinstance(self.lower_time_choices, list)
            and not callable(self.lower_time_choices)
        ):
            raise ValueError("lower_time_choices can only be a static list or a callable.")
        self.upper_time_choices = upper_time_choices
        if (
            self.upper_time_choices
            and not isinstance(self.upper_time_choices, list)
            and not callable(self.upper_time_choices)
        ):
            raise ValueError("upper_time_choices can only be a static list or a callable.")
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        if self.lower_time_choices is not None:
            if callable(self.lower_time_choices):
                representation["lower_time_choices"] = self.lower_time_choices(self, request)
            else:
                representation["lower_time_choices"] = self.lower_time_choices

        if self.upper_time_choices is not None:
            if callable(self.upper_time_choices):
                representation["upper_time_choices"] = self.upper_time_choices(self, request)
            else:
                representation["upper_time_choices"] = self.upper_time_choices
        return key, representation


class TimeRange(RangeMixin, ShortcutMixin, serializers.TimeField):
    field_type = WBCoreType.TIMERANGE.value
    internal_field = TimestampRange

    def __init__(self, *args, timerange_fields: tuple[str, str] | None = None, **kwargs):
        self.timerange_fields = timerange_fields
        super().__init__(*args, **kwargs)
        self.default_date_repr = date.min.strftime(getattr(self, "format", api_settings.DATE_FORMAT))
        if self.timerange_fields:
            self.source = "*"

    def _transform_range(self, lower, upper, **kwargs):
        if isinstance(lower, datetime):
            lower = lower.time()
        if isinstance(upper, datetime):
            upper = upper.time()
        return lower, upper

    def get_attribute(self, instance):
        if self.timerange_fields:
            return [getattr(instance, self.timerange_fields[0]), getattr(instance, self.timerange_fields[1])]
        return super().get_attribute(instance)

    def to_internal_value(self, data):
        ts_range = super().to_internal_value(data)
        if self.timerange_fields:
            return dict(zip(self.timerange_fields, (ts_range.lower, ts_range.upper), strict=False))
        return ts_range


class DurationField(NumberFieldMixin, WBCoreSerializerFieldMixin, serializers.DurationField):
    field_type = WBCoreType.DURATION.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = 0


class TimeZoneField(WBCoreSerializerFieldMixin, TimeZoneSerializerField):
    field_type = WBCoreType.SELECT.value

    def __init__(self, choices=None, choices_display=None, *args, **kwargs):
        if choices:
            values, displays = zip(*choices, strict=False)
        else:
            values = pytz.common_timezones
            displays = None

        if choices_display == "WITH_GMT_OFFSET":
            choices = with_gmt_offset(values, use_pytz=self.use_pytz)
        elif choices_display == "STANDARD":
            choices = standard(values)
        elif choices_display is None:
            choices = zip(values, displays, strict=False) if displays else standard(values)
        else:
            raise ValueError(f"Unrecognized value for kwarg 'choices_display' of '{choices_display}'")

        self.choices = choices
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["choices"] = [{"value": k, "label": v} for k, v in self.choices]
        return key, representation
