import datetime
from pytz import utc
from rest_framework import mixins, viewsets, response, status
from push_notification.event import serializers
from push_notification.event import models


class PushNotificationViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Push notifications is a convenient way to get notified about events from the system.
    One can register a callback, i.e a valid URL that will be called whenever there is an
    event dispatched for this subscriber. Note that this can result in a large numbers of calls
    """
    queryset = models.PushNotification.actual_objects.all().order_by('-created_at')
    serializer_class = serializers.PushNotificationSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        push_notification, is_created = self.perform_create(serializer)

        return response.Response({
            'is_created': is_created,
            **self.get_serializer(instance=push_notification).data,
        }, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))

    def perform_create(self, serializer):
        # TODO: should we check not full path ?
        #  e.g. added earlier consumers/registration/created
        #  now he wants to add consumers/registration/*
        # push_notifications = models.PushNotification.objects.filter(
        #     callback_url=validated_data['callback_url'],
        # )
        # for push_notification in push_notifications:
        #     if fnmatch.fnmatch(push_notification.pattern, validated_data['pattern']):
        #         created = True
        #         return push_notification, created
        push_notification, created = models.PushNotification.objects.update_or_create(
            **serializer.data,
            defaults={
                'deleted_at': None
            }
        )
        return push_notification, created

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.datetime.utcnow().replace(tzinfo=utc)
        instance.save()
