import sys
import uuid
from contextlib import suppress
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.exceptions import AppRegistryNotReady
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CharField, Exists, F, OuterRef, Q, Subquery, Value
from django.db.models.functions import Concat
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.registries import global_preferences_registry
from modeltrans.fields import TranslationField
from slugify import slugify

from wbcore.contrib.agenda.models import CalendarItem
from wbcore.contrib.authentication.models import User
from wbcore.contrib.currency.models import Currency
from wbcore.contrib.directory.models.contacts import (
    AddressContact,
    BankingContact,
    ContactLocationChoices,
    EmailContact,
    SocialMediaContact,
    TelephoneContact,
    WebsiteContact,
)
from wbcore.contrib.directory.models.relationships import (
    ClientManagerRelationship,
    EmployerEmployeeRelationship,
    Relationship,
)
from wbcore.contrib.directory.signals import deactivate_profile
from wbcore.contrib.directory.typings import Person as PersonDTO
from wbcore.models import WBModel
from wbcore.utils.models import (
    ActiveObjectManager,
    ComplexToStringMixin,
    DeleteToDisableMixin,
    MergeError,
    MergeMixin,
)


class CustomerStatus(WBModel):
    title = models.CharField(
        max_length=32,
        verbose_name=_("Title"),
        unique=True,
        blank=False,
        null=False,
    )

    slugify_title = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="Slugified Title",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.title}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:customerstatus"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:customerstatusrepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    class Meta:
        verbose_name = _("Customer Status")
        verbose_name_plural = _("Customer Statuses")

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        super().save(*args, **kwargs)


class CompanyType(WBModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title"),
        unique=True,
        blank=False,
        null=False,
    )

    slugify_title = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Slugified Title",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.title}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:companytype"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:companytyperepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    class Meta:
        verbose_name = _("Company Type")
        verbose_name_plural = _("Company Types")

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        super().save(*args, **kwargs)


class Specialization(WBModel):
    title = models.CharField(
        max_length=128,
        verbose_name=_("Title"),
        unique=True,
        blank=False,
        null=False,
    )

    slugify_title = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Slugified Title",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.title}"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:specialization"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:specializationrepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    class Meta:
        verbose_name = _("Specialization")
        verbose_name_plural = _("Specializations")

    def save(self, *args, **kwargs):
        self.slugify_title = slugify(self.title, separator=" ")
        super().save(*args, **kwargs)


def upload_to_profile_images(instance, filename):
    file_extension = "".join(Path(filename).suffixes)
    return f"crm/entry/profile_images/{instance.uuid}{file_extension}"


def upload_to_signatures(instance, filename):
    file_extension = "".join(Path(filename).suffixes)
    return f"crm/entry/signatures/{instance.uuid}{file_extension}"


class EntryDefaultQueryset(models.QuerySet):
    def filter_for_user(self, user: User) -> models.QuerySet:
        """
        Protect the chained queryset and filter the entries that this user cannot see based on the following rules:

        * internal user or supersuer: All
        * external user: only itself, its colleagues and all its clients
        * else: None
        """
        profile = user.profile
        if user.is_superuser or profile.is_internal:
            return self
        else:
            return (
                self.annotate(
                    has_valid_relationship_manager_role=Exists(
                        ClientManagerRelationship.objects.filter(
                            client__id=OuterRef("pk"), relationship_manager=profile
                        ).exclude(status=ClientManagerRelationship.Status.REMOVED)
                    ),
                    is_colleague=Exists(
                        EmployerEmployeeRelationship.objects.filter(
                            employee_id=OuterRef("pk"), employer__in=profile.employers.all()
                        )
                    ),
                )
                .filter(
                    Q(is_colleague=True)  # can see its colleagues
                    | Q(id__in=profile.employers.values("id"))  # can see its colleagues
                    | Q(id=profile.id)  # can see itself
                    | Q(
                        has_valid_relationship_manager_role=True
                    )  # can see all entry where they have a valid relationship manager role
                )
                .distinct()
            )

    def filter_only_internal(self) -> models.QuerySet:
        return self.filter(id__in=User.objects.filter_internal().values("profile"))

    def annotate_all(self) -> models.QuerySet:
        qs = self
        with suppress(AppRegistryNotReady):
            qs = qs.annotate(
                primary_manager_repr=Subquery(
                    ClientManagerRelationship.objects.filter(
                        client__id=OuterRef("id"),
                        primary=True,
                        status__in=[
                            ClientManagerRelationship.Status.APPROVED,
                            ClientManagerRelationship.Status.PENDINGREMOVE,
                        ],
                    ).values("relationship_manager__computed_str")[:1]
                ),
                primary_email=Subquery(
                    EmailContact.objects.filter(primary=True, entry__id=OuterRef("pk")).values("address")[:1],
                    output_field=CharField(),
                ),
                primary_telephone=Subquery(
                    TelephoneContact.objects.filter(primary=True, entry__id=OuterRef("pk")).values("number")[:1],
                    output_field=CharField(),
                ),
                primary_address=Subquery(
                    AddressContact.objects.filter(primary=True, entry__id=OuterRef("pk"))
                    .annotate(
                        primary_address=Concat(
                            F("street"), Value(" "), F("zip"), Value(" "), F("geography_city__name")
                        )
                    )
                    .values("primary_address")[:1],
                    output_field=CharField(),
                ),
                primary_website=Subquery(
                    WebsiteContact.objects.filter(primary=True, entry__id=OuterRef("pk")).values("url")[:1],
                    output_field=CharField(),
                ),
                primary_social=Subquery(
                    SocialMediaContact.objects.filter(primary=True, entry__id=OuterRef("pk")).values("url")[:1],
                    output_field=CharField(),
                ),
                last_event=Subquery(
                    CalendarItem.objects.filter(
                        period__endswith__lte=timezone.now(),
                        visibility=CalendarItem.Visibility.PUBLIC,
                        entities=OuterRef("pk"),
                    )
                    .order_by("-period__startswith")
                    .values("title")[:1]
                ),
                last_event_period_endswith=Subquery(
                    CalendarItem.objects.filter(
                        period__endswith__lte=timezone.now(),
                        visibility=CalendarItem.Visibility.PUBLIC,
                        entities=OuterRef("pk"),
                    )
                    .order_by("-period__startswith")
                    .values("period__endswith")[:1]
                ),
                cities=ArrayAgg("addresses__geography_city", filter=Q(addresses__geography_city__isnull=False)),
            )
        return qs


class EntryManager(ActiveObjectManager):
    def get_queryset(self) -> EntryDefaultQueryset:
        return EntryDefaultQueryset(self.model).filter(is_active=True)

    def filter_for_user(self, user: User) -> models.QuerySet:
        return self.get_queryset().filter_for_user(user)

    def filter_only_internal(self) -> models.QuerySet:
        return self.get_queryset().filter_only_internal()

    def annotate_all(self):
        return self.get_queryset().annotate_all()


class Entry(MergeMixin, ComplexToStringMixin, DeleteToDisableMixin, WBModel):
    AUTOMATICALLY_CLEAN_SOFT_DELETED_OBJECTS = True

    class EntryType(models.TextChoices):
        PERSON = "PERSON", _("Person")
        COMPANY = "COMPANY", _("Company")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    entry_type = models.CharField(max_length=255, default="", choices=EntryType.choices, verbose_name=_("Type"))
    additional_fields = models.JSONField(default=dict, blank=True, null=True, verbose_name=_("Additional Fields"))
    is_draft_entry = models.BooleanField(
        default=False,
        verbose_name=_("Draft Entry"),
        help_text=_(
            "Draft entries are entries that have been created automatically and still need verification by a human user."
        ),
    )
    relationship_managers = models.ManyToManyField(
        "Person",
        related_name="clients",
        blank=True,
        through="directory.ClientManagerRelationship",
        through_fields=("client", "relationship_manager"),
        verbose_name=_("Relationship Managers"),
        help_text=_("People in charge of this entry"),
    )
    relationships = models.ManyToManyField(
        blank=True,
        symmetrical=False,
        to="self",
        through="directory.Relationship",
        through_fields=("from_entry", "to_entry"),
        verbose_name=_("The Entry's Relationships"),
    )
    # Activity heat describes how active a customer is. The more active a customer, the higher their activity heat.
    activity_heat = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0,
        verbose_name=_("Activity Heat"),
    )
    slugify_computed_str = models.CharField(
        max_length=512, blank=True, null=True, verbose_name="Slugified Search Name"
    )
    profile_image = models.ImageField(blank=True, null=True, upload_to=upload_to_profile_images, max_length=256)
    # TODO: Move to Person Model?
    signature = models.ImageField(blank=True, null=True, upload_to=upload_to_signatures, max_length=256)
    external_identifier = models.CharField(null=True, blank=True, max_length=128, unique=True)
    salutation = models.CharField(max_length=255, verbose_name=_("Salutation"), null=True, blank=True)

    telephones: models.QuerySet[TelephoneContact]
    emails: models.QuerySet[EmailContact]
    addresses: models.QuerySet[AddressContact]
    websites: models.QuerySet[WebsiteContact]
    banking: models.QuerySet[BankingContact]

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

        ordering = ("entry_type",)

    objects = EntryManager()

    def __str__(self):
        return self.computed_str

    @property
    def is_company(self) -> bool:
        return self.entry_type == Company.__name__

    @staticmethod
    def _primary_contact(ref: models.QuerySet) -> models.Model | None:
        with suppress(ref.model.DoesNotExist):
            return ref.get(primary=True)

    def primary_email_contact(self):
        return self._primary_contact(self.emails)

    def primary_telephone_contact(self):
        return self._primary_contact(self.telephones)

    def primary_address_contact(self):
        return self._primary_contact(self.addresses)

    def primary_website_contact(self):
        return self._primary_contact(self.websites)

    def primary_banking_contact(self):
        return self._primary_contact(self.banking)

    def get_casted_entry(self):
        """
        Cast the entry into its child representative. We use the all manager to be sure to get the casted object even after its "deletion"
        """
        try:
            model_class = getattr(sys.modules[__name__], self.entry_type)
        except AttributeError:
            model_class = self.__class__
        return model_class.all_objects.get(pk=self.pk)

    def compute_str(self):
        self.slugify_computed_str = slugify(_("Entry {id}").format(id=self.id), separator=" ")
        return _("Entry {id}").format(id=self.id)

    def delete_additional_fields(self, additional_field_key=None):
        if additional_field_key in self.additional_fields:
            del self.additional_fields[additional_field_key]

    def get_banking_contact(self, currency: Currency) -> BankingContact | None:
        bank_accounts = self.banking.all()
        if bank_accounts.filter(currency=currency).exists():
            bank_accounts = bank_accounts.filter(currency=currency)
        if bank_accounts.filter(primary=True).exists():
            bank_accounts = bank_accounts.filter(primary=True)
        return bank_accounts.first()

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:entry"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:entryrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    def get_merge_senders_kwargs(self, merged_object):
        if type(self) is not type(merged_object):
            raise MergeError(
                f"Cannot merge {merged_object} (type {type(merged_object)}) into {self} (type {type(self)}): mismatch type"
            )
        if isinstance(self, Person):
            yield (Person, merged_object, self)
        elif isinstance(self, Company):
            yield (Company, merged_object, self)
        yield (Entry, getattr(merged_object, "entry_ptr", merged_object), getattr(self, "entry_ptr", self))

    def _merge(self, merged_entry, **kwargs):
        models = [
            (BankingContact, "iban"),
            (EmailContact, "address"),
            (SocialMediaContact, "url"),
            (TelephoneContact, "number"),
            (WebsiteContact, "url"),
        ]
        AddressContact.objects.filter(entry=merged_entry).update(entry=self)
        Relationship.objects.filter(to_entry=merged_entry).update(to_entry=self)
        Relationship.objects.filter(from_entry=merged_entry).update(from_entry=self)

        for model_class, field_name in models:
            for contact in model_class.objects.filter(entry=merged_entry):
                if model_class.objects.filter(**{field_name: getattr(contact, field_name), "entry": self}).exists():
                    contact.delete()
                else:
                    contact.entry = self
                    contact.primary = False
                    contact.save()
        for rel in ClientManagerRelationship.objects.filter(client=merged_entry):
            if ClientManagerRelationship.objects.filter(
                client=merged_entry, relationship_manager=rel.relationship_manager
            ).exists():
                rel.delete()
            else:
                rel.client = self
                rel.save()


class PersonDefaultQueryset(EntryDefaultQueryset):
    def annotate_all(self) -> models.QuerySet:
        qs = super().annotate_all()
        with suppress(AppRegistryNotReady):
            qs = qs.annotate(
                primary_employer=Subquery(
                    EmployerEmployeeRelationship.objects.filter(employee__id=OuterRef("pk"), primary=True).values(
                        "employer__id"
                    )[:1]
                ),
                primary_employer_repr=Subquery(
                    EmployerEmployeeRelationship.objects.filter(primary=True, employee=OuterRef("pk")).values(
                        "employer__computed_str"
                    )[:1]
                ),
                primary_employer_number=Subquery(
                    TelephoneContact.objects.filter(primary=True, entry__id=OuterRef("primary_employer")).values(
                        "number"
                    )[:1],
                    output_field=CharField(),
                ),
                name=Concat(F("first_name"), Value(" "), F("last_name")),
                customer_status=Subquery(
                    EmployerEmployeeRelationship.objects.filter(primary=True, employee=OuterRef("pk")).values(
                        "employer__customer_status__title"
                    )[:1]
                ),
                position_in_company=Subquery(
                    EmployerEmployeeRelationship.objects.filter(primary=True, employee=OuterRef("pk")).values(
                        "position__title"
                    )[:1]
                ),
                tier=Subquery(
                    EmployerEmployeeRelationship.objects.filter(
                        primary=True,
                        employee=OuterRef("pk"),
                    ).values("employer__tier")[:1]
                ),
            )
        return qs


class DefaultPersonManager(EntryManager):
    def get_queryset(self):
        qs = PersonDefaultQueryset(self.model).filter(is_active=True)
        with suppress(Exception):
            qs = qs.exclude(user_account__email=getattr(settings, "ANONYMOUS_USER_NAME", "AnonymousUser"))
        return qs


class RegisteredPersonManager(DefaultPersonManager):
    """Custom Manager for filtering directly for registered user or non user"""

    def get_queryset(self):
        qs = super().get_queryset()
        with suppress(Exception):
            qs = qs.exclude(Q(user_account__isnull=False) & Q(user_account__is_register=False))
        return qs


class PersonEmployeeManager(RegisteredPersonManager):
    """Custom Manager for filtering directly for Employees"""

    def get_queryset(self):
        if apps.is_installed("wbhuman_resources"):
            return (
                super()
                .get_queryset()
                .filter(
                    Q(human_resources__isnull=False)
                    & Q(human_resources__is_active=True)
                    & Q(user_account__isnull=False)
                )
            )
        else:
            try:
                main_company_id = global_preferences_registry.manager()["directory__main_company"]
                return super().get_queryset().filter(employers__id=main_company_id).distinct()
            except Exception:
                return super().get_queryset().none()


class Person(Entry):
    class Prefix(models.TextChoices):
        MR = "MR", _("Mr.")
        MRS = "MRS", _("Mrs.")
        PROF = "PROF", _("Prof.")
        DR = "DR", _("Dr.")
        MED = "MED", _("Med.")
        ME = "ME", _("Me.")

    """Person Model that represents a person in the CRM"""
    prefix = models.CharField(max_length=4, choices=Prefix.choices, verbose_name=_("Prefix"))

    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    initials = models.CharField(max_length=4, blank=True, null=True, verbose_name=_("Initials"))

    employers = models.ManyToManyField(
        "Company",
        related_name="employees",
        blank=True,
        through="directory.EmployerEmployeeRelationship",
        through_fields=("employee", "employer"),
        verbose_name=_("Employers"),
        help_text=_("The person's employers"),
    )

    active_employee = models.BooleanField(default=True, verbose_name=_("Available Employee"))
    birthday = models.DateField(null=True, blank=True, verbose_name=_("Birthday"))
    personality_profile_red = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0,
    )
    personality_profile_green = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0,
    )
    personality_profile_blue = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0,
    )

    formal = models.BooleanField(default=True, verbose_name=_("Formal"))
    specializations = models.ManyToManyField(
        to="Specialization",
        blank=True,
        verbose_name=_("Specializations"),
    )
    description = models.TextField(default="", blank=True)
    i18n = TranslationField(fields=["description"])

    objects = DefaultPersonManager()
    registered_users = RegisteredPersonManager()

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    @property
    def is_internal(self) -> bool:
        if user := getattr(self, "user_account", None):
            return user.is_internal
        return False

    @cached_property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def _build_dto(self):
        return PersonDTO(
            first_name=self.first_name,
            last_name=self.last_name,
            email=contact.address if (contact := self.primary_email_contact()) else None,
            id=self.id,
        )

    def _merge(self, merged_person, **kwargs):
        super()._merge(merged_person.entry_ptr, **kwargs)
        for contact in BankingContact.objects.filter(access=merged_person):
            contact.access.remove(merged_person)
            if self not in contact.access.all():
                contact.access.add(self)
        for rel in ClientManagerRelationship.objects.filter(relationship_manager=merged_person):
            if ClientManagerRelationship.objects.filter(relationship_manager=self, client=rel.client).exists():
                rel.delete()
            else:
                rel.relationship_manager = self
                rel.save()

        for rel in EmployerEmployeeRelationship.objects.filter(employee=merged_person):
            if EmployerEmployeeRelationship.objects.filter(employee=merged_person, employer=rel.employer).exists():
                rel.delete()
            else:
                rel.employer = self
                rel.save()

    def str_full(self):
        """
        Get the string representation including Employers seperated title
        """
        employers_repr = None
        eer_rel = EmployerEmployeeRelationship.objects.filter(employee=self.id, primary=True)
        try:
            if eer_rel.exists():
                employers_repr = Company.all_objects.get(id=eer_rel[0].employer.id).name
            else:
                employers_repr = (
                    "/".join(self.employers.all().values_list("name", flat=True)) if self.employers.exists() else ""
                )
            if employers_repr:
                return f"{self.first_name} {self.last_name}{(' (%s)' % employers_repr)}"
        except ValueError:
            pass
        return f"{self.first_name} {self.last_name}"

    def compute_str(self):
        self.slugify_computed_str = slugify(self.str_full(), separator=" ")
        return self.str_full()

    def get_initials(self):
        initials = []
        if self.first_name and len(self.first_name) > 1:
            n = 1 if self.last_name else 2
            initials.append(self.first_name.upper()[:n])

        if self.last_name and len(self.last_name) > 1:
            n = 1 if self.first_name else 2
            initials.append(self.last_name.upper()[:n])

        if len(initials) == 0:
            initials.append("n.a.")

        return "".join(initials)

    def save(self, *args, **kwargs):
        self.entry_type = "Person"
        self.initials = self.get_initials()
        if not self.salutation:
            self.salutation = global_preferences_registry.manager()["directory__person_salutation"].format(
                self.first_name, self.last_name
            )
        super().save(*args, **kwargs)

    @classmethod
    def get_or_create_with_user(cls, user, first_name="", last_name=""):
        """
        Helper method that creates the CRM profile from user

        Arguments:
            user {User} -- The user used to generate the profile
        """

        if profile := getattr(user, "profile", None):
            return profile
        else:
            contact = EmailContact.objects.get_or_create(address=user.email.lower().strip())[0]
            if contact.entry:
                with suppress(Person.DoesNotExist):
                    return Person.objects.get(id=contact.entry.id)
            usernames = user.username.split("-")
            if not first_name:
                first_name = usernames[0]
            if not last_name and len(usernames) > 1:
                last_name = usernames[1]
            person = cls.objects.create(first_name=first_name.title(), last_name=last_name.title())
            contact.entry_id = person.id
            contact.save()
            return person

    @classmethod
    def create_with_attributes(cls, first_name, last_name, email=None):
        """
        Helper method that creates the CRM profile from user

        Arguments:
            user {User} -- The user used to generate the profile
        """

        person = cls.objects.create(first_name=first_name.title(), last_name=last_name.title())
        if email:
            EmailContact.objects.get_or_create(
                address=email.lower().strip(),
                defaults={
                    "primary": True,
                    "location": ContactLocationChoices.WORK.name,
                    "entry": person,
                },
            )

        return person

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:person"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:personrepresentation-list"

    @classmethod
    def get_relationship_managers_representation_endpoint(cls):
        return "wbcore:directory:personinchargerepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"


class BankCompanyManager(EntryManager):
    """Custom Manager for filtering directly for Investment Banks"""

    def get_queryset(self):
        if hasattr(self, "issues_products"):
            return super().get_queryset().filter(issues_products__isnull=False).distinct()

        # This model manager is called from other places on startup time,
        # hence we suppress the programming error if the migration has not yet run
        return super().get_queryset().filter(type__title="Bank").distinct()


class Company(Entry):
    class Tiering(models.TextChoices):
        ONE = "ONE", "1"
        TWO = "TWO", "2"
        THREE = "THREE", "3"
        FOUR = "FOUR", "4"
        FIVE = "FIVE", "5"

    """
    Company Model that represents a Company in the CRM
    """

    type = models.ForeignKey(
        "CompanyType",
        related_name="company",
        on_delete=models.SET_NULL,
        verbose_name=_("Type"),
        null=True,
        blank=False,
    )

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    objects = EntryManager()

    customer_status = models.ForeignKey(
        "CustomerStatus",
        related_name="company",
        on_delete=models.SET_NULL,
        verbose_name=_("Customer Status"),
        null=True,
        blank=True,
    )

    headcount = models.CharField(max_length=32, default="", blank=True, verbose_name=_("Number of employees"))
    tier = models.CharField(max_length=16, null=True, blank=True, choices=Tiering.choices, verbose_name=_("Tier"))

    description = models.TextField(default="", blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return f"{self.name}"

    def _merge(self, merged_person, **kwargs):
        super()._merge(merged_person.entry_ptr, **kwargs)
        for p in Person.objects.filter(employers=merged_person):
            p.employers.remove(merged_person)
            if self not in p.employers.all():
                p.employers.add(self)

        for rel in EmployerEmployeeRelationship.objects.filter(employer=merged_person):
            if EmployerEmployeeRelationship.objects.filter(employer=self, employee=rel.employee).exists():
                rel.delete()
            else:
                rel.employer = self
                rel.save()

    def save(self, *args, **kwargs):
        self.entry_type = "Company"
        if not self.salutation:
            self.salutation = global_preferences_registry.manager()["directory__company_salutation"].format(self.name)
        super().save(*args, **kwargs)

    def compute_str(self):
        self.slugify_computed_str = slugify(self.name, separator=" ")
        return self.name

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:company"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:companyrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"


@receiver(models.signals.post_save, sender=Entry)
def post_save_base_info(sender, instance, created, raw, **kwargs):
    if not raw:
        casted_entry = instance.get_casted_entry()
        Entry.objects.filter(id=instance.id).update(
            entry_type=casted_entry.__class__.__name__, computed_str=casted_entry.compute_str()
        )


@receiver(models.signals.post_save, sender=Company)
def post_save_company(sender, instance, created, raw, **kwargs):
    """
    Company post save signal: Triggers the post_save signals of all its employees, which updates their computed_str.
    """
    if not raw:
        if instance.employees.exists():
            for employee in instance.employees.all():
                employee.save()


@receiver(m2m_changed, sender=Person.employers.through)
def notify_entry_for_potential_claim(sender, instance, action, **kwargs):
    """
    m2m change signal: If an employer is removed or added from the person employeers M2M, we need to recompute the computed_str
    """
    if not instance.is_company:
        instance.employers.all()
        if action in ["post_add", "post_remove", "post_clear"]:
            new_computed_str = instance.str_full()
            Person.objects.filter(id=instance.id).update(computed_str=new_computed_str)


@receiver(deactivate_profile)
def handle_user_deactivation(sender, instance, substitute_profile=None, **kwargs):
    messages = []
    main_company_id = global_preferences_registry.manager()["directory__main_company"]
    try:
        main_company = Company.objects.get(id=main_company_id)

        if main_company in instance.employers.all():
            instance.employers.remove(main_company)
            messages.append(
                _("Removed {main_company} from {profile}'s employers").format(
                    main_company=main_company.computed_str, profile=instance.computed_str
                )
            )
    except Company.DoesNotExist:
        pass
    users_clients = ClientManagerRelationship.objects.filter(relationship_manager=instance).exclude(
        status=ClientManagerRelationship.Status.REMOVED
    )
    if users_clients.exists():
        if substitute_profile:
            client_number = users_clients.count()
            for relationship in users_clients:
                substitute_relationships = ClientManagerRelationship.objects.filter(
                    relationship_manager=substitute_profile, client=relationship.client
                )

                if relationship.status in [
                    ClientManagerRelationship.Status.DRAFT,
                    ClientManagerRelationship.Status.PENDINGADD,
                    ClientManagerRelationship.Status.PENDINGREMOVE,
                ]:
                    if substitute_relationships.exists():
                        relationship.delete()
                    else:
                        relationship.relationship_manager = substitute_profile
                        relationship.save()
                elif relationship.status == ClientManagerRelationship.Status.APPROVED:
                    if substitute_relationships.exists():
                        for rel in substitute_relationships.all():
                            rel.primary = relationship.primary
                            rel.status = ClientManagerRelationship.Status.APPROVED
                            rel.save()
                    else:
                        ClientManagerRelationship.objects.create(
                            relationship_manager=substitute_profile,
                            client=relationship.client,
                            status=ClientManagerRelationship.Status.APPROVED,
                            primary=relationship.primary,
                        )
                    relationship.status = ClientManagerRelationship.Status.REMOVED
                    relationship.primary = False
                    relationship.save()

            messages.append(
                _("Assigned {clients} manager role(s) to {substitute_profile}").format(
                    clients=client_number, substitute_profile=substitute_profile.computed_str
                )
            )

        else:
            for rel in users_clients.all():
                rel.status = ClientManagerRelationship.Status.REMOVED
                rel.primary = False
                rel.save()
    return messages
