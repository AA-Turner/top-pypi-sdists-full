import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, ClassVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from esi.exceptions import HTTPNotModified
from esi.models import Token

if TYPE_CHECKING:
    from allianceauth.authentication.models import CharacterOwnership
    from esi.stubs import CorporationID

from allianceauth.eveonline.evelinks import eveimageserver
from allianceauth.eveonline.managers import (
    EveAllianceManager, EveCharacterManager, EveCorporationManager,
    EveFactionManager,
)
from allianceauth.eveonline.providers import open_api_provider
from allianceauth.notifications import notify

logger = logging.getLogger(__name__)

_DEFAULT_IMAGE_SIZE = 32
DOOMHEIM_CORPORATION_ID = 1000001


class EveFactionInfo(models.Model):
    """A faction in Eve Online."""
    # There exists some soft FKs in this model as otherwise the Corp<>Faction relation is circular.
    # This cannot be fully resolved with reverse fields, as militia things?

    faction_id = models.PositiveIntegerField(unique=True, db_index=True)

    corporation_id = models.PositiveIntegerField(unique=True, blank=True, null=True)  # Soft FK
    description = models.TextField(blank=True, default="")
    # is_unique boolean required # skipped
    militia_corporation_id = models.PositiveIntegerField(unique=True, blank=True, null=True)  # Soft FK
    faction_name = models.CharField(max_length=254, unique=True)
    size_factor = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    solar_system_id = models.PositiveIntegerField(blank=True, null=True, default=None)
    station_count = models.PositiveIntegerField(blank=True, null=True, default=None)
    station_system_count = models.PositiveIntegerField(blank=True, null=True, default=None)

    last_updated = models.DateTimeField(default=now)  # auto_now_add=True doesn't allow override from Last_Modified header

    objects: ClassVar[EveFactionManager] = EveFactionManager()  # pyright: ignore[reportIncompatibleVariableOverride]

    class Meta:
        default_permissions = ()
        verbose_name = _("Faction")
        verbose_name_plural = _("Factions")
        indexes = [
            models.Index(fields=['corporation_id',]),
            models.Index(fields=['militia_corporation_id',]),
            models.Index(fields=['faction_name',])
        ]

    def __str__(self) -> str:
        return self.faction_name

    @staticmethod
    def generic_logo_url(faction_id: int, size: int = _DEFAULT_IMAGE_SIZE) -> str:
        """image URL for the given faction ID"""
        return eveimageserver.corporation_logo_url(faction_id, size)

    def logo_url(self, size: int = _DEFAULT_IMAGE_SIZE) -> str:
        """image URL of this faction"""
        return self.generic_logo_url(self.faction_id, size)

    @property
    def logo_url_32(self) -> str:
        """image URL for this faction"""
        return self.logo_url(32)

    @property
    def logo_url_64(self) -> str:
        """image URL for this faction"""
        return self.logo_url(64)

    @property
    def logo_url_128(self) -> str:
        """image URL for this faction"""
        return self.logo_url(128)

    @property
    def logo_url_256(self) -> str:
        """image URL for this faction"""
        return self.logo_url(256)

    @property
    def name(self) -> str:  # This is the literal ESI field
        return self.faction_name

    @property
    def militia_corporation(self) -> "EveCorporationInfo | None":
        """Return militia corporation of this faction or None if not found."""
        try:
            return EveCorporationInfo.objects.get(corporation_id=self.militia_corporation_id)
        except EveCorporationInfo.DoesNotExist:
            return None

    @property
    def corporation(self) -> "EveCorporationInfo | None":
        """Return corporation of this faction or None if not found."""
        try:
            return EveCorporationInfo.objects.get(corporation_id=self.corporation_id)
        except EveCorporationInfo.DoesNotExist:
            return None


class EveAllianceInfo(models.Model):
    """An alliance in Eve Online."""
    # There exists some soft FKs in this model as otherwise the Corp<>Alliance relation is circular.
    # Executor and Creator are not reverse fields on Corp.

    alliance_id = models.PositiveIntegerField(unique=True)

    creator_corporation_id = models.PositiveIntegerField(  # Soft FK
        help_text="Alliance's creator corporation ID",
        blank=True, null=True, default=None)
    creator_id = models.PositiveIntegerField(
        help_text="Alliance's creator ID",
        blank=True, null=True, default=None)
    date_founded = models.DateField(
        help_text="Alliance's founding date",
        blank=True, null=True, default=None)
    executor_corp_id = models.PositiveIntegerField(  # Soft FK
        help_text="Alliance's executor corporation ID",
        blank=True, null=True, default=None)
    faction = models.ForeignKey(
        "EveFactionInfo",
        verbose_name=_("Faction"),
        related_name="alliance",
        help_text="Alliance's faction ID",
        on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    alliance_name = models.CharField(
        help_text="Alliance's name",
        max_length=254)
    alliance_ticker = models.CharField(
        help_text="Alliance's ticker",
        max_length=254)

    last_updated = models.DateTimeField(default=now)  # auto_now_add=True doesn't allow override from Last_Modified header

    objects: ClassVar[EveAllianceManager] = EveAllianceManager()  # pyright: ignore[reportIncompatibleVariableOverride]

    class Meta:
        default_permissions = ()
        verbose_name = _("alliance")
        verbose_name_plural = _("alliances")
        indexes = [
            models.Index(fields=['creator_corporation_id',]),
            models.Index(fields=['alliance_name',]),
            models.Index(fields=['executor_corp_id',]),
        ]

    def __str__(self) -> str:
        return self.alliance_name

    @staticmethod
    def generic_logo_url(
        alliance_id: int, size: int = _DEFAULT_IMAGE_SIZE
    ) -> str:
        """image URL for the given alliance ID"""
        return eveimageserver.alliance_logo_url(alliance_id, size)

    def logo_url(self, size: int = _DEFAULT_IMAGE_SIZE) -> str:
        """image URL of this alliance"""
        return self.generic_logo_url(self.alliance_id, size)

    @property
    def logo_url_32(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(32)

    @property
    def logo_url_64(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(64)

    @property
    def logo_url_128(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(128)

    @property
    def logo_url_256(self) -> str:
        """image URL for this alliance"""
        return self.logo_url(256)

    @property
    def creator_corporation(self) -> "EveCorporationInfo | None":
        """Return creator corporation of this alliance or None if not found."""
        try:
            return EveCorporationInfo.objects.get(corporation_id=self.creator_corporation_id)
        except EveCorporationInfo.DoesNotExist:
            return None

    @property
    def name(self) -> str:  # This is the literal ESI field
        return self.alliance_name

    @property
    def ticker(self) -> str:  # This is the literal ESI field
        return self.alliance_ticker

    @property
    def executor_corporation(self) -> "EveCorporationInfo | None":
        """Return executor corporation of this alliance or None if not found."""
        if self.executor_corp_id is None:
            return None

        try:
            return EveCorporationInfo.objects.get(corporation_id=self.executor_corp_id)
        except EveCorporationInfo.DoesNotExist:
            return None

    @property
    def executor_corporation_id(self) -> "CorporationID | None":
        """Return executor corporation of this alliance or None if not found."""
        return self.executor_corp_id if self.executor_corp_id else None

    def populate_alliance(self) -> "EveAllianceInfo":
        try:
            corp_ids = open_api_provider.get_alliance_corps(self.alliance_id)
        except HTTPNotModified:
            # nothing to update
            return self

        for corp_id in corp_ids:
            if not EveCorporationInfo.objects.filter(corporation_id=corp_id).exists():
                EveCorporationInfo.objects.create_corporation(corporation_id=corp_id)
        EveCorporationInfo.objects.filter(
            corporation_id__in=corp_ids
        ).update(
            alliance=self
        )
        EveCorporationInfo.objects.filter(alliance=self).exclude(
            corporation_id__in=corp_ids
        ).update(
            alliance=None
        )

        return self

    def update_alliance(self) -> "EveAllianceInfo":
        try:
            alliance, response = open_api_provider.get_alliance(alliance_id=self.alliance_id, last_modified=self.last_updated, use_etag=True)
        except HTTPNotModified:
            # nothing to update
            return self

        if alliance.faction_id:
            try:
                self.faction = EveFactionInfo.objects.get(faction_id=alliance.faction_id)
            except EveFactionInfo.DoesNotExist:
                self.faction = EveFactionInfo.objects.create_faction(faction_id=alliance.faction_id)
        else:
            self.faction = None

        self.creator_corporation_id = alliance.creator_corporation_id if alliance.creator_corporation_id else None
        self.creator_id = alliance.creator_id if alliance.creator_id else None
        self.date_founded = alliance.date_founded
        self.executor_corp_id = alliance.executor_corporation_id if alliance.executor_corporation_id else None
        self.alliance_name = alliance.name
        self.alliance_ticker = alliance.ticker
        self.last_updated = datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        self.save()

        return self


class EveCorporationInfo(models.Model):
    """A corporation in Eve Online."""
    corporation_id = models.PositiveIntegerField(unique=True)

    alliance = models.ForeignKey(
        EveAllianceInfo,
        blank=True, null=True, on_delete=models.SET_NULL
    )
    ceo_id = models.PositiveIntegerField(  # CEO_ID = 1 for closed corps
        help_text="Corporation's CEO ID",
        blank=True, null=True, default=None)
    creator_id = models.PositiveIntegerField(
        help_text="Corporation's creator ID",
        blank=True, null=True, default=None)
    date_founded = models.DateField(
        help_text="Corporation's founding date",
        blank=True, null=True, default=None)
    description = models.TextField(
        help_text="Corporation's description",
        blank=True, default="")
    faction = models.ForeignKey(
        "EveFactionInfo",
        blank=True, null=True, on_delete=models.SET_NULL)
    home_station_id = models.PositiveIntegerField(
        help_text="Corporation's home station ID",
        blank=True, null=True, default=None)
    member_count = models.PositiveIntegerField(
        help_text="Corporation's member count",
        blank=True, null=True, default=None)
    corporation_name = models.CharField(
        help_text="Corporation's name",
        max_length=254)
    shares = models.PositiveBigIntegerField(
        help_text="Corporation's shares",
        blank=True, null=True, default=None)
    tax_rate = models.FloatField(
        help_text="Corporation's tax rate",
        blank=True, null=True, default=None)
    corporation_ticker = models.CharField(
        help_text="Corporation's short name",
        max_length=254)
    url = models.URLField(
        help_text="Corporation's URL",
        max_length=2048,
        blank=True, default="")
    war_eligible = models.BooleanField(
        help_text="Corporation's war eligibility",
        blank=True, null=True, default=None)

    last_updated = models.DateTimeField(default=now)  # auto_now_add=True doesn't allow override from Last_Modified header

    objects: ClassVar[EveCorporationManager] = EveCorporationManager()  # pyright: ignore[reportIncompatibleVariableOverride]

    class Meta:
        indexes = [
            models.Index(fields=['ceo_id',]),
            models.Index(fields=['corporation_name',]),
        ]
        verbose_name = _("corporation")
        verbose_name_plural = _("corporations")

    def __str__(self) -> str:
        return self.corporation_name

    @staticmethod
    def generic_logo_url(
        corporation_id: int, size: int = _DEFAULT_IMAGE_SIZE
    ) -> str:
        """image URL for the given corporation ID"""
        return eveimageserver.corporation_logo_url(corporation_id, size)

    def logo_url(self, size: int = _DEFAULT_IMAGE_SIZE) -> str:
        """image URL for this corporation"""
        return self.generic_logo_url(self.corporation_id, size)

    @property
    def logo_url_32(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(32)

    @property
    def logo_url_64(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(64)

    @property
    def logo_url_128(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(128)

    @property
    def logo_url_256(self) -> str:
        """image URL for this corporation"""
        return self.logo_url(256)

    @property
    def name(self) -> str:  # This is the literal ESI field
        return self.corporation_name

    @property
    def ticker(self) -> str:  # This is the literal ESI field
        return self.corporation_ticker

    def update_corporation(self) -> "EveCorporationInfo":
        try:
            corporation, response = open_api_provider.get_corporation(corporation_id=self.corporation_id, last_modified=self.last_updated, use_etag=True)
        except HTTPNotModified:
            # nothing to update
            return self

        if corporation.alliance_id:
            try:
                self.alliance = EveAllianceInfo.objects.get(alliance_id=corporation.alliance_id)
            except EveAllianceInfo.DoesNotExist:
                self.alliance = EveAllianceInfo.objects.create_alliance(alliance_id=corporation.alliance_id)
        else:
            self.alliance = None

        if corporation.faction_id:
            try:
                self.faction = EveFactionInfo.objects.get(faction_id=corporation.faction_id)
            except EveFactionInfo.DoesNotExist:
                self.faction = EveFactionInfo.objects.create_faction(faction_id=corporation.faction_id)
        else:
            self.faction = None

        self.ceo_id = corporation.ceo_id
        self.creator_id = corporation.creator_id
        self.date_founded = corporation.date_founded
        self.description = corporation.description if corporation.description else ""
        self.home_station_id = corporation.home_station_id if corporation.home_station_id else None
        self.member_count = corporation.member_count if corporation.member_count else None
        self.corporation_name = corporation.name
        self.shares = corporation.shares if corporation.shares else None
        self.tax_rate = corporation.tax_rate if corporation.tax_rate else None
        self.corporation_ticker = corporation.ticker
        self.url = corporation.url if corporation.url and len(corporation.url) <= 2048 else ""
        self.war_eligible = corporation.war_eligible if corporation.war_eligible is not None else None
        self.last_updated = datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        self.save()

        return self


class EveCharacter(models.Model):
    """A character in Eve Online."""
    class Gender(models.TextChoices):
        male = "Male"
        female = "Female"

    character_id = models.PositiveIntegerField(unique=True)

    alliance_id = models.PositiveIntegerField(
        help_text="Character's alliance ID",
        blank=True, null=True, default=None)
    birthday = models.DateField(
        help_text="Character's creation date",
        blank=True, null=True, default=None)
    bloodline_id = models.PositiveSmallIntegerField(
        help_text="Character's bloodline ID",
        blank=True, null=True, default=None)
    corporation_id = models.PositiveIntegerField(
        help_text="Character's corporation ID",
        blank=False, null=False, default=DOOMHEIM_CORPORATION_ID)
    description = models.TextField(
        help_text="Character's description (biography)",
        blank=True, default="")
    faction_id = models.PositiveIntegerField(
        help_text="Character's faction ID",
        blank=True, null=True, default=None)
    gender = models.CharField(
        help_text="Character's gender",
        max_length=10,
        choices=Gender,
        blank=True, default="")
    character_name = models.CharField(
        help_text="Character's name",
        max_length=254)
    race_id = models.PositiveSmallIntegerField(
        help_text="Character's race ID",
        blank=True, null=True, default=None)
    security_status = models.FloatField(
        help_text="Character's security status",
        blank=True, null=True, default=0.0)
    title = models.CharField(
        help_text="Character's title",
        max_length=254,
        blank=True, default="")

    corporation_name = models.CharField(max_length=254, blank=True, default="")  # Cached attribute
    corporation_ticker = models.CharField(max_length=5, blank=True, default="")
    alliance_name = models.CharField(max_length=254, blank=True, default="")
    alliance_ticker = models.CharField(max_length=5, blank=True, default="")
    faction_name = models.CharField(max_length=254, blank=True, default="")

    last_updated = models.DateTimeField(default=now)  # auto_now_add=True doesn't allow override from Last_Modified header

    objects: ClassVar[EveCharacterManager] = EveCharacterManager()  # pyright: ignore[reportIncompatibleVariableOverride]
    character_ownership: models.OneToOneField["CharacterOwnership"]

    class Meta:
        indexes = [
            models.Index(fields=['character_name',]),
            models.Index(fields=['corporation_id',]),
            models.Index(fields=['alliance_id',]),
            models.Index(fields=['corporation_name',]),
            models.Index(fields=['alliance_name',]),
            models.Index(fields=['faction_id',]),
        ]
        verbose_name = _("character")
        verbose_name_plural = _("characters")

    def __str__(self) -> str:
        return self.character_name

    @property
    def is_biomassed(self) -> bool:
        """Whether this character is dead or not."""
        return self.corporation_id == DOOMHEIM_CORPORATION_ID

    @property
    def alliance(self) -> EveAllianceInfo | None:
        """
        Pseudo foreign key from alliance_id to EveAllianceInfo
        :raises: EveAllianceInfo.DoesNotExist
        :return: EveAllianceInfo or None
        """
        if self.alliance_id is None:
            return None
        return EveAllianceInfo.objects.get(alliance_id=self.alliance_id)

    @property
    def corporation(self) -> EveCorporationInfo:
        """
        Pseudo foreign key from corporation_id to EveCorporationInfo
        :raises: EveCorporationInfo.DoesNotExist
        :return: EveCorporationInfo
        """
        return EveCorporationInfo.objects.get(corporation_id=self.corporation_id)

    @property
    def faction(self) -> EveFactionInfo | None:
        """
        Pseudo foreign key from faction_id to EveFactionInfo
        :raises: EveFactionInfo.DoesNotExist
        :return: EveFactionInfo
        """
        if self.faction_id is None:
            return None
        return EveFactionInfo.objects.get(faction_id=self.faction_id)

    def update_character(self) -> "EveCharacter":

        try:
            character, response = open_api_provider.get_character(character_id=self.character_id, last_modified=self.last_updated, use_etag=True)
        except HTTPNotModified:
            # nothing to update
            return self

        try:
            corporation_obj = EveCorporationInfo.objects.get(corporation_id=character.corporation_id)
        except EveCorporationInfo.DoesNotExist:
            corporation_obj = EveCorporationInfo.objects.create_corporation(corporation_id=character.corporation_id)

        if character.alliance_id:
            try:
                alliance_obj = EveAllianceInfo.objects.get(alliance_id=character.alliance_id)
            except EveAllianceInfo.DoesNotExist:
                alliance_obj = EveAllianceInfo.objects.create_alliance(alliance_id=character.alliance_id)
        else:
            alliance_obj = None

        if character.faction_id:
            try:
                faction_obj = EveFactionInfo.objects.get(faction_id=character.faction_id)
            except EveFactionInfo.DoesNotExist:
                faction_obj = EveFactionInfo.objects.create_faction(faction_id=character.faction_id)
        else:
            faction_obj = None

        self.alliance_id = character.alliance_id if character.alliance_id else None
        self.birthday = character.birthday
        self.bloodline_id = character.bloodline_id
        self.corporation_id = character.corporation_id
        self.description = character.description if character.description else ""
        self.faction_id = character.faction_id if character.faction_id else None
        self.gender = character.gender
        self.character_name = character.name
        self.race_id = character.race_id
        self.security_status = character.security_status if character.security_status else 0.0
        self.title = character.title if character.title else ""
        self.corporation_name = corporation_obj.corporation_name
        self.corporation_ticker = corporation_obj.corporation_ticker
        self.alliance_name = alliance_obj.alliance_name if alliance_obj else ""
        self.alliance_ticker = alliance_obj.alliance_ticker if alliance_obj else ""
        self.faction_name = faction_obj.faction_name if faction_obj else ""
        self.last_updated = datetime.strptime(response.headers.get("Last-Modified"), "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
        self.save()
        if self.is_biomassed:
            self._remove_tokens_of_biomassed_character()

        return self

    def _remove_tokens_of_biomassed_character(self) -> None:
        """Remove tokens of this biomassed character."""
        try:
            user = self.character_ownership.user
        except ObjectDoesNotExist:
            return
        tokens_to_delete = Token.objects.filter(character_id=self.character_id)
        tokens_count = tokens_to_delete.count()
        if not tokens_count:
            return
        tokens_to_delete.delete()
        logger.info(
            "%d tokens from user %s for biomassed character %s [id:%s] deleted.",
            tokens_count,
            user,
            self,
            self.character_id,
        )
        notify(
            user=user,
            title=f"Character {self} biomassed",
            message=(
                f"Your former character {self} has been biomassed "
                "and has been removed from the list of your alts."
            )
        )

    @staticmethod
    def generic_portrait_url(
        character_id: int, size: int = _DEFAULT_IMAGE_SIZE
    ) -> str:
        """image URL for the given character ID"""
        return eveimageserver.character_portrait_url(character_id, size)

    def portrait_url(self, size=_DEFAULT_IMAGE_SIZE) -> str:
        """image URL for this character"""
        return self.generic_portrait_url(self.character_id, size)

    @property
    def portrait_url_32(self) -> str:
        """image URL for this character"""
        return self.portrait_url(32)

    @property
    def portrait_url_64(self) -> str:
        """image URL for this character"""
        return self.portrait_url(64)

    @property
    def portrait_url_128(self) -> str:
        """image URL for this character"""
        return self.portrait_url(128)

    @property
    def portrait_url_256(self) -> str:
        """image URL for this character"""
        return self.portrait_url(256)

    def corporation_logo_url(self, size=_DEFAULT_IMAGE_SIZE) -> str:
        """image URL for corporation of this character"""
        return EveCorporationInfo.generic_logo_url(self.corporation_id, size)

    @property
    def corporation_logo_url_32(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(32)

    @property
    def corporation_logo_url_64(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(64)

    @property
    def corporation_logo_url_128(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(128)

    @property
    def corporation_logo_url_256(self) -> str:
        """image URL for corporation of this character"""
        return self.corporation_logo_url(256)

    def alliance_logo_url(self, size=_DEFAULT_IMAGE_SIZE) -> str:
        """image URL for alliance of this character or empty string"""
        if self.alliance_id:
            return EveAllianceInfo.generic_logo_url(self.alliance_id, size)
        else:
            return ''

    @property
    def alliance_logo_url_32(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(32)

    @property
    def alliance_logo_url_64(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(64)

    @property
    def alliance_logo_url_128(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(128)

    @property
    def alliance_logo_url_256(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.alliance_logo_url(256)

    def faction_logo_url(self, size=_DEFAULT_IMAGE_SIZE) -> str:
        """image URL for alliance of this character or empty string"""
        if self.faction_id:
            return EveFactionInfo.generic_logo_url(self.faction_id, size)
        else:
            return ''

    @property
    def faction_logo_url_32(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.faction_logo_url(32)

    @property
    def faction_logo_url_64(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.faction_logo_url(64)

    @property
    def faction_logo_url_128(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.faction_logo_url(128)

    @property
    def faction_logo_url_256(self) -> str:
        """image URL for alliance of this character or empty string"""
        return self.faction_logo_url(256)
