import json
from contextlib import suppress
from functools import cached_property

import numpy as np
import pandas as pd
from django.core.cache import cache
from django.db.models import QuerySet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from wbcore.cache.mixins import CacheMixin
from wbcore.contrib.pandas import fields
from wbcore.contrib.pandas.filters import PandasDjangoFilterBackend, PandasOrderingFilter, PandasSearchFilter
from wbcore.contrib.pandas.metadata import PandasMetadata
from wbcore.metadata.mixins import WBCoreMetadataConfigViewMixin
from wbcore.utils.renderers import BrowsableAPIRendererWithoutForms
from wbcore.viewsets.encoders import PandasDataCustomRenderer
from wbcore.viewsets.mixins import DocumentationMixin, MessageMixin


class PandasMixin(CacheMixin):
    filter_backends = [
        PandasOrderingFilter,
        PandasSearchFilter,
        PandasDjangoFilterBackend,
    ]

    metadata_class = PandasMetadata
    pagination_class = None
    filterset_fields = {}
    search_fields = []
    ordering_fields = []

    renderer_classes = [PandasDataCustomRenderer, BrowsableAPIRendererWithoutForms]

    # CACHE FRAMEWORK METHODS
    @cached_property
    def df(self) -> pd.DataFrame:
        if not hasattr(self, "_df"):
            setattr(self, "_df", self._get_dataframe())
        return getattr(self, "_df")

    # BASIC DATAFRAME GENERATION FRAMEWORK METHODS
    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def filter_dataframe(self, df, **kwargs):
        for backend in list(self.filter_backends):
            if hasattr(backend, "filter_dataframe"):
                df = backend().filter_dataframe(self.request, df, self)
        return df

    def _sanitize_dataframe(self, df):
        pd_fields = self.get_pandas_fields(self.request)
        # Ensure the returned data satisfy the primitive field type
        for field in pd_fields.fields:
            if isinstance(field, fields.PKField) and field.key not in df.columns:
                with suppress(
                    IndexError
                ):  # if df is empty with an empty multi-index, the pandas subrountine fails with an IndexError
                    df = df.reset_index(names=field.key)
            if field.key in df.columns:
                df.loc[:, field.key] = field.to_representation(df[field.key])
        with pd.option_context("future.no_silent_downcasting", True):
            return (
                df.drop(columns=df.columns.difference(pd_fields.to_dict().keys()))
                .infer_objects(copy=False)
                .replace(
                    {
                        np.nan: None,
                        np.inf: "Infinity",
                        -np.inf: "-Infinity",
                    }
                )
            )

    def get_queryset(self):
        assert hasattr(self, "queryset"), "Either specify a queryset or implement the get_queryset method."
        return self.queryset

    def get_dataframe(self, request, queryset, **kwargs):
        assert self.get_pandas_fields(request), "No pandas_fields specified"
        return pd.DataFrame(queryset.values(*self.get_pandas_fields(request).to_dict().keys()))

    def manipulate_dataframe(self, df):
        return df

    def _get_dataframe(self, **kwargs):
        df = pd.DataFrame()
        queryset = self.get_queryset()
        if queryset.exists():
            if self.cache_enabled:
                df = self._get_cached_res()
            if df.empty:
                self.extra_cache_kwargs = {}
                queryset = self.filter_queryset(queryset)
                df = self.manipulate_dataframe(self.get_dataframe(self.request, queryset, **kwargs))
                # we loop over the other cached kwargs and set them as class attributes
                for k, v in self.extra_cache_kwargs.items():
                    setattr(self, k, v)
                if self.cache_enabled:
                    cached_res = self.serialize_cache_results(df)
                    cache.set(self._get_cache_key(), cached_res, timeout=self._get_cache_timeout())
        else:
            df = pd.DataFrame(
                columns=[field.key for field in self.get_pandas_fields(self.request).fields]
            )  # if queryset is empty, we make sure the returning df contains all the columns to avoid keyerrors exception
        setattr(self, "_df", df)
        df = self.filter_dataframe(df, **kwargs)
        return df

    def get_aggregates(self, request, df):
        return {}

    def get_pandas_fields(self, request):
        return getattr(self, "pandas_fields", None)


class PandasAPIView(MessageMixin, PandasMixin, WBCoreMetadataConfigViewMixin, DocumentationMixin, APIView):
    """
    IMPORTANT: This view will be deprecated. Please us PandasAPIViewSet and register it though the router
    """

    def get(self, request, **kwargs):
        self.request = request
        df = self._sanitize_dataframe(self._get_dataframe(**kwargs))
        aggregates = self.get_aggregates(request, df) if not df.empty else {}
        results = json.loads(
            df.to_json(orient="records", force_ascii=False)
        )  # We do that to benefiate from the PandasJSONEncoder
        data = {"results": results, "aggregates": aggregates}
        data["messages"] = list(self._get_messages(request))
        return Response()


class PandasAPIViewSet(
    MessageMixin, PandasMixin, WBCoreMetadataConfigViewMixin, DocumentationMixin, ListModelMixin, GenericViewSet
):
    def list(self, request, *args, **kwargs):
        self.request = request
        df = self._sanitize_dataframe(self._get_dataframe(**kwargs))
        aggregates = self.get_aggregates(request, df) if not df.empty else {}
        results = json.loads(
            df.to_json(orient="records", force_ascii=False)
        )  # We do that to benefiate from the PandasJSONEncoder
        data = {"results": results, "aggregates": aggregates}
        data["messages"] = list(self._get_messages(request))
        return Response(data)

    def get_serializer(self, *args, **kwargs):
        return None
