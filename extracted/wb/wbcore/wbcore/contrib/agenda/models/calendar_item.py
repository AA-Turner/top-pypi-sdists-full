from contextlib import suppress

from celery import shared_task
from django.apps import apps
from django.contrib.auth.backends import ModelBackend
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models, transaction
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from ics import Event

from wbcore.contrib.color.fields import ColorField
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.icons.models import IconField
from wbcore.models import WBModel
from wbcore.signals import pre_merge
from wbcore.utils.itertools import get_inheriting_subclasses
from wbcore.utils.models import DeleteToDisableMixin
from wbcore.workers import Queue


class CalendarItem(DeleteToDisableMixin, WBModel):
    AUTOMATICALLY_CLEAN_SOFT_DELETED_OBJECTS = True

    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC", _("Public")
        PRIVATE = "PRIVATE", _("Private")
        CONFIDENTIAL = "CONFIDENTIAL", _("Confidential")

    color = ColorField(
        blank=True,
        null=True,
    )
    entities = models.ManyToManyField(
        to="directory.Entry", verbose_name=_("Entities"), related_name="calendar_entities"
    )
    entity_list = models.JSONField(blank=True, null=True)
    icon = IconField(
        max_length=128,
        verbose_name=_("Icon"),
        blank=True,
        null=True,
    )
    visibility = models.CharField(
        max_length=255,
        choices=Visibility.choices,
        verbose_name=_("Visibility"),
        default=Visibility.PUBLIC,
    )
    item_type = models.CharField(max_length=255, verbose_name=_("Type"), blank=True, null=True)

    period = DateTimeRangeField(
        blank=True,
        null=True,
        # Translator: In this context, it is a period of time
        verbose_name=_("Period"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    conference_room = models.ForeignKey(
        to="agenda.ConferenceRoom",
        verbose_name=_("Conference Room"),
        related_name="calendar_item",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    all_day = models.BooleanField(
        default=False, verbose_name=_("All Day"), help_text=_("Check this if the activity spans throughout the day")
    )
    is_cancelled = models.BooleanField(default=False, verbose_name=_("Is Cancelled"))
    is_deletable = models.BooleanField(default=True, verbose_name=_("Is Deletable"))

    def get_casted_calendar_item(self) -> models.Model:
        """
        Cast the calendar item into its child representative

        Raises ValueError, AttributeError or LookupError on wrong item_type
        """
        model = apps.get_model(self.item_type)
        return model.objects.get(pk=self.pk)

    def get_color(self) -> str:
        """Sets a default color value. This method should be overridden by subclasses.

        Returns:
            str: black as hex string
        """

        return "#000000"

    def get_icon(self) -> str:
        """Sets a default icon value. This method should be overridden by subclasses

        Returns:
            str: event icon string based on the icon backend
        """

        return WBIcon.EVENT.icon

    @classmethod
    def get_item_types_choices(cls) -> tuple[str, str]:
        """
        Iterate over all implementing classes and extract its item type
        """
        choices = []
        for snd in get_inheriting_subclasses(CalendarItem):
            if (
                (_meta := getattr(snd, "_meta", None))
                and hasattr(snd, "get_item_type")
                and callable(snd.get_item_type)
            ):
                choices.append((snd.get_item_type(), _meta.verbose_name))
        return choices

    @classmethod
    def get_item_type(cls) -> str:
        # Problems with the app label can occur with nested apps. To prevent these cases,
        # we must ensure that only the last part of the app label is used.
        app_label: str = cls._meta.app_label.split(".")[-1]
        return f"{app_label}.{cls.__name__}"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.item_type:
            self.item_type = self.get_item_type()

        self.color = self.get_color()
        self.icon = self.get_icon()
        super().save(*args, **kwargs)

    @property
    def endpoint_basename(self) -> str | None:
        with suppress(ValueError, AttributeError, LookupError):
            return apps.get_model(self.item_type).get_endpoint_basename()

    def to_ics(self, start=None, end=None):
        """
        Convert calendar item model to ICS event

        Arguments:
            start {datetime.date} -- Start calendar item time if self.start is None
            end {datetime.date} -- End calendar item time if self.end is None
        Returns:
            Event -- The calendar item as ICS event
        """
        e = Event()
        if self.period:
            if not start:
                start = self.period.lower  # type: ignore
            if not end:
                end = self.period.upper  # type: ignore
        if (start and end) and (start < end):
            e.name = self.title
            e.begin = start
            e.end = end

            _id = f"workbench-{self.id}-{start}-{end}"
            e.uid = _id.replace(" ", "_")
            with suppress(ValueError, AttributeError, LookupError):
                casted_calendar_item = self.get_casted_calendar_item()
                if hasattr(casted_calendar_item, "get_extra_ics_kwargs") and callable(
                    casted_calendar_item.get_extra_ics_kwargs
                ):
                    for k, v in casted_calendar_item.get_extra_ics_kwargs():
                        setattr(e, k, v)

                return e
        else:
            return None

    def can_delete(self, user):
        try:
            return self.get_casted_calendar_item().is_deletable and (
                self.entities.filter(id=user.profile.id).exists()
                or self.has_user_administrate_permission(user, include_superusers=True)
            )
        except (ValueError, AttributeError, LookupError):
            return False

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:agenda:calendaritem"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:agenda:calendaritemrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    @classmethod
    def has_user_administrate_permission(cls, user, include_superusers: bool = False) -> bool:
        return user in ModelBackend().with_perm(
            "agenda.administrate_confidential_items", include_superusers=include_superusers
        )

    @property
    def duration(self):
        if self.period.lower and self.period.upper:
            return self.period.upper - self.period.lower

    class Meta:
        verbose_name = _("Calendar Item")
        verbose_name_plural = _("Calendar Items")
        permissions = [
            ("administrate_confidential_items", "Can administrate calendar items"),
        ]
        indexes = [models.Index(fields=["period"])]


@receiver(models.signals.m2m_changed, sender=CalendarItem.entities.through)
def m2m_entities_changed(sender, instance, action, pk_set, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        transaction.on_commit(set_entity_list.s(instance.id).delay)


@shared_task(queue=Queue.HIGH_PRIORITY.value)
def set_entity_list(calendar_item_id: int):
    frontend_list = []
    with suppress(
        CalendarItem.DoesNotExist
    ):  # for sanitization reason, we catch this error in case of db slowness. It doesn't really matter as this is computed frequently.
        instance = CalendarItem.objects.get(id=calendar_item_id)
        for entity in instance.entities.exclude(entry_type="Company"):
            person = entity.get_casted_entry()
            frontend_list.append(
                {
                    "id": person.id,
                    "label": person.initials,
                    "tooltip": person.computed_str,
                }
            )
        instance.entity_list = frontend_list
        instance.save()


@receiver(pre_merge, sender="directory.Entry")
def pre_merge_entry_calendaritem(sender: models.Model, merged_object, main_object, **kwargs):
    for item in CalendarItem.objects.filter(entities=merged_object):
        item.entities.remove(merged_object)
        if main_object not in item.entities.all():
            item.entities.add(main_object)
