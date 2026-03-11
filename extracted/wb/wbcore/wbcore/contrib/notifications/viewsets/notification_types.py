from django.db.models import Case, Value, When
from django.db.models.query import F, QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from wbcore import viewsets
from wbcore.contrib.notifications.models import (
    NotificationType,
    NotificationTypeSetting,
)
from wbcore.contrib.notifications.serializers import (
    NotificationTypeRepresentationSerializer,
    NotificationTypeSettingModelSerializer,
)

from ...icons import WBIcon
from .configs.notification_types import NotificationTypeSettingDisplayConfig, NotificationTypeSettingEndpointConfig


class NotificationTypeRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeRepresentationSerializer


class NotificationTypeSettingModelViewSet(viewsets.ModelViewSet):
    queryset = NotificationTypeSetting.objects.all()
    serializer_class = NotificationTypeSettingModelSerializer

    endpoint_config_class = NotificationTypeSettingEndpointConfig
    display_config_class = NotificationTypeSettingDisplayConfig

    search_fields = ["notification_type__title", "notification_type__help_text"]

    def create(self, request: Request) -> Response:
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request: Request, pk=None) -> Response:
        return Response(status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self) -> QuerySet[NotificationTypeSetting]:
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .annotate(
                help_text=F("notification_type__help_text"),
                locked=F("notification_type__is_lock"),
                locked_icon=Case(When(locked=True, then=Value(WBIcon.LOCK.icon)), default=Value(None)),
            )
            .select_related("notification_type", "user")
        )
