import operator
from contextlib import suppress
from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.urls import NoReverseMatch, Resolver404

from wbcore import serializers
from wbcore.serializers import HyperlinkField


class ContentTypeRepresentationSerializer(serializers.RepresentationSerializer):
    endpoint = "wbcore:content_type:contenttyperepresentation-list"
    value_key = "id"

    model_title = serializers.SerializerMethodField()

    def __init__(self, *args, model_callback_title=None, label_key="{{app_label}} | {{model}}", **kwargs):
        self.allowed_types = kwargs.pop("allowed_types", ContentType.objects.none())

        # for ease of use, we allow the allowed_type attribute to be set as a list of app_label and model (as tuple). In that case, we extract the valid content type queryset base on the join of conditions
        if isinstance(self.allowed_types, list):
            _conditions = [
                (Q(app_label=allowed_type[0]) & Q(model__iexact=allowed_type[1]))
                for allowed_type in self.allowed_types
                if isinstance(allowed_type, tuple) and len(allowed_type) == 2
            ]
            if _conditions:
                self.allowed_types = ContentType.objects.filter(reduce(operator.or_, _conditions))
            else:
                self.allowed_types = ContentType.objects.none()
        self.model_callback_title = model_callback_title
        super().__init__(*args, label_key=label_key, **kwargs)

    def get_model_title(self, obj):
        return obj.model.title()

    def _get_filter_params(self, request):
        filter_params = super()._get_filter_params(request)
        if self.allowed_types.exists():
            filter_params["id__in"] = ",".join(map(str, self.allowed_types.values_list("id", flat=True)))
        return filter_params

    class Meta:
        model = ContentType
        read_only_fields = (
            "app_label",
            "model",
            "model_title",
        )
        fields = ("id", "app_label", "model", "model_title")


class GenericModel(models.Model):  # noqa
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=256)

    class Meta:
        managed = False


class DynamicObjectIDRepresentationSerializer(serializers.RepresentationSerializer):
    endpoint = "wbcore:content_type:dynamiccontenttyperepresentation-list"
    value_key = "{{id}}"
    label_key = "{{label}}"

    label = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    def __init__(self, *args, content_type_field_name: str = "content_type", **kwargs):
        self.content_type_field_name = content_type_field_name
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        representation = super().to_representation(value)
        representation["id"] = getattr(value, "pk", value)
        obj = None
        with suppress(ObjectDoesNotExist):
            if content_type := getattr(self.parent.instance, self.content_type_field_name, None):
                obj = content_type.get_object_for_this_type(id=value)
        if obj:
            representation["label"] = str(obj)
            with suppress(AttributeError, NoReverseMatch, Resolver404):
                detail_field = HyperlinkField(reverse_name=obj.get_endpoint_basename() + "-detail")
                representation["_detail"] = detail_field.get_attribute(obj)

        return representation

    class Meta:
        model = GenericModel
        read_only_fields = (
            "id",
            "label",
        )
        fields = ("id", "label")
