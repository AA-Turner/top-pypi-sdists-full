import json
import operator
from functools import reduce

import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_filters.constants import EMPTY_VALUES

from wbcore.filters.mixins import WBCoreFilterMixin
from wbcore.forms import ContentTypeMultiValueField


class MultipleChoiceContentTypeFilter(WBCoreFilterMixin, django_filters.Filter):
    field_class = ContentTypeMultiValueField
    filter_type = "text"

    def _validate_initial_with_request(self, initial, request, name):
        initial = super()._validate_initial_with_request(initial, request, name)
        if initial:
            initial = json.dumps(initial)
        return initial

    def __init__(self, object_id_label="object_id", content_type_label="content_type", **kwargs):
        self.object_id_label = object_id_label
        self.content_type_label = content_type_label
        super().__init__(**kwargs)

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        conditions = [
            (
                Q(**{self.content_type_label: ContentType.objects.get_for_model(val)})
                & Q(**{self.object_id_label: val.id})
            )
            for val in filter(None, value)
        ]
        if conditions:
            qs = qs.filter(reduce(operator.or_, conditions))
        else:
            qs = qs.none()
        if self.distinct:
            qs = qs.distinct()
        return qs
