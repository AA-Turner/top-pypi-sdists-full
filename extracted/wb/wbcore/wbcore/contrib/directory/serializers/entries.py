import phonenumbers
from django.core.validators import validate_email
from django.forms import ValidationError
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.registries import global_preferences_registry
from rest_framework.reverse import reverse
from slugify import slugify

from wbcore import serializers as wb_serializers
from wbcore.contrib.geography.serializers import GeographyRepresentationSerializer

from ..models import (
    ClientManagerRelationship,
    Company,
    CompanyType,
    CustomerStatus,
    EmailContact,
    EmployerEmployeeRelationship,
    Entry,
    Person,
    Specialization,
    TelephoneContact,
)
from .contacts import SocialMediaContactRepresentationSerializer
from .entry_representations import EntryRepresentationSerializer


class CompanyRepresentationSerializer(EntryRepresentationSerializer):
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:company-detail")
    profile_image = wb_serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "computed_str",
            "_detail",
            "_detail_preview",
            "primary_email",
            "primary_telephone",
            "profile_image",
            "_additional_resources",
        )


class PersonRepresentationSerializer(EntryRepresentationSerializer):
    _detail_preview = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:person-detail")
    profile_image = wb_serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = Person
        fields = (
            "id",
            "computed_str",
            "first_name",
            "last_name",
            "_detail",
            "_detail_preview",
            "primary_email",
            "primary_telephone",
            "profile_image",
            "_additional_resources",
        )


class FullDetailPersonRepresentationSerializer(PersonRepresentationSerializer):
    primary_email = wb_serializers.SerializerMethodField(
        read_only=True, required=False, label=_("Primary Email"), allow_null=True
    )
    primary_telephone = wb_serializers.SerializerMethodField(
        read_only=True, required=False, label=_("Primary Telephone"), allow_null=True
    )
    primary_position = wb_serializers.SerializerMethodField(
        read_only=True, required=False, label=_("Primary Position"), allow_null=True
    )

    def get_primary_email(self, person):
        try:
            return EmailContact.objects.get(entry_id=person.id, primary=True).address
        except EmailContact.DoesNotExist:
            return None

    def get_primary_telephone(self, person):
        try:
            return TelephoneContact.objects.get(entry_id=person.id, primary=True).number
        except TelephoneContact.DoesNotExist:
            return None

    def get_primary_position(self, person):
        try:
            rel = EmployerEmployeeRelationship.objects.get(employee_id=person.id, primary=True)
            return rel.position.title if rel.position else rel.position_name
        except EmployerEmployeeRelationship.DoesNotExist:
            return None

    class Meta:
        model = Person
        fields = (
            "id",
            "computed_str",
            "first_name",
            "last_name",
            "primary_email",
            "primary_telephone",
            "primary_position",
            "profile_image",
            "description",
            "_detail",
            "_detail_preview",
            "_additional_resources",
        )


class InternalUserProfileRepresentationSerializer(PersonRepresentationSerializer):
    def get_filter_params(self, request):
        return {"only_internal_users": True}


class CompanyTypeModelSerializer(wb_serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = (
            "id",
            "title",
        )

    def validate(self, data):
        title = data.get("title", None)
        if title:
            type = CompanyType.objects.filter(slugify_title=slugify(title, separator=" "))
            if obj := self.instance:
                type = type.exclude(id=obj.id)
            if type.exists():
                raise ValidationError({"title": _("Cannot add a duplicate company type.")})
        return data


class SpecializationModelSerializer(wb_serializers.ModelSerializer):
    def validate(self, data):
        title = data.get("title", None)
        if title:
            specialization = Specialization.objects.filter(slugify_title=slugify(title, separator=" "))
            if obj := self.instance:
                specialization = specialization.exclude(id=obj.id)
            if specialization.exists():
                raise ValidationError({"title": _("Cannot add a duplicate specialization.")})
        return data

    class Meta:
        model = Specialization
        fields = (
            "id",
            "title",
        )


class CustomerStatusModelSerializer(wb_serializers.ModelSerializer):
    class Meta:
        model = CustomerStatus
        fields = (
            "id",
            "title",
        )

    def validate(self, data):
        title = data.get("title", None)
        if title:
            status = CustomerStatus.objects.filter(slugify_title=slugify(title, separator=" "))
            if obj := self.instance:
                status = status.exclude(id=obj.id)
            if status.exists():
                raise ValidationError({"title": _("Cannot add a duplicate customer status.")})
        return data


class CompanyTypeRepresentationSerializer(wb_serializers.RepresentationSerializer):
    endpoint = "wbcore:directory:companytyperepresentation-list"
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:companytype-detail")

    class Meta:
        model = CompanyType
        fields = (
            "id",
            "title",
            "_detail",
        )


class CustomerStatusRepresentationSerializer(wb_serializers.RepresentationSerializer):
    endpoint = "wbcore:directory:customerstatusrepresentation-list"
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:customerstatus-detail")

    class Meta:
        model = CustomerStatus
        fields = (
            "id",
            "title",
            "_detail",
        )


class SpecializationRepresentationSerializer(wb_serializers.RepresentationSerializer):
    endpoint = "wbcore:directory:specializationrepresentation-list"
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:specialization-detail")

    class Meta:
        model = Specialization
        fields = (
            "id",
            "title",
            "_detail",
        )


class EntryModelSerializer(wb_serializers.ModelSerializer):
    last_event = wb_serializers.CharField(read_only=True)
    last_event_period_endswith = wb_serializers.DateTimeField(read_only=True)
    activity_heat = wb_serializers.RangeSelectField(
        color="rgb(220,20,60)", label=_("Activity Heat"), read_only=True, required=False
    )
    cities = wb_serializers.PrimaryKeyRelatedField(read_only=True)
    _cities = GeographyRepresentationSerializer(source="cities", many=True, read_only=True)

    customer_status = wb_serializers.CharField(
        help_text=_(
            "This field indicates a person's primary employer's status. It is automatically filled when the status of the primary employer is set."
        ),
        label=_("Customer Status"),
        read_only=True,
        required=False,
    )
    is_primary_employer = wb_serializers.BooleanField(read_only=True)
    position_in_company = wb_serializers.CharField(
        allow_null=True,
        default="",
        help_text=_(
            "This field indicates a person's position with their primary employer. It is automatically filled when this person is assigned an employer and this person's position with that employer is filled in."
        ),
        label=_("Position In Company"),
        read_only=True,
        required=False,
    )
    primary_address = wb_serializers.CharField(
        allow_null=True, read_only=True, required=False, label=_("Primary Address")
    )
    primary_email = wb_serializers.CharField(
        allow_null=True, required=False, read_only=False, label=_("Primary Email")
    )
    primary_manager_repr = wb_serializers.CharField(
        allow_null=True, read_only=True, required=False, label=_("Primary Manager")
    )
    primary_telephone = wb_serializers.TelephoneField(
        allow_null=True,
        required=False,
        label=_("Primary Telephone"),
    )
    primary_website = wb_serializers.URLField(allow_null=True, required=False, label=_("Primary Website"))
    primary_social = wb_serializers.URLField(allow_null=True, required=False, label=_("Primary Social"))
    profile_image = wb_serializers.ImageField(allow_null=True, required=False, label=_("Profile Image"))
    _relationship_managers = PersonRepresentationSerializer(many=True, source="relationship_managers")
    _social_media = SocialMediaContactRepresentationSerializer(many=True, read_only=True, source="social_media")
    primary_manager = wb_serializers.PrimaryKeyRelatedField(label=_("Primary Manager"), required=False, read_only=True)
    _primary_manager = InternalUserProfileRepresentationSerializer(source="primary_manager")

    @wb_serializers.register_resource()
    def detail(self, instance: Entry, request, user):
        if not (request := self.context.get("request")):
            return
        if instance.is_company:
            reverse_url = reverse("wbcore:directory:company-detail", args=[instance.id], request=request)
        else:
            reverse_url = reverse("wbcore:directory:person-detail", args=[instance.id], request=request)
        return {"detail": reverse_url}

    @wb_serializers.register_resource()
    def relationships(self, instance, request, user):
        if user.has_perm("directory.view_relationship"):
            return {
                "relationships": reverse(
                    "wbcore:directory:entry-relationship-list", args=[instance.id], request=request
                )
            }
        return {}

    @wb_serializers.register_resource()
    def get_managers(self, instance, request, user):
        return {
            "manager": f"{reverse('wbcore:directory:clientmanagerrelationship-list', args=[], request=request)}?client={instance.id}"
        }

    @wb_serializers.register_resource()
    def contacts(self, instance, request, user):
        crms = {
            "addresses": reverse("wbcore:directory:entry-addresscontact-list", args=[instance.id], request=request),
            "bankings": reverse("wbcore:directory:entry-bankingcontact-list", args=[instance.id], request=request),
            "emails": reverse("wbcore:directory:entry-emailcontact-list", args=[instance.id], request=request),
            "telephones": reverse("wbcore:directory:entry-telephonecontact-list", args=[instance.id], request=request),
            "social_media": reverse(
                "wbcore:directory:entry-socialmediacontact-list", args=[instance.id], request=request
            ),
            "websites": reverse("wbcore:directory:entry-websitecontact-list", args=[instance.id], request=request),
        }

        return crms

    def validate(self, data):
        if primary_email := data.get("primary_email", None):
            try:
                validate_email(primary_email)
            except ValidationError as e:
                raise ValidationError({"primary_email": "Invalid e-mail address"}) from e

        if primary_telephone := data.get("primary_telephone", None):
            try:
                parser_number = phonenumbers.parse(
                    primary_telephone, global_preferences_registry.manager()["directory__main_country_code"]
                )
                if parser_number:
                    formatted_number = phonenumbers.format_number(parser_number, phonenumbers.PhoneNumberFormat.E164)
                    data["primary_telephone"] = formatted_number
                else:
                    raise ValidationError({"primary_telephone": gettext("Invalid phone number format")})
            except Exception as e:
                raise ValidationError({"primary_telephone": gettext("Invalid phone number format")}) from e
        return super().validate(data)

    def update(self, instance, validated_data):
        if "primary_email" in validated_data.keys():
            primary_email = validated_data.get("primary_email", None)
            if primary_email:
                EmailContact.set_entry_primary_email(instance, primary_email)
            else:
                instance.emails.filter(primary=True).delete()

        if "primary_telephone" in validated_data.keys():
            primary_telephone = validated_data.get("primary_telephone", None)
            if primary_telephone:
                TelephoneContact.set_entry_primary_telephone(instance, primary_telephone)
            else:
                instance.telephones.filter(primary=True).delete()
        return super().update(instance, validated_data)

    def create(self, validated_data: dict) -> Entry:
        primary_email = validated_data.pop("primary_email", None)
        primary_telephone = validated_data.pop("primary_telephone", None)
        primary_manager = validated_data.pop("primary_manager", None)
        instance = super().create(validated_data)
        if primary_email:
            EmailContact.set_entry_primary_email(instance, primary_email)
        if primary_telephone:
            TelephoneContact.set_entry_primary_telephone(instance, primary_telephone)

        if primary_manager:
            manager: Person = primary_manager
        elif request := self.context.get("request"):
            manager: Person = request.user.profile
        else:
            manager = None

        if manager:
            ClientManagerRelationship.objects.create(
                client=instance,
                relationship_manager=manager,
                status=ClientManagerRelationship.Status.PENDINGADD,
                primary=True,
            )
        return instance

    class Meta:
        model = Entry
        read_only_fields = ("entry_type",)

        fields = (
            "last_event",
            "last_event_period_endswith",
            "id",
            "computed_str",
            "activity_heat",
            "addresses",
            "cities",
            "_cities",
            "customer_status",
            "entry_type",
            "is_draft_entry",
            "is_primary_employer",
            "position_in_company",
            "primary_address",
            "primary_email",
            "primary_manager_repr",
            "primary_telephone",
            "primary_website",
            "primary_social",
            "profile_image",
            "relationship_managers",
            "_relationship_managers",
            "salutation",
            "social_media",
            "_social_media",
            "signature",
            "_additional_resources",
            "primary_manager",
            "_primary_manager",
        )
