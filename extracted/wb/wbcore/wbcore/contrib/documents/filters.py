from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from wbcore import filters as wb_filters
from wbcore.contrib.documents.models import (
    Document,
    DocumentType,
    ShareableLink,
    ShareableLinkAccess,
)


class ShareableLinkFilter(wb_filters.FilterSet):
    valid = wb_filters.BooleanFilter(label=_("Valid"), method="boolean_is_valid")
    valid_until = wb_filters.DateTimeRangeFilter(
        label="Valid Until",
    )
    link = wb_filters.CharFilter(label=_("Link"), method="filter_uuid")

    def filter_uuid(self, queryset, name, value):
        if value:
            return queryset.filter(Q(uuid__icontains=value))
        return queryset

    def boolean_is_valid(self, queryset, name, value):
        if value is not None:
            return queryset.filter(valid=value)
        return queryset

    class Meta:
        model = ShareableLink
        fields = {"one_time_link": ["exact"], "document": ["exact"]}


class ShareableLinkAccessFilter(wb_filters.FilterSet):
    clearable = (False,)
    accessed = wb_filters.DateTimeRangeFilter(
        label="Accessed between date",
    )

    class Meta:
        model = ShareableLinkAccess
        fields = {"shareable_link": ["exact"]}


class DocumentFilter(wb_filters.FilterSet):
    document_type = wb_filters.ModelChoiceFilter(
        label=_("Document Types"),
        queryset=DocumentType.objects.all(),
        endpoint=DocumentType.get_representation_endpoint(),
        value_key=DocumentType.get_representation_value_key(),
        label_key=DocumentType.get_representation_label_key(),
        method="filter_document_type",
    )

    def filter_document_type(self, queryset, name, value):
        if value:
            return queryset.filter(document_type__in=value.get_descendants(include_self=True))
        return queryset

    class Meta:
        model = Document
        fields = {"name": ["exact", "icontains"], "system_created": ["exact"], "updated": ["lte", "gte"]}


class DocumentTypeFilter(wb_filters.FilterSet):
    document_count__lte = wb_filters.NumberFilter(
        label=_("Document Count"),
        field_name="document_count",
        lookup_expr="lte",
    )

    document_count__gte = wb_filters.NumberFilter(
        label=_("Document Count"),
        field_name="document_count",
        lookup_expr="gte",
    )

    class Meta:
        model = DocumentType
        fields = {"parent": ["exact"], "name": ["exact", "icontains"]}
