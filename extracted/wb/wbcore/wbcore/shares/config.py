from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers
from wbcore import shares
from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.authentication.serializers import UserRepresentationSerializer
from wbcore.contrib.icons import WBIcon
from wbcore.metadata.configs.buttons import ActionButton, ButtonConfig
from wbcore.metadata.configs.display.instance_display import (
    create_simple_display,
    create_simple_section,
    repeat_field,
)

from .sites import share_site


@shares.register(
    section=create_simple_section(
        "base_section",
        "Share to someone",
        [[repeat_field(2, "share"), repeat_field(2, "share_recipients")], [repeat_field(4, "share_message")]],
        collapsed=True,
    ),
    weight=-100,
)
class DefaultShareSerializer(wb_serializers.Serializer):
    share = wb_serializers.BooleanField(label=_("Share to someone"), default=False)
    share_message = wb_serializers.TextField(
        label=_("Message"),
        default="Check out this Widget.",
        required=False,
        depends_on=[{"field": "share", "options": {}}],
    )
    share_recipients = wb_serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        label=_("Recipient"),
        required=False,
        depends_on=[{"field": "share", "options": {}}],
    )
    _share_recipients = UserRepresentationSerializer(
        many=True, source="share_recipients", depends_on=[{"field": "share", "options": {}}]
    )


def share_action_button(request):
    fields = [[repeat_field(4, "widget_endpoint")]]
    for section in share_site.sorted_sections:
        fields.append([repeat_field(4, section.key)])

    btn = ActionButton(
        icon=WBIcon.SHARE.icon,
        description_fields=_("Are you sure you want to share this widget?"),
        endpoint=reverse("wbcore:share", request=request),
        instance_display=create_simple_display(fields, share_site.sorted_sections),
        confirm_config=ButtonConfig(label=_("Share"), icon=WBIcon.SHARE.icon),
        serializer=share_site.serializer_class,
        action_label=_("Share"),
        title=_("Share"),
        label=_("Share"),
    )
    return btn
