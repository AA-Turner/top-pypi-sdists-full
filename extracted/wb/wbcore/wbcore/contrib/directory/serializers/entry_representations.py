from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers

from ..models import Entry


class EntryRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.SerializerMethodField()
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:entry-detail")
    primary_email = wb_serializers.CharField(read_only=True, required=False, label=_("Primary Email"), allow_null=True)
    primary_telephone = wb_serializers.TelephoneField(
        read_only=True, required=False, label=_("Primary Telephone"), allow_null=True
    )

    def get__detail(self, obj):
        if obj.is_company:
            return reverse("wbcore:directory:company-detail", args=[obj.id], request=self.context.get("request"))
        else:
            return reverse("wbcore:directory:person-detail", args=[obj.id], request=self.context.get("request"))

    class Meta:
        model = Entry
        fields = (
            "id",
            "computed_str",
            "_detail",
            "_detail_preview",
            "primary_email",
            "primary_telephone",
        )


class EntryUnlinkedRepresentationSerializer(EntryRepresentationSerializer):
    class Meta(EntryRepresentationSerializer.Meta):
        model = Entry
        fields = ("id", "computed_str")
