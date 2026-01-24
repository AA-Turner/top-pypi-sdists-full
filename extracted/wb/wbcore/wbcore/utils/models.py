from contextlib import suppress
from typing import Self

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import models, transaction
from django.db.models.signals import post_delete, pre_delete
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModelManager
from rest_framework.fields import get_attribute

from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.color.fields import ColorField
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.icons.models import IconField
from wbcore.signals import post_clone, pre_merge
from wbcore.signals.merge import post_merge
from wbcore.utils.enum import ChoiceEnum
from wbcore.workers import Queue


def get_and_update_or_create(model, filter_params, defaults):
    """get or create with default values applied to existing instances

    {model}.objects.get_or_create(*{filter_params}, defaults={defaults})

    Arguments:
        model {django.db.models.Model} -- The model the queryset gets applied to
        filter_params {dict} -- The parameters that the queryset gets filter against
        defaults {dict} -- The default values that will be applied to the instance (create, update)

    Returns:
        django.db.models.Model -- The created/updated instance of the model
    """

    instance, created = model.objects.get_or_create(**filter_params, defaults=defaults)
    if not created:
        model.objects.filter(id=instance.id).update(**defaults)
        instance = model.objects.get(id=instance.id)
        instance.save()
    return instance


class NoGroupBySubquery(models.Subquery):
    """Same as the default django subquery, however does not perform a group by"""

    def get_group_by_cols(self):
        return []


class NoGroupByExpressionWrapper(models.ExpressionWrapper):
    def get_group_by_cols(self):
        return []


class ComplexToStringMixin(models.Model):
    """Mixin that allows to store a complex to string method in the database"""

    COMPUTED_STR_RECOMPUTE_PERIODICALLY: bool = True
    COMPUTED_STR_RECOMPUTE_ON_SAVE: bool = True
    COMPUTED_STR_MAX_LENGTH: int = 512

    class Meta:
        abstract = True

    computed_str = models.CharField(max_length=COMPUTED_STR_MAX_LENGTH, null=True, blank=True, verbose_name=_("Name"))

    def compute_str(self):
        raise NotImplementedError

    def __str__(self):
        if self.computed_str:
            return self.computed_str
        return ""

    def save(self, *args, **kwargs):
        if self.COMPUTED_STR_RECOMPUTE_ON_SAVE or not self.id:
            self.computed_str = self.compute_str()

        if (
            self.computed_str and len(self.computed_str) > self.COMPUTED_STR_MAX_LENGTH
        ):  # ensure computed str does not exceed the provided max length
            self.computed_str = (
                self.computed_str[: self.COMPUTED_STR_MAX_LENGTH - 3] + "..."
            )  # we materialize the fact that we pruned the computed str with ...

        super().save(*args, **kwargs)

    @classmethod
    def get_representation_label_key(cls):
        return "{{computed_str}}"


class LabelKeyMixin:
    @classmethod
    def get_label_key(cls):
        if hasattr(cls, "LABEL_KEY"):
            return cls.LABEL_KEY
        raise AssertionError(
            f"You need to implement the get_label_key method in the class {cls} or remove the LabelKeyMixin from {cls}."
        )


class Status(ChoiceEnum):
    PENDING = _("Pending")
    DENIED = _("Denied")
    APPROVED = _("Approved")

    @classmethod
    def get_color_map(cls):
        colors = [WBColor.YELLOW_LIGHT.value, WBColor.RED_LIGHT.value, WBColor.GREEN_LIGHT.value]
        return [choice for choice in zip(cls, colors, strict=False)]


class PrimaryMixin(models.Model):
    """
    Ensures that there is only one entry with primary=True
    for models with a foreign key field to a different model and a primary field.
    """

    PRIMARY_ATTR_FIELDS: list = []  # define the list of fields that needs to introduce uniqueness
    primary = models.BooleanField(default=False, verbose_name="Primary")

    @property
    def can_update_primary_field(self) -> bool:
        """
        Check if any of the primary fields have non-None values for updating.

        This property evaluates whether any of the primary fields defined in
        `PRIMARY_ATTR_FIELDS` have non-None values in the current instance.
        It is useful to determine if the primary fields can be updated.

        Returns:
            bool: True if any primary field has a non-None value, False otherwise.
        """
        return any([get_attribute(self, field.split(".")) is not None for field in self.PRIMARY_ATTR_FIELDS])

    def get_related_queryset(self):
        """
        Retrieve a queryset of related objects based on primary attributes.

        This method generates a queryset for related objects of the same model
        by filtering on primary attributes. Primary attributes are defined in
        the class attribute `PRIMARY_ATTR_FIELDS`.

        Returns:
            QuerySet: A Django QuerySet containing related objects.

        """
        return self._meta.model.objects.filter(
            **{field.replace(".", "__"): get_attribute(self, field.split(".")) for field in self.PRIMARY_ATTR_FIELDS}
        )

    def save(self, *args, **kwargs):
        if self.can_update_primary_field:
            related_qs = self.get_related_queryset()
            if self.primary:
                related_qs = related_qs.exclude(id=self.id).filter(
                    primary=True
                )  # if self id is None, it will not exclude anything
                if related_qs.exists():
                    self.previous_primary_entity = related_qs.first()
                    related_qs.update(primary=False)
            elif not related_qs.filter(primary=True).exists():
                self.primary = True
        super().save(*args, **kwargs)

    def delete(self, no_deletion=True, **kwargs):
        if self.primary and (qs := self.get_related_queryset().exclude(id=self.id)).exists():
            next_primary = qs.first()
            next_primary.primary = True
            next_primary.save()
        if no_deletion:
            self.primary = False
            for field_name in self.PRIMARY_ATTR_FIELDS:
                with suppress(FieldError, FieldDoesNotExist):
                    if self._meta.get_field(field_name).null:  # ensure the field is nullable
                        setattr(
                            self, field_name, None
                        )  # We don't delete the object, we just un-assign the entry to "hide" it
            self.save()
        else:
            super().delete(**kwargs)

    class Meta:
        abstract = True


class DefaultMixin(models.Model):
    """
    Ensures that there is only one instance with default=True.
    """

    default = models.BooleanField(
        verbose_name=_("Default"),
        default=False,
    )

    def save(self, *args, **kwargs):
        if hasattr(self, "default"):
            if self.default:
                self._meta.model.objects.all().update(default=False)
            elif self._meta.model.objects.all().count() == 0:
                self.default = True
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ActiveObjectManager(OrderedModelManager):
    def get_queryset(self):
        try:
            return super().get_queryset().filter(is_active=True)
        except FieldError:
            return super().get_queryset()


class DeleteToDisableMixin(models.Model):
    AUTOMATICALLY_CLEAN_SOFT_DELETED_OBJECTS = False

    is_active = models.BooleanField(default=True)
    deletion_datetime = models.DateTimeField(blank=True, null=True)

    objects = ActiveObjectManager()
    all_objects = models.Manager()

    def delete(self, using=None, no_deletion=True, **kwargs):
        if no_deletion:
            pre_delete.send(
                sender=self.__class__,
                instance=self,
            )
            self.is_active = False
            self.deletion_datetime = timezone.now()
            self.save()
            post_delete.send(sender=self.__class__, instance=self, using=using)
        else:
            super().delete(using=using, **kwargs)

    class Meta:
        abstract = True


def get_object(model_class: models.Model, object_id: int):
    if issubclass(model_class, DeleteToDisableMixin):
        objects = model_class.all_objects
    else:
        objects = model_class.objects
    return objects.get(id=object_id)


class CalendarItemTypeMixin(models.Model):
    color = ColorField(
        verbose_name=_("Color"),
        default="#000000",
        unique=False,
        blank=False,
        null=False,
    )

    icon = IconField(
        max_length=128,
        unique=False,
        verbose_name=_("Icon"),
        blank=False,
        null=False,
        default=WBIcon.EVENT.value,
    )

    class Meta:
        abstract = True


class ResolvableModelMixin(models.Model):
    class Meta:
        abstract = True

    resolved = models.BooleanField(default=False, verbose_name="Resolved")

    def delete(self, *args, **kwargs):
        if self.resolved:
            raise ValueError("Resolved Entities cannot be deleted.")
        super().delete(*args, **kwargs)


class CloneMixin(models.Model):
    # Clone mixin

    def _clone(self, **kwargs) -> Self:
        raise NotImplementedError()

    def clone(self, **kwargs) -> Self:
        clone = self._clone(**kwargs)
        post_clone.send(sender=self.__class__, instance=self, clone=clone, **kwargs)
        return clone

    class Meta:
        abstract = True


class MergeError(ValueError):
    pass


class MergeMixin(models.Model):
    """
    Abstract Django model mixin that provides a standardized interface for merging
    two model instances of the same type, typically used to consolidate duplicate
    records (e.g., merging two Instruments, Clients, or Accounts).
    """

    @property
    def is_mergeable(self) -> bool:
        return True

    def get_merge_senders_kwargs(self, merged_object):
        # Default implementation: return tuple of (sender, main, merged) for signal dispatch.
        # Subclasses can override to yield multiple entries if related models require updates.
        # ideal for multi-inheritance
        yield (self.__class__, merged_object, self)

    def _merge(self, merged_object, **kwargs):
        # Must be implemented by subclasses. It should define the data
        # or relationship consolidation logic between self and merged_object.
        # Example: transfer related foreign key references, update counters, etc.
        raise NotImplementedError()

    def merge(self, merged_object, dispatch: bool = True, **kwargs):
        with transaction.atomic():  # We want this to either succeed fully or fail
            if dispatch:
                for sender, casted_merged_object, casted_main_object in self.get_merge_senders_kwargs(merged_object):
                    pre_merge.send(
                        sender=sender, merged_object=casted_merged_object, main_object=casted_main_object
                    )  # default signal dispatch for the Instrument class
                # We refresh the reference in case the underlying signal receivers modify these objects
                self.refresh_from_db()
                merged_object.refresh_from_db()
            self._merge(merged_object, **kwargs)
            # We delete finally the merged object. All unlikage should have been done in the signal receivers function
            if isinstance(merged_object, DeleteToDisableMixin):
                merged_object.delete(no_deletion=False)
            else:
                merged_object.delete()

            self.save()
            post_merge.send(sender=self.__class__, merged_object=merged_object, main_object=self)

    class Meta:
        abstract = True


@shared_task(queue=Queue.DEFAULT.value)
def merge_as_task(content_type_id: int, main_object_id: int, merged_object_id: int):
    content_type = ContentType.objects.get(id=content_type_id)
    with suppress(content_type.model_class().DoesNotExist):
        main_object = content_type.get_object_for_this_type(id=main_object_id)
        merged_object = content_type.get_object_for_this_type(id=merged_object_id)
        if hasattr(main_object, "merge") and callable(main_object.merge):
            main_object.merge(merged_object)
