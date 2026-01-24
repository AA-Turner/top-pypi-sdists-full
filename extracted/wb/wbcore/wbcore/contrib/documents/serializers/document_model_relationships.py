from wbcore import serializers
from wbcore.contrib.content_type.serializers import (
    ContentTypeRepresentationSerializer,
    DynamicObjectIDRepresentationSerializer,
)
from wbcore.contrib.documents.models import DocumentModelRelationship


class DocumentModelRelationshipModelSerializer(serializers.ModelSerializer):
    _content_type = ContentTypeRepresentationSerializer(
        source="content_type",
        label_key="{{model_title}}",
    )
    _object_id = DynamicObjectIDRepresentationSerializer(
        source="object_id",
        optional_get_parameters={"content_type": "content_type"},
        depends_on=[{"field": "content_type", "options": {}}],
    )

    class Meta:
        model = DocumentModelRelationship
        fields = (
            "id",
            "content_type",
            "_content_type",
            "object_id",
            "_object_id",
            "content_object_repr",
            "document",
            "primary",
        )
