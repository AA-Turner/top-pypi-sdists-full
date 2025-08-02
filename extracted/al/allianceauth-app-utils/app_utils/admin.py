"""Utilities for the admin site."""

from collections import Counter

from django.contrib import admin
from django.db.models import Count


class FieldFilterCountsMemory(admin.SimpleListFilter):
    """Filter by field and show counts for admin site.

    Counts are calculated in memory.
    """

    field_name = ""  # field to filter by

    def lookups(self, request, model_admin: admin.ModelAdmin):
        """:meta private:"""
        field_in_rows = model_admin.get_queryset(request).values_list(
            self.field_name, flat=True
        )
        field_counts = Counter(field_in_rows)
        result = [
            (field, f"{field} ({count:,})") for field, count in field_counts.items()
        ]
        return sorted(result, key=lambda obj: obj[0])

    def queryset(self, request, queryset):
        """:meta private:"""
        if self.value():
            params = {self.field_name: self.value()}
            return queryset.filter(**params)


class FieldFilterCountsDb(admin.SimpleListFilter):
    """Filter by field and show counts for admin site.

    Counts are calculated by the database.
    """

    field_name = ""  # field to filter by

    def lookups(self, request, model_admin: admin.ModelAdmin):
        """:meta private:"""
        qs = model_admin.get_queryset(request)
        field = qs.model._meta.get_field(self.field_name)
        if not field.choices:
            qs = qs.exclude(**{self.field_name: ""})
        field_counts = (
            qs.values(self.field_name)
            .annotate(num_words=Count(self.field_name))
            .order_by(self.field_name)
        )
        if field.choices:
            field_counts = self.__map_choices_field(field, field_counts)
            result = [
                (
                    obj[self.field_name][0],
                    f'{obj[self.field_name][1]} ({obj["num_words"]:,})',
                )
                for obj in field_counts
            ]
        else:
            result = [
                (obj[self.field_name], f'{obj[self.field_name]} ({obj["num_words"]:,})')
                for obj in field_counts
            ]
        return result

    def __map_choices_field(self, field, field_counts):
        """Map choices field values to corresponding labels and keep values."""
        mapper = {obj[0]: obj[1] for obj in field.choices}
        field_counts = [
            {
                self.field_name: (obj[self.field_name], mapper[obj[self.field_name]]),
                "num_words": obj["num_words"],
            }
            for obj in field_counts
        ]
        return field_counts

    def queryset(self, request, queryset):
        """:meta private:"""
        if self.value():
            params = {self.field_name: self.value()}
            return queryset.filter(**params)
