from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class ObjectPermissionsFilter(BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """

    def filter_queryset(self, request, queryset, view):
        from guardian.shortcuts import get_objects_for_user

        from wbcore.contrib.permission.models.mixins import PermissionObjectModelMixin

        model_class = queryset.model
        if issubclass(model_class, PermissionObjectModelMixin):
            user = request.user
            protected_objects = get_objects_for_user(
                user, [model_class.view_perm_str], queryset, **model_class.permission_shortcut_kwargs
            )
            public_objects = queryset.filter(permission_type=PermissionObjectModelMixin.PermissionType.PUBLIC)
            return queryset.filter(
                Q(id__in=public_objects.values("id")) | Q(id__in=protected_objects.values("id"))
            ).distinct()
        return queryset
