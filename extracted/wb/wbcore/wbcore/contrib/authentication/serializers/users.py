import logging

from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from jwt import decode
from rest_framework import exceptions, serializers
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from wbcore import serializers as wb_serializers
from wbcore.contrib.directory.models import Person
from wbcore.contrib.directory.serializers import PersonRepresentationSerializer

from ..models import Group, Permission, User
from ..models.users_activities import refresh_user_activity

logger = logging.getLogger()


class ChangePasswordSerializer(wb_serializers.Serializer):
    old_password = wb_serializers.CharField(label=gettext_lazy("Old password"), required=True, secure=True)
    new_password = wb_serializers.CharField(label=gettext_lazy("New Password"), required=True, secure=True)
    confirm_password = wb_serializers.CharField(label=gettext_lazy("Confirm new Password"), required=True, secure=True)

    def validate(self, data):
        if not (request := self.context.get("request")):
            raise ValueError(_("No request found"))
        user = request.user
        # user = data.get("user")
        current_password = data.get("old_password")
        if not user.check_password(current_password):
            raise serializers.ValidationError({"old_password": _("Wrong password")})

        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"new_password": _("Password don't match"), "confirm_password": _("Password don't match")}
            )

        if user.check_password(new_password):
            raise serializers.ValidationError(
                {
                    "new_password": _("New and old password cannot be the same"),
                    "confirm_password": _("New and old password cannot be the same"),
                }
            )

        if user.check_password(current_password):
            try:
                validate_password(new_password)
                return super().validate(data)
            except serializers.ValidationError as e:
                raise serializers.ValidationError({"new_password": e, "confirm_password": e}) from e

    class Meta:
        fields = ("current_password", "new_password", "confirm_password")


class UserRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:authentication:user-detail")
    computed_str = wb_serializers.SerializerMethodField()

    def get_computed_str(self, obj):
        if obj.profile:
            return obj.profile.computed_str
        return f"{obj.username} ({obj.email})"

    class Meta:
        model = User
        fields = ("id", "username", "computed_str", "email", "_detail")


class PermissionRepresentationField(serializers.RelatedField):
    def to_representation(self, value):
        return "{0.content_type.app_label}.{0.codename}".format(value)


class GroupRepresentationSerializer(wb_serializers.RepresentationSerializer):
    # _detail = wb_serializers.HyperlinkField(reverse_name='wbcore:authentication:group-detail')
    value_key = "id"
    label_key = "name"

    class Meta:
        model = Group
        fields = ("id", "name")


class PermissionRepresentationSerializer(wb_serializers.RepresentationSerializer):
    # _detail = serializers.SerializerMethodField()

    endpoint = "wbcore:authentication:permissionrepresentation-list"
    value_key = "id"
    label_key = "{{name}}"

    # _detail = wb_serializers.HyperlinkField(reverse_name='wbcore:authentication:permission-detail')

    class Meta:
        model = Permission
        fields = ("id", "name")


class GroupModelSerializer(wb_serializers.ModelSerializer):
    _permissions = PermissionRepresentationSerializer(many=True, read_only=True, source="permissions")

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "permissions",
            "_permissions",
        )


class PermissionModelSerializer(wb_serializers.ModelSerializer):
    content_type_repr = wb_serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ("id", "name", "content_type", "content_type_repr", "codename", "group_set")

    def get_content_type_repr(self, obj):
        return str(obj.content_type.app_label)


class UserModelSerializer(wb_serializers.ModelSerializer):
    _groups = GroupRepresentationSerializer(source="groups", many=True)
    _user_permissions = PermissionRepresentationSerializer(source="user_permissions", many=True)
    _profile = PersonRepresentationSerializer(many=False, required=False, source="profile")

    is_active = wb_serializers.BooleanField(default=True, label=gettext_lazy("Is Active"))
    is_superuser = wb_serializers.BooleanField(default=False)
    last_connection = wb_serializers.DateTimeField(read_only=True, label=gettext_lazy("Last Connection"))
    email = wb_serializers.CharField(required=False, label=gettext_lazy("E-Mail"))
    username = wb_serializers.CharField(required=False, label=gettext_lazy("Username"))
    profile = wb_serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), label=gettext_lazy("Profile"))

    @wb_serializers.register_resource()
    def reset_password(self, instance, request, user):
        res = {
            "reset_password": reverse(
                "wbcore:authentication:user-reset-password", args=[instance.id], request=request
            ),
            "user_permissions": reverse(
                "wbcore:authentication:user-permissions-list", args=[instance.id], request=request
            ),
        }
        if instance.profile:
            res["profile"] = reverse("wbcore:directory:person-detail", args=[instance.profile.id], request=request)
        return res

    @wb_serializers.register_resource()
    def user_activity(self, instance, request, user):
        additional_resources = dict()
        additional_resources["user_activity"] = reverse(
            "wbcore:authentication:user-useractivity-list", args=[instance.id], request=request
        )
        additional_resources["user_activity_chart"] = reverse(
            "wbcore:authentication:user-useractivitychart-list", args=[instance.id], request=request
        )
        return additional_resources

    def get_all_permissions(self, obj):
        permissions = list(obj.user_permissions.all().values_list("id", flat=True))
        for group in obj.groups.all():
            group_permissions = group.permissions.all().values_list("id", flat=True)
            permissions.extend(list(group_permissions))
        return list(set(permissions))

    def get_all_permissions_repr(self, obj):
        permissions = list()
        permissions_dict = list(obj.user_permissions.all().values_list("content_type__app_label", "codename"))
        permissions.extend(["{0[0]}.{0[1]}".format(_permission) for _permission in permissions_dict])
        for group in obj.groups.all():
            group_permissions = group.permissions.all().values_list("content_type__app_label", "codename")
            permissions.extend(["{0[0]}.{0[1]}".format(_permission) for _permission in group_permissions])
        return list(set(permissions))

    @classmethod
    def prefetch_related(cls, queryset, request):
        queryset = queryset.prefetch_related("groups")
        queryset = queryset.prefetch_related("user_permissions")
        return queryset

    def validate(self, data):
        obj = self.instance

        username = data.pop("username", obj.username if obj else None)
        email = data.pop("email", obj.email if obj else None)
        errors = {}
        if profile := data.pop("profile", obj.profile if obj else None):
            if not username:
                username = User.generate_username(profile.first_name, profile.last_name)
            if not email and (primary_emails := profile.emails.filter(primary=True).first()):
                email = primary_emails.address

        if not email:
            errors["email"] = _("You need to assign a profile or add a valid email address")
        if not username:
            errors["username"] = _("You need to assign a profile or add a valid last name")

        if len(errors.keys()) > 0:
            raise serializers.ValidationError(errors)
        if (user_account := getattr(profile, "user_account", None)) and (user_account != self.instance):
            errors["profile"] = f"An account already exists for this profile under the email {user_account.email}"
        data["profile"] = profile

        data["username"] = username
        data["email"] = email
        if errors:
            raise ValidationError(errors)
        return super().validate(data)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "date_joined",
            "last_connection",
            "user_permissions",
            "_user_permissions",
            "groups",
            "_groups",
            # 'all_permissions',
            # 'all_permissions_repr',
            "profile",
            "_profile",
            "is_staff",
            "is_active",
            "is_superuser",
            # 'change_password',
            # 'reset_password',
            # 'main_manager_of',
            "_additional_resources",
        )


class UserProfileModelSerializer(wb_serializers.ModelSerializer):
    username = wb_serializers.CharField()
    email = wb_serializers.ReadOnlyField()
    profile = wb_serializers.PrimaryKeyRelatedField(read_only=True)
    _profile = PersonRepresentationSerializer(many=False, read_only=True, source="profile")
    generic_auth_token_key = wb_serializers.SerializerMethodField(label="Generic Token Key")

    calendar_subscription_link = wb_serializers.SerializerMethodField()
    profile_image = wb_serializers.ImageField(source="profile.profile_image", read_only=True)
    first_name = wb_serializers.CharField(source="profile.first_name", read_only=True)
    prefix = wb_serializers.CharField(source="profile.prefix", read_only=True)
    last_name = wb_serializers.CharField(source="profile.last_name", read_only=True)
    birthday = wb_serializers.DateField(source="profile.birthday", read_only=True)

    @wb_serializers.register_resource()
    def additional_resources(self, instance, request, user):
        resources = dict()
        if user.id == instance.id:
            resources["change_password"] = reverse(
                "wbcore:authentication:userprofile-change-password", args=[instance.id], request=request
            )
            resources["reset_settings"] = reverse(
                "wbcore:authentication:userprofile-reset-settings", args=[instance.id], request=request
            )
            if user.profile.is_internal:
                resources["see_profile"] = reverse(
                    "wbcore:directory:person-detail", args=[instance.profile.id], request=request
                )
        return resources

    def get_calendar_subscription_link(self, obj):
        if (key := obj.generic_auth_token_key) and (request := self.context.get("request")):
            full_url = request.build_absolute_uri(reverse("wbcore:agenda:get_ics"))
            return f"{full_url}?token={key}"
        return "N/A"

    def get_generic_auth_token_key(self, obj):
        return obj.generic_auth_token_key

    def update(self, instance, validated_data):
        profile = validated_data.get("profile", None)
        if profile:
            instance.profile.profile_image = profile.get("profile_image", instance.profile.profile_image)
            instance.profile.first_name = profile.get("first_name", instance.profile.first_name)
            instance.profile.prefix = profile.get("prefix", instance.profile.prefix)
            instance.profile.last_name = profile.get("last_name", instance.profile.last_name)
            instance.profile.birthday = profile.get("birthday", instance.profile.birthday)
            instance.profile.save()
        return instance

    class Meta:
        model = User
        fields = (
            "id",
            "profile_image",
            "first_name",
            "last_name",
            "prefix",
            "birthday",
            "username",
            "email",
            "_profile",
            "profile",
            "generic_auth_token_key",
            "calendar_subscription_link",
            "_additional_resources",
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authentication_status = True
        try:
            data = super().validate(attrs)
            refresh = RefreshToken(data["refresh"])
            user = User.objects.filter(email=attrs[self.username_field]).first()
            jti = refresh.payload.get("jti", None)
            if user and jti:
                user_logged_in.send(
                    sender=MyTokenObtainPairSerializer.__class__,
                    request=self.context.get("request"),
                    user=user,
                    authentication_status=authentication_status,
                    jti=jti,
                )
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            ) from None
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_data = decode(attrs["refresh"], settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get("user_id", None)
        jti = decoded_data.get("jti", None)
        if user_id and jti:
            refresh_user_activity.delay(user_id, timezone.now(), jti)
        return data
