from datetime import datetime, timedelta

from celery import group, shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone
from django.utils.html import strip_tags

from wbcore.contrib.authentication.models import User
from wbcore.contrib.notifications.models import NotificationType
from wbcore.workers import Queue


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def send_notification_brief(rendered_template: str, email: str):
    msg = EmailMultiAlternatives(
        subject="Notification Digest",
        body=strip_tags(rendered_template),
        from_email=getattr(settings, "WBCORE_NOTIFICATION_EMAIL_FROM", "no_reply@stainly.com"),
        to=[email],  # type: ignore
    )
    msg.attach_alternative(rendered_template, "text/html")
    msg.send()


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def orchestrate_aggregated_email_notification(now: datetime | None = None):
    if not now:
        now = timezone.now()
    # as a safeguard, we don't trigger notification for unsent notifications that are older than 24 hours.
    due_notifications = NotificationType.objects.filter(created__gt=now - timedelta(days=1)).filter_unsent_and_due()

    users = User.objects.filter(
        id__in=due_notifications.values_list("user_id", flat=True), is_active=True
    ).filter_internal()
    tasks = []
    for user in users:
        user_due_notifications = due_notifications.filter(user=user)
        rendered_template = get_template("notifications/notification_aggregated_template.html").render(
            {"notifications": user_due_notifications.distinct("checksum")}
        )
        tasks.append(send_notification_brief.si(rendered_template, user.email))
        user_due_notifications.update(sent_email=now)
    # we trigger the mail sending asynchronously to release this task as fast as possible
    if tasks:
        group(tasks).apply_async()
