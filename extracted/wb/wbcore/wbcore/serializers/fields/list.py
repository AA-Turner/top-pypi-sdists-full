import enum

from rest_framework import serializers
from rest_framework.fields import empty

from .mixins import WBCoreSerializerFieldMixin
from .types import WBCoreType


class ListFieldMixin:
    def get_attribute(self, instance):
        # Can't have any relationships if not created
        try:
            return super().get_attribute(instance)

        except (AttributeError, KeyError):
            return []

    def run_validation(self, data=empty):
        # If the data is send through form data, we need to convert the data into a proper list of ids
        if data not in [None, empty] and len(data) == 1 and isinstance(data[0], str) and "," in data[0]:
            data = data[0].split(",")

        # If the data is a list of an empty string we need to convert it (FORM DATA)
        if data not in [None, empty] and len(data) == 1 and isinstance(data[0], str) and data[0] == "":
            data = []

        # If the data is a list and contains the string null, then we need to convert it (FORM DATA)
        if data == ["null"]:
            data = []

        # If the data is None and null is an allowed value, data needs to be set to an empty list
        if data is None and self.allow_null:
            data = []
        return super().run_validation(data)


class ListField(ListFieldMixin, WBCoreSerializerFieldMixin, serializers.ListField):
    field_type = WBCoreType.LIST.value


class SparklineField(WBCoreSerializerFieldMixin, serializers.ListField):
    """Readonly field to create a sparline representation from an annotated aggregated array

    Important: This is potentially very slow, use accordingly

    Example:
        View:
            def get_queryset(self):
                return super().get_queryset().annotate(
                    prices_date=ArrayAgg("prices__date", filter=Q(prices__date__gt="2023-03-01")),
                    prices_price=ArrayAgg("prices__net_value", filter=Q(prices__date__gt="2023-03-01"))
                )

        Serializer:
            prices_sparkline = wb_serializers.SparklineField(x_data_label="prices_date", y_data_label="prices_price")
    """

    field_type = WBCoreType.SPARKLINE.value

    class Type(enum.Enum):
        LINE = "line"
        BAR = "bar"
        COLUMN = "column"
        AREA = "area"

    def __init__(
        self, *args, x_data_label=None, y_data_label=None, sparkline_type=Type.LINE, sparkline_option=None, **kwargs
    ):
        """
        Args:
            *args: based serializer positional argument
            x_data_label: The field name as find in the serialized object representative the easting data
            y_data_label: The field name as find in the serialized object representive the northing data
            sparkline_type: Either one of LINE, BAR, COLUMN or AREA
            sparkline_option: a json serializable dictionary representing additional option as allowed by ag-grid.
            **kwargs:based serializer keyword argument
        """
        self.x_data_label = x_data_label
        self.y_data_label = y_data_label
        self.sparkline_type = sparkline_type
        kwargs.pop("read_only", None)
        if not sparkline_option:
            sparkline_option = {}
        self.sparkline_option = sparkline_option
        super().__init__(*args, read_only=True, **kwargs)

    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["read_only"] = True
        representation["sparkline_type"] = self.sparkline_type.value
        representation["sparkline_option"] = self.sparkline_option
        return key, representation

    def to_representation(self, obj):
        representation = [[]]  # if row is [] or null, we default to an empty list of list
        if (x_data := getattr(obj, self.x_data_label, None)) and (y_data := getattr(obj, self.y_data_label, None)):
            representation = zip(x_data, y_data, strict=False)
        return representation
