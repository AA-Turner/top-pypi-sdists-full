from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition
from slugify import slugify

from wbcore.contrib.icons import WBIcon
from wbcore.contrib.notifications.dispatch import send_notification
from wbcore.contrib.notifications.utils import create_notification_type
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton, ButtonDefaultColor
from wbcore.models import WBModel
from wbcore.utils.models import ComplexToStringMixin, PrimaryMixin


class RelationshipType(WBModel):
    title = models.CharField(
        max_length=256,
        verbose_name=_("Relationship Type"),
        unique=True,
        blank=False,
        null=False,
    )

    counter_relationship = models.OneToOneField(
        to="self",
        blank=True,
        null=True,
        related_name="reverse_counter_relationship",
        on_delete=models.CASCADE,
        verbose_name=_("Counter Relationship"),
    )

    slugify_title = models.CharField(
        max_length=256,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Slugified Title",
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        if not self.id:
            # self will have no id, when it is getting creating. In this case post_save will update
            # the counter relationship if one is given.
            super().save(*args, **kwargs)
        else:
            if self.counter_relationship:
                RelationshipType.objects.filter(
                    Q(reverse_counter_relationship=self) & ~Q(id=self.counter_relationship.id)
                ).update(counter_relationship=None)

                RelationshipType.objects.filter(id=self.counter_relationship.id).update(counter_relationship=self)
            else:
                RelationshipType.objects.filter(reverse_counter_relationship=self).update(counter_relationship=None)

            super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Relationship Type")
        verbose_name_plural = _("Relationship Types")

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:relationship-type"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:relationshiptyperepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"


class Relationship(ComplexToStringMixin, WBModel):
    relationship_type = models.ForeignKey(
        on_delete=models.PROTECT,
        to="directory.RelationshipType",
        verbose_name=_("Type"),
    )
    from_entry = models.ForeignKey(
        on_delete=models.CASCADE,
        null=True,
        related_name="from_entry",
        to="directory.Entry",
        verbose_name=_("Relationship From"),
    )
    to_entry = models.ForeignKey(
        on_delete=models.CASCADE,
        null=True,
        related_name="to_entry",
        to="directory.Entry",
        verbose_name=_("Relationship To"),
    )

    def compute_str(self) -> str:
        return f"{self.from_entry} is {self.relationship_type} of {self.to_entry}"

    def delete(self, *args, **kwargs):
        Relationship.objects.filter(
            Q(to_entry=self.from_entry)
            & Q(from_entry=self.to_entry)
            & (
                Q(relationship_type=self.relationship_type)
                | Q(relationship_type=self.relationship_type.counter_relationship)
            )
        ).delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Relationship")
        verbose_name_plural = _("Relationships")

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:relationship"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:relationshiprepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{relationship_type}}: {{from_entry}} {{to_entry}}"


class ClientManagerRelationship(ComplexToStringMixin, PrimaryMixin, WBModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PENDINGADD = "PENDINGADD", _("Pending Add")
        PENDINGREMOVE = "PENDINGREMOVE", _("Pending Remove")
        APPROVED = "APPROVED", _("Approved")
        REMOVED = "REMOVED", _("Removed")

    @property
    def can_update_primary_field(self):
        return super().can_update_primary_field and self.status in [
            ClientManagerRelationship.Status.APPROVED,
            ClientManagerRelationship.Status.PENDINGREMOVE,
        ]

    def get_related_queryset(self):
        return ClientManagerRelationship.objects.filter(
            client=self.client,
            status__in=[
                ClientManagerRelationship.Status.APPROVED,
                ClientManagerRelationship.Status.PENDINGREMOVE,
            ],
        )

    PRIMARY_ATTR_FIELDS = ["client"]

    relationship_manager = models.ForeignKey(
        on_delete=models.CASCADE,
        to="directory.Person",
        verbose_name=_("Relationship Manager"),
        related_name="manager_of",
    )
    client = models.ForeignKey(
        on_delete=models.CASCADE,
        to="directory.Entry",
        verbose_name=_("Client"),
        related_name="client_of",
    )
    status = FSMField(default=Status.DRAFT, choices=Status.choices, verbose_name=_("Status"))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))

    @transition(
        field=status,
        source=[Status.DRAFT],
        target=Status.PENDINGADD,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                color=ButtonDefaultColor.PRIMARY,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.SEND.icon,
                key="submit",
                label=_("Submit"),
                action_label=_("Submitting"),
                description_fields=_("Are you sure you want to submit your draft for review?"),
            )
        },
    )
    def submit(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.DRAFT],
        target=Status.APPROVED,
        permission=lambda instance, user: user.has_perm("directory.administrate_clientmanagerrelationship"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                color=ButtonDefaultColor.SUCCESS,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.CONFIRM.icon,
                key="mngapprove",
                label=_("Approve"),
                action_label=_("Approve"),
                description_fields=_("Are you sure you want to approve this relationship?"),
            )
        },
    )
    def mngapprove(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.PENDINGADD],
        target=Status.DRAFT,
        permission=lambda instance, user: user.has_perm("directory.administrate_clientmanagerrelationship"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                color=ButtonDefaultColor.ERROR,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.REJECT.icon,
                key="deny",
                label=_("Deny"),
                action_label=_("Denial"),
                description_fields=_("Are you sure you want to deny this relationship?"),
            )
        },
    )
    def deny(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.PENDINGADD],
        target=Status.APPROVED,
        permission=lambda instance, user: user.has_perm("directory.administrate_clientmanagerrelationship"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.CONFIRM.icon,
                color=ButtonDefaultColor.SUCCESS,
                key="approve",
                label=_("Approve"),
                action_label=_("Approval"),
                description_fields=_("Are you sure you want to approve this relationship?"),
            )
        },
    )
    def approve(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.PENDINGREMOVE],
        target=Status.APPROVED,
        permission=lambda instance, user: user.has_perm("directory.administrate_clientmanagerrelationship"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.REJECT.icon,
                color=ButtonDefaultColor.ERROR,
                key="denyremoval",
                label=_("Deny"),
                action_label=_("Denial"),
                description_fields=_("Are you sure you want to deny removal of this relationship?"),
            )
        },
    )
    def denyremoval(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.PENDINGREMOVE],
        target=Status.REMOVED,
        permission=lambda instance, user: user.has_perm("directory.administrate_clientmanagerrelationship"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.DELETE.icon,
                color=ButtonDefaultColor.SUCCESS,
                key="approveremoval",
                label=_("Approve"),
                action_label=_("Approval"),
                description_fields=_("Are you sure you want to remove this relationship?"),
            )
        },
    )
    def approveremoval(self, by=None, description=None, **kwargs):
        pass

    def is_not_primary(instance):
        return not instance.primary

    @transition(
        field=status,
        source=[Status.APPROVED],
        target=Status.PENDINGADD,
        conditions=[is_not_primary],
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.FAVORITE.icon,
                color=ButtonDefaultColor.PRIMARY,
                key="makeprimary",
                label=_("Make Primary"),
                action_label=_("Make Primary"),
                description_fields=_("Are you sure you want to request making this relationship manager primary?"),
            )
        },
    )
    def makeprimary(self, by=None, description=None, **kwargs):
        self.primary = True

    def last_primary(instance):
        return not instance.primary and (
            ClientManagerRelationship.objects.exclude(id=instance.id)
            .filter(status=ClientManagerRelationship.Status.APPROVED, client=instance.client, primary=True)
            .exists()
        )

    @transition(
        field=status,
        source=[Status.APPROVED],
        target=Status.PENDINGREMOVE,
        conditions=[last_primary],
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.DELETE.icon,
                color=ButtonDefaultColor.ERROR,
                key="remove",
                label=_("Remove"),
                action_label=_("Removal"),
                description_fields=_("Are you sure you want to request removal of this relationship?"),
            )
        },
    )
    def remove(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=[Status.REMOVED],
        target=Status.PENDINGADD,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:clientmanagerrelationship",),
                icon=WBIcon.UNDO.icon,
                color=ButtonDefaultColor.SUCCESS,
                key="reinstate",
                label=_("Reinstate"),
                action_label=_("Reinstate"),
                description_fields=_("Are you sure you want to request reinstating this relationship?"),
            )
        },
    )
    def reinstate(self, by=None, description=None, **kwargs):
        pass

    def compute_str(self) -> str:
        return _("{client} is client of {manager}").format(client=self.client, manager=self.relationship_manager)

    def delete(self, **kwargs):
        super().delete(no_deletion=False)  # For this model we actually want to delete the object

    class Meta:
        verbose_name = _("Client Manager Relationship")
        verbose_name_plural = _("Client Manager Relationships")

        notification_types = [
            create_notification_type(
                code="directory.clientmanagerrelationship.approval",
                title="Relationship Manager Approval",
                help_text="Sends you a notification when there is a Relationship manager change to approve.",
            )
        ]
        permissions = (("administrate_clientmanagerrelationship", "Can administrate Client Manager Relationship"),)

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:clientmanagerrelationshiprepresentation-list"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:clientmanagerrelationship"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{relationship_manager}} {{client}} {{primary}}"


@receiver(post_save, sender=ClientManagerRelationship)
def post_save_client_manager_relationship(sender, instance, created, **kwargs):
    """
    Post save signal receiver sending notifications to all managers when a new client manager relationship is requested
    """
    if instance.status in [
        ClientManagerRelationship.Status.PENDINGADD.name,
        ClientManagerRelationship.Status.PENDINGREMOVE.name,
    ]:
        user_qs = (
            get_user_model()
            .objects.filter(
                models.Q(groups__permissions__codename="can_administer_entry_in_charge_request")
                | models.Q(user_permissions__codename="can_administer_entry_in_charge_request")
            )
            .distinct()
        )
        if instance.status == ClientManagerRelationship.Status.PENDINGADD.name:
            for user in user_qs.all():
                send_notification(
                    code="directory.clientmanagerrelationship.approval",
                    title=_("New Client Manager Relationship for {client}").format(
                        client=instance.client.computed_str
                    ),
                    body=_("User requested that {manager} is the relationship manager of {client}.").format(
                        manager=str(instance.relationship_manager), client=instance.client.computed_str
                    ),
                    user=user,
                    reverse_name="directory:clientmanagerrelationship-detail",
                    reverse_args=[instance.id],
                )
        if instance.status == ClientManagerRelationship.Status.PENDINGREMOVE.name:
            for user in user_qs.all():
                send_notification(
                    code="directory.clientmanagerrelationship.approval",
                    title=_("Removal of Client Manager Relationship for {client}").format(
                        client=instance.client.computed_str
                    ),
                    body=_("User requested that relationship manager {manager} of {client} should be removed.").format(
                        manager=str(instance.relationship_manager), client=instance.client.computed_str
                    ),
                    user=user,
                    reverse_name="directory:clientmanagerrelationship-detail",
                    reverse_args=[instance.id],
                )


class Position(WBModel):
    title = models.CharField(max_length=128, verbose_name=_("Title"), unique=True, blank=False, null=False)

    slugify_title = models.CharField(
        max_length=128, unique=True, verbose_name="Slugified Title", blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.title}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:position"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:positionrepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        super().save(*args, **kwargs)


class EmployerEmployeeRelationship(PrimaryMixin):
    PRIMARY_ATTR_FIELDS = ["employee"]

    employee = models.ForeignKey(
        on_delete=models.CASCADE,
        to="directory.Person",
        verbose_name=_("Employee"),
        related_name="employer",
    )
    primary = models.BooleanField(
        verbose_name=_("Primary"),
        default=False,
    )
    position = models.ForeignKey(
        null=True,
        on_delete=models.SET_NULL,
        to="directory.Position",
        verbose_name=_("Position"),
        related_name="position_of_employee",
    )
    position_name = models.CharField(
        verbose_name=_("Alternative Position Name"),
        help_text=_(
            "If the selected position isn't an exact match, feel free to use this field to provide more details about the position. You can edit this field once the position is confirmed."
        ),
        max_length=128,
        null=True,
        blank=True,
    )
    employer = models.ForeignKey(
        on_delete=models.CASCADE,
        to="directory.Company",
        verbose_name=_("Employer"),
        related_name="employee",
    )

    def save(self, *args, **kwargs):
        if self.position and not self.position_name:
            self.position_name = str(self.position)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_employeremployee",
                fields=["employee", "employer"],
            )
        ]
        verbose_name = _("Employer Employee Relationship")

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:employeremployeerelationship"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    def representation_label_key(cls):
        return "{{position_name}}"

    def delete(self, **kwargs):
        super().delete(no_deletion=False)  # For this model we actually want to delete the object


@receiver(post_save, sender=EmployerEmployeeRelationship)
def post_save_eer(sender, instance, created, raw, **kwargs):
    """
    Post save EER signal: Triggers the post_save signals of the employee which updates his computed_str and adds the
    employer to future planned activities if it became the only employer
    """

    if not raw:
        instance.employee.save()


@receiver(post_delete, sender=EmployerEmployeeRelationship)
def post_delete_eer(sender, instance, **kwargs):
    """
    Post delete EER signal: Triggers the post_delete signals of the employee which updates his computed_str and adds the
    employer to future planned activities if it became the only employer
    """
    new_computed_str = instance.employee.compute_str()
    instance.employee._meta.model.objects.filter(id=instance.employee.id).update(
        computed_str=new_computed_str, slugify_computed_str=slugify(new_computed_str, separator=" ")
    )


@receiver(post_save, sender=RelationshipType)
def post_save_relationship_type(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.counter_relationship:
            sender.objects.filter(id=instance.counter_relationship.id).update(counter_relationship=instance)


@receiver(post_save, sender=Relationship)
def post_save_relationship(sender, instance, created, raw, **kwargs):
    if raw:
        return
    rel_ship_type = (
        instance.relationship_type.counter_relationship
        if instance.relationship_type.counter_relationship
        else instance.relationship_type
    )
    # The type of relationship the to_entry should have.
    qs = sender.objects.filter(
        from_entry=instance.to_entry, to_entry=instance.from_entry, relationship_type=rel_ship_type
    )

    if not created:
        # An existing instance was changed
        if not qs.exists():
            sender.objects.filter(
                from_entry=instance.to_entry,
                to_entry=instance.from_entry,
            ).update(relationship_type=rel_ship_type)
    else:
        # A new instance was created
        if not qs.exists():
            sender.objects.create(
                from_entry=instance.to_entry,
                to_entry=instance.from_entry,
                relationship_type=rel_ship_type,
            )
