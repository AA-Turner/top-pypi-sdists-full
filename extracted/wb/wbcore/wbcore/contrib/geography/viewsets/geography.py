from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.expressions import Value
from rest_framework.filters import OrderingFilter

from wbcore import viewsets
from wbcore.contrib.permission.filters import ObjectPermissionsFilter
from wbcore.viewsets.mixins import DjangoFilterBackend

from ..models import Geography
from ..serializers import GeographyModelSerializer, GeographyRepresentationSerializer
from .display import GeographyDisplayConfig
from .preview import GeographyPreviewConfig
from .titles.geography import GeographyTitleConfig


class GeographyRepresentationViewSet(viewsets.RepresentationViewSet):
    filter_backends = (ObjectPermissionsFilter, DjangoFilterBackend, OrderingFilter)
    ordering = ["-trigram", "ranking", "representation"]
    filterset_fields = {"level": ["exact"]}

    queryset = Geography.objects.all()
    serializer_class = GeographyRepresentationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if search := self.request.GET.get("search", None):
            if search.startswith("^"):
                return queryset.annotate(trigram=Value(1)).filter(search_vector=search[1:])

            return queryset.filter(trigram_search_vector__icontains=search).annotate(
                trigram=TrigramSimilarity("name", search)
            )

        return queryset.annotate(trigram=Value(1))


class GeographyModelViewSet(viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "geography/markdown/documentation/geography.md"
    display_config_class = GeographyDisplayConfig
    preview_config_class = GeographyPreviewConfig
    title_config_class = GeographyTitleConfig
    ordering_fields = [
        "code_2",
        "code_3",
        "parent__name",
    ]
    ordering = ["name"]
    search_fields = ["name"]
    filterset_fields = {
        "code_2": ["exact", "icontains"],
        "code_3": ["exact", "icontains"],
        "parent": ["exact"],
        "level": ["exact"],
    }

    queryset = Geography.objects.all()
    serializer_class = GeographyModelSerializer
