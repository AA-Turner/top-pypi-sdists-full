from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Exists, F, Model, OuterRef, Q, QuerySet
from django.utils.functional import cached_property
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.exceptions import ValidationError
from wbcore import serializers, viewsets
from wbcore.contrib.authentication.models.users import Permission, User
from wbcore.contrib.authentication.serializers import UserRepresentationSerializer
from wbcore.contrib.guardian.models import UserObjectPermission
from wbcore.contrib.guardian.viewsets.configs import (
    PivotUserObjectPermissionButtonViewConfig,
    PivotUserObjectPermissionDisplayViewConfig,
    PivotUserObjectPermissionEndpointViewConfig,
    PivotUserObjectPermissionTitleViewConfig,
)


class PivotUserObjectPermissionModelViewSet(viewsets.ModelViewSet):
    queryset = UserObjectPermission.objects.all()

    button_config_class = PivotUserObjectPermissionButtonViewConfig
    display_config_class = PivotUserObjectPermissionDisplayViewConfig
    endpoint_config_class = PivotUserObjectPermissionEndpointViewConfig
    title_config_class = PivotUserObjectPermissionTitleViewConfig

    lookup_field = "user_id"

    @cached_property
    def permissions(self):
        return Permission.objects.filter(
            Q(content_type=self.kwargs.get("content_type_id"))
            & ~Q(codename__icontains="administrate")
            & ~Q(codename__icontains="import")
            & ~Q(codename__icontains="export")
        )

    @cached_property
    def linked_object(self):
        return ContentType.objects.get(id=self.kwargs.get("content_type_id")).get_object_for_this_type(
            id=self.kwargs.get("object_pk")
        )

    def get_queryset(self):
        queryset = super().get_queryset()

        if (content_type_id := self.kwargs.get("content_type_id")) and (object_pk := self.kwargs.get("object_pk")):
            queryset = queryset.filter(content_type_id=content_type_id, object_pk=object_pk)

        queryset = queryset.values("user").annotate(
            id=F("user__id"),
            userref=F("user__id"),
            count=Count("id"),  # This is needed as we need at least 1 aggregation function to have a group by
            non_editable=Exists(queryset.filter(user=OuterRef("user"), editable=False)),
            **{
                permission.codename: Exists(queryset.filter(user=OuterRef("user"), permission_id=permission.pk))
                for permission in self.permissions
            },
        )

        return queryset

    def get_serializer_class(self):
        def assign_and_remove_perms(
            self,
            perms: dict[str, bool],
            permissions: QuerySet[Permission],
            user: User,
            linked_object: Model,
            remove: bool = True,
        ):
            for codename, perm in perms.items():
                if UserObjectPermission.objects.filter(
                    user=user,
                    content_type_id=self.context["view"].kwargs.get("content_type_id"),
                    object_pk=linked_object.pk,
                    editable=False,
                ).exists():
                    raise ValidationError(
                        {
                            "non_field_errors": "This user permission is not editable as it was created through the system"
                        }
                    )
                if perm:
                    assign_perm(
                        permissions.get(codename=codename),
                        user,
                        linked_object,
                    )
                elif remove:
                    remove_perm(
                        permissions.get(codename=codename),
                        user,
                        linked_object,
                    )

        def create(self, validated_data):
            user = validated_data.pop("userref")
            view = self.context["view"]
            self.assign_and_remove_perms(validated_data, view.permissions, user, view.linked_object, remove=False)
            self.context["view"].kwargs["user_id"] = user.id
            return self.context["view"].get_object()

        def update(self, instance, validated_data):
            view = self.context["view"]
            self.assign_and_remove_perms(
                validated_data, view.permissions, User.objects.get(id=instance.get("user")), view.linked_object
            )
            return instance

        attributes = {
            "id": serializers.PrimaryKeyField(),
            "count": serializers.IntegerField(required=False, read_only=True),
            "userref": serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), label="User"),
            "_userref": UserRepresentationSerializer(source="userref"),
            "non_editable": serializers.BooleanField(default=False),
            **{permission.codename: serializers.BooleanField(default=False) for permission in self.permissions},
            "Meta": type(
                "Meta",
                (),
                {
                    "model": User,
                    "fields": (
                        "id",
                        "count",
                        "userref",
                        "_userref",
                        "non_editable",
                        *[perm.codename for perm in self.permissions],
                    ),
                },
            ),
            "update": update,
            "create": create,
            "assign_and_remove_perms": assign_and_remove_perms,
        }

        return type(
            "PivotedUserObjectPermissionModelSerializer",
            (serializers.ModelSerializer,),
            attributes,
        )
