from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore import serializers
from wbcore.contrib.documents.models import Document
from wbcore.contrib.documents.serializers import DocumentTypeRepresentationSerializer


class DocumentModelSerializer(serializers.ModelSerializer):
    _document_type = DocumentTypeRepresentationSerializer(source="document_type")
    system_created = serializers.BooleanField(read_only=True, label=_("System Created"))

    @serializers.register_resource()
    def shareable_links(self, instance, request, user):
        base_url = reverse("wbcore:documents:link-list", request=request)
        return {"shareable_links": f"{base_url}?document={instance.id}"}

    @serializers.register_resource()
    def download_file(self, instance, request, user):
        return {"download_file": instance.file.url}

    @serializers.register_resource()
    def send_mail(self, instance, request, user):
        return {"send_mail": reverse("wbcore:documents:document-sendmail", args=[instance.id], request=request)}

    @serializers.register_only_instance_resource()
    def relationships(self, instance, request, user, view):
        return {
            "relationships": reverse(
                "wbcore:documents:document-documentmodelrelationship-list", args=[instance.id], request=request
            )
        }

    class Meta:
        model = Document
        fields = (
            "id",
            "name",
            "description",
            "file",
            "document_type",
            "_document_type",
            "system_created",
            "system_key",
            "updated",
            "created",
            "valid_from",
            "valid_until",
            "permission_type",
            "_additional_resources",
        )


class ReadOnlyDocumentModelSerializer(DocumentModelSerializer):
    class Meta(DocumentModelSerializer.Meta):
        read_only_fields = DocumentModelSerializer.Meta.fields


class DocumentRepresentationSerializer(serializers.RepresentationSerializer):
    endpoint = "wbcore:documents:documentrepresentation-list"
    _detail = serializers.HyperlinkField(reverse_name="wbcore:documents:document-detail")
    _detail_preview = serializers.HyperlinkField(reverse_name="wbcore:documents:document-detail")

    class Meta:
        model = Document
        fields = ("id", "_detail", "_detail_preview", "name")
