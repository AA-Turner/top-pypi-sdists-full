"""Tasks for Inactivity."""

import datetime as dt
from http import HTTPStatus

import discord
import humanize
import requests
from celery import Task, shared_task
from memberaudit.models import Character

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Max, Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from allianceauth.notifications import notify
from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

from . import __title__
from .app_settings import INACTIVITY_TASKS_DEFAULT_PRIORITY
from .models import InactivityPing, InactivityPingConfig, Webhook

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class ModifiedSession(requests.Session):
    """Modified requests session for adding a timeout
    when sending message to a Webhook.
    """

    def post(self, *args, **kwargs) -> requests.Response:
        return super().post(*args, timeout=30, **kwargs)


@shared_task
def check_inactivity():
    """Check all users with registered Member Audit characters for inactivity.
    This is the main periodic task.
    """
    if not InactivityPingConfig.objects.exists():
        logger.warning("No inactivity config found. Nothing to do.")
        return

    registered_users = User.objects.filter(
        character_ownerships__character__memberaudit_character__isnull=False
    ).distinct()
    for user_pk in registered_users.values_list("pk", flat=True):
        check_inactivity_for_user.apply_async(
            kwargs={"user_pk": user_pk}, priority=INACTIVITY_TASKS_DEFAULT_PRIORITY
        )


@shared_task
def check_inactivity_for_user(user_pk: int):
    """Perform inactivity checks for given user."""
    user = User.objects.get(pk=user_pk)
    today = dt.date.today()

    has_active_loa = user.leave_of_absence_requests.filter(
        Q(start__lt=today), Q(end=None) | Q(end__gt=today), ~Q(approver=None)
    ).exists()
    if has_active_loa:
        return

    last_loa = (
        user.leave_of_absence_requests.filter(Q(end__lt=today), ~Q(approver=None))
        .order_by("-end")
        .first()
    )
    for config in InactivityPingConfig.objects.relevant_for_user(user):
        threshold_date = today - dt.timedelta(days=config.days)
        threshold_datetime = dt.datetime.combine(
            date=threshold_date, time=dt.datetime.min.time(), tzinfo=dt.timezone.utc
        )
        characters = Character.objects.owned_by_user(user)

        is_active = characters.filter(
            Q(online_status__last_login__gt=threshold_datetime)
            | Q(online_status__last_logout__gt=threshold_datetime),
        ).exists()
        if is_active:
            InactivityPing.objects.filter(user__pk=user_pk, config=config).delete()

        is_excused = last_loa and (not last_loa.end or threshold_date < last_loa.end)
        was_pinged = InactivityPing.objects.filter(
            user__pk=user_pk, config=config
        ).exists()
        is_registered = characters.exists()
        if not is_active and is_registered and not was_pinged and not is_excused:
            last_login_at = characters.aggregate(Max("online_status__last_login")).get(
                "online_status__last_login__max"
            )
            send_inactivity_ping.apply_async(
                kwargs={
                    "user_pk": user_pk,
                    "config_pk": config.pk,
                    "last_login_at": last_login_at,
                },
                priority=INACTIVITY_TASKS_DEFAULT_PRIORITY,
            )


@shared_task
def send_inactivity_ping(user_pk: int, config_pk: int, last_login_at: dt.datetime):
    """Send an inactivity ping to webhooks."""
    config = InactivityPingConfig.objects.get(pk=config_pk)
    user = User.objects.get(pk=user_pk)
    notify.danger(user, title="Inactivity notification", message=config.text)
    InactivityPing.objects.create(config=config, user=user, last_login_at=last_login_at)
    relevant_webhooks = Webhook.objects.filter(
        Q(ping_configs=config) | Q(ping_configs=None),
        Q(is_active=True),
    ).filter_notification_type(Webhook.NotificationType.INACTIVE_USER)
    for webhook in relevant_webhooks:
        duration = humanize.naturaldelta(now() - last_login_at)
        message = _(
            "**%(user_name)s** has been inactive for **%(duration)s** "
            "and has been notified according to **%(config_name)s** policy"
        ) % {
            "user_name": user.profile.main_character.character_name,
            "duration": duration,
            "config_name": config.name,
        }
        send_message_to_webhook.apply_async(
            kwargs={"webhook_pk": webhook.pk, "content": message},
            priority=INACTIVITY_TASKS_DEFAULT_PRIORITY,
        )


@shared_task(bind=True, autoretry_for=(requests.Timeout,), retry_backoff=True)
def send_message_to_webhook(self: Task, webhook_pk: int, content: str):
    """Send a message to the webhook"""
    webhook = Webhook.objects.get(pk=webhook_pk)
    logger.info("Sending message to webhook: %s", webhook)
    with ModifiedSession() as session:
        hook = discord.SyncWebhook.from_url(webhook.url, session=session)
        try:
            with cache.lock(f"inactivity-lock-webhook-{webhook.pk}"):
                hook.send(content=content)
        except discord.HTTPException as exc:
            if exc.status == HTTPStatus.TOO_MANY_REQUESTS:
                try:
                    retry_after = int(exc.response.headers["Retry-After"])
                except KeyError:
                    retry_after = 60
                logger.error(
                    "%s: Rate limited. Trying again in %s seconds. Error: %s",
                    webhook,
                    retry_after,
                    exc.response.text,
                )
                raise self.retry(countdown=retry_after)
            raise exc
