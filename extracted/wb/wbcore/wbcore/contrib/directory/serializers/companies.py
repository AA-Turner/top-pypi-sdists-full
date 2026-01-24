from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers

from ..models import Company, CustomerStatus, Person
from .entries import (
    CompanyTypeRepresentationSerializer,
    CustomerStatusRepresentationSerializer,
    EntryModelSerializer,
    PersonRepresentationSerializer,
)


class CompanyModelSerializer(EntryModelSerializer):
    customer_status = wb_serializers.PrimaryKeyRelatedField(
        queryset=CustomerStatus.objects.all(),
        label=_("Customer Status"),
    )
    _customer_status = CustomerStatusRepresentationSerializer(source="customer_status")
    employees = wb_serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        default=wb_serializers.DefaultFromGET("employees", many=True),
        required=False,
        many=True,
    )
    _employees = PersonRepresentationSerializer(source="employees", many=True)
    is_primary_employer = wb_serializers.BooleanField(read_only=True)
    tier = wb_serializers.CharField(help_text=settings.DEFAULT_TIERING_HELP_TEXT, label=_("Tier"), required=False)
    _type = CompanyTypeRepresentationSerializer(source="type")

    @wb_serializers.register_resource()
    def employees_list(self, instance, request, user):
        return {"employees": reverse("wbcore:directory:employer-employee-list", args=[instance.id], request=request)}

    class Meta:
        model = Company
        read_only_fields = (
            "activity_heat",
            "entry_type",
        )
        fields = (
            "id",
            "computed_str",
            "activity_heat",
            "addresses",
            "cities",
            "_cities",
            "customer_status",
            "_customer_status",
            "description",
            "employees",
            "_employees",
            "entry_type",
            "headcount",
            "is_draft_entry",
            "is_primary_employer",
            "name",
            "primary_address",
            "primary_email",
            "primary_manager_repr",
            "primary_telephone",
            "primary_website",
            "primary_social",
            "profile_image",
            "salutation",
            "signature",
            "tier",
            "type",
            "_type",
            "_additional_resources",
            "primary_manager",
            "_primary_manager",
        )


class CompanyModelListSerializer(CompanyModelSerializer):
    eer_id = wb_serializers.CharField(default="", required=False, read_only=True)
    is_primary_employer = wb_serializers.BooleanField(read_only=True)

    @wb_serializers.register_resource()
    def delete(self, instance, request, user):
        if "view" in request.parser_context:
            try:
                person_id = request.parser_context["view"].kwargs.get("person_id", None)
            except AttributeError:
                return {}
            if person_id and instance.eer_id:
                if not (instance.is_primary_employer is True and len(self.instance) > 1):
                    return {
                        "delete": reverse(
                            "wbcore:directory:employeremployee-delete",
                            args=[instance.eer_id],
                            request=request,
                        )
                    }
        return {}

    @wb_serializers.register_resource()
    def eer_relationship_instance(self, instance, request, user):
        if "view" in request.parser_context:
            try:
                person_id = request.parser_context["view"].kwargs.get("person_id", None)
            except AttributeError:
                return {}
            if person_id and instance.eer_id:
                return {
                    "eer_relationship_instance": reverse(
                        "wbcore:directory:employeremployee-detail",
                        args=[instance.eer_id],
                        request=request,
                    )
                }
        return {}

    class Meta:
        model = Company

        fields = (
            "id",
            "name",
            "activity_heat",
            "cities",
            "_cities",
            "customer_status",
            "_customer_status",
            "eer_id",
            "is_primary_employer",
            "primary_address",
            "primary_email",
            "primary_manager_repr",
            "primary_telephone",
            "primary_website",
            "primary_social",
            "last_event",
            "last_event_period_endswith",
            "tier",
            "type",
            "_type",
            "_additional_resources",
        )


class BankModelSerializer(wb_serializers.ModelSerializer):
    primary_address = wb_serializers.CharField(
        allow_null=True, label=_("Primary Address"), read_only=True, required=False
    )
    primary_email = wb_serializers.CharField(allow_null=True, label=_("Primary Email"), required=False, read_only=True)
    primary_telephone = wb_serializers.TelephoneField(
        allow_null=True, label=_("Primary Telephone"), read_only=True, required=False
    )
    _relationship_managers = PersonRepresentationSerializer(many=True, source="relationship_managers")

    def create(self, validated_data: dict) -> Company:
        validated_data.pop("primary_manager", None)
        return super().create(validated_data)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "primary_address",
            "primary_email",
            "primary_telephone",
            "_relationship_managers",
            "relationship_managers",
        )
