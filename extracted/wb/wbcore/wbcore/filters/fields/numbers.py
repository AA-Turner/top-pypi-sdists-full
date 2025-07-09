import django_filters

from wbcore.filters.mixins import WBCoreFilterMixin
from wbcore.serializers import WBCoreType


class NumberFilter(WBCoreFilterMixin, django_filters.NumberFilter):
    filter_type = "number"

    def __init__(self, precision: int = 0, percent: bool = False, disable_formatting: bool = False, *args, **kwargs):
        self.precision = precision
        self.percent = percent
        self.disable_formatting = disable_formatting
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["precision"] = self.precision
        if self.percent:  # TODO: Discuss with Christoph if this is necessary like this
            lookup_expr["input_properties"]["type"] = WBCoreType.PERCENT.value
            lookup_expr["input_properties"]["precision"] = max(self.precision - 2, 0)
        lookup_expr["input_properties"]["disable_formatting"] = self.disable_formatting
        return representation, lookup_expr

    def filter(self, qs, value):
        if self.percent and value is not None:
            value /= 100
        return super().filter(qs, value)


class YearFilter(NumberFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disable_formatting = True


class RangeSelectFilter(NumberFilter):
    filter_type = "rangeselect"

    def __init__(self, precision=2, *args, **kwargs):
        self.precision = precision
        self.color = kwargs.pop("color", "rgb(133, 144, 162)")
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["color"] = self.color
        return representation, lookup_expr
