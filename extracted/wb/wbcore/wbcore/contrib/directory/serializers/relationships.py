from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from rest_framework.serializers import ValidationError
from slugify import slugify

from wbcore import serializers
from wbcore import serializers as wb_serializers

from ..models import (
    ClientManagerRelationship,
    Company,
    EmployerEmployeeRelationship,
    Entry,
    Person,
    Position,
    Relationship,
    RelationshipType,
)
from .entries import (
    CompanyRepresentationSerializer,
    EntryRepresentationSerializer,
    PersonRepresentationSerializer,
)


class ClientManagerRelationshipRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:clientmanagerrelationship-detail")

    class Meta:
        model = ClientManagerRelationship
        fields = (
            "id",
            "computed_str",
            "_detail",
        )


class RelationshipTypeRepresentationSerializer(wb_serializers.RepresentationSerializer):
    class Meta:
        model = RelationshipType
        fields = ("id", "counter_relationship", "title")


class RelationshipRepresentationSerializer(wb_serializers.RepresentationSerializer):
    class Meta:
        model = Relationship
        fields = (
            "id",
            "computed_str",
        )


class PositionRepresentationSerializer(wb_serializers.RepresentationSerializer):
    endpoint = "wbcore:directory:positionrepresentation-list"
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:directory:position-detail")

    class Meta:
        model = Position
        fields = (
            "id",
            "title",
            "_detail",
        )


class PositionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "id",
            "title",
        )

    def validate(self, data):
        title = data.get("title", None)
        if title:
            position = Position.objects.filter(slugify_title=slugify(title, separator=" "))
            if obj := self.instance:
                position = position.exclude(id=obj.id)
            if position.exists():
                raise ValidationError({"title": _("Cannot add a duplicate position.")})
        return data


class RelationshipTypeModelSerializer(serializers.ModelSerializer):
    _counter_relationship = RelationshipTypeRepresentationSerializer(source="counter_relationship")

    class Meta:
        model = RelationshipType
        fields = (
            "id",
            "title",
            "counter_relationship",
            "_counter_relationship",
        )

    def validate(self, data):
        title = data.get("title", None)
        if title:
            type = RelationshipType.objects.filter(slugify_title=slugify(title, separator=" "))
            if obj := self.instance:
                type = type.exclude(id=obj.id)
            if type.exists():
                raise ValidationError({"title": _("Cannot add duplicate relationship type.")})
        return data


class RelationshipModelSerializer(serializers.ModelSerializer):
    _relationship_type = RelationshipTypeRepresentationSerializer(source="relationship_type")
    from_entry = serializers.PrimaryKeyRelatedField(required=False, queryset=Entry.objects.all())
    _from_entry = EntryRepresentationSerializer(source="from_entry")
    _to_entry = EntryRepresentationSerializer(source="to_entry")

    class Meta:
        model = Relationship
        fields = (
            "id",
            "relationship_type",
            "_relationship_type",
            "from_entry",
            "_from_entry",
            "to_entry",
            "_to_entry",
        )

    def validate(self, data):
        try:
            if data.get("from_entry"):
                data["from_entry_id"] = data["from_entry"].id
            elif self.instance and self.instance.from_entry:
                data["from_entry_id"] = self.instance.from_entry.id
            else:
                data["from_entry_id"] = self.context["view"].kwargs["entry_id"]
        except KeyError as e:
            raise ValidationError(_("From entry has to be set.")) from e
        from_entry = data.get("from_entry", getattr(self.instance, "from_entry", None))
        to_entry = data.get("to_entry", getattr(self.instance, "to_entry", None))

        if from_entry == to_entry:
            msg = _("Cannot add a duplicate relationship type.")
            raise ValidationError({"from_entry": msg, "to_entry": msg})
        return super().validate(data)


class EmployerEmployeeRelationshipSerializer(serializers.ModelSerializer):
    _employer = CompanyRepresentationSerializer(source="employer")
    _employee = PersonRepresentationSerializer(source="employee")
    _position = PositionRepresentationSerializer(source="position")

    employer_profile_pic = serializers.ImageField(
        source="employer.profile_image", label=_("Profile Picture"), read_only=True
    )
    employee_profile_pic = serializers.ImageField(
        source="employee.profile_image", label=_("Profile Picture"), read_only=True
    )

    class Meta:
        model = EmployerEmployeeRelationship
        fields = (
            "id",
            "primary",
            "employer",
            "_employer",
            "employee",
            "_employee",
            "primary",
            "position",
            "_position",
            "employer_profile_pic",
            "employee_profile_pic",
            "position_name",
        )
        dependency_map = {
            "position_name": ["position"],
        }

    def validate(self, data: dict) -> dict:
        employee: Person | None = data.get("employee", None)
        employer: Company | None = data.get("employer", None)
        primary: bool | None = data.get("primary", None)

        if employee and employer and not self.instance:
            if employer in employee.employers.all():
                raise ValidationError(
                    {
                        "employee": _("{employee} is already an employee of {employer}.").format(
                            employee=employee.computed_str, employer=employer.computed_str
                        )
                    }
                )
        elif primary is not None and self.instance:
            if (
                EmployerEmployeeRelationship.objects.exclude(id=self.instance.id)
                .filter(employer=self.instance.employer, employee=self.instance.employee, primary=True)
                .exists()
                and primary is False
            ):
                raise ValidationError(
                    {"primary": _("Cannot degrade primary employer. Add a new primary employer instead.")}
                )
        return data


class ClientManagerModelSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(
        queryset=Entry.objects.all(),
        default=serializers.DefaultFromGET("client"),
        label=gettext_lazy("Client"),
        read_only=lambda view: not view.is_modifiable,
    )
    _client = EntryRepresentationSerializer(many=False, source="client")
    relationship_manager = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        default=serializers.DefaultFromGET("relationship_manager"),
        label=gettext_lazy("Relationship Manager"),
        read_only=lambda view: not view.is_modifiable,
    )
    primary = wb_serializers.BooleanField(read_only=lambda view: not view.is_modifiable)
    _relationship_manager = PersonRepresentationSerializer(many=False, source="relationship_manager")

    def validate(self, data):
        client = data.get("client", self.instance.client if self.instance else None)
        relationship_manager = data.get(
            "relationship_manager", self.instance.relationship_manager if self.instance else None
        )
        primary = data.get("primary", self.instance.primary if self.instance else None)

        if not client and not relationship_manager:
            raise ValidationError(
                {"client": _("You need to select a client"), "relationship_manager": _("You need to select a manager")}
            )

        if not client:
            raise ValidationError({"client": _("You need to select a client")})

        if not relationship_manager:
            raise ValidationError({"relationship_manager": _("You need to select a manager")})

        if client and relationship_manager:
            is_primary_manager = ClientManagerRelationship.objects.filter(
                client=client, relationship_manager=relationship_manager, primary=True
            ).exists()

            qs = ClientManagerRelationship.objects.filter(
                relationship_manager=relationship_manager,
                client=client,
                status=ClientManagerRelationship.Status.PENDINGADD,
            )
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise ValidationError(
                    {
                        "non_field_errors": _(
                            "There is already a pending request to put {manager} in charge of {client}."
                        ).format(manager=str(relationship_manager), client=client.computed_str)
                    }
                )

            qs = ClientManagerRelationship.objects.filter(
                relationship_manager=relationship_manager, client=client, status=ClientManagerRelationship.Status.DRAFT
            )
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise ValidationError(
                    {
                        "non_field_errors": _("A draft to put {manager} in charge of {client} already exists.").format(
                            manager=str(relationship_manager), client=client.computed_str
                        )
                    }
                )
            if relationship_manager.id == client.id:
                raise ValidationError(
                    {"relationship_manager": _("Client and relationship manager cannot be the same person.")}
                )
            if relationship_manager in client.relationship_managers.all() and not primary and is_primary_manager:
                raise ValidationError(
                    {
                        "primary": _(
                            "Cannot degrade primary manager. Make a primary request for a different manager instead."
                        )
                    }
                )

            qs = ClientManagerRelationship.objects.filter(
                relationship_manager=relationship_manager,
                client=client,
                status__in=[ClientManagerRelationship.Status.APPROVED, ClientManagerRelationship.Status.PENDINGREMOVE],
            )
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise ValidationError(
                    {
                        "non_field_errors": _("{manager} is already in charge of {client}.").format(
                            manager=str(relationship_manager), client=client.computed_str
                        )
                    }
                )
        return data

    class Meta:
        model = ClientManagerRelationship
        fields = (
            "id",
            "status",
            "client",
            "_client",
            "relationship_manager",
            "_relationship_manager",
            "created",
            "primary",
            "_additional_resources",
        )
        read_only_fields = ("created",)


class UserIsClientModelSerializer(wb_serializers.ModelSerializer):
    relationship_manager_name = wb_serializers.CharField(read_only=True, label="Name")
    relationship_manager_email = wb_serializers.CharField(read_only=True, label="Email")
    relationship_manager_phone_number = wb_serializers.CharField(read_only=True, label="Phone")

    class Meta:
        model = ClientManagerRelationship
        fields = (
            "id",
            "primary",
            "relationship_manager",
            "relationship_manager_name",
            "relationship_manager_email",
            "relationship_manager_phone_number",
        )
