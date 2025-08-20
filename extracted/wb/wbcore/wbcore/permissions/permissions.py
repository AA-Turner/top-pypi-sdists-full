from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from wbcore.enums import WidgetType

from .shortcuts import is_internal_user


class RestAPIModelPermissions(permissions.DjangoModelPermissions):
    """
    Mixin for adding the view permission to the perms_map
    NOTE: This is only here until Django Rest Framework patches
    their DjangoModelPermissions to include view permissions
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.select_%(model_name)s"],
        "SELECT": ["%(app_label)s.select_%(model_name)s"],
        "HEAD": ["%(app_label)s.select_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        method = request.method
        if getattr(view, "WIDGET_TYPE", None) == WidgetType.SELECT.value:
            method = "SELECT"
        if getattr(view, "_ignore_model_permissions", False):
            return True

        if not request.user or (not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(method, queryset.model)

        return request.user.has_perms(perms)


class IsInternalUser(IsAuthenticated):
    def has_permission(self, request, view) -> bool:
        return is_internal_user(request.user, True)


class InternalUserPermissionMixin:
    def get_permissions(self):
        permissions = super().get_permissions()  # type: ignore
        return [*permissions, IsInternalUser()]
