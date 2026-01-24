from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django_fsm import FSMField, transition

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.notifications.dispatch import send_notification
from wbcore.contrib.notifications.utils import create_notification_type
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons.buttons import ActionButton
from wbcore.models import WBModel
from wbcore.utils.models import ComplexToStringMixin, PrimaryMixin


class ContactLocationChoices(models.TextChoices):
    WORK = "WORK", _("Work")
    PRIVATE = "PRIVATE", _("Private")
    HOME = "HOME", pgettext_lazy("Indicates the contact location", "Home")
    OTHER = "OTHER", _("Other")


class ContactTelephoneChoices(models.TextChoices):
    FIX = "FIX", _("Fix")
    CELL = "CELL", _("Cell")
    FAX = "FAX", _("Fax")
    OTHER = "OTHER", _("Other")


class BankingContact(PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")

        @classmethod
        def get_color_map(cls):
            colors = [WBColor.RED_LIGHT.value, WBColor.YELLOW_LIGHT.value, WBColor.GREEN_LIGHT.value]
            return [choice for choice in zip(cls, colors, strict=False)]

    status = FSMField(
        default=Status.DRAFT,
        choices=Status.choices,
        verbose_name=_("Status"),
    )

    @transition(
        field=status,
        source=Status.DRAFT,
        target=Status.PENDING,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:bankingcontact",),
                key="submit",
                label=_("Submit"),
                action_label=_("Submit"),
                icon=WBIcon.SEND.icon,
                description_fields=_("Are you sure you want to submit this banking contact for review?"),
            )
        },
    )
    def submit(self, **kwargs):
        msg = _("<p>A banking contact is in need of approving.</p>")
        title = _("New pending banking contact")
        self.notify(title, msg)

    @transition(
        field=status,
        source=Status.PENDING,
        target=Status.APPROVED,
        permission=lambda instance, user: user.has_perm("directory.administrate_bankingcontact"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:bankingcontact",),
                key="approve",
                label=_("Approve"),
                action_label=_("Approve"),
                icon=WBIcon.CONFIRM.icon,
                description_fields=_("Are you sure you want to approve this banking contact?"),
            )
        },
    )
    def approve(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=Status.PENDING,
        target=Status.DRAFT,
        permission=lambda instance, user: user.has_perm("directory.administrate_bankingcontact"),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:bankingcontact",),
                key="deny",
                label=_("Deny"),
                action_label=_("Deny"),
                icon=WBIcon.REJECT.icon,
                description_fields=_("Are you sure you want to deny this banking contact?"),
            )
        },
    )
    def deny(self, by=None, description=None, **kwargs):
        pass

    @transition(
        field=status,
        source=Status.APPROVED,
        target=Status.DRAFT,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("directory:bankingcontact",),
                key="edit",
                label=_("Edit"),
                action_label=_("Edit"),
                icon=WBIcon.EDIT.icon,
                description_fields=_("Are you sure you want to edit this banking contact?"),
            )
        },
    )
    def edit(self, by=None, description=None, **kwargs):
        pass

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for banking contact", "Primary")
    )
    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )

    entry = models.ForeignKey(
        "Entry",
        related_name="banking",
        on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy("Banking Entry", "Entry"),
        null=True,
        blank=True,
    )
    institute = models.CharField(max_length=255, verbose_name=_("Institute"))
    institute_additional = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Institute (Additional)")
    )
    iban = models.CharField(max_length=38, blank=True, null=True, verbose_name=_("IBAN"))
    swift_bic = models.CharField(max_length=11, blank=True, null=True, verbose_name=_("SWIFT/BIC"))
    edited = models.DateTimeField(auto_now=True, verbose_name=_("Edited"))
    currency = models.ForeignKey(
        "currency.Currency",
        null=True,
        blank=True,
        db_column="linked_currency",
        on_delete=models.SET_NULL,
        verbose_name=_("Currency"),
    )

    additional_information = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Additional Information"),
        help_text=_("Can be used in place of IBAN to communicate banking information"),
    )

    # Access does nothing but signals other modules that someone has further access to this bank account
    access = models.ManyToManyField(
        to="directory.Person",
        related_name="access_to_bank_accounts",
        blank=True,
    )

    def __str__(self):
        return "%s, %s" % (self.institute, self.iban)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:bankingcontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:bankingcontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{_entry.computed_str}} {{iban}} {{institute}}"

    def notify(self, title: str, msg: str):
        """
        Get a message and a title and create a notification object for the user handling the banking contact verification.
        Args:
            title (str): The Notification title
            msg (str): The Notification message
        """

        user_qs = User.objects.filter(
            models.Q(user_permissions__codename__in=["administrate_bankingcontact"])
            | models.Q(groups__permissions__codename="administrate_bankingcontact")
        )
        for user in user_qs.all().distinct():
            send_notification(
                code="directory.banking_contact.approval",
                title=title,
                body=msg,
                user=user,
                reverse_name="wbcore:directory:bankingcontact-detail",
                reverse_args=[self.id],
            )

    class Meta:
        verbose_name = _("Banking Contact")
        verbose_name_plural = _("Banking Contacts")
        permissions = (("administrate_bankingcontact", "Can Administrate Banking Contact"),)
        constraints = [
            UniqueConstraint(name="unique_iban_entry", fields=["iban", "entry"]),
        ]

        notification_types = [
            create_notification_type(
                code="directory.banking_contact.approval",
                title="Banking Contact Notification",
                help_text="Sends out a notification when you want need to approve a change in bank details",
            )
        ]


class AddressContact(PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for address contact", "Primary")
    )
    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )
    entry = models.ForeignKey(
        "Entry", related_name="addresses", on_delete=models.SET_NULL, verbose_name=_("Entry"), null=True, blank=True
    )
    street = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Street"))
    street_additional = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Street (Additional)"))
    zip = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("ZIP"))
    province = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Province"))

    geography_city = models.ForeignKey(
        "geography.Geography",
        limit_choices_to={"level": 3},
        related_name="contact_city",
        on_delete=models.PROTECT,
        verbose_name=_("City"),
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.geography_city:
            return "%s, %s %s, %s" % (
                self.street,
                self.zip,
                self.geography_city.name,
                self.geography_city.parent.parent.name,
            )
        else:
            return "%s, %s" % (
                self.street,
                self.zip,
            )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:addresscontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:addresscontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{street}}, {{_geography_city.representation}}"

    class Meta:
        verbose_name = _("Address Contact")
        verbose_name_plural = _("Address Contacts")


class TelephoneContact(PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for telephone contact", "Primary")
    )
    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )
    entry = models.ForeignKey(
        "Entry", related_name="telephones", on_delete=models.SET_NULL, verbose_name=_("Entry"), null=True, blank=True
    )
    number = models.CharField(max_length=255, verbose_name=_("Number"))
    telephone_type = models.CharField(
        max_length=32,
        default=ContactTelephoneChoices.FIX,
        choices=ContactTelephoneChoices.choices,
        verbose_name=_("Type"),
    )

    def __str__(self):
        return self.number

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:telephonecontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:telephonecontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{number}}"

    class Meta:
        verbose_name = _("Telephone Contact")
        verbose_name_plural = _("Telephone Contacts")
        constraints = [
            UniqueConstraint(name="unique_number_entry", fields=["number", "entry"]),
        ]

    @classmethod
    def set_entry_primary_telephone(cls, entry, number):
        primaries = entry.telephones.filter(primary=True)
        duplicates = entry.telephones.filter(number=number)
        if primaries.exists():
            if duplicates.exists():
                entry = entry.telephones.get(id=duplicates.first().id)
                entry.primary = True
                entry.save()
            else:
                entry = entry.telephones.get(id=primaries.first().id)
                entry.number = number
                entry.save()
        else:
            if duplicates.exists():
                entry = entry.telephones.get(id=duplicates.first().id)
                entry.primary = True
                entry.save()
            else:
                cls.objects.create(entry=entry, number=number, primary=True)


class EmailContact(ComplexToStringMixin, PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for email contact", "Primary")
    )
    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )

    entry = models.ForeignKey(
        "Entry", related_name="emails", on_delete=models.SET_NULL, verbose_name=_("Entry"), null=True, blank=True
    )

    address = models.EmailField(verbose_name=_("Email Address"), unique=True)

    def compute_str(self) -> str:
        repr = self.address
        if self.entry:
            repr += f" - {self.entry.computed_str}"
        return repr

    def save(self, *args, **kwargs):
        if self.address:
            self.address = self.address.lower()
        return super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:emailcontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:emailcontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    class Meta:
        verbose_name = _("E-Mail Contact")
        verbose_name_plural = _("E-Mail Contacts")
        constraints = [
            models.UniqueConstraint(fields=["entry", "address"], name="entry_address_unique_together"),
            models.UniqueConstraint(fields=["entry"], condition=Q(primary=True), name="unique_primary_entry_address"),
        ]

    @classmethod
    def set_entry_primary_email(cls, entry, address):
        try:
            contact = EmailContact.objects.get(address=address, entry=entry)
        except EmailContact.DoesNotExist:
            try:
                contact = EmailContact.objects.get(address=address)
                contact.entry = entry
            except EmailContact.DoesNotExist:
                contact = EmailContact(address=address, entry=entry)
        contact.primary = True
        contact.save()


class WebsiteContact(PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for website contact", "Primary")
    )
    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )

    entry = models.ForeignKey(
        "Entry", related_name="websites", on_delete=models.SET_NULL, verbose_name=_("Entry"), null=True, blank=True
    )
    url = models.URLField(verbose_name=_("URL"))

    def __str__(self):
        return self.url

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:websitecontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:websitecontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{address}}"

    class Meta:
        verbose_name = _("Website Contact")
        verbose_name_plural = _("Website Contacts")
        constraints = [
            UniqueConstraint(name="unique_website_entry", fields=["url", "entry"]),
        ]


class SocialMediaContact(PrimaryMixin, WBModel):
    PRIMARY_ATTR_FIELDS = ["entry"]

    class Platforms(models.TextChoices):
        FACEBOOK = "FACEBOOK", "Facebook"
        INSTAGRAM = "INSTAGRAM", "Instagram"
        LINKEDIN = "LINKEDIN", "LinkedIn"
        REDDIT = "REDDIT", "Reddit"
        TIKTOK = "TIKTOK", "TikTok"
        TUMBLR = "TUMBLR", "Tumblr"
        TWITTER = "TWITTER", "Twitter"
        XING = "XING", "Xing"

    primary = models.BooleanField(
        default=False, verbose_name=pgettext_lazy("Primary flag for social media contact", "Primary")
    )

    location = models.CharField(
        max_length=32,
        default=ContactLocationChoices.WORK,
        choices=ContactLocationChoices.choices,
        verbose_name=_("Location"),
    )

    platform = models.CharField(
        max_length=32,
        choices=Platforms.choices,
        verbose_name=_("Platform"),
        help_text=_("The social media platform for this contact"),
    )

    entry = models.ForeignKey(
        "Entry",
        related_name="social_media",
        on_delete=models.CASCADE,
        verbose_name=_("Entry"),
        null=True,
        blank=True,
    )
    url = models.URLField(null=False, blank=False, verbose_name=_("URL"))

    def __str__(self):
        return self.url

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:directory:socialmediacontact"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:directory:socialmediacontactrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{platform}} - {{entry}}"

    class Meta:
        verbose_name = _("Social Media Contact")
        verbose_name_plural = _("Social Media Contacts")
        constraints = [
            UniqueConstraint(name="unique_social_entry", fields=["url", "entry"]),
        ]
