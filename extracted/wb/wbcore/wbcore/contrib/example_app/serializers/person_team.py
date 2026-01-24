from datetime import date
from enum import Enum

import phonenumbers
from django.core.validators import validate_email
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from dynamic_preferences.registries import global_preferences_registry
from rest_framework.reverse import reverse
from slugify import slugify

from wbcore import serializers
from wbcore.contrib.directory.models import Person
from wbcore.contrib.directory.serializers import PersonRepresentationSerializer
from wbcore.contrib.example_app.models import Player, Role, SportPerson, Stadium, Team
from wbcore.contrib.example_app.serializers import (
    RoleRepresentationSerializer,
    StadiumRepresentationSerializer,
)
from wbcore.contrib.geography.serializers import GeographyRepresentationSerializer
from wbcore.serializers.fields.number import DisplayMode


class TeamErrorMessages(Enum):
    team_exists = _("A team with this name already exists.")
    wrong_founding_date = _("The founding date must be in the past.")


class SportPersonModelSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    _profile = PersonRepresentationSerializer(many=False, source="profile")
    _roles = RoleRepresentationSerializer(source="roles", many=True)

    def create(self, validated_data):
        if not validated_data.get("profile", None):
            person = Person.objects.create(
                first_name=validated_data["first_name"], last_name=validated_data["last_name"]
            )
            validated_data["profile"] = person
        return super().create(validated_data)

    class Meta:
        model = SportPerson
        fields = (
            "id",
            "first_name",
            "last_name",
            "computed_str",
            "roles",
            "_roles",
            "profile",
            "_profile",
            "profile_image",
            "_additional_resources",
        )


class SportPersonTooltipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportPerson
        fields = ("id", "first_name", "last_name", "profile_image")


class SportPersonRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="example_app:person-detail")

    class Meta:
        model = SportPerson
        fields = ("id", "computed_str", "_detail")


class TeamRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="example_app:team-detail")

    class Meta:
        model = Team
        fields = ("id", "name", "_detail")


class TeamModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(placeholder=_("Enter team name here"))
    _coach = SportPersonRepresentationSerializer(source="coach")
    home_stadium = serializers.PrimaryKeyRelatedField(
        queryset=Stadium.objects.all(), label=_("Home Stadium"), default=serializers.DefaultFromGET("stadium")
    )
    _home_stadium = StadiumRepresentationSerializer(source="home_stadium")
    _city = GeographyRepresentationSerializer(filter_params={"level": 3}, source="city")
    _opponents = TeamRepresentationSerializer(source="opponents", many=True)
    _group_key = serializers.IntegerField(read_only=True)
    phone_number = serializers.TelephoneField(label=pgettext_lazy("Phonenumber", "Number"), required=False)

    def validate(self, data: dict) -> dict:
        name: str | None = data.get("name", None)
        founded_date: date | None = data.get("founded_date", None)
        phone_number = data.get("phone_number", None)
        email = data.get("email", None)

        if name:
            team = Team.objects.filter(slugify_name=slugify(name, separator=" "))
            if obj := self.instance:
                team = team.exclude(id=obj.id)
            if team.exists():
                raise ValidationError({"name": TeamErrorMessages.team_exists.value})
        if founded_date and founded_date > timezone.now().date():
            raise ValidationError({"founded_date": TeamErrorMessages.wrong_founding_date.value})
        if email:
            try:
                validate_email(email)
            except ValidationError as e:
                raise ValidationError({"email": _("Invalid e-mail address")}) from e
        if phone_number:
            try:
                if phone_number.startswith("00"):
                    phone_number = phone_number.replace("00", "+", 1)
                parser_number = phonenumbers.parse(
                    phone_number, global_preferences_registry.manager()["directory__main_country_code"]
                )
                if parser_number:
                    formatted_number = phonenumbers.format_number(parser_number, phonenumbers.PhoneNumberFormat.E164)
                    data["phone_number"] = formatted_number
            except Exception as e:
                raise ValidationError({"phone_number": _("Invalid phone number format")}) from e

        return super().validate(data)

    @serializers.register_resource()
    def website(self, instance: Team, request, user):
        return {"website": instance.website}

    @serializers.register_resource()
    def coach(self, instance: Team, request, user):
        if instance.coach:
            return {
                "coach": reverse(
                    "example_app:person-detail",
                    args=[instance.coach.id],
                    request=self.context.get("request"),
                )
            }
        return {}

    @serializers.register_resource()
    def coach_tooltip(self, instance: Team, request, user):
        if instance.coach:
            return {
                "coach_tooltip": reverse(
                    "example_app:persontooltip-detail",
                    args=[instance.coach.id],
                    request=self.context.get("request"),
                )
            }
        return {}

    @serializers.register_only_instance_resource()
    def players_inline(self, instance: Team, request, user, view, **kwargs) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "players": reverse("example_app:player-team-list", args=[instance.pk], request=self.context["request"])
        }

    @serializers.register_only_instance_resource()
    def matches_inline(self, instance: Team, request, user, view, **kwargs) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "recent_matches": reverse(
                "example_app:match-team-list", args=[instance.pk], request=self.context["request"]
            )
        }

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "slugify_name",
            "computed_str",
            "city",
            "_city",
            "coach",
            "_coach",
            "home_stadium",
            "_home_stadium",
            "opponents",
            "_opponents",
            "founded_date",
            "website",
            "phone_number",
            "email",
            "duration_since_last_win",
            "order",
            "_group_key",
            "_additional_resources",
        )
        read_only_fields = ("duration_since_last_win",)
        optional_fields = ("current_players", "former_players", "home_matches", "away_matches")


def get_player_role() -> list[Role]:
    player_role, created = Role.objects.get_or_create(title="Player")
    return [player_role]


class PlayerModelSerializer(SportPersonModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), label=_("Roles"), default=get_player_role, many=True
    )
    _roles = RoleRepresentationSerializer(source="roles", many=True)
    current_team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        label=_("Current Team"),
        default=serializers.DefaultFromGET("team"),
    )
    transfer_value = serializers.DecimalField(
        display_mode=DisplayMode.SHORTENED, precision=1, max_digits=10, decimal_places=2
    )
    game_activity = serializers.RangeSelectField(
        color="rgb(220,20,60)", label=_("Activity Heat"), read_only=True, required=False
    )
    _current_team = TeamRepresentationSerializer(source="current_team")
    _former_teams = TeamRepresentationSerializer(source="former_teams", many=True)
    _overwrites = serializers.SerializerMethodField("overwrites")
    player_strength = serializers.StarRatingField()

    def overwrites(self, obj):
        if obj:
            transfer_value = obj.transfer_value if obj.transfer_value else 0
            operator = "!=" if transfer_value < 99999 else "="
            overwrite = {
                "fields": [
                    {
                        "rule": {"key": "transfer_value", "operator": operator, "value": "number"},
                        "overwrite": {"displayMode": "decimal", "precision": 0},
                    }
                ]
            }
            return overwrite

    def validate_player_strength(self, value):
        if value < 0 or value > 5:
            raise ValidationError(_("Rating must be between 0 and 5."))
        return value

    class Meta:
        model = Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "computed_str",
            "roles",
            "_roles",
            "current_team",
            "_current_team",
            "is_active",
            "is_injured",
            "former_teams",
            "_former_teams",
            "position",
            "player_strength",
            "game_activity",
            "transfer_value",
            "_overwrites",
        )


class TreeViewPlayerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "order", "computed_str", "current_team")


class PlayerRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="example_app:player-detail")

    class Meta:
        model = Player
        fields = ("id", "computed_str", "_detail")
