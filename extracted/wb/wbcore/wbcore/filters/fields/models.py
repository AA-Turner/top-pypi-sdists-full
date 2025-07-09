from typing import Iterable

import django_filters
from django.core.exceptions import ObjectDoesNotExist
from django.forms.widgets import SelectMultiple, TextInput
from django.utils.http import urlencode
from django_filters.fields import ModelChoiceField, ModelMultipleChoiceField
from rest_framework.exceptions import ParseError
from rest_framework.reverse import reverse

from wbcore.filters.mixins import WBCoreFilterMixin


class ModelChoiceFilterMixin(WBCoreFilterMixin):
    MULTIPLE: bool = False

    def _validate_initial_with_request(self, initial, request, name):
        if request_default := request.GET.get(name):
            return request_default.split(",")
        return initial

    @classmethod
    def get_parsed_values(cls, queryset, value_ids: int | str | Iterable[int]):
        if isinstance(value_ids, str):
            value_ids = value_ids.split(",")
        elif isinstance(value_ids, int):
            value_ids = [value_ids]

        if isinstance(value_ids, list):
            for value_id in value_ids:
                try:
                    yield {
                        "value": value_id,
                        "label": str(queryset.get(id=value_id)),
                    }
                except ObjectDoesNotExist:
                    raise ParseError("Filter value invalid")

    def get_representation(self, request, name, view):
        representation, lookup_expr = super().get_representation(request, name, view)
        lookup_expr["input_properties"]["multiple"] = self.MULTIPLE

        queryset = self.get_queryset(request)

        if hasattr(queryset.model, "get_label_key"):
            label_key = queryset.model.get_label_key()
        else:
            label_key = self.label_key

        url = reverse(self.endpoint, request=request)
        if self.filter_params:
            if callable(self.filter_params):
                filter_params = self.filter_params(request, view)
            else:
                filter_params = self.filter_params
            # we need to convert any list into comma seperated string
            for key, value in filter_params.items():
                if isinstance(value, list):
                    filter_params[key] = ",".join(map(lambda x: str(x), value))

            url += f"?{urlencode(filter_params, doseq=True)}"
        lookup_expr["input_properties"]["endpoint"] = {
            "url": url,
            "value_key": self.value_key,
            "label_key": label_key,
        }

        if initial_ids := lookup_expr["input_properties"].get("initial", None):
            values = self.get_parsed_values(queryset, initial_ids)
            lookup_expr["input_properties"]["initial"] = list(values) if self.MULTIPLE else next(values)

        return representation, lookup_expr


class ModelMultipleChoiceFilter(ModelChoiceFilterMixin, django_filters.ModelMultipleChoiceFilter):
    class SimpleModelMultipleChoiceField(ModelMultipleChoiceField):
        """
        field class that define a simple text input as widget (instead of select). This is necessary in order to use the
        browsable api for model with a lot of items. Without it, the widget would load all the queryset option and will probably destroy the performance
        """

        class SimpleSelectMultiple(SelectMultiple):
            template_name = "django/forms/widgets/text.html"

        widget = SimpleSelectMultiple

    MULTIPLE: bool = True
    field_class = SimpleModelMultipleChoiceField
    filter_type = "select"

    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop("endpoint", None)
        self.filter_params = kwargs.pop("filter_params", None)
        self.value_key = kwargs.pop("value_key", None)
        self.label_key = kwargs.pop("label_key", None)
        # TODO: This is monkeypatched. Make sure that the CSVWidget is set here and only here!
        if "widget" not in kwargs:
            kwargs["widget"] = django_filters.widgets.CSVWidget
        super().__init__(*args, **kwargs)

        # django filter sets it to True by default. In our case, the fitlering will happen on primary keys, so we do not expect any duplicate. Furthermore, for table without explicit unique constraint, using "distinct" leads to unexpected results (i.e. row with same value are dropped)
        self.distinct = False


class ModelChoiceFilter(ModelChoiceFilterMixin, django_filters.ModelChoiceFilter):
    class SimpleModelChoiceField(ModelChoiceField):
        """
        field class that define a simple text input as widget (instead of select). This is necessary in order to use the
        browsable api for model with a lot of items. Without it, the widget would load all the queryset option and will probably destroy the performance
        """

        widget = TextInput

    field_class = SimpleModelChoiceField
    filter_type = "select"
    MULTIPLE: bool = False

    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop("endpoint", None)
        self.value_key = kwargs.pop("value_key", None)
        self.filter_params = kwargs.pop("filter_params", None)
        self.label_key = kwargs.pop("label_key", None)
        super().__init__(*args, **kwargs)
