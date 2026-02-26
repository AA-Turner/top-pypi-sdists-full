from typing import Iterable

import django_filters
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.forms.widgets import SelectMultiple, TextInput
from django.utils.http import urlencode
from django_filters.fields import ModelChoiceField, ModelMultipleChoiceField
from rest_framework.exceptions import ParseError
from rest_framework.reverse import reverse

from wbcore.filters.mixins import WBCoreFilterMixin


class ModelChoiceFilterMixin(WBCoreFilterMixin):
    MULTIPLE: bool = False

    def _parse_request_initial(self, request_initial):
        return request_initial.split(",")

    def get_parsed_values(
        self, queryset, values: int | Iterable[int] | Model | Iterable[Model]
    ) -> list[dict] | dict | None:
        if not isinstance(values, list):
            values = [values]
        parsed_values = []
        for value in values:
            if isinstance(value, int):
                try:
                    parsed_values.append(
                        {
                            "value": value,
                            "label": str(queryset.get(id=value)),
                        }
                    )
                except ObjectDoesNotExist as e:
                    raise ParseError("Filter value invalid") from e
            else:
                parsed_values.append(
                    {
                        "value": value.id,
                        "label": str(value),
                    }
                )
        if self.MULTIPLE:
            return parsed_values
        elif parsed_values:
            return parsed_values[0]

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

        if values := lookup_expr["input_properties"].get("initial", None):
            # ensure given values are in the proper representation (we expect values to be a raw int, or directly a model or a iterable of either)
            lookup_expr["input_properties"]["initial"] = self.get_parsed_values(queryset, values)

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
