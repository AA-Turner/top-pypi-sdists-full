"""Models for Inactivity."""

import humanize
from multiselectfield import MultiSelectField
from multiselectfield.utils import get_max_length

from django.contrib.auth.models import Group, User
from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from allianceauth.authentication.models import State

from .app_settings import INACTIVITY_TASKS_DEFAULT_PRIORITY
from .helpers import user_for_display
from .managers import InactivityPingConfigManager, LeaveOfAbsenceManager, WebhookManager


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access this app"),
            ("manage_leave", "Can manage leave of absence requests"),
        )


class InactivityPingConfig(models.Model):
    """A ping configuration."""

    name = models.CharField(
        max_length=48,
        unique=True,
        help_text=_("Internal name for the inactivity policy. Must be unique."),
    )
    days = models.PositiveIntegerField(
        help_text=_("The number of days the user must be inactive.")
    )
    text = models.TextField(
        help_text=_("The text of the message or notification sent to the end user.")
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_(
            "Groups subject to the inactivity policy. If empty, applies to all groups."
        ),
        related_name="+",
    )

    states = models.ManyToManyField(
        State,
        blank=True,
        help_text=_(
            "States subject to the inactivity policy. If empty, applies to all states."
        ),
        related_name="+",
    )

    objects = InactivityPingConfigManager()

    class Meta:
        default_permissions = ()
        verbose_name = _("inactivity policy")
        verbose_name_plural = _("inactivity policies")

    def __str__(self):
        return _("inactivity policy: %(name)s") % {"name": self.name}

    def is_applicable_to(self, user: User) -> bool:
        """Return True if use is applicable to this config, else False."""
        is_applicable = True
        if self.groups.count() > 0:
            is_applicable &= self.groups.filter(user=user).count() > 0
        if self.states.count() > 0:
            is_applicable &= self.states.filter(userprofile=user.profile).count() > 0
        return is_applicable


class InactivityPing(models.Model):
    """An inactive user who has been notified."""

    config = models.ForeignKey(InactivityPingConfig, on_delete=models.CASCADE)
    last_login_at = models.DateTimeField(null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        default_permissions = ()

    def __str__(self):
        try:
            user_name = self.user.profile.main_character.character_name
        except AttributeError:
            user_name = self.user.username

        return _("ping [policy='%(config_name)s' user='%(user_name)s']") % {
            "config_name": self.config.name,
            "user_name": user_name,
        }


class LeaveOfAbsence(models.Model):
    """A leave of absence request."""

    class Status(models.TextChoices):
        """A leave of absence status."""

        PENDING = "pending"
        APPROVED = "approved"
        DENIED = "denied"

    approver = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="+"
    )
    created_at = models.DateTimeField(null=True, default=None)
    reason = models.TextField(
        blank=True,
        null=True,
        default=None,
        help_text=_("Reason for rejecting a request"),
    )
    end = models.DateField(
        blank=True,
        null=True,
        help_text=_(
            "The end of the leave of absence. Leave blank for an indefinite leave."
        ),
    )
    notes = models.TextField(
        blank=True,
        verbose_name="description",
        help_text=_("Description what this leave of absence request is about."),
    )
    start = models.DateField(help_text=_("The start of the leave of absence."))
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leave_of_absence_requests",
        help_text="The requestor",
    )

    objects = LeaveOfAbsenceManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        requestor = user_for_display(self.user)
        return _(
            "%(requestor)s's leave of absence request "
            "from %(start)s to %(end)s %(details)s"
        ) % {
            "end": self.end_text,
            "start": self.start,
            "requestor": requestor.name_with_ticker,
            "details": f'"{self.notes[:25]}"' if self.notes else "",
        }

    def save(self, *args, **kwargs) -> None:
        is_new = self._state.adding is True
        if is_new and not self.created_at:
            self.created_at = now()
        return super().save(*args, **kwargs)

    @property
    def approver_name(self) -> str:
        """Name of the approver."""
        if not self.approver:
            return ""
        approver = user_for_display(self.approver)
        return approver.name_with_ticker

    @property
    def end_text(self) -> str:
        """Return text for end property."""
        return str(self.end) if self.end else _("open end")

    @property
    def requestor_name(self) -> str:
        """Name of the requestor."""
        requestor = user_for_display(self.user)
        return requestor.name_with_ticker

    def to_output_dict(self) -> dict:
        """Convert object to an output dictionary."""
        requestor_display = user_for_display(self.user)
        requestor_corporation_name = (
            requestor_display.character.corporation_name
            if requestor_display.character
            else ""
        )
        approver_display = user_for_display(self.approver) if self.approver else None
        duration = (
            humanize.naturaldelta(self.end - self.start) if self.end else _("open end")
        )
        created_at_display = (
            humanize.naturaltime(self.created_at) if self.created_at else "?"
        )
        try:
            status = self.status  # type: ignore
        except AttributeError:
            status_html = ""
        else:
            if status == self.Status.DENIED:
                status_html = format_html(
                    '<span class="text-danger text-underline-dotted" title="{}">{}</span>',
                    f"Reason: {self.reason}",
                    status,
                )
            else:
                status_html = format_html(
                    '<span class="text-success">{}</span>', status
                )

        result = {
            "approver": approver_display.name if approver_display else "",
            "approver_html": approver_display.html if approver_display else "",
            "created_at": {
                "display": created_at_display,
                "sort": self.created_at.isoformat() if self.created_at else "",
            },
            "duration": duration,
            "end": self.end_text,
            "notes": self.notes if self.notes else "-",
            "requestor": requestor_display.name,
            "requestor_html": requestor_display.html,
            "requestor_corporation": requestor_corporation_name,
            "pk": self.pk,
            "start": self.start,
            "status_html": status_html,
        }
        return result


class Webhook(models.Model):
    "A webhook configuration to send message to."

    class NotificationType(models.TextChoices):
        """A notification type."""

        INACTIVE_USER = "1", "Inactive User"
        LOA_NEW = "10", "Leave of Absence - Created"
        LOA_APPROVED = "11", "Leave of Absence - Approved"

    class WebhookType(models.IntegerChoices):
        """A type of a webhook."""

        DISCORD = 1, _("Discord Webhook")

    name = models.CharField(
        max_length=64, unique=True, help_text=_("short name to identify this webhook")
    )

    notification_types = MultiSelectField(
        choices=NotificationType.choices,
        max_length=get_max_length(NotificationType.choices, None),
        help_text=_(
            "only notifications of the selected types are sent to this webhook"
        ),
    )

    ping_configs = models.ManyToManyField(
        InactivityPingConfig,
        blank=True,
        help_text=_(
            "The inactivity policies to alert for. "
            "If left blank, all policies are alerted for."
        ),
    )

    url = models.CharField(
        max_length=255,
        unique=True,
        help_text=_(
            "URL of this webhook, e.g. "
            "https://discordapp.com/api/webhooks/123456/abcdef"
        ),
    )
    webhook_type = models.IntegerField(
        choices=WebhookType.choices,
        default=WebhookType.DISCORD,
        help_text=_("type of this webhook"),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("whether notifications are currently sent to this webhook"),
    )

    objects = WebhookManager()

    def __str__(self):
        return self.name

    def send_message(self, content: str):
        """Send message to webhook asynchronously."""
        from .tasks import send_message_to_webhook

        if self.webhook_type == self.WebhookType.DISCORD:
            send_message_to_webhook.apply_async(
                kwargs={"webhook_pk": self.pk, "content": content},
                priority=INACTIVITY_TASKS_DEFAULT_PRIORITY,
            )
