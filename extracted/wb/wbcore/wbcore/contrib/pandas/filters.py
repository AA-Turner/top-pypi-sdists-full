"""
Provide Filters for Pandas based views
"""

import operator
from functools import reduce

from rest_framework.filters import OrderingFilter, SearchFilter

from wbcore import filters as wb_filters
from wbcore.filters import DjangoFilterBackend
from wbcore.filters.utils import check_required_filters


class PandasDjangoFilterBackend(DjangoFilterBackend):
    lookups_operator = {
        "lte": operator.le,
        "lt": operator.lt,
        "gte": operator.ge,
        "gt": operator.gt,
        "exact": operator.eq,
    }

    def filter_queryset(self, request, queryset, view):
        filterset_class = self.get_filterset_class(view, queryset)
        if filterset_class and callable(filterset_class):
            kwargs = self.get_filterset_kwargs(request, queryset, view)
            filterset = filterset_class(**kwargs)
            if filterset.is_valid():
                check_required_filters(request, view, filterset)
        return super().filter_queryset(request, queryset, view)

    def filter_dataframe(self, request, df, view):
        if not df.empty:
            filterset_class = self.get_filterset_class(view, view.get_queryset())
            if filterset_class and callable(filterset_class):
                kwargs = self.get_filterset_kwargs(request, view.get_queryset(), view)
                filter_terms = filterset_class(**kwargs).form.data
                conditions = []
                for filter_term, value in filter_terms.items():
                    if _filter := getattr(filterset_class.Meta, "df_fields", {}).get(filter_term, None):
                        # We support only number for now
                        lookup_expr = getattr(_filter, "lookup_expr", "exact")
                        if isinstance(_filter, wb_filters.NumberFilter):
                            try:
                                conditions.append(
                                    self.lookups_operator[lookup_expr](
                                        df[_filter.field_name],
                                        float(value) if not _filter.percent else float(value) / 100,
                                    )
                                )
                            except ValueError:
                                pass
                if conditions:
                    df = df[reduce(operator.and_, conditions)]
        return df


class PandasSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        return queryset

    def filter_dataframe(self, request, df, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        search_fields = [field for field in search_fields if field in df.columns]

        if not search_fields or not search_terms or df.empty:
            return df

        conditions = []

        for search_term in search_terms:
            queries = [
                df[field].str.contains(search_term, na=False, case=False, regex=False) for field in search_fields
            ]
            conditions.append(reduce(operator.or_, queries))

        df = df[reduce(operator.and_, conditions)]

        return df


class PandasOrderingFilter(OrderingFilter):
    def get_ordering(self, request, df, view) -> tuple[list[str], list[bool]]:
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        base_ordering_fields = view.get_ordering_fields()
        potential_ordering_fields = params.split(",") if params else self.get_default_ordering(view)
        ordering_res = []
        ascending_res = []
        if potential_ordering_fields:
            for ordering_field in potential_ordering_fields:
                ordering_field = ordering_field.strip()
                ascending = True
                if ordering_field.startswith("-"):
                    ordering_field = ordering_field[1:]
                    ascending = False

                if ordering_field in df.columns and ordering_field in base_ordering_fields:
                    ordering_res.append(ordering_field)
                    ascending_res.append(ascending)
        return ordering_res, ascending_res

    def filter_queryset(self, request, queryset, view):
        return queryset

    def filter_dataframe(self, request, df, view):
        ordering_by, ascending_list = self.get_ordering(request, df, view)
        if ordering_by and ascending_list:
            df.sort_values(by=list(ordering_by), ascending=list(ascending_list), inplace=True)
        return df
