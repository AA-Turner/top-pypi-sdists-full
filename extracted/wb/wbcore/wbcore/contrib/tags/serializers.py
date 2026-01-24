from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse

from wbcore import serializers
from wbcore.contrib.content_type.serializers import ContentTypeRepresentationSerializer
from wbcore.contrib.content_type.utils import get_view_content_type_id

from .models import Tag, TagGroup


class TagGroupRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="wbcore:tags:taggroup-detail")

    class Meta:
        model = TagGroup
        fields = ("id", "title", "_detail")


class TagGroupModelSerializer(serializers.ModelSerializer):
    @serializers.register_resource()
    def additional_resources(self, instance, request, user):
        return {
            "tags": reverse(
                "wbcore:tags:group-tag-list",
                args=[instance.id],
                request=request,
            )
        }

    class Meta:
        model = TagGroup
        read_only_fields = ("slug",)
        fields = ("id", "title", "_additional_resources")


class TagRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="wbcore:tags:tag-detail")
    _detail_preview = serializers.HyperlinkField(reverse_name="wbcore:tags:tag-detail")

    def get_filter_params(self, request):
        content_type_id = get_view_content_type_id(request.parser_context["view"])
        return {"content_type": content_type_id}

    class Meta:
        model = Tag
        read_only_fields = ("slug",)
        fields = (
            "id",
            "title",
            "computed_str",
            "color",
            "slug",
            "description",
            "_detail",
            "_detail_preview",
        )


class TagModelSerializer(serializers.ModelSerializer):
    _groups = TagGroupRepresentationSerializer(source="groups", many=True)
    _content_type = ContentTypeRepresentationSerializer(source="content_type")
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), required=False, allow_null=True
    )
    groups = serializers.PrimaryKeyRelatedField(
        queryset=TagGroup.objects.all(),
        many=True,
        default=serializers.DefaultFromKwargs("group_id"),
    )

    class Meta:
        model = Tag
        read_only_fields = ("slug",)
        fields = (
            "id",
            "title",
            "computed_str",
            "color",
            "content_type",
            "_content_type",
            "slug",
            "description",
            "groups",
            "_groups",
        )


class TagSerializerMixin(serializers.Serializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), label="Tags", many=True)
    _tags = TagRepresentationSerializer(source="tags", many=True)
