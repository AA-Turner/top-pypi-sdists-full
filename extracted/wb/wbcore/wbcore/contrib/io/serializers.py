import re

from django.db import transaction
from rest_framework.serializers import ValidationError

from wbcore import serializers as wb_serializers
from wbcore.serializers import ModelSerializer, RepresentationSerializer

from .models import (
    DataBackend,
    ImportSource,
    ParserHandler,
    Source,
    import_data_as_task,
)


class ImportSourceRepresentationSerializer(RepresentationSerializer):
    class Meta:
        model = ImportSource
        fields = ("id", "file")


class SourceRepresentationSerializer(RepresentationSerializer):
    def __init__(self, *args, label_key="{{id}} - {{title}}", **kwargs):
        self.allowed_sources = kwargs.pop("allowed_sources", Source.objects.none())
        super().__init__(*args, label_key=label_key, **kwargs)

    def get_filter_params(self, request):
        filter_params = {}
        if self.allowed_sources.exists():
            filter_params["id__in"] = ",".join(map(str, self.allowed_sources.values_list("id", flat=True)))
        return filter_params

    class Meta:
        model = Source
        fields = ("id", "title")


class ParserHandlerRepresentationSerializer(RepresentationSerializer):
    def __init__(self, *args, **kwargs):
        self.allowed_handler = kwargs.pop("allowed_handler", None)
        super().__init__(*args, **kwargs)

    def get_filter_params(self, request):
        filter_params = {}
        if self.allowed_handler:
            filter_params["handler__icontains"] = self.allowed_handler
        return filter_params

    class Meta:
        model = ParserHandler
        fields = ("id", "parser", "handler")


class DataBackendRepresentationSerializer(RepresentationSerializer):
    def __init__(self, *args, **kwargs):
        self.allowed_backend_class_path = kwargs.pop("allowed_backend_class_path", ParserHandler.objects.none())
        super().__init__(*args, **kwargs)

    def get_filter_params(self, request):
        filter_params = {}
        if self.allowed_backend_class_path:
            filter_params["backend_class_path__icontains"] = self.allowed_backend_class_path
        return filter_params

    class Meta:
        model = DataBackend
        fields = ("id", "title", "backend_class_path")


class ParserHandlerModelSerializer(ModelSerializer):
    class Meta:
        model = ParserHandler
        fields = ("id", "parser", "handler")


class ImportSourceModelSerializer(ModelSerializer):
    parser_handler = wb_serializers.CharField(required=False)

    def validate(self, data):
        if "creator" not in data and "request" in self.context:
            data["creator"] = self.context["request"].user
        if parser_handler := data.get("parser_handler"):
            if match := re.search(r"([\w\.]+)::(\w+\.\w+)", parser_handler):
                parser_lookup = dict(parser=match.group(1), handler=match.group(2))
            else:
                parser_lookup = dict(id=parser_handler)
            try:
                data["parser_handler"] = ParserHandler.objects.get(**parser_lookup)
            except (ParserHandler.DoesNotExist, ValueError) as e:
                raise ValidationError({"parser_handler": "Invalid parser handler"}) from e
        return data

    def create(self, validated_data):
        if "parser_handler" not in validated_data and "source" in validated_data:
            # if parser handler is not provided, we default it to the first source parser handler
            validated_data["parser_handler"] = validated_data["source"].parser_handler.first()
        instance = super().create(validated_data)
        transaction.on_commit(import_data_as_task.s(instance.id).delay)
        return instance

    class Meta:
        model = ImportSource
        read_only_fields = ("id", "status")
        fields = (
            "id",
            "status",
            "origin",
            "creator",
            "file",
            "save_data",
            "parser_handler",
            "source",
        )


class SourceModelSerializer(wb_serializers.ModelSerializer):
    _parser_handler = ParserHandlerRepresentationSerializer(source="parser_handler", many=True)
    _data_backend = DataBackendRepresentationSerializer(source="data_backend")
    crontab = wb_serializers.StringRelatedField()

    class Meta:
        model = Source
        fields = (
            "title",
            "uuid",
            "parser_handler",
            "_parser_handler",
            "is_active",
            "connection_parameters",
            "import_parameters",
            "data_backend",
            "_data_backend",
            "crontab",
            "import_timedelta_interval",
        )
