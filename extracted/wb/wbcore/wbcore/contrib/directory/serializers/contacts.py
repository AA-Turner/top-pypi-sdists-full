import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, pgettext, pgettext_lazy
from dynamic_preferences.registries import global_preferences_registry
from rest_framework import serializers
from rest_framework.reverse import reverse
from schwifty import BIC, IBAN

from wbcore import serializers as wb_serializers
from wbcore.contrib.currency.serializers import CurrencyRepresentationSerializer
from wbcore.contrib.geography.serializers import GeographyRepresentationSerializer

from ..models import (
    AddressContact,
    BankingContact,
    EmailContact,
    SocialMediaContact,
    TelephoneContact,
    WebsiteContact,
)
from .entry_representations import EntryRepresentationSerializer


class AddressContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:addresscontact-detail")
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:addresscontact-detail")

    geography_city = wb_serializers.CharField(max_length=255, read_only=True)
    label_key = "{{street}}, {{geography_city}}"

    class Meta:
        model = AddressContact
        fields = (
            "id",
            "street",
            "_detail",
            "_detail_preview",
            "geography_city",
        )


class CityRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:addresscontact-detail")
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:addresscontact-detail")

    geography_city = wb_serializers.CharField(max_length=255, read_only=True)
    label_key = "{{geography_city}}"

    class Meta:
        model = AddressContact
        fields = (
            "id",
            "_detail",
            "_detail_preview",
            "geography_city",
        )


class BankingContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _entry = EntryRepresentationSerializer(source="entry")
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:bankingcontact-detail")

    class Meta:
        model = BankingContact
        fields = ("id", "_detail", "iban", "institute", "entry", "_entry", "status", "swift_bic")


class EmailContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:emailcontact-detail")

    def get_filter_params(self, request):
        if entry_id := request.parser_context["view"].kwargs.get("entry_id", None):
            return {"entry": entry_id}
        return dict()

    class Meta:
        model = EmailContact
        fields = ("id", "_detail", "address", "computed_str")


class TelephoneContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:telephonecontact-detail")

    class Meta:
        model = TelephoneContact
        fields = ("id", "_detail", "number", "primary")


class WebsiteContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:websitecontact-detail")

    class Meta:
        model = WebsiteContact
        fields = ("id", "_detail", "url")


class SocialMediaContactRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:socialmediacontact-detail")

    class Meta:
        model = SocialMediaContact
        fields = ("id", "_detail")


class EmailContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True)
    _entry = EntryRepresentationSerializer(source="entry")

    def validate(self, data):
        address = data.get("address", None)
        entry = data.get("entry", None)
        if address and entry:
            email_contacts = EmailContact.objects.filter(address=address, entry=entry)
            if obj := self.instance:
                email_contacts = email_contacts.exclude(id=obj.id)
            if email_contacts.exists():
                raise serializers.ValidationError(
                    {
                        "address": pgettext(
                            "Warning for wrong email", "E-Mail address already in use for this {type}."
                        ).format(type=entry.entry_type.lower())
                    }
                )
        if address:
            try:
                validate_email(address)
            except ValidationError as e:
                raise serializers.ValidationError({"address": _("Invalid e-mail address")}) from e
        return data

    class Meta:
        model = EmailContact
        fields = (
            "id",
            "address",
            "company_contact",
            "entry",
            "_entry",
            "location",
            "primary",
        )


class WebsiteContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True)
    _entry = EntryRepresentationSerializer(source="entry")

    def validate(self, data):
        url = data.get("url", None)
        entry = data.get("entry", None)
        if url and entry:
            website_contact = WebsiteContact.objects.filter(url=url, entry=entry)
            if obj := self.instance:
                website_contact = website_contact.exclude(id=obj.id)
            if website_contact.exists():
                raise serializers.ValidationError(
                    {"url": _("Website already in use for this {type}.").format(type=entry.entry_type.lower())}
                )
        return data

    class Meta:
        model = WebsiteContact
        fields = ("id", "company_contact", "entry", "_entry", "location", "primary", "url")


class AddressContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True)
    _entry = EntryRepresentationSerializer(source="entry")
    _geography_city = GeographyRepresentationSerializer(source="geography_city", filter_params={"level": 3})
    geography_state = wb_serializers.CharField(read_only=True, label=gettext_lazy("State"))
    geography_country = wb_serializers.CharField(read_only=True, label=gettext_lazy("Country"))
    geography_continent = wb_serializers.CharField(read_only=True, label=gettext_lazy("Continent"))

    def validate(self, data):
        entry = data.get("entry", None)
        street = data.get("street", None)
        street_additional = data.get("street_additional", None)
        zip = data.get("zip", None)
        geography_city = data.get("geography_city", None)

        if entry and street and street_additional and zip and geography_city:
            address_contact = AddressContact.objects.filter(
                street=street, street_additional=street_additional, zip=zip, geography_city=geography_city, entry=entry
            )
            if obj := self.instance:
                address_contact = address_contact.exclude(id=obj.id)
            if address_contact.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": _("Address already in use for this {type}.").format(
                            type=entry.entry_type.lower()
                        )
                    }
                )
        return data

    @wb_serializers.register_resource()
    def entry_address(self, instance, request, user):
        if entry := instance.entry:
            return {
                "addresses": reverse("wbcore:directory:entry-addresscontact-list", args=[entry.id], request=request),
            }

        return {}

    class Meta:
        model = AddressContact
        fields = (
            "id",
            "entry",
            "_entry",
            "primary",
            "location",
            "street",
            "street_additional",
            "zip",
            "province",
            "company_contact",
            "_additional_resources",
            "geography_city",
            "_geography_city",
            "geography_state",
            "geography_country",
            "geography_continent",
        )


class TelephoneContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True)
    _entry = EntryRepresentationSerializer(source="entry")
    number = wb_serializers.TelephoneField(label=pgettext_lazy("Phonenumber", "Number"))

    def validate(self, data):
        number = data.get("number", None)
        entry = data.get("entry", None)
        formatting_successful = False
        if number:
            if entry:
                telephone_contact = TelephoneContact.objects.filter(number=number, entry=entry)
                if obj := self.instance:
                    telephone_contact = telephone_contact.exclude(id=obj.id)
                if telephone_contact.exists():
                    raise serializers.ValidationError(
                        {
                            "number": _("Phone number already in use for this {type}.").format(
                                type=entry.entry_type.lower()
                            )
                        }
                    )
            try:
                if number.startswith("00"):
                    number = number.replace("00", "+", 1)
                parser_number = phonenumbers.parse(
                    number, global_preferences_registry.manager()["directory__main_country_code"]
                )
                if parser_number:
                    formatted_number = phonenumbers.format_number(parser_number, phonenumbers.PhoneNumberFormat.E164)
                    formatting_successful = True
                    data["number"] = formatted_number
                else:
                    raise serializers.ValidationError({"number": _("Invalid phone number format")})
            except Exception as e:
                raise serializers.ValidationError({"number": _("Invalid phone number format")}) from e

            if entry and formatting_successful:
                telephone_contact = TelephoneContact.objects.filter(number=formatted_number, entry=entry)
                if obj := self.instance:
                    telephone_contact = telephone_contact.exclude(id=obj.id)
                if telephone_contact.exists():
                    raise serializers.ValidationError(
                        {
                            "number": _("Phone number already in use for this {entry}.").format(
                                type=entry.entry_type.lower()
                            )
                        }
                    )
        return data

    class Meta:
        model = TelephoneContact
        required_fields = ("entry",)
        fields = (
            "id",
            "company_contact",
            "entry",
            "_entry",
            "location",
            "number",
            "primary",
            "telephone_type",
            "_additional_resources",
        )


class BankingContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True, default=False)
    _currency = CurrencyRepresentationSerializer(source="currency")
    _entry = EntryRepresentationSerializer(source="entry")

    def validate(self, data):
        iban_repr = data.get("iban", None)
        swift_bic_repr = data.get("swift_bic", None)
        entry = data.get("entry", None)

        if iban_repr and iban_repr not in ["", "null"]:
            try:
                iban = IBAN(iban_repr)
                iban_formatted = iban.formatted
                data["iban"] = iban_formatted
            except ValueError as e:
                raise serializers.ValidationError({"iban": e}) from e

            if entry and iban_formatted:
                banking_contact = BankingContact.objects.filter(iban=iban_formatted, entry=entry)
                if obj := self.instance:
                    banking_contact = banking_contact.exclude(id=obj.id)
                if banking_contact.exists():
                    raise serializers.ValidationError(
                        {"iban": _("IBAN already in use for this {type}.").format(type=entry.entry_type.lower())}
                    )

        if swift_bic_repr and swift_bic_repr not in ["", "null"]:
            try:
                BIC(swift_bic_repr)
            except ValueError as e:
                raise serializers.ValidationError({"swift_bic": e}) from e
        return data

    class Meta:
        model = BankingContact
        read_only_fields = ("edited",)
        fields = (
            "id",
            "additional_information",
            "company_contact",
            "currency",
            "_currency",
            "edited",
            "entry",
            "_entry",
            "iban",
            "institute",
            "institute_additional",
            "location",
            "primary",
            "status",
            "swift_bic",
            "_additional_resources",
        )


class ReadOnlyBankingContactSerializer(BankingContactSerializer):
    class Meta(BankingContactSerializer.Meta):
        read_only_fields = BankingContactSerializer.Meta.fields


class SocialMediaContactSerializer(wb_serializers.ModelSerializer):
    company_contact = wb_serializers.BooleanField(read_only=True)
    _entry = EntryRepresentationSerializer(source="entry")

    def validate(self, data):
        url = data.get("url", self.instance.url if self.instance else "")
        try:
            URLValidator()(url)
        except ValidationError as e:
            raise serializers.ValidationError({"url": _("The URL you provided seems to be wrong.")}) from e

        if self.instance and (
            ((data_entry := data.get("entry")) != self.instance.entry)
            or ((data_url := data.get("url")) != self.instance.url)
        ):
            if SocialMediaContact.objects.filter(entry=data_entry, url=data_url).exists():
                raise serializers.ValidationError(
                    {"url": _("This social media account is already in use for this user")}
                )

        return super().validate(data)

    @wb_serializers.register_resource()
    def entry_social_media(self, instance, request, user):
        if entry := instance.entry:
            return {
                "social_media": reverse(
                    "wbcore:directory:entry-socialmediacontact-list", args=[entry.id], request=request
                ),
            }
        return {}

    class Meta:
        model = SocialMediaContact
        required_fields = ("entry", "platform", "url")
        fields = (
            "id",
            "company_contact",
            "entry",
            "_entry",
            "platform",
            "location",
            "primary",
            "url",
            "_additional_resources",
        )
