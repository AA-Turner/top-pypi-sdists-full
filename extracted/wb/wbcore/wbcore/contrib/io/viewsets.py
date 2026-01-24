import json

import tablib

from wbcore.contrib.pandas import fields as pf
from wbcore.contrib.pandas.views import PandasAPIViewSet
from wbcore.viewsets import ModelViewSet, ReadOnlyModelViewSet, RepresentationViewSet

from .configs.endpoints import (
    ImportSourceModelViewSetEndpointConfig,
    SourceModelViewSetEndpointConfig,
)
from .models import DataBackend, ImportSource, ParserHandler, Source
from .resources import ViewResource
from .serializers import (
    DataBackendRepresentationSerializer,
    ImportSourceModelSerializer,
    ImportSourceRepresentationSerializer,
    ParserHandlerModelSerializer,
    ParserHandlerRepresentationSerializer,
    SourceModelSerializer,
    SourceRepresentationSerializer,
)
from .viewset_mixins import ImportExportDRFMixin


class ImportSourceRepresentationViewSet(RepresentationViewSet):
    ordering = ["id"]
    queryset = ImportSource.objects.all()
    serializer_class = ImportSourceRepresentationSerializer


class SourceRepresentationViewSet(RepresentationViewSet):
    ordering = ["id"]
    search_fields = ["id", "title"]
    filterset_fields = {"title": ["exact", "icontains"], "id": ["in", "exact"]}
    queryset = Source.objects.all()
    serializer_class = SourceRepresentationSerializer


class ParserHandlerRepresentationViewSet(RepresentationViewSet):
    ordering = ["parser", "handler", "id"]
    search_fields = ["parser", "handler"]
    filterset_fields = {
        "parser": ["exact", "icontains"],
        "handler": ["exact", "icontains"],
    }
    queryset = ParserHandler.objects.all()
    serializer_class = ParserHandlerRepresentationSerializer


class DataBackendRepresentationViewSet(RepresentationViewSet):
    ordering = ["title", "id"]
    search_fields = ["title"]
    filterset_fields = {
        "title": ["exact", "icontains"],
        "backend_class_path": ["exact", "icontains"],
    }
    queryset = DataBackend.objects.all()
    serializer_class = DataBackendRepresentationSerializer


class ParserHandlerModelViewSet(ModelViewSet):
    ordering = ["parser", "handler", "id"]
    search_fields = ["parser", "handler"]
    filterset_fields = {
        "parser": ["exact", "icontains"],
        "handler": ["exact", "icontains"],
    }
    queryset = ParserHandler.objects.all()
    serializer_class = ParserHandlerModelSerializer


class ImportSourceModelViewSet(ModelViewSet):
    ordering = ["id"]
    search_fields = ["parser_handler__parser", "parser_handler__handler"]
    filterset_fields = {
        "parser_handler": ["exact"],
        "status": ["exact"],
        "source": ["exact"],
        "creator": ["exact"],
        "created": ["lte", "gte"],
        "last_updated": ["lte", "gte"],
    }
    queryset = ImportSource.objects.all()
    serializer_class = ImportSourceModelSerializer
    endpoint_config_class = ImportSourceModelViewSetEndpointConfig


class SourceModelViewSet(ReadOnlyModelViewSet):
    ordering = ["id"]
    search_fields = ["parser_handler__parser", "parser_handler__handler", "title", "uuid", "data_backend__title"]
    filterset_fields = {
        "title": ["icontains"],
        "uuid": ["exact"],
        "parser_handler": ["exact"],
        "is_active": ["exact"],
        "data_backend": ["exact"],
    }
    queryset = Source.objects.all()
    serializer_class = SourceModelSerializer
    endpoint_config_class = SourceModelViewSetEndpointConfig
    lookup_field = "uuid"


class ExportPandasAPIViewSet(ImportExportDRFMixin, PandasAPIViewSet):
    IMPORT_ALLOWED: bool = False

    def _get_validated_headers(self, request, df) -> list[str]:
        """
        This method validates the available columns and their ability to serialize
        """
        validated_headers = []
        pandas_fields = {f.key: f for f in self.get_pandas_fields(request).fields}
        for col in df.columns:
            if (pdf := pandas_fields.get(col, None)) and not isinstance(
                pdf, pf.SparklineField
            ):  # exclude sparkeline from exported data
                validated_headers.append(pdf.key)
        return validated_headers

    def _get_data_for_export(self, request, queryset, *args, **kwargs) -> tablib.Dataset:
        df = self._get_dataframe(export=True, **kwargs)
        validated_headers = self._get_validated_headers(request, df)
        df = df[
            df.columns.intersection(validated_headers)
        ]  # ensure df contains only the validated header, in that specific order

        columns_map = ViewResource.get_columns_map(self)
        dataset = tablib.Dataset(headers=list(columns_map.values()))
        df = json.loads(
            df.to_json(orient="records", date_format="iso")
        )  # we do that do ensure that dataframe values have be converted to json friendly data
        for data in df:
            row = []
            for key in columns_map.keys():  # Ensure data is appended to the row in the header order
                row.append(data.get(key, None))
            dataset.append(row)
        return dataset
