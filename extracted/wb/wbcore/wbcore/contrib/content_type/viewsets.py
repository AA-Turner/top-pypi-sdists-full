import re
from contextlib import suppress

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from wbcore import viewsets

from .filters import ContentTypeFilterSet
from .serializers import (
    ContentTypeRepresentationSerializer,
    DynamicObjectIDRepresentationSerializer,
    GenericModel,
)


class ContentTypeRepresentationViewSet(viewsets.RepresentationViewSet):
    filterset_class = ContentTypeFilterSet
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeRepresentationSerializer
    search_fields = ["app_label", "model"]


class DynamicObjectIDRepresentationViewSet(viewsets.RepresentationViewSet):
    IDENTIFIER = "wbcore:object_id"
    queryset = GenericModel.objects.none()
    search_fields = ["label"]

    @cached_property
    def model(self):
        content_type = get_object_or_404(ContentType, pk=self.kwargs.get("pk", self.request.GET.get("content_type")))
        return content_type.model_class()

    @cached_property
    def label_keys(self) -> list[str]:
        label_keys = ["computed_str"]
        if (r := getattr(self.model, "get_representation_label_key", None)) and callable(r):
            label_keys = re.findall(r"\{\{(.*?)\}\}", r())
        validated_keys = []
        for key in label_keys:
            with suppress(FieldDoesNotExist):
                if self.model._meta.get_field(key):
                    validated_keys.append(key)
        return validated_keys

    def get_serializer_class(self):
        class ComputedStrSerializer(DynamicObjectIDRepresentationSerializer):
            class Meta:
                fields = ("id", "label", *self.label_keys)
                model = self.model

        return ComputedStrSerializer

    def filter_queryset(self, queryset):
        """
        We allow basic filtering on the model fields
        """
        filter_params = dict(self.request.GET.dict())  # convert immutable QueryDict into a mutable dict
        filter_params.pop("content_type", None)
        for key, value in filter_params.items():
            with suppress(FieldError, ValueError):
                queryset = queryset.filter(**{key: value})
        return super().filter_queryset(queryset)

    def get_queryset(self):
        try:
            if not self.label_keys:
                raise FieldError()
            concat_fields = []
            for field in self.label_keys:
                concat_fields.append(F(field))
                concat_fields.append(Value(" "))
            return self.model.objects.annotate(
                label=Concat(*concat_fields, output_field=CharField()),
            )
        except FieldError:
            return self.model.objects.none()
