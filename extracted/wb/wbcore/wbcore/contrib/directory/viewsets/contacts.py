from typing import TYPE_CHECKING

from django.contrib.messages import info
from django.db.models import BooleanField, Case, F, Q, Value, When
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from wbcore import viewsets
from wbcore.contrib.directory.models import (
    AddressContact,
    BankingContact,
    Company,
    EmailContact,
    EmployerEmployeeRelationship,
    Entry,
    Person,
    SocialMediaContact,
    TelephoneContact,
    WebsiteContact,
)

from ..filters import (
    AddressContactCompanyFilter,
    AddressContactPersonFilter,
    BankingContactCompanyFilter,
    BankingContactFilter,
    BankingContactPersonFilter,
    EmailContactCompanyFilter,
    EmailContactPersonFilter,
    SocialMediaContactCompanyFilter,
    SocialMediaContactPersonFilter,
    TelephoneContactCompanyFilter,
    TelephoneContactPersonFilter,
    WebsiteContactCompanyFilter,
    WebsiteContactPersonFilter,
)
from ..serializers import (
    AddressContactSerializer,
    BankingContactRepresentationSerializer,
    BankingContactSerializer,
    EmailContactRepresentationSerializer,
    EmailContactSerializer,
    ReadOnlyBankingContactSerializer,
    SocialMediaContactRepresentationSerializer,
    SocialMediaContactSerializer,
    TelephoneContactRepresentationSerializer,
    TelephoneContactSerializer,
    WebsiteContactRepresentationSerializer,
    WebsiteContactSerializer,
)
from .buttons import TelephoneContactButtonConfig
from .display.contacts import (
    AddressContactDisplay,
    AddressContactEntryDisplay,
    BankingContactDisplay,
    BankingContactEntryDisplay,
    EmailContactDisplay,
    EmailContactEntryDisplay,
    SocialMediaContactEntryDisplay,
    TelephoneContactDisplay,
    TelephoneContactEntryDisplay,
    WebsiteContactEntryDisplay,
)
from .endpoints.contacts import (
    AddressContactEntryEndpointConfig,
    BankingContactEndpointConfig,
    BankingContactEntryEndpointConfig,
    EmailContactEntryEndpointConfig,
    SocialMediaContactEntryEndpointConfig,
    TelephoneContactEntryEndpointConfig,
    WebsiteContactEntryEndpointConfig,
)
from .previews.contacts import AddressPreviewConfig
from .titles.contacts import (
    AddressContactEntryTitleConfig,
    AddressContactTitleConfig,
    BankingContactEntryTitleConfig,
    BankingContactTitleConfig,
    EmailContactEntryTitleConfig,
    EmailContactTitleConfig,
    SocialMediaContactEntryTitleConfig,
    TelephoneContactEntryTitleConfig,
    TelephoneContactTitleConfig,
    WebsiteContactEntryTitleConfig,
)

if TYPE_CHECKING:
    _Base = viewsets.ModelViewSet
else:
    _Base = object


def get_propagated_contact(qs, entry_id, propage=True):
    """
    Convenience function.
    Annotates if the contact is from a Company or Person.
    """

    entry = get_object_or_404(Entry, pk=entry_id)
    if not entry.is_company:
        person = Person.objects.get(id=entry.id)
        if person.employers.exists():
            return qs.filter(Q(entry__id=person.id) | Q(entry__in=person.employers.all())).annotate(
                company_contact=Case(
                    When(entry__entry_type=Company.__name__, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
    return qs.filter(entry__id=entry.id)


class ContactModelMixin(_Base):
    def add_messages(self, request, instance=None, **kwargs):
        if instance and instance.primary:
            contact = self.queryset.model._meta.verbose_name
            info(
                request,
                _(
                    "This is the primary {contact}. In order to delete the primary {contact}"
                    + " you have to specify a different primary contact or make it the only contact. "
                    + "To change primary status make a different contact primary instead."
                ).format(contact=contact),
            )

    def get_queryset(self):
        if "entry_id" in self.kwargs:
            entry: Entry = Entry.all_objects.get(id=self.kwargs["entry_id"])
            if not entry.is_company:
                person = entry.get_casted_entry()
                if (
                    EmployerEmployeeRelationship.objects.filter(employee=person, primary=True).exists()
                    and EmployerEmployeeRelationship.objects.filter(employee=person).count() > 1
                ):
                    return (
                        super()
                        .get_queryset()
                        .exclude(
                            entry__in=EmployerEmployeeRelationship.objects.filter(
                                employee=person, primary=False
                            ).values_list("employer", flat=True)
                        )
                    )
        return super().get_queryset()


class EmailContactRepresentationViewSet(viewsets.RepresentationViewSet):
    search_fields = ("address",)
    ordering = ["address", "pk"]
    ordering_fields = ["address"]
    serializer_class = EmailContactRepresentationSerializer
    queryset = EmailContact.objects.all().select_related("entry")

    filterset_fields = {
        "entry": ["exact"],
        "location": ["exact"],
        "primary": ["exact"],
    }


class EmailContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/email.md"
    title_config_class = EmailContactTitleConfig
    display_config_class = EmailContactDisplay
    ordering = ["primary", "location", "pk"]
    search_fields = ("address",)
    ordering_fields = ("address", "location")
    queryset = EmailContact.objects.select_related("entry")
    serializer_class = EmailContactSerializer


class AddressContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/address.md"
    title_config_class = AddressContactTitleConfig
    display_config_class = AddressContactDisplay
    filterset_fields = {
        "location": ["exact"],
        "street": ["exact", "icontains"],
        "street_additional": ["exact", "icontains"],
        "zip": ["exact", "icontains"],
    }
    preview_config_class = AddressPreviewConfig

    search_fields = ("street", "zip", "geography_city__name")
    ordering = ["primary", "location", "pk"]
    ordering_fields = [
        "zip",
        "geography_country__name",
        "street",
        "location",
        "street_additional",
        "geography_city__name",
        "geography_state__name",
        "geography_continent__name",
    ]
    queryset = AddressContact.objects.select_related("entry", "geography_city")
    serializer_class = AddressContactSerializer


class BankingContactRepresentationViewSet(viewsets.RepresentationViewSet):
    search_fields = ("institute", "iban", "swift_bic", "entry__computed_str")
    ordering_fields = ["status"]
    ordering = ["status", "pk"]
    serializer_class = BankingContactRepresentationSerializer
    queryset = BankingContact.objects.all()


class BankingContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/banking.md"
    filterset_class = BankingContactFilter
    search_fields = ("iban", "institute", "swift_bic")
    ordering = ["status", "primary", "location", "pk"]
    ordering_fields = [
        "additional_information",
        "currency__title",
        "entry__computed_str",
        "iban",
        "institute",
        "institute_additional",
        "location",
        "status",
        "swift_bic",
        "edited",
    ]
    endpoint_config_class = BankingContactEndpointConfig
    queryset = BankingContact.objects.select_related("currency", "entry")
    serializer_class = BankingContactSerializer
    display_config_class = BankingContactDisplay
    title_config_class = BankingContactTitleConfig

    def get_serializer_class(self):
        if self.new_mode or (
            "pk" in self.kwargs and (contact := self.get_object()) and contact.status == BankingContact.Status.DRAFT
        ):
            return BankingContactSerializer
        return ReadOnlyBankingContactSerializer


class EmailContactEntryViewSet(EmailContactViewSet):
    display_config_class = EmailContactEntryDisplay
    title_config_class = EmailContactEntryTitleConfig
    endpoint_config_class = EmailContactEntryEndpointConfig
    serializer_class = EmailContactSerializer

    def get_queryset(self):
        return get_propagated_contact(super().get_queryset(), self.kwargs["entry_id"])

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return EmailContactCompanyFilter
        return EmailContactPersonFilter


class AddressContactEntryViewSet(AddressContactViewSet):
    display_config_class = AddressContactEntryDisplay
    title_config_class = AddressContactEntryTitleConfig
    endpoint_config_class = AddressContactEntryEndpointConfig

    def get_queryset(self):
        qs = get_propagated_contact(super().get_queryset(), self.kwargs["entry_id"])
        qs = qs.annotate(
            geography_state=F("geography_city__parent__name"),
            geography_country=F("geography_city__parent__parent__name"),
            geography_continent=F("geography_city__parent__parent__parent__name"),
        )
        return qs

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return AddressContactCompanyFilter
        return AddressContactPersonFilter


class TelephoneContactRepresentationViewSet(viewsets.RepresentationViewSet):
    search_fields = ("number",)
    ordering = ["primary", "pk"]
    ordering_fields = ["primary"]
    serializer_class = TelephoneContactRepresentationSerializer
    queryset = TelephoneContact.objects.all()


class TelephoneContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/telephone.md"
    ordering = ["primary", "location", "pk"]
    search_fields = ["number"]
    ordering_fields = ["number", "telephone_type", "location"]
    filterset_fields = {
        "primary": ["exact"],
        "location": ["exact"],
        "entry": ["exact"],
        "number": ["contains"],
        "telephone_type": ["exact"],
    }
    queryset = TelephoneContact.objects.select_related("entry")
    serializer_class = TelephoneContactSerializer
    display_config_class = TelephoneContactDisplay
    title_config_class = TelephoneContactTitleConfig
    button_config_class = TelephoneContactButtonConfig


class TelephoneContactEntryViewSet(TelephoneContactViewSet):
    display_config_class = TelephoneContactEntryDisplay
    title_config_class = TelephoneContactEntryTitleConfig
    endpoint_config_class = TelephoneContactEntryEndpointConfig
    search_fields = ["number"]

    def get_queryset(self):
        return get_propagated_contact(super().get_queryset(), self.kwargs["entry_id"])

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return TelephoneContactCompanyFilter
        return TelephoneContactPersonFilter


class WebsiteContactRepresentationViewSet(viewsets.RepresentationViewSet):
    serializer_class = WebsiteContactRepresentationSerializer
    queryset = WebsiteContact.objects.all()


class WebsiteContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    serializer_class = WebsiteContactSerializer
    queryset = WebsiteContact.objects.select_related("entry")


class WebsiteContactEntryViewSet(ContactModelMixin, viewsets.ModelViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/website.md"
    ordering = ["primary", "location", "pk"]
    ordering_fields = ["url", "location"]
    search_fields = ["url"]
    queryset = WebsiteContact.objects.select_related("entry")
    serializer_class = WebsiteContactSerializer
    display_config_class = WebsiteContactEntryDisplay
    title_config_class = WebsiteContactEntryTitleConfig
    endpoint_config_class = WebsiteContactEntryEndpointConfig

    def get_queryset(self):
        return get_propagated_contact(super().get_queryset(), self.kwargs["entry_id"])

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return WebsiteContactCompanyFilter
        return WebsiteContactPersonFilter


class BankingContactEntryViewSet(BankingContactViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/bankingentry.md"
    display_config_class = BankingContactEntryDisplay
    title_config_class = BankingContactEntryTitleConfig
    endpoint_config_class = BankingContactEntryEndpointConfig

    def get_queryset(self):
        return get_propagated_contact(super().get_queryset(), entry_id=self.kwargs["entry_id"])

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return BankingContactCompanyFilter
        return BankingContactPersonFilter


class SocialMediaContactViewSet(ContactModelMixin, viewsets.ModelViewSet):
    search_fields = ("platform",)
    ordering_fields = ("location", "platform", "url")
    ordering = ("platform", "location", "pk")
    queryset = SocialMediaContact.objects.select_related("entry")
    serializer_class = SocialMediaContactSerializer


class SocialMediaContactEntryViewSet(SocialMediaContactViewSet):
    LIST_DOCUMENTATION = "directory/markdown/documentation/socialmedia.md"
    display_config_class = SocialMediaContactEntryDisplay
    endpoint_config_class = SocialMediaContactEntryEndpointConfig
    title_config_class = SocialMediaContactEntryTitleConfig

    def get_queryset(self):
        return get_propagated_contact(super().get_queryset(), self.kwargs["entry_id"])

    def get_filterset_class(self, request):
        entry = get_object_or_404(Entry, id=self.kwargs["entry_id"])
        if entry.is_company:
            return SocialMediaContactCompanyFilter
        return SocialMediaContactPersonFilter


class SocialMediaContactRepresentationViewSet(viewsets.RepresentationViewSet):
    serializer_class = SocialMediaContactRepresentationSerializer
    queryset = SocialMediaContact.objects.all()
