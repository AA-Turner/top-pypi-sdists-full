import pytest
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.shortcuts import assign_perm

from wbcore.contrib.authentication.models.users import Permission
from wbcore.contrib.permission.viewsets import PivotUserObjectPermissionModelViewSet


class TestPivotUserObjectPermissionModelViewSet:
    def test_cached_property_permissions(self, mocker, request):
        mocked_filter = mocker.patch("wbcore.contrib.permission.viewsets.viewsets.Permission.objects.filter")
        view = PivotUserObjectPermissionModelViewSet(request=request, kwargs={"content_type_id": 1})
        assert view.permissions

        mocked_filter.assert_called_once_with(
            Q(content_type=1)
            & ~Q(codename__icontains="administrate")
            & ~Q(codename__icontains="import")
            & ~Q(codename__icontains="export")
        )

    def test_linked_object(self, mocker, request):
        mocked_contrib_type = mocker.patch("wbcore.contrib.permission.viewsets.viewsets.ContentType.objects")
        mocked_get_object_for_this_type = mocker.Mock()
        mocked_contrib_type.get.return_value = mocked_get_object_for_this_type
        view = PivotUserObjectPermissionModelViewSet(request=request, kwargs={"content_type_id": 1, "object_pk": 1})
        assert view.linked_object

        mocked_get_object_for_this_type.get_object_for_this_type.assert_called_once()

    @pytest.mark.django_db
    def test_queryset(self, user, request):
        assign_perm("view_user", user, user)
        view = PivotUserObjectPermissionModelViewSet(
            request=request, kwargs={"content_type_id": ContentType.objects.get_for_model(user), "object_pk": user.id}
        )

        permissions = view.permissions
        instance = view.get_queryset().order_by("id").first()

        for permission in permissions:
            assert permission.codename in instance.keys()

    def test_serializer_class(self, request, mocker):
        view = PivotUserObjectPermissionModelViewSet(request=request, kwargs={"content_type_id": 1, "object_pk": 1})
        mocker.patch.object(view, "permissions", [Permission(codename="view_user")])
        serializer_class = view.get_serializer_class()
        assert "view_user" in serializer_class.Meta.fields  # type: ignore
