from psycopg.types.range import NumericRange
from rest_framework import serializers

from .mixins import RangeMixin, WBCoreSerializerFieldMixin, decorator
from .types import DisplayMode, WBCoreType

percent_decorator = decorator(position="right", value="%", decorator_type="text")


class NumberFieldMixin:
    def __init__(
        self,
        *args,
        percent=False,
        display_mode=DisplayMode.DECIMAL,
        precision=2,
        signed: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.percent = percent
        self.disable_formatting = getattr(self, "disable_formatting", kwargs.pop("disable_formatting", False))
        self.display_mode = display_mode
        self.precision = kwargs.get("decimal_places", precision)
        self.max_digits = kwargs.get("max_digits", 34)
        self.signed = signed

    def set_precision(self, precision):
        self.precision = precision
        self._kwargs["precision"] = self.precision

    def set_percent(self, percent):
        self.percent = percent
        self._kwargs["percent"] = self.percent

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["display_mode"] = self.display_mode.value
        representation["precision"] = self.precision
        representation["max_digits"] = self.max_digits
        representation["disable_formatting"] = self.disable_formatting
        representation["signed"] = self.signed

        if self.percent:  # TODO: Discuss with Christoph if this is necessary like this
            representation["type"] = WBCoreType.PERCENT.value
            representation["precision"] = self.precision - 2
        return key, representation


class IntegerField(NumberFieldMixin, WBCoreSerializerFieldMixin, serializers.IntegerField):
    field_type = WBCoreType.NUMBER.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = 0


class YearField(IntegerField):
    disable_formatting = True


class DecimalField(NumberFieldMixin, WBCoreSerializerFieldMixin, serializers.DecimalField):
    field_type = WBCoreType.NUMBER.value

    # TODO: If this is used, then the validation for max_digits and decimal_fields is not done
    # def validate_precision(self, value):
    #     return value

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        field_name, representation = super().get_representation(request, field_name)

        if meta := getattr(self.parent, "Meta", None):
            odp = getattr(meta, "override_decimal_places", None)
            percent_fields = getattr(meta, "percent_fields", [])
            if odp is not None and field_name not in percent_fields:
                representation["precision"] = odp

        return field_name, representation


class FloatField(NumberFieldMixin, WBCoreSerializerFieldMixin, serializers.FloatField):
    field_type = WBCoreType.NUMBER.value


class DecimalRangeField(RangeMixin, WBCoreSerializerFieldMixin, serializers.DecimalField):
    field_type = WBCoreType.NUMBERRANGE.value
    internal_field = NumericRange

    def __init__(self, max_digits=None, decimal_places=None, **kwargs):
        if not max_digits:
            max_digits = 3
        if not decimal_places:
            decimal_places = 2
        super().__init__(max_digits, decimal_places, **kwargs)
