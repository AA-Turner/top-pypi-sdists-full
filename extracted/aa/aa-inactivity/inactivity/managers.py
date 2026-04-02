"""Managers for Inactivity."""

# pylint: disable = missing-class-docstring

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Case, Q, Value, When
from django.utils.timezone import now

if TYPE_CHECKING:
    from .models import LeaveOfAbsence, Webhook


class LeaveOfAbsenceQuerySet(models.QuerySet):
    def filter_pending(self):
        """Filter all pending requests."""
        return self.filter(Q(end=None) | Q(end__gt=now()), Q(approver=None))

    def filter_processed(self):
        """Filter all processed requests."""
        return self.filter(approver__isnull=False)

    def annotate_status(self):
        """Add status annotations."""
        return self.annotate(
            status=Case(
                When(approver__isnull=True, then=Value(self.model.Status.PENDING)),
                When(reason__isnull=False, then=Value(self.model.Status.DENIED)),
                default=Value(self.model.Status.APPROVED),
            )
        )


class LeaveOfAbsenceManagerBase(models.Manager):
    def unapproved_count(self):
        """Count number of unapproved requests."""
        return self.filter_pending().count()


LeaveOfAbsenceManager = LeaveOfAbsenceManagerBase.from_queryset(LeaveOfAbsenceQuerySet)


class InactivityPingConfigQueryset(models.QuerySet):
    def relevant_for_user(self, user: User):
        """Webhooks that are relevant for the given user."""
        pks = {config.pk for config in self.all() if config.is_applicable_to(user)}
        return self.filter(pk__in=pks)


class InactivityPingConfigManagerBase(models.Manager):
    pass


InactivityPingConfigManager = InactivityPingConfigManagerBase.from_queryset(
    InactivityPingConfigQueryset
)


class WebhookQueryset(models.QuerySet):
    def relevant_for_user(self, user: User):
        """Webhooks that are relevant for the given user."""
        from .models import InactivityPingConfig

        configs = list(InactivityPingConfig.objects.relevant_for_user(user))
        return self.filter(Q(ping_configs__in=configs) | Q(ping_configs=None))

    def filter_notification_type(self, notif_type: Webhook.NotificationType):
        """Return Queryset with a filter for a notification type."""
        return self.filter(
            notification_types__regex=rf"(^|,){re.escape(notif_type)}(,|$)"
        )


class WebhookManagerBase(models.Manager):
    def send_message_to_active_webhooks(
        self, loa: LeaveOfAbsence, notif_type: Webhook.NotificationType, message: str
    ):
        """Send a message to all active webhooks."""
        webhooks = (
            self.relevant_for_user(loa.user)
            .filter(is_active=True)
            .filter_notification_type(notif_type)
        )
        for webhook in webhooks:
            webhook.send_message(message)


WebhookManager = WebhookManagerBase.from_queryset(WebhookQueryset)
