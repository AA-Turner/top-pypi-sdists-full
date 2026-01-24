import logging
from contextlib import suppress

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.utils import DataError
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.utils.translation import gettext as _
from rest_framework import filters, permissions, status
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from wbcore import viewsets
from wbcore.utils.html import convert_html2text

from ..models import User, UserActivity
from ..serializers import (
    ChangePasswordSerializer,
    GroupModelSerializer,
    GroupRepresentationSerializer,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
    PermissionModelSerializer,
    PermissionRepresentationSerializer,
    UserModelSerializer,
    UserProfileModelSerializer,
    UserRepresentationSerializer,
)
from .buttons import UserModelButtonConfig, UserProfileButtonConfig
from .display import (
    UserModelDisplay,
    UserPermissionModelDisplay,
    UserProfileModelDisplay,
)
from .endpoints import (
    UserPermissionsModelEndpointConfig,
    UserProfileModelEndpointConfig,
)
from .titles import (
    UserModelTitleConfig,
    UserPermissionsModelTitleConfig,
    UserProfileModelTitleConfig,
)

logger = logging.getLogger()


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny])
@authentication_classes([])
def reset_password_email(request):
    with suppress(User.DoesNotExist):
        user = User.objects.get(email=request.data["email"])
        try:
            user.reset_password(request)
        except Exception as e:
            logger.error("While user try to reset password, we encounter the error", extra={"user": user, "detail": e})
    return Response(
        {
            "status": "ok",
            "msg": _("If the email matches a user, it will receive an email inviting him to reset his password."),
        },
        status=status.HTTP_200_OK,
    )


@api_view(("POST",))
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    email = request.POST.get("email", "")
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    password = request.POST.get("password", "")
    if len(first_name) > 100 or len(last_name) > 100:
        return Response(
            data={"status": "fail", "msg": _("first and last name are too long. please provider a shorter name.")},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(password) > 128:
        return Response(
            data={
                "status": "fail",
                "msg": _("password is too long. please provider a password shorter than 128 characters."),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(email) > 255:
        return Response(
            data={
                "status": "fail",
                "msg": _("email is too long. please provider an email shorter than 255 characters."),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    if email and first_name and last_name and password:
        try:
            user = User.create_with_attributes(email, password, first_name=first_name, last_name=last_name)
            query_params = {}
            if success_redirect_url := request.POST.get("success_redirect_url", None):
                query_params["success_redirect_url"] = success_redirect_url
            if error_redirect_url := request.POST.get("error_redirect_url", None):
                query_params["error_redirect_url"] = error_redirect_url

            token = user.generate_temporary_token()
            url = f"{reverse('wbcore:authentication:activate', args=[user.uuid, token], request=request)}?{urlencode(query_params)}"

            # Construct registration mail and send
            rendered_message = render_to_string("user_registration_email.html", {"user": user, "url": url})
            email = EmailMultiAlternatives(
                _("Activate your account."),
                convert_html2text(rendered_message),
                settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email.attach_alternative(rendered_message, "text/html")
            email.send()
            return Response(
                {"status": "success", "msg": _("Please confirm your email address to complete the registration")},
                status=status.HTTP_200_OK,
            )
        except IntegrityError:
            return Response(
                {"status": "fail", "msg": _("Your account already exists")}, status=status.HTTP_409_CONFLICT
            )
        except DataError:
            return Response(
                {"status": "fail", "msg": _("Something went wrong with the submitted data, please try again later")},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(
        {"status": "fail", "msg": _("email, first_name, last_name and password must be provided")},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(("GET",))
@permission_classes([AllowAny])
@authentication_classes([])
def activate_user(request, uuid, token):
    user = get_object_or_404(User, uuid=uuid)
    if user.verify_temporary_token(token):
        user.is_active = True
        user.is_register = True
        user.save()
        # return redirect('home')
        if success_redirect_url := request.GET.get("success_redirect_url", None):
            return redirect(success_redirect_url, status=status.HTTP_200_OK)
        return render(
            request,
            "activate_confirm.html",
            {
                "title": _("Activation Successful"),
                "message": _("You are successfully registered. Please login"),
                "button_title": _("Login"),
                "redirect_url": getattr(settings, "AUTHENTICATION_ACTIVATION_REDIRECTION_URL", "/"),
            },
            status=status.HTTP_200_OK,
        )
    if error_redirect_url := request.GET.get("error_redirect_url", None):
        return redirect(error_redirect_url)
    else:
        return render(
            request,
            "activate_confirm.html",
            {
                "title": _("Activation Failed"),
                "message": _(
                    "The registration link you clicked was probably expired or your account is already activated. Please try to register again."
                ),
                "button_title": _("Register"),
                "redirect_url": reverse_lazy("wbcore:authentication:register"),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserRepresentationViewSet(viewsets.RepresentationViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    queryset = User.objects.none()
    serializer_class = UserRepresentationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.profile.is_internal:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    ordering_fields = ("username", "email", "date_joined")
    search_fields = ("profile__first_name", "profile__last_name", "email")
    ordering = ["email"]


class GroupRepresentationViewSet(viewsets.RepresentationViewSet):
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    ordering_fields = ordering = ("name",)
    search_fields = ("name",)
    queryset = Group.objects.all()
    serializer_class = GroupRepresentationSerializer
    ordering = ["name"]


class PermissionRepresentationViewSet(viewsets.RepresentationViewSet):
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    ordering_fields = ordering = ("name",)
    search_fields = ("name",)
    queryset = Permission.objects.all()
    serializer_class = PermissionRepresentationSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer


class UserPermissionsModelViewSet(PermissionViewSet):
    title_config_class = UserPermissionsModelTitleConfig
    endpoint_config_class = UserPermissionsModelEndpointConfig
    display_config_class = UserPermissionModelDisplay

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs["user_id"])
        return Permission.objects.filter(Q(user__id=user.id) | Q(group__in=user.groups.all())).distinct()


class UserProfileModelViewSet(viewsets.ModelViewSet):
    title_config_class = UserProfileModelTitleConfig
    endpoint_config_class = UserProfileModelEndpointConfig
    button_config_class = UserProfileButtonConfig
    display_config_class = UserProfileModelDisplay

    serializer_class = UserProfileModelSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=["PATCH"], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        data = request.POST.dict()
        data["user"] = user
        serializer = ChangePasswordSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            user.set_password(request.data["new_password"])
            user.save()
            return Response({"__notification": {"title": _("Password changed.")}}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], permission_classes=[permissions.IsAuthenticated])
    def reset_settings(self, request, pk=None):
        return Response(True)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    search_fields = ("profile__computed_str", "email", "profile__emails__address", "username")
    ordering_fields = ordering = ("email", "date_joined", "last_connection")

    serializer_class = UserModelSerializer

    filterset_fields = {
        "email": ["exact", "icontains"],
        "is_active": ["exact"],
        "date_joined": ["gte", "exact", "lte"],
    }
    title_config_class = UserModelTitleConfig
    button_config_class = UserModelButtonConfig
    display_config_class = UserModelDisplay

    def get_queryset(self):
        if self.request.user.has_perm("authentication.administrate_user"):
            qs = User.objects.all()
        elif self.request.user.profile.is_internal:
            qs = User.objects.filter(profile__relationship_managers=self.request.user.profile)
        else:
            qs = User.objects.filter(id=self.request.user.id)

        return (
            qs.annotate(last_connection=Coalesce(UserActivity.get_latest_login_datetime_subquery(use_user=True), None))
            .select_related("profile")
            .prefetch_related("groups", "user_permissions")
        )

    @action(detail=True, methods=["GET"], permission_classes=[permissions.IsAuthenticated])
    def reset_password(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        try:
            user.reset_password(request)
            return Response({"detail": _("Reset Password E-Mail sent: Check your mailbox")})
        except Exception:
            return Response({"detail": _("Reset Password Failed. Please contact an administrator")}, status=500)


class MyTokenObtainPairModelView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshModelView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
