import logging
from contextlib import suppress

from django.contrib.postgres.fields import DateRangeField, DateTimeRangeField
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import GeneratedField
from django.db.models.fields.related import ManyToManyRel, ManyToOneRel, OneToOneRel
from django_filters.filterset import FilterSetMetaclass, remote_queryset, settings
from django_filters.rest_framework import FilterSet as DjangoFilterSet

from wbcore.filters import fields
from wbcore.filters.fields.multiple_lookups import MultipleLookupFilter
from wbcore.models.fields import YearField
from wbcore.signals.filters import add_filters

from .utils import check_required_filters

logger = logging.getLogger(__name__)


def _is_number(field):
    return (
        issubclass(field.__class__, models.DecimalField)
        or issubclass(field.__class__, models.FloatField)
        or issubclass(field.__class__, models.IntegerField)
    )


class CustomFilterSetMetaClass(FilterSetMetaclass):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if _meta := getattr(new_class, "Meta", None):
            for parent_field_name, child_fields in getattr(_meta, "flatten_fields", dict()).items():
                if remote_field := getattr(_meta.model._meta.get_field(parent_field_name), "remote_field", None):
                    for child_field_name, lookup_exps in child_fields.items():
                        child_field = remote_field.model._meta.get_field(child_field_name)
                        if _is_number(child_field):
                            nested_field_name = f"{parent_field_name}__{child_field_name}"
                            for lookup_exp in lookup_exps:
                                new_class.base_filters[f"{nested_field_name}__{lookup_exp}"] = fields.NumberFilter(
                                    field_name=nested_field_name,
                                    lookup_expr=lookup_exp,
                                    precision=2,
                                    label=child_field.verbose_name,
                                )

                        # TODO extend with other filter fields type
        return new_class

    @classmethod
    def get_declared_filters(cls, bases, attrs):
        filters = super().get_declared_filters(bases, attrs)

        multi_filters: list[tuple[str, MultipleLookupFilter]] = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in list(attrs.items())
            if isinstance(obj, MultipleLookupFilter)
        ]

        for field_name, filter in multi_filters:
            filters |= filter.get_filters(field_name)

        return filters


class FilterSet(DjangoFilterSet, metaclass=CustomFilterSetMetaClass):
    FILTER_DEFAULTS = {
        models.BooleanField: {"filter_class": fields.BooleanFilter},
        models.NullBooleanField: {"filter_class": fields.BooleanFilter},
        models.CharField: {"filter_class": fields.CharFilter},
        models.TextField: {"filter_class": fields.CharFilter},
        models.SlugField: {"filter_class": fields.CharFilter},
        models.EmailField: {"filter_class": fields.CharFilter},
        models.FilePathField: {"filter_class": fields.CharFilter},
        models.UUIDField: {"filter_class": fields.CharFilter},
        models.URLField: {"filter_class": fields.CharFilter},
        models.GenericIPAddressField: {"filter_class": fields.CharFilter},
        models.CommaSeparatedIntegerField: {"filter_class": fields.CharFilter},
        models.DateField: {"filter_class": fields.DateFilter},
        models.DateTimeField: {"filter_class": fields.DateTimeFilter},
        models.TimeField: {"filter_class": fields.TimeFilter},
        models.IntegerField: {"filter_class": fields.NumberFilter},
        models.FloatField: {"filter_class": fields.NumberFilter},
        models.DecimalField: {"filter_class": fields.NumberFilter},
        DateTimeRangeField: {"filter_class": fields.DateTimeRangeFilter},
        DateRangeField: {"filter_class": fields.DateRangeFilter},
        YearField: {"filter_class": fields.YearFilter},
        # models.DurationField: {"filter_class": DurationFilter},
        # models.SmallIntegerField: {"filter_class": NumberFilter},
        # models.AutoField: {"filter_class": NumberFilter},
        # models.PositiveIntegerField: {"filter_class": NumberFilter},
        # models.PositiveSmallIntegerField: {"filter_class": NumberFilter},
        # models.UUIDField: {"filter_class": UUIDFilter},
        # Forward relationships
        models.OneToOneField: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
                "to_field_name": f.remote_field.field_name,
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        models.ForeignKey: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
                "to_field_name": f.remote_field.field_name,
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        models.ManyToManyField: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
            },
        },
        # Reverse relationships
        OneToOneRel: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        ManyToOneRel: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
            },
        },
        ManyToManyRel: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "endpoint": f.related_model.get_representation_endpoint(),
                "value_key": f.related_model.get_representation_value_key(),
                "label_key": f.related_model.get_representation_label_key(),
            },
        },
    }

    @classmethod
    def filter_class_for_remote_filter(cls):
        if hasattr(cls, "get_filter_class_for_remote_filter") and callable(cls.get_filter_class_for_remote_filter()):
            return cls.get_filter_class_for_remote_filter()
        return cls

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, view=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        remote_filters = add_filters.send(sender=self.filter_class_for_remote_filter(), request=request)
        self.view = view
        for _, res in remote_filters:
            if res:
                for remote_filter_key, remote_filter in res.items():
                    setattr(remote_filter, "column_field_name", remote_filter_key)
                    self.filters[remote_filter_key] = remote_filter

    @classmethod
    def filter_for_lookup(cls, field, lookup_type):
        if isinstance(field, GeneratedField):
            return cls.filter_for_lookup(field.output_field, lookup_type)
        if lookup_type == "exact" and getattr(field, "choices", None):
            filter_class, params = fields.ChoiceFilter, {"choices": field.choices}
        else:
            filter_class, params = super().filter_for_lookup(field, lookup_type)

        # Check if it is a decimal field:
        if hasattr(field, "decimal_places"):
            params["precision"] = field.decimal_places

        if hasattr(field, "verbose_name"):
            params["label"] = field.verbose_name

        return filter_class, params

    @classmethod
    def get_dependency_map(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "dependency_map", dict()).items()

    @classmethod
    def get_filters(cls):
        filters = super().get_filters()
        remote_filters = add_filters.send(sender=cls.filter_class_for_remote_filter())
        for _, res in remote_filters:
            if res:
                for remote_filter_key, remote_filter in res.items():
                    setattr(remote_filter, "column_field_name", remote_filter_key)
                    filters[remote_filter_key] = remote_filter

        for field, help_text in getattr(cls, "help_texts", {}).items():
            filters[field].help_text = help_text

        # Get dependency map specified in Meta and append the argument accordingly
        for field, values in cls.get_dependency_map():
            for value in values:
                filters[field].depends_on.append({"field": value, "options": {}})
        return filters

    def extract_required_field_labels(self):
        return [label for label, filter in self.base_filters.items() if getattr(filter, "required", False)]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        check_required_filters(self.request, self.view, self)
        return queryset

    def fake_filter(self, queryset, name, value):
        return queryset

    # we enable for all filterset a way to easily narrow down the result based on related name not null
    notnull_related_name = fields.CharFilter(hidden=True, method="filter_notnull_related_name")

    def filter_notnull_related_name(self, queryset, name, value):
        if value:
            with suppress(FieldError):
                return queryset.filter(**{f"{value}__isnull": False}).distinct()
        return queryset
