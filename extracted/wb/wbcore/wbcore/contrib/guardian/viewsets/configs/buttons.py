from contextlib import suppress

from django.dispatch import receiver
from rest_framework.reverse import reverse
from wbcore.contrib.guardian.models.mixins import PermissionObjectModelMixin
from wbcore.contrib.icons.icons import WBIcon
from wbcore.metadata.configs.buttons import ButtonViewConfig
from wbcore.metadata.configs.buttons.buttons import WidgetButton
from wbcore.metadata.configs.buttons.enums import Button
from wbcore.signals.instance_buttons import add_extra_button


class PivotUserObjectPermissionButtonViewConfig(ButtonViewConfig):
    def get_create_buttons(self):
        return {
            Button.SAVE_AND_CLOSE.value,
        }


@receiver(add_extra_button)
def add_object_permission_button(sender, instance, request, view, pk=None, **kwargs):
    with suppress(AttributeError):
        if (
            (
                request.user.has_perm(f"administrate_{view.queryset.model._meta.model_name}")
                or request.user.is_superuser
            )
            and issubclass(view.queryset.model, PermissionObjectModelMixin)
            and pk is not None
        ):
            endpoint = reverse(
                "wbcore:guardian:pivoteduserobjectpermission-list",
                args=[view.get_content_type().id, pk],
                request=request,
            )
            return WidgetButton(endpoint=endpoint, label="Permissions", icon=WBIcon.LOCK.icon)
