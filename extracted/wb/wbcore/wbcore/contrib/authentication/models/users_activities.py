from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import user_logged_in
from django.db import models
from django.db.models import DateTimeField, OuterRef, Subquery
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wbcore.workers import Queue

from .users import User

ACCESS_TOKEN_LIFETIME = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds


class UserActivity(models.Model):
    SUCCESS = _("Success")
    FAILED = _("Failed")

    ACTIVITY_STATUS = ((SUCCESS, _("Success")), (FAILED, _("Failed")))

    class Type(models.TextChoices):
        LOGIN = "LOGIN", _("Login")

    IP = models.GenericIPAddressField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "authentication.User", related_name="login_activities", null=True, on_delete=models.SET_NULL
    )
    status = models.CharField(max_length=8, default=SUCCESS, choices=ACTIVITY_STATUS, null=True, blank=True)
    jti = models.CharField(max_length=32, default="", blank=True)
    type = models.CharField(max_length=16, default=Type.LOGIN, choices=Type.choices, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    latest_refresh = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return _("Activity of {user} at {date}").format(user=str(self.user), date=self.date)

    class Meta:
        verbose_name = _("User Login Activity")
        verbose_name_plural = _("User Login Activities")

    @classmethod
    def get_latest_login_datetime_subquery(cls, profile_name="pk", use_user=False):
        """
        Create a subquery to retrieve the latest login datetime information

        Arguments:
            profile_name {str} -- The OuterRef field for user__profile
        Returns:
            Subquery -- Subquery for latest login detail
        """

        if use_user:
            qs = UserActivity.objects.filter(user__id=OuterRef("id"))
        else:
            qs = UserActivity.objects.filter(user__profile__id=OuterRef(profile_name))
        return Subquery(qs.order_by("-latest_refresh").values("latest_refresh")[:1], output_field=DateTimeField())

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:authentication:useractivity"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{user}}: {{date}}-{{latest_refresh}}"


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    """
    Signal triggerd whenever a user log into a new session. Create a new UserActivity for that user
    """
    user_agent_info = (request.META.get("HTTP_USER_AGENT", "<unknown>")[:255],)
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    access_token_lifespan = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds
    state = UserActivity.SUCCESS if kwargs.get("authentication_status", True) else UserActivity.FAILED
    if jti := kwargs.get("jti", None):
        # TODO: What if request is None?
        UserActivity.objects.create(
            IP=ip,
            user=user,
            user_agent_info=user_agent_info,
            status=state,
            jti=jti,
            latest_refresh=timezone.now() + timedelta(seconds=access_token_lifespan),
        )


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def refresh_user_activity(user_id, refresh_time, jti):
    """
    Signal triggerd whenever a refresh token is submit from the frontend. Update latest_refresh to the associated UserActivity.
    """
    user = User.objects.get(id=user_id)
    user_activity, created = UserActivity.objects.get_or_create(user=user, jti=jti)
    if created:
        elapse = (refresh_time - user_activity.latest_refresh).seconds
        access_token_lifespan = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds
        if elapse > access_token_lifespan:
            user_activity.latest_refresh = refresh_time
            user_activity.save()
