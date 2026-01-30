from contextlib import suppress

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from wbcore import viewsets
from wbcore.contrib.authentication.authentication import JWTCookieAuthentication
from wbcore.contrib.content_type.utils import get_ancestors_content_type
from wbcore.contrib.documents.filters import DocumentFilter
from wbcore.contrib.documents.models import Document, DocumentModelRelationship
from wbcore.contrib.documents.serializers import (
    DocumentModelSerializer,
    DocumentRepresentationSerializer,
    ReadOnlyDocumentModelSerializer,
)
from wbcore.contrib.documents.viewsets.buttons import DocumentButtonConfig
from wbcore.contrib.documents.viewsets.display import DocumentModelDisplay
from wbcore.contrib.documents.viewsets.endpoints import DocumentEndpointConfig
from wbcore.contrib.documents.viewsets.previews import DocumentPreviewConfig
from wbcore.contrib.documents.viewsets.titles import DocumentModelTitleConfig
from wbcore.contrib.permission.viewsets.mixins import ObjectPermissionFilterMixin


class DocumentModelViewSet(ObjectPermissionFilterMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "documents/markdown/documentation/documents.md"
    search_fields = ("name",)
    ordering = ["-updated", "name"]
    ordering_fields = ("name", "document_type", "updated")
    filterset_class = DocumentFilter
    preview_config_class = DocumentPreviewConfig
    queryset = Document.objects.all()
    serializer_class = DocumentModelSerializer
    title_config_class = DocumentModelTitleConfig
    endpoint_config_class = DocumentEndpointConfig
    button_config_class = DocumentButtonConfig
    display_config_class = DocumentModelDisplay

    def get_queryset(self):
        if (content_type_id := self.kwargs.get("content_type")) and (object_id := self.kwargs.get("content_id")):
            content_types = list(get_ancestors_content_type(ContentType.objects.get_for_id(content_type_id)))
            return (
                super()
                .get_queryset()
                .filter(
                    relationships__content_type__in=content_types,
                    relationships__object_id=object_id,
                )
            )
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if (content_type_id := self.kwargs.get("content_type")) and (object_id := self.kwargs.get("content_id")):
            DocumentModelRelationship.objects.create(
                document_id=response.data["instance"]["id"],
                content_type_id=content_type_id,
                object_id=object_id,
            )

        return response

    def get_serializer_class(self):
        if "pk" in self.kwargs:
            if (document := self.get_object()) and document.system_created:
                return ReadOnlyDocumentModelSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["PATCH"])
    def sendmail(self, request, pk=None):
        document = get_object_or_404(Document, id=pk)
        if to_email := request.POST.get("to_email", None):
            document.send_email(to_email)
            return Response(
                {"__notification": {"title": _("Document is going to be sent with email")}},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], authentication_classes=[JWTCookieAuthentication])
    def urlredirect(self, request, pk=None):
        """
        List Action to redirect the document url when a unique relationship is found for the given content type pair values and optional query parameters
        """
        filter_kwargs = {"system_created": request.GET.get("system_created", "true") == "true"}
        if "system_key" in request.GET:
            filter_kwargs["system_key"] = request.GET["system_key"]

        with suppress(Document.DoesNotExist, ObjectDoesNotExist, ContentType.DoesNotExist):
            content_type = ContentType.objects.get_for_id(self.request.GET.get("content_type"))
            obj = content_type.get_object_for_this_type(id=self.request.GET.get("object_id"))
            document = Document.get_for_object(obj).get(**filter_kwargs)
            if self.request.user.has_perm(Document.view_perm_str, document):
                return HttpResponseRedirect(document.file.url)
        return HttpResponse("Document could not be found", status=status.HTTP_404_NOT_FOUND)


class DocumentRepresentationViewSet(ObjectPermissionFilterMixin, viewsets.RepresentationViewSet):
    IDENTIFIER = "wbcore:documents:documentrepresentation"
    serializer_class = DocumentRepresentationSerializer
    queryset = Document.objects.all()
    search_fields = ("name",)
