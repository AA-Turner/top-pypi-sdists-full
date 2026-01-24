import json
import re
from enum import Enum

import plotly.graph_objects as go
from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ViewSetMixin

from wbcore.contrib.io.viewset_mixins import ImportExportDRFMixin
from wbcore.enums import WidgetType
from wbcore.filters import DjangoFilterBackend
from wbcore.fsm.mixins import FSMViewSetMixin
from wbcore.metadata.mixins import WBCoreMetadataConfigViewMixin
from wbcore.pagination import CursorPagination, LimitOffsetPagination
from wbcore.utils.renderers import BrowsableAPIRendererWithoutForms

from ..cache.mixins import CacheMixin
from .encoders import PandasDataCustomRenderer
from .generics import GenericAPIView
from .mixins import (
    ActionMixin,
    CreateModelMixin,
    DestroyModelMixin,
    DestroyMultipleModelMixin,
    DocumentationMixin,
    FilterMixin,
    ListModelMixin,
    MessageMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)


class GenericViewSet(ViewSetMixin, ActionMixin, GenericAPIView):
    pass


class ViewSet(WBCoreMetadataConfigViewMixin, DocumentationMixin, ActionMixin, ViewSet):
    def get_serializer(self):
        if hasattr(self, "serializer_class"):
            return self.serializer_class()
        return None

    def get_serializer_class(self):
        return getattr(self, "serializer_class", None)


class ReadOnlyModelViewSet(
    ImportExportDRFMixin,
    DocumentationMixin,
    WBCoreMetadataConfigViewMixin,
    RetrieveModelMixin,
    ListModelMixin,
    FilterMixin,
    GenericViewSet,
):
    pagination_class = LimitOffsetPagination
    ONLY_READ_ONLY_ENDPOINT = True


class ModelViewSet(
    ImportExportDRFMixin,
    DocumentationMixin,
    FSMViewSetMixin,
    WBCoreMetadataConfigViewMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    DestroyMultipleModelMixin,
    ListModelMixin,
    FilterMixin,
    GenericViewSet,
):
    pagination_class = LimitOffsetPagination


class ReadOnlyInfiniteModelViewSet(ReadOnlyModelViewSet):
    pagination_class = None


class RepresentationViewSet(ReadOnlyModelViewSet):
    WIDGET_TYPE = WidgetType.SELECT.value
    NO_CACHE = True
    pagination_class = CursorPagination


class InfiniteDataModelView(ModelViewSet):
    pagination_class = None


class ChartType(Enum):
    TIME_SERIES = "time_series"


class ChartViewSet(MessageMixin, ImportExportDRFMixin, FilterMixin, CacheMixin, ViewSet):
    IMPORT_ALLOWED: bool = False  # Disabled by default for chart
    EXPORT_ALLOWED: bool = False  # Disabled by default for chart

    filter_backends = [DjangoFilterBackend]
    WIDGET_TYPE = WidgetType.CHART.value
    CHART_TYPE: ChartType | None = None

    renderer_classes = [PandasDataCustomRenderer, BrowsableAPIRendererWithoutForms]

    CACHE_EMPTY_VALUE = dict()
    CACHE_MAIN_KEY = "figure_dict"

    def _get_dataframe(self) -> dict:
        figure_dict = dict()
        if self.cache_enabled:
            figure_dict = self._get_cached_res()
        if not figure_dict:
            self.extra_cache_kwargs = {}
            queryset = self.filter_queryset(self.get_queryset())
            figure = go.Figure()
            if queryset.exists():
                figure = self.get_plotly(queryset)
                figure = self.apply_style(figure)
            figure_json = figure.to_json()  # we serialize to use the default PlotlyEncoder
            figure_dict = json.loads(
                figure_json
            )  # we reserialize to be able to hijack the figure config. This adds an extra steps of serialization/deserialization but the overhead is negligable.
            if self.cache_enabled:
                cached_res = self.serialize_cache_results(figure_dict)
                cache.set(self._get_cache_key(), cached_res, timeout=self._get_cache_timeout())
        return figure_dict

    def list(self, request: Request, *args, **kwargs):
        self.request = request
        figure_dict = self._get_dataframe()
        data = self.parse_figure_dict(figure_dict)
        data["messages"] = list(self._get_messages(request))
        return Response(data)

    def get_queryset(self):
        return self.queryset

    def parse_figure_dict(self, figure_dict: dict[str, any]) -> dict[str, any]:
        figure_dict["config"] = {"responsive": True, "displaylogo": False}
        figure_dict["useResizeHandler"] = True
        figure_dict["style"] = {"width": "100%", "height": "100%", "minHeight": "300px"}
        return figure_dict

    def apply_style(self, figure: go.Figure) -> go.Figure:
        if self.CHART_TYPE is ChartType.TIME_SERIES:
            figure.update_layout(
                yaxis=dict(side="right"),
            )

        if chart_style := getattr(settings, "CHART_STYLE", None):
            return chart_style(self, figure)

        return figure

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class TimeSeriesChartViewSet(ChartViewSet):
    CHART_TYPE = ChartType.TIME_SERIES


class HTMLViewSet(MessageMixin, FilterMixin, ViewSet):
    IMPORT_ALLOWED: bool = False  # Disabled by default for chart
    EXPORT_ALLOWED: bool = False  # Disabled by default for chart

    filter_backends = [DjangoFilterBackend]
    WIDGET_TYPE = WidgetType.HTML.value

    renderer_classes = [PandasDataCustomRenderer, BrowsableAPIRendererWithoutForms]

    def get_queryset(self):
        return self.queryset

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def _parse_html(self, html: str) -> str:
        # Remove script tags and their contents
        cleaned_html = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", html, flags=re.DOTALL)
        return cleaned_html

    def get_html(self, queryset):
        raise NotImplementedError

    def list(self, request: Request, *args, **kwargs):
        self.request = request
        queryset = self.filter_queryset(self.get_queryset())
        html = self.get_html(queryset)
        html = self._parse_html(html)
        # data["messages"] = list(self._get_messages(request))
        return HttpResponse(html)
