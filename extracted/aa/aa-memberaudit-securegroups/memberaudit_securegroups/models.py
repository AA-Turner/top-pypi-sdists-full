"""The models"""

import datetime
from collections import defaultdict

import humanize

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import F, OuterRef, Q, QuerySet, Subquery
from django.utils.formats import localize
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from eveuniverse.models import EveType

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from memberaudit.app_settings import MEMBERAUDIT_APP_NAME
from memberaudit.models import (
    Character,
    CharacterAsset,
    CharacterCloneInfo,
    CharacterCorporationHistory,
    CharacterRole,
    CharacterSkillSetCheck,
    CharacterTitle,
    General,
    Location,
    SkillSet,
)


def _get_threshold_date(timedelta_in_days: int) -> datetime.datetime:
    """Get the threshold date

    Args:
        timedelta_in_days: The timedelta in days

    Returns:
        datetime.datetime: The threshold date
    """

    return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        days=timedelta_in_days
    )


class BaseFilter(models.Model):
    """The base model for all filters."""

    description = models.CharField(
        max_length=500,
        help_text=_("The filter description that is shown to end users."),
    )  # this is what is shown to the user

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    @property
    def name(self) -> str:
        """Return the name of the filter."""
        raise NotImplementedError()

    def process_filter(self, user: User) -> bool:
        """Process the filter

        Args:
            user: The user

        Returns:
            Report whether the filter applies to the user.
        """

        raise NotImplementedError("Must be defined")

    def audit_filter(self, users: QuerySet[User]) -> dict:
        """Return information for each given user weather they pass the filter,
        and a help message shown in the audit feature.

        Args:
            users: The users to be covered

        Returns:
            The audit information
        """

        raise NotImplementedError("Must be defined")


class ActivityFilter(BaseFilter):
    """ActivityFilter"""

    inactivity_threshold = models.PositiveIntegerField(
        help_text=_("Maximum allowable inactivity, in <strong>days</strong>.")
    )

    class Meta:
        verbose_name = _("Smart Filter: Activity")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        inactivity_threshold = ngettext(
            singular="{inactivity_threshold:d} day",
            plural="{inactivity_threshold:d} days",
            number=self.inactivity_threshold,
        ).format(inactivity_threshold=self.inactivity_threshold)

        return str(
            _("Activity [Last {inactivity_threshold}]").format(
                inactivity_threshold=inactivity_threshold
            )
        )

    def process_filter(self, user: User) -> bool:
        threshold_date = _get_threshold_date(
            timedelta_in_days=self.inactivity_threshold
        )

        return (
            Character.objects.owned_by_user(user=user)
            .filter(
                Q(online_status__last_login__gt=threshold_date)
                | Q(online_status__last_logout__gt=threshold_date),
            )
            .count()
            > 0
        )

    def audit_filter(self, users: QuerySet[User]) -> dict:
        threshold_date = _get_threshold_date(
            timedelta_in_days=self.inactivity_threshold
        )

        output = defaultdict(lambda: {"message": "", "check": False})

        for user in users:
            characters = Character.objects.owned_by_user(user=user).filter(
                Q(online_status__last_login__gt=threshold_date)
                | Q(online_status__last_logout__gt=threshold_date),
            )

            if not characters.exists():
                output[user.pk] = {
                    "message": "No characters active within threshold",
                    "check": False,
                }
                continue

            chars = defaultdict(list)

            for char in characters:
                chars[char.user.pk].append(char.eve_character.character_name)

            for char_user, char_list in chars.items():
                message = ngettext(
                    singular="Active character: ",
                    plural="Active characters: ",
                    number=len(char_list),
                )

                output[char_user] = {
                    "message": message + ", ".join(sorted(char_list)),
                    "check": True,
                }

        return output


class AgeFilter(BaseFilter):
    """AgeFilter"""

    age_threshold = models.PositiveIntegerField(
        help_text=_("Minimum allowable age, in <strong>days</strong>.")
    )

    class Meta:
        verbose_name = _("Smart Filter: Character Age")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        age_threshold = ngettext(
            "{age_threshold:d} day",
            "{age_threshold:d} days",
            self.age_threshold,
        ).format(age_threshold=self.age_threshold)

        return str(
            _("Character age [{age_threshold}]").format(age_threshold=age_threshold)
        )

    def process_filter(self, user: User) -> bool:
        threshold_date = _get_threshold_date(timedelta_in_days=self.age_threshold)

        return (
            Character.objects.owned_by_user(user=user)
            .filter(details__birthday__lt=threshold_date)
            .count()
            > 0
        )

    def audit_filter(self, users: QuerySet[User]) -> dict:
        threshold_date = _get_threshold_date(timedelta_in_days=self.age_threshold)

        output = defaultdict(lambda: {"message": "", "check": False})

        for user in users:
            characters: QuerySet[Character] = Character.objects.owned_by_user(
                user=user
            ).filter(details__birthday__lt=threshold_date)

            if not characters.exists():
                output[user.pk] = {
                    "message": "No characters are old enough",
                    "check": False,
                }
                continue

            chars = defaultdict(list)

            for char in characters:
                chars[char.user.pk].append(char.eve_character.character_name)

            for char_user, char_list in chars.items():
                output[char_user] = {
                    "message": ", ".join(sorted(char_list)),
                    "check": True,
                }

        return output


class AssetFilter(BaseFilter):
    """AssetFilter"""

    assets = models.ManyToManyField(
        to=EveType,
        help_text=_("User must possess <strong>one</strong> of the selected assets."),
    )

    class Meta:
        verbose_name = _("Smart Filter: Asset")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Member Audit Asset"))

    def process_filter(self, user: User) -> bool:
        return CharacterAsset.objects.filter(
            character__eve_character__character_ownership__user=user,
            eve_type__in=self.assets.all(),
        ).exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        matching_assets = CharacterAsset.objects.filter(
            character=OuterRef("pk"), eve_type__in=list(self.assets.all())
        )
        characters = (
            Character.objects.filter(
                eve_character__character_ownership__user__in=list(users)
            )
            .annotate(asset_name=Subquery(matching_assets.values("eve_type__name")[:1]))
            .values(
                "asset_name",
                user_id=F("eve_character__character_ownership__user_id"),
                character_name=F("eve_character__character_name"),
            )
        )

        output_users = {}
        for character in characters:
            user_id = character["user_id"]
            if user_id not in output_users:
                output_users[user_id] = []

            asset_name = character["asset_name"]
            if asset_name:
                character_name = character["character_name"]
                output_users[character["user_id"]].append(
                    f"{character_name} ({asset_name})"
                )

        output = {}
        for user_id, matches in output_users.items():
            if matches:
                message = ", ".join(sorted(matches))
                check = True
            else:
                message = _("No matching assets found")
                check = False

            output[user_id] = {"message": message, "check": check}

        user_ids = set(users.values_list("id", flat=True))
        missing_user_ids = user_ids - set(output.keys())
        for user_id in missing_user_ids:
            output[user_id] = {
                "message": _("No audit information found"),
                "check": False,
            }

        return output


class ComplianceFilter(BaseFilter):
    """ComplianceFilter"""

    reversed_logic = models.BooleanField(
        default=False,
        help_text=_("If set, all members WITHOUT compliance will pass this check."),
    )

    class Meta:
        verbose_name = _("Smart Filter: Compliance")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Compliance"))

    def process_filter(self, user: User) -> bool:
        unregistered_characters = EveCharacter.objects.filter(
            character_ownership__user=user, memberaudit_character__isnull=True
        )

        if self.reversed_logic:
            return unregistered_characters.exists()

        return not unregistered_characters.exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        unregistered_characters = EveCharacter.objects.filter(
            character_ownership__user__in=list(users),
            memberaudit_character__isnull=True,
        ).values("character_name", user_id=F("character_ownership__user_id"))

        user_with_unregistered_characters = defaultdict(list)

        for obj in unregistered_characters:
            character_name = obj["character_name"]
            user_with_unregistered_characters[obj["user_id"]].append(
                f"{character_name}"
            )

        all_memberaudit_users_ids = General.users_with_basic_access().values_list(
            "id", flat=True
        )

        output = {}
        all_characters_message = _(
            "All characters have been added to {MEMBERAUDIT_APP_NAME}"
        ).format(MEMBERAUDIT_APP_NAME=MEMBERAUDIT_APP_NAME)

        for user_id in all_memberaudit_users_ids:
            unregistered_chars = user_with_unregistered_characters.get(user_id)

            if unregistered_chars:
                missing_characters_message = ngettext(
                    singular="Missing character: ",
                    plural="Missing characters: ",
                    number=len(unregistered_chars),
                )
                message = missing_characters_message + ", ".join(
                    sorted(unregistered_chars)
                )
                check = self.reversed_logic
            else:
                message = all_characters_message
                check = not self.reversed_logic

            output[user_id] = {"message": message, "check": check}

        return output


class CorporationRoleFilter(BaseFilter):
    """Filter for corporation roles."""

    corporations = models.ManyToManyField(
        to=EveCorporationInfo,
        related_name="+",
        help_text=_(
            "The character with the role must be in one of these corporations."
        ),
    )
    role = models.CharField(
        max_length=3,
        choices=CharacterRole.Role.choices,
        db_index=True,
        help_text=_("User must have a character with this role."),
    )
    include_alts = models.BooleanField(
        default=False,
        help_text=_(
            "When True, the filter will also include the users alt-characters."
        ),
    )

    class Meta:
        verbose_name = _("Smart Filter: Corporation Role")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Member Audit Corporation Role"))

    def process_filter(self, user: User) -> bool:
        qs = CharacterRole.objects.filter(
            character__eve_character__character_ownership__user=user,
            character__eve_character__corporation_id__in=self._corporation_ids(),
            role=self.role,
            location=CharacterRole.Location.UNIVERSAL,
        )

        if not self.include_alts:
            qs = qs.filter(character__eve_character__userprofile__isnull=False)

        return qs.exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        qs = Character.objects.filter(
            eve_character__character_ownership__user__in=list(users),
            eve_character__corporation_id__in=self._corporation_ids(),
            roles__role=self.role,
            roles__location=(CharacterRole.Location.UNIVERSAL),
        )

        if not self.include_alts:
            qs = qs.filter(eve_character__userprofile__isnull=False)

        matching_characters = qs.values(
            user_id=F("eve_character__character_ownership__user_id"),
            character_name=F("eve_character__character_name"),
        )

        user_with_characters = defaultdict(list)
        for user_id in matching_characters:
            character_name = user_id["character_name"]
            user_with_characters[user_id["user_id"]].append(f"{character_name}")

        output = {
            user_id: {"message": _("No matching character found"), "check": False}
            for user_id in users.values_list("id", flat=True)
        }

        for user_id, character_names in user_with_characters.items():
            output[user_id] = {
                "message": ", ".join(sorted(character_names)),
                "check": True,
            }

        return output

    def _corporation_ids(self) -> list[int]:
        """Return Eve IDs of corporations in this filter."""

        return list(self.corporations.values_list("corporation_id", flat=True))


class CorporationTitleFilter(BaseFilter):
    """Filter for corporation titles."""

    corporations = models.ManyToManyField(
        to=EveCorporationInfo,
        related_name="+",
        help_text=_(
            "The character with the title must be in one of these corporations."
        ),
    )
    title = models.CharField(
        max_length=100,
        db_index=True,
        help_text=_("User must have a character with this title."),
    )
    include_alts = models.BooleanField(
        default=False,
        help_text=_(
            "When True, the filter will also include the users alt-characters."
        ),
    )

    class Meta:
        verbose_name = _("Smart Filter: Corporation Title")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Member Audit Corporation Title"))

    def process_filter(self, user: User) -> bool:
        qs = CharacterTitle.objects.filter(
            character__eve_character__character_ownership__user=user,
            character__eve_character__corporation_id__in=self._corporation_ids(),
            name=self.title,
        )

        if not self.include_alts:
            qs = qs.filter(character__eve_character__userprofile__isnull=False)

        return qs.exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        qs = Character.objects.filter(
            eve_character__character_ownership__user__in=list(users),
            eve_character__corporation_id__in=self._corporation_ids(),
            titles__name=self.title,
        )

        if not self.include_alts:
            qs = qs.filter(eve_character__userprofile__isnull=False)

        matching_characters = qs.values(
            user_id=F("eve_character__character_ownership__user_id"),
            character_name=F("eve_character__character_name"),
        )

        user_with_characters = defaultdict(list)
        for user_id in matching_characters:
            character_name = user_id["character_name"]
            user_with_characters[user_id["user_id"]].append(f"{character_name}")

        output = {
            user_id: {"message": _("No matching character found"), "check": False}
            for user_id in users.values_list("id", flat=True)
        }

        for user_id, character_names in user_with_characters.items():
            output[user_id] = {
                "message": ", ".join(sorted(character_names)),
                "check": True,
            }

        return output

    def _corporation_ids(self) -> list[int]:
        """Return Eve IDs of corporations in this filter."""

        return list(self.corporations.values_list("corporation_id", flat=True))


class HomeStationFilter(BaseFilter):
    """Filter for home station."""

    home_station = models.ForeignKey(
        to=Location,
        related_name="home_station_filter",
        on_delete=models.CASCADE,
        help_text=_("User must have a character with this home station."),
    )
    include_alts = models.BooleanField(
        default=False,
        help_text=_(
            "When True, the filter will also include the users alt-characters."
        ),
    )

    class Meta:
        verbose_name = _("Smart Filter: Home Station (Death Clone)")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Member Audit Home Station"))

    def process_filter(self, user: User) -> bool:
        qs = CharacterCloneInfo.objects.filter(
            character__eve_character__character_ownership__user=user,
            home_location=self.home_station,
        )

        if not self.include_alts:
            qs = qs.filter(character__eve_character__userprofile__isnull=False)

        return qs.exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        qs = CharacterCloneInfo.objects.filter(
            character__eve_character__character_ownership__user__in=list(users),
            home_location=self.home_station,
        )

        if not self.include_alts:
            qs = qs.filter(character__eve_character__userprofile__isnull=False)

        matching_characters = qs.values(
            user_id=F("character__eve_character__character_ownership__user_id"),
            character_name=F("character__eve_character__character_name"),
        )

        user_with_characters = defaultdict(list)
        for character in matching_characters:
            character_name = character["character_name"]
            user_with_characters[character["user_id"]].append(f"{character_name}")

        output = {
            user_id: {"message": _("No matching character found"), "check": False}
            for user_id in users.values_list("id", flat=True)
        }

        for user_id, character_names in user_with_characters.items():
            output[user_id] = {
                "message": ", ".join(sorted(character_names)),
                "check": True,
            }

        return output


class SkillPointFilter(BaseFilter):
    """SkillPointFilter"""

    skill_point_threshold = models.PositiveBigIntegerField(
        help_text=_("Minimum allowable skill points.")
    )

    class Meta:
        verbose_name = _("Smart Filter: Skill Points")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        sp_threshold = humanize.intword(self.skill_point_threshold)

        skill_point_threshold = ngettext(
            singular="{sp_threshold} skill point",
            plural="{sp_threshold} skill points",
            number=self.skill_point_threshold,
        ).format(sp_threshold=sp_threshold)

        return str(
            _("Member Audit Skill Points [{skill_point_threshold}]").format(
                skill_point_threshold=skill_point_threshold
            )
        )

    def process_filter(self, user: User) -> bool:
        return (
            Character.objects.owned_by_user(user=user)
            .filter(skillpoints__total__gt=self.skill_point_threshold)
            .count()
            > 0
        )

    def audit_filter(self, users: QuerySet[User]) -> dict:
        output = defaultdict(lambda: {"message": "", "check": False})

        for user in users:
            characters = Character.objects.owned_by_user(user=user).filter(
                skillpoints__total__gt=self.skill_point_threshold
            )

            if not characters.exists():
                output[user.pk] = {
                    "message": "No characters with sufficient skill points",
                    "check": False,
                }
                continue

            chars = defaultdict(list)

            for char in characters:
                chars[char.user.pk].append(char.eve_character.character_name)

            for char_user, char_list in chars.items():
                output[char_user] = {
                    "message": ", ".join(sorted(char_list)),
                    "check": True,
                }

        return output


class SkillSetFilter(BaseFilter):
    """SkillSetFilter"""

    class CharacterType(models.TextChoices):
        """A character type."""

        ANY = "AN", _("Any")
        MAINS_ONLY = "MO", _("Mains only")
        ALTS_ONLY = "AO", _("Alts only")

    skill_sets = models.ManyToManyField(
        to=SkillSet,
        help_text=_(
            "Users must have a character who possess all of the skills in "
            "<strong>one</strong> of the selected skill sets."
        ),
    )
    character_type = models.CharField(
        max_length=2,
        choices=CharacterType.choices,
        default=CharacterType.ANY,
        blank=True,
        help_text=_("Specify the type of character that needs to have the skill set."),
    )

    class Meta:
        verbose_name = _("Smart Filter: Skill Set")
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # Make sure a character_type is set
        if self.character_type == "":
            self.character_type = self.CharacterType.ANY

        super().save()

    @property
    def name(self) -> str:
        return str(_("Member Audit Skill Set"))

    def process_filter(self, user: User) -> bool:
        qs = CharacterSkillSetCheck.objects.filter(
            character__eve_character__character_ownership__user=user,
            skill_set__in=list(self.skill_sets.all()),
            failed_required_skills__isnull=True,
        )

        if self.character_type == self.CharacterType.MAINS_ONLY:
            qs = qs.filter(character__eve_character__userprofile__isnull=False)
        elif self.character_type == self.CharacterType.ALTS_ONLY:
            qs = qs.filter(character__eve_character__userprofile__isnull=True)

        return qs.exists()

    def audit_filter(self, users: QuerySet[User]) -> dict:
        qs = Character.objects.filter(
            skill_set_checks__skill_set__in=list(self.skill_sets.all()),
            skill_set_checks__failed_required_skills__isnull=True,
        )

        if self.character_type == self.CharacterType.MAINS_ONLY:
            qs = qs.filter(eve_character__userprofile__isnull=False)
        elif self.character_type == self.CharacterType.ALTS_ONLY:
            qs = qs.filter(eve_character__userprofile__isnull=True)

        matching_characters = qs.values(
            user_id=F("eve_character__character_ownership__user_id"),
            character_name=F("eve_character__character_name"),
        )

        user_with_characters = defaultdict(list)

        for user_id in matching_characters:
            character_name = user_id["character_name"]
            user_with_characters[user_id["user_id"]].append(f"{character_name}")

        output = {
            user_id: {"message": _("No matching character found"), "check": False}
            for user_id in users.values_list("id", flat=True)
        }

        for user_id, character_names in user_with_characters.items():
            output[user_id] = {
                "message": ", ".join(sorted(character_names)),
                "check": True,
            }

        return output


class TimeInCorporationFilter(BaseFilter):
    """Filter for time in a corporation."""

    minimum_days = models.PositiveIntegerField(
        default=30,
        help_text=_(
            "Minimum number of days a main character needs to be member "
            "of his/her current corporation."
        ),
    )

    reversed_logic = models.BooleanField(
        default=False,
        help_text=_(
            "If set, all members with LESS than the minimum days will pass this check."
        ),
    )

    class Meta:
        verbose_name = _("Smart Filter: Time in Corporation")
        verbose_name_plural = verbose_name

    @property
    def name(self) -> str:
        return str(_("Member Audit Time in Corporation Filter"))

    def process_filter(self, user: User) -> bool:
        try:
            character = user.profile.main_character.memberaudit_character
        except (ObjectDoesNotExist, AttributeError):
            return False

        history = (
            character.corporation_history.exclude(is_deleted=True)
            .order_by("-record_id")
            .first()
        )

        if not history:
            return False

        passes = (
            (now() - history.start_date).days < self.minimum_days
            if self.reversed_logic
            else (now() - history.start_date).days >= self.minimum_days
        )

        return passes

    def audit_filter(self, users: QuerySet[User]) -> dict:
        current_membership = (
            CharacterCorporationHistory.objects.filter(
                character=OuterRef("profile__main_character__memberaudit_character__pk")
            )
            .exclude(is_deleted=True)
            .order_by("-record_id")
        )
        users_days_in_corporation = users.annotate(
            start_date=Subquery(current_membership.values("start_date")[:1])
        )

        output = defaultdict(lambda: {"message": "", "check": False})

        for user in users_days_in_corporation:
            if not user.start_date:
                check = False
                msg = _("No audit information found")
            else:
                days_in_corporation = (now() - user.start_date).days
                check = (
                    days_in_corporation < self.minimum_days
                    if self.reversed_logic
                    else days_in_corporation >= self.minimum_days
                )
                end_date = localize(
                    (
                        user.start_date + datetime.timedelta(days=self.minimum_days)
                    ).date()
                )
                msg = (
                    ngettext(
                        singular="{days_in_corporation:d} day",
                        plural="{days_in_corporation:d} days",
                        number=days_in_corporation,
                    ).format(days_in_corporation=days_in_corporation)
                    if not self.reversed_logic
                    else ngettext(
                        singular="{days_in_corporation:d} day (End date: {end_date})",
                        plural="{days_in_corporation:d} days (End date: {end_date})",
                        number=days_in_corporation,
                    ).format(days_in_corporation=days_in_corporation, end_date=end_date)
                )

            output[user.id] = {"message": msg, "check": check}

        return output
