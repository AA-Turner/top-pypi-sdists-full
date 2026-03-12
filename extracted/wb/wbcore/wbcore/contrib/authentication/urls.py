from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from rest_framework_simplejwt.views import (  # TokenObtainPairView,; TokenRefreshView,
    TokenVerifyView,
)

from wbcore.routers import WBCoreRouter

from .viewsets import (
    GroupRepresentationViewSet,
    GroupViewSet,
    MyTokenObtainPairModelView,
    MyTokenRefreshModelView,
    PermissionRepresentationViewSet,
    PermissionViewSet,
    UserActivityChart,
    UserActivityModelViewSet,
    UserActivityTable,
    UserActivityUserChart,
    UserActivityUserModelViewSet,
    UserModelViewSet,
    UserPermissionsModelViewSet,
    UserProfileModelViewSet,
    UserRepresentationViewSet,
)
from .viewsets.users import activate_user, register_user, reset_password_email

router = WBCoreRouter()
router.register(r"userrepresentation", UserRepresentationViewSet, basename="userrepresentation")
router.register(r"grouprepresentation", GroupRepresentationViewSet, basename="grouprepresentation")
router.register(r"permissionrepresentation", PermissionRepresentationViewSet, basename="permissionrepresentation")

router.register(r"group", GroupViewSet)
router.register(r"permission", PermissionViewSet)
router.register(r"user", UserModelViewSet, basename="user")
router.register(r"userprofile", UserProfileModelViewSet, basename="userprofile")

router.register(r"useractivitychart", UserActivityChart, basename="useractivitychart")
router.register(r"useractivity", UserActivityModelViewSet, basename="useractivity")
router.register(r"useractivitytable", UserActivityTable, basename="useractivitytable")

user_router = WBCoreRouter()
user_router.register(r"useractivity", UserActivityUserModelViewSet, basename="user-useractivity")
user_router.register(r"useractivitychart", UserActivityUserChart, basename="user-useractivitychart")
user_router.register(
    r"permissions",
    UserPermissionsModelViewSet,
    basename="user-permissions",
)

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/", MyTokenObtainPairModelView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", MyTokenRefreshModelView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # url(r'^api_token/', get_api_token, name='api-token'),
    # url(r'^wb_menu/', WBMenuAPIView.as_view(), name='wb-menu'),
    path("", include(router.urls)),
    path("user/<int:user_id>/", include(user_router.urls)),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/reset_password.html",
            email_template_name="authentication/email/password_reset_email.html",
            html_email_template_name="authentication/email/password_reset_email_html.html",
            success_url=reverse_lazy("wbcore:authentication:password_reset_done"),
        ),
        name="reset_password",
    ),
    # OR direct Post request view
    path("reset_password_email/", reset_password_email, name="reset_password_email"),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_sent.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_form.html",
            success_url=reverse_lazy("wbcore:authentication:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_done.html"),
        name="password_reset_complete",
    ),
    path("register/", register_user, name="register"),
    path("activate/<uuid>/<token>", activate_user, name="activate"),
]
