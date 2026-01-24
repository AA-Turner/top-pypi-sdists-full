from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers
from wbcore.contrib.color.enums import WBColor
from wbcore.contrib.i18n.serializers.mixins import ModelTranslateSerializerMixin

from ..models import Company, EmployerEmployeeRelationship, Person, Position
from .entries import (
    CompanyRepresentationSerializer,
    EntryModelSerializer,
    SpecializationRepresentationSerializer,
)
from .relationships import PositionRepresentationSerializer


class PersonModelSerializer(ModelTranslateSerializerMixin, EntryModelSerializer):
    primary_employer_repr = wb_serializers.CharField(read_only=True, required=False, label=_("Primary Employer"))
    has_user_account = wb_serializers.CharField(read_only=True, label=_("User Account"))
    name = wb_serializers.CharField(read_only=True)
    last_connection = wb_serializers.DateTimeField(read_only=True, default=None, label=_("Last Connection"))
    personality_profile_red = wb_serializers.RangeSelectField(
        color=WBColor.RED_LIGHT.value, required=False, label=_("Personality Profile Red")
    )
    personality_profile_green = wb_serializers.RangeSelectField(
        color=WBColor.GREEN_LIGHT.value, required=False, label=_("Personality Profile Green")
    )
    personality_profile_blue = wb_serializers.RangeSelectField(
        color=WBColor.BLUE_LIGHT.value, required=False, label=_("Personality Profile Blue")
    )
    _specializations = SpecializationRepresentationSerializer(source="specializations", many=True)
    tier = wb_serializers.CharField(help_text=_("Tier of the primary employer"), label=_("Tier"), required=False)

    def get_user_account_email(self, obj):
        if hasattr(obj, "user_account"):
            return obj.user_account.email

    def get_user_account_last_login(self, obj):
        if hasattr(obj, "user_account"):
            return obj.user_account.last_login

    @wb_serializers.register_resource()
    def employers_list(self, instance, request, user):
        return {"employers": reverse("wbcore:directory:employee-employer-list", args=[instance.id], request=request)}

    @wb_serializers.register_resource()
    def get_clients(self, instance, request, user):
        return {
            "client": f"{reverse('wbcore:directory:clientmanagerrelationship-list', args=[], request=request)}?relationship_manager={instance.id}&status=APPROVED"
        }

    @wb_serializers.register_resource()
    def activity_report(self, instance, request, user):
        return {"activity_report": None}

    def create(self, validated_data):
        instance = super().create(validated_data)

        # When setting a person's employer via the DefaultFromGet in the serializer no save method gets called and the primary mixin doesn't trigger.
        # We need to set the employer as primary manually.
        if instance.employers.exists():
            EmployerEmployeeRelationship.objects.filter(employee=instance, employer=instance.employers.first()).update(
                primary=True
            )
        return instance

    class Meta:
        model = Person
        read_only_fields = (
            "activity_heat",
            "entry_type",
            "primary_employer",
            "initials",
        )
        fields = (
            "id",
            "first_name",
            "last_name",
            "name",
            "computed_str",
            "active_employee",
            "activity_heat",
            "addresses",
            "cities",
            "_cities",
            "birthday",
            "customer_status",
            "entry_type",
            "formal",
            "has_user_account",
            "is_draft_entry",
            "last_connection",
            "personality_profile_blue",
            "personality_profile_green",
            "personality_profile_red",
            "position_in_company",
            "prefix",
            "primary_address",
            "primary_email",
            "primary_manager_repr",
            "primary_employer_repr",
            "primary_telephone",
            "primary_website",
            "primary_social",
            "profile_image",
            "salutation",
            "specializations",
            "_specializations",
            "tier",
            "_additional_resources",
            "initials",
            "description",
            "_i18n",
        )


class NewPersonModelSerializer(PersonModelSerializer):
    primary_employer = wb_serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Company.objects.all(),
        default=wb_serializers.DefaultFromGET("employers"),
        many=False,
        label=_("Primary Employer"),
        required=False,
        allow_null=True,
    )
    _primary_employer = CompanyRepresentationSerializer(
        source="primary_employer",
        many=False,
    )
    position_in_company = wb_serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Position.objects.all(),
        many=False,
        label=_("Position In Company"),
        required=False,
        allow_null=True,
        depends_on=[{"field": "primary_employer", "options": {}}],
    )
    _position_in_company = PositionRepresentationSerializer(
        source="position_in_company",
        many=False,
        depends_on=[{"field": "primary_employer", "options": {}}],
    )
    position_name = wb_serializers.CharField(
        label=_("Position Name"),
        allow_null=True,
        required=False,
        depends_on=[{"field": "primary_employer", "options": {}}],
    )

    def create(self, validated_data: dict) -> Person:
        primary_employer = validated_data.pop("primary_employer", None)
        position_in_company = validated_data.pop("position_in_company", None)
        position_name = validated_data.pop("position_name", None)
        validated_data.pop("employers", None)
        instance = super().create(validated_data)
        if primary_employer:
            EmployerEmployeeRelationship.objects.create(
                employee=instance,
                employer=primary_employer,
                primary=True,
                position=position_in_company,
                position_name=position_name,
            )
        return instance

    class Meta(PersonModelSerializer.Meta):
        model = Person
        read_only_fields = (
            "activity_heat",
            "entry_type",
            "initials",
        )
        fields = PersonModelSerializer.Meta.fields + (
            "_position_in_company",
            "primary_manager",
            "_primary_manager",
            "primary_employer",
            "_primary_employer",
            "position_name",
        )


class PersonModelListSerializer(PersonModelSerializer):
    @wb_serializers.register_resource()
    def get_managers(self, instance, request, user):
        return {
            "manager": f"{reverse('wbcore:directory:clientmanagerrelationship-list', args=[], request=request)}?client={instance.id}"
        }

    class Meta:
        model = Person

        fields = (
            "id",
            "name",
            "activity_heat",
            "addresses",
            "cities",
            "_cities",
            "customer_status",
            "primary_employer_repr",
            "primary_address",
            "primary_email",
            "primary_manager_repr",
            "primary_website",
            "primary_social",
            "primary_telephone",
            "last_event",
            "position_in_company",
            "tier",
            "_additional_resources",
        )
