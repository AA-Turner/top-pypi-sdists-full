from django.core.exceptions import FieldError
from django.db import models


class PandasFilterSetMixin:
    def filter_queryset(self, queryset):
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        for name, value in self.form.cleaned_data.items():
            try:
                queryset = self.filters[name].filter(queryset, value)
            except FieldError:
                pass
            if not isinstance(queryset, models.QuerySet):
                raise AssertionError(
                    "Expected '%s.%s' to return a QuerySet, but got a %s instead."
                    % (
                        type(self).__name__,
                        name,
                        type(queryset).__name__,
                    )
                )
        return queryset
