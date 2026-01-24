from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from wbcore import filters
from wbcore.contrib.content_type.utils import (
    get_ancestors_content_type,
    get_view_content_type_id,
)

from .models import Tag


class TagFilterMixin(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        endpoint=Tag.get_representation_endpoint(),
        value_key=Tag.get_representation_value_key(),
        label_key=Tag.get_representation_label_key(),
        label="Tags",
        filter_params=lambda request, view: {"content_type": get_view_content_type_id(view)},
        queryset=Tag.objects.all(),
    )


class TagFilterSet(filters.FilterSet):
    content_type = filters.ModelMultipleChoiceFilter(
        endpoint="wbcore:content_type:contenttyperepresentation-list",
        value_key="id",
        label_key="{{app_label}} | {{model}}",
        queryset=ContentType.objects.all(),
        method="filter_content_type",
    )

    def filter_content_type(self, queryset, label, value):
        if value:
            content_types = list(chain(*[get_ancestors_content_type(content_type) for content_type in value]))
            return queryset.filter(Q(content_type__isnull=True) | Q(content_type__in=content_types))
        return queryset

    class Meta:
        model = Tag
        fields = {"title": ["icontains", "exact"], "description": ["icontains"], "groups": ["exact"]}
