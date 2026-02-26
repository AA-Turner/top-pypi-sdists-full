import itertools
from urllib.parse import quote

import django_filters
from django_filters.filters import MultipleChoiceField

from wbcore.filters.mixins import WBCoreFilterMixin


class WBCoreChoiceFilterMixin(WBCoreFilterMixin):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["choices"] = list()
        if callable(self.choices):
            choice_keys = [
                choice[0] for choice in self.field.choices
            ]  # we save the choices key for validation in case we narrow down the choices list in get_representation
            # we get a new choices set but make sure its keys are still valid regarding the initial choices
            choices = list(filter(lambda x: x[0] in choice_keys, self.choices(request, view)))
        else:
            choices = self.choices

        for choice in choices:
            lookup_expr["input_properties"]["choices"].append(
                {"value": quote(choice[0]) if isinstance(choice[0], str) else choice[0], "label": choice[1]}
            )
        return representation, lookup_expr


class ChoiceFilter(WBCoreChoiceFilterMixin, django_filters.ChoiceFilter):
    filter_type = "select"


class WBCoreMultipleChoiceField(MultipleChoiceField):
    def to_python(self, value):
        # We do this because DRF wrap a coma seperated list of choices into a one list element
        if value and isinstance(value, list):
            value = list(itertools.chain(*[v.split(",") for v in value]))
        return super().to_python(value)


class MultipleChoiceFilter(WBCoreChoiceFilterMixin, django_filters.MultipleChoiceFilter):
    field_class = WBCoreMultipleChoiceField
    filter_type = "select"

    def _parse_request_initial(self, request_initial):
        return request_initial.split(",")

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["multiple"] = True
        if (initial := lookup_expr["input_properties"].get("initial")) and not isinstance(initial, list):
            lookup_expr["input_properties"]["initial"] = [initial]
        return representation, lookup_expr
