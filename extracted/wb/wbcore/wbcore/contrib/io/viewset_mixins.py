from contextlib import suppress

import tablib
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from import_export.admin import ImportExportMixin
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action, parser_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wbcore import serializers
from wbcore.contrib.authentication.authentication import JWTCookieAuthentication
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.io.import_export.parsers.base_csv import parse
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt
from wbcore.metadata.configs.display.instance_display import create_simple_display
from wbcore.signals.instance_buttons import add_extra_button

from .enums import ExportFormat, get_django_import_export_format
from .resources import ViewResource
from .utils import get_import_export_identifier, parse_endpoint


class ImportFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class ExportFileSerializer(serializers.Serializer):
    format = serializers.ChoiceField(choices=ExportFormat.choices, label="Format", required=True)


class ImportExportDRFMixin(ImportExportMixin):
    """
    This mixin can be imported to enable import export out of the box. This will add two action to import a file given its extension
    or Export the filtered queryset content as a file
    """

    IMPORT_ALLOWED: bool = False  # by default import is disabled and requires an explicit defined resource
    EXPORT_ALLOWED: bool = True

    @cached_property
    def model(self):
        try:
            return getattr(self.queryset, "model", None)
        except AttributeError:
            raise ParseError("Malformed Queryset")

    @cached_property
    def opts(self):
        return self.model._meta

    @cached_property
    def export_pagination_limit(self) -> int:
        return getattr(
            settings, "WBIMPORT_EXPORT_DEFAULT_EXPORT_PAGINATION_LIMIT", settings.REST_FRAMEWORK.get("page_size", 25)
        )

    def get_resource_class(self) -> type:
        """
        This function returns return the resource class to use. Default to the model resource factory on the queryset model
        """
        return ViewResource

    def get_import_resource_kwargs(self):
        return {
            "extra_columns_values": self.kwargs,  # contains the extra column to inject into the dataset during parsing
            "columns_mapping": {},  # Store the column mapping to rename dataset column during parsing
        }

    def get_import_parser_path(self) -> str:
        return parse.__module__

    def get_resource_serializer_class(self):
        resource_kwargs = {}
        with suppress(AttributeError, AssertionError):
            # we have to mocky patch the action to be "list" because sometime we differentiate the serializer to use
            previous_action = getattr(self, "action", "list")
            setattr(self, "action", "list")
            serializer_class = getattr(
                self, "serializer_class", self.get_serializer_class()
            )  # we prioritize the default serializer class attribute
            resource_kwargs["serializer_class_path"] = serializer_class.__module__ + "." + serializer_class.__name__
            setattr(self, "action", previous_action)
        return resource_kwargs

    def _get_data_for_export(self, request, queryset, *args, **kwargs) -> tablib.Dataset:
        raise NotImplementedError()

    def has_import_permission(self, request) -> bool:
        """
        called by the import workflow to determine if a user can import data

        Can be overriden if custom behavior is necessary
        """
        return self.IMPORT_ALLOWED and request and super().has_import_permission(request) and "pk" not in self.kwargs

    def has_export_permission(self, request) -> bool:
        """
        called by the import workflow to determine if a user can export data

        Can be overriden if custom behavior is necessary
        """
        return self.EXPORT_ALLOWED and request and super().has_export_permission(request) and "pk" not in self.kwargs

    @action(
        detail=False,
        methods=["PATCH"],
        permission_classes=[IsAuthenticated],
        # authentication_classes=[SessionAuthentication, JWTCookieAuthentication],
        url_name="processimport",
    )
    @parser_classes([MultiPartParser])
    def process_import(self, request, **kwargs):
        """
        This action parse a file and trigger the import workflow from its dataset
        """
        if not self.has_import_permission(request):
            raise PermissionDenied
        if request.data:
            if file_tmp := request.FILES.get("file"):
                from wbcore.contrib.io.models import (  # for circular dependency. Will fix later
                    ImportSource,
                    ParserHandler,
                    import_data_as_task,
                )

                parser_handler, _ = ParserHandler.objects.get_or_create(
                    handler=f"{self.model._meta.app_label}.{self.model.__name__}", parser=self.get_import_parser_path()
                )
                import_source = ImportSource.objects.create(
                    parser_handler=parser_handler,
                    file=file_tmp,
                    origin="Internal Import",
                    creator=request.user,
                    resource_kwargs=self.get_import_resource_kwargs(),
                )
                import_data_as_task.delay(import_source.id)

                return HttpResponse("Your file will be imported shortly", status=status.HTTP_200_OK)
        return HttpResponse("Not all expected parameter were provided", status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["PATCH"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTCookieAuthentication],
        url_name="processexport",
    )
    def process_export(self, request, **kwargs):
        """
        This action export a queryset into a file
        """
        if not self.has_export_permission(request):
            raise PermissionDenied
        if (export_format := int(request.data.get("format", -1))) is not None and export_format in ExportFormat.values:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                from wbcore.contrib.io.models import ExportSource

                # The export job is too big and needs to be ran asynchronously
                try:
                    export_data = self._get_data_for_export(request, queryset, **kwargs)
                    _data = [list(row) for row in export_data._data]

                    ExportSource.objects.create(
                        creator=request.user,
                        format=export_format,
                        content_type=self.get_content_type(),
                        data={"data": _data, "headers": export_data.headers},
                    )
                except NotImplementedError:
                    resource_kwargs = {
                        "columns_map": ViewResource.get_columns_map(self),
                    }
                    resource_kwargs.update(self.get_resource_serializer_class())

                    resource_class = self.get_resource_class()
                    query_str, query_params = queryset.query.sql_with_params()

                    ExportSource.objects.create(
                        creator=request.user,
                        format=export_format,
                        content_type=self.get_content_type(),
                        resource_path=resource_class.__module__ + "." + resource_class.__name__,
                        resource_kwargs=resource_kwargs,
                        query_str=query_str,
                        query_params=query_params,
                    )
                return Response("export job created", status=status.HTTP_200_OK)
        return HttpResponse("Not all expected parameter were provided", status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[SessionAuthentication, JWTCookieAuthentication],
        url_name="exporttemplate",
    )
    def export_template(self, request, **kwargs):
        """
        This action export a template into a file
        """
        file_format = get_django_import_export_format(ExportFormat.CSV)()
        export_data = self.get_export_data(file_format, request, None, **kwargs)
        content_type = file_format.get_content_type()
        response = HttpResponse(export_data, content_type=content_type)
        response["Content-Disposition"] = 'attachment; filename="%s"' % (
            self.get_export_filename(request, None, file_format),
        )
        return response


@receiver(add_extra_button)
def add_template_extra_button(sender, instance, request, view, pk=None, **kwargs):
    if view and not instance and hasattr(view, "has_import_permission") and view.has_import_permission(request):
        return bt.HyperlinkButton(
            endpoint=parse_endpoint(request, "export_template", export_format=ExportFormat.CSV),
            title="Import Template (CSV)",
            label="Import Template (CSV)",
        )


@receiver(add_extra_button)
def add_import_extra_button(sender, instance, request, view, pk=None, **kwargs):
    if (
        view
        and not instance
        and hasattr(view, "has_import_permission")
        and view.has_import_permission(request)
        and view.get_resource_class()
    ):
        return bt.ActionButton(
            method=RequestType.PATCH,
            icon=WBIcon.DOWNLOAD.icon,
            identifiers=(get_import_export_identifier(view),),
            endpoint=parse_endpoint(request, "process_import"),
            action_label=_("Import"),
            title=_("Import"),
            label=_("Import"),
            description_fields=_("Please provide a valid CSV file (Coma Separated Value)"),
            serializer=ImportFileSerializer,
            instance_display=create_simple_display([["file"]]),
            weight=0,
        )


@receiver(add_extra_button)
def add_export_extra_button(sender, instance, request, view, pk=None, **kwargs):
    if view and not instance and hasattr(view, "has_export_permission") and view.has_export_permission(request):
        return bt.ActionButton(
            method=RequestType.PATCH,
            icon=WBIcon.DOWNLOAD.icon,
            identifiers=(get_import_export_identifier(view),),
            endpoint=parse_endpoint(request, "process_export"),
            action_label=_("Export"),
            title=_("Export"),
            label=_("Export"),
            description_fields=_("Select the export format"),
            serializer=ExportFileSerializer,
            instance_display=create_simple_display([["format"]]),
            weight=1,
        )
