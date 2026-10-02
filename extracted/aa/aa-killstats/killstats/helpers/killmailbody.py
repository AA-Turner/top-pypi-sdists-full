# Standard Library
import time
from datetime import datetime
from http import HTTPStatus
from json import JSONDecodeError
from typing import TYPE_CHECKING, ClassVar

# Third Party
import requests
from pydantic import BaseModel, Field, ValidationError

# Django
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# Alliance Auth (External Libs)
from eve_sde.models import ItemType, SolarSystem

# AA Killstats
from killstats import USER_AGENT_TEXT, __title__, app_settings, constants
from killstats.providers import logger

if TYPE_CHECKING:
    # AA Killstats
    from killstats.models import EveEntity, Killmail


class KillboardException(Exception):
    """Exception from Killboard"""


class KillmailDoesNotExist(KillboardException):
    """Killmail does not exist in storage."""


class Sequence(BaseModel):
    """A sequence entry for the zKillboard feed."""

    sequence: int


class _KillmailBodyBase(BaseModel):
    """Base class for killmail body representations."""

    def as_dict(self) -> dict:
        """Return the killmail body as a JSON-serializable dictionary."""
        return self.model_dump(mode="json")

    def to_dict(self) -> dict:
        """Alias for as_dict."""
        return self.as_dict()

    def as_json(self) -> str:
        """Return the killmail body as a JSON string."""
        return self.model_dump_json()

    def to_json(self) -> str:
        """Alias for as_json."""
        return self.as_json()


class KillmailPosition(BaseModel):
    """A position for a killmail."""

    x: float | None = None
    y: float | None = None
    z: float | None = None


class KillmailItems(BaseModel):
    flag: int | None = None
    item_type_id: int | None = None
    items: list | None = None
    quantity_dropped: int | None = None
    quantity_destroyed: int | None = None
    singleton: int | None = None


class _KillmailCharacter(BaseModel):
    character_id: int | None = None
    corporation_id: int | None = None
    alliance_id: int | None = None
    faction_id: int | None = None
    ship_type_id: int | None = None


class KillmailVictim(_KillmailCharacter):
    """A victim on a killmail."""

    items: list[KillmailItems] = []
    position: KillmailPosition | None = Field(default_factory=KillmailPosition)
    damage_taken: int | None = None


class KillmailAttacker(_KillmailCharacter):
    """An attacker on a killmail."""

    damage_done: int | None = None
    final_blow: bool | None = None
    security_status: float | None = None
    weapon_type_id: int | None = None


class esiKillmail(BaseModel):  # pylint: disable=invalid-name
    """An ESI killmail entry."""

    attackers: list[KillmailAttacker] | None = None
    killmail_id: int
    killmail_time: datetime
    solar_system_id: int
    victim: KillmailVictim | None = None


class zKBKillmail(BaseModel):  # pylint: disable=invalid-name
    """A zKB killmail data entry."""

    locationID: int | None = None
    hash: str | None = None
    fittedValue: float | None = None
    droppedValue: float | None = None
    destroyedValue: float | None = None
    totalValue: float | None = None
    totalDroppableValue: float | None = None
    points: int | None = None
    npc: bool | None = None
    solo: bool | None = None
    awox: bool | None = None
    labels: list[str] | None = None
    attackerCount: int | None = None
    href: str | None = None


class KillmailBody(_KillmailBodyBase):
    """A detailed representation of a killmail body."""

    _STORAGE_BASE_KEY: ClassVar[str] = "aakillstats_storage_"

    killmail_id: int
    hash: str
    esi: esiKillmail
    zkb: zKBKillmail

    moon_id: int | None = None
    war_id: int | None = None

    uploaded_at: int | None = None
    sequence_id: int | None = None

    def __repr__(self) -> str:
        return f"<KillmailBody id={self.killmail_id} time={self.esi.killmail_time} solar_system_id={self.esi.solar_system_id} moon_id={self.moon_id} war_id={self.war_id}>"

    @property
    def id(self) -> int:
        """Return the killmail ID."""
        return self.killmail_id

    @property
    def killmail_time(self) -> datetime:
        """Return the killmail time from ESI data."""
        return self.esi.killmail_time

    @property
    def solar_system_id(self) -> int:
        """Return the solar system ID from ESI data."""
        return self.esi.solar_system_id

    @property
    def victim(self) -> KillmailVictim | None:
        """Return the victim from ESI data."""
        return self.esi.victim

    @property
    def attackers(self) -> list[KillmailAttacker]:
        """Return the attackers list from ESI data."""
        return self.esi.attackers or []

    def attackers_distinct_alliance_ids(self) -> set[int]:
        return {
            attacker.alliance_id
            for attacker in (self.esi.attackers or [])
            if attacker.alliance_id is not None
        }

    def attackers_distinct_corporation_ids(self) -> set[int]:
        return {
            attacker.corporation_id
            for attacker in (self.esi.attackers or [])
            if attacker.corporation_id is not None
        }

    @staticmethod
    def get_esi_killmail_bucket_remaining() -> int:
        """Return remaining tokens in django-esi 'killmail' bucket from cache, or 1200 if not initialized (full bucket)."""
        val = cache.get("esi:bucket:killmail")
        if val is not None:
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
        return 1200

    @staticmethod
    def _rate_limit() -> bool:
        """
        Check and wait for zKB rate limit.
        Returns True if it's ok to proceed, False if the rate limit was reached and
        the operation should be skipped.
        """
        # pylint: disable=too-many-nested-blocks
        last_iso = cache.get(constants.LAST_REQUEST_KEY)
        retry_after = cache.get(constants.RETRY_AFTER_KEY)

        if retry_after is not None:
            retry_after: datetime = retry_after
            wait_time = (retry_after - timezone.now()).total_seconds()
            if wait_time > 0:
                logger.warning(
                    "ZKB rate limit requires waiting %.3fs due to Too Many Requests",
                    wait_time,
                )
                time.sleep(wait_time)
                return True
            # Retry-After has passed, remove it
            cache.delete(constants.RETRY_AFTER_KEY)

        if last_iso is not None:
            last_dt = parse_datetime(last_iso)
            if last_dt is not None:
                # Minimum interval between requests in seconds
                min_interval = 1.0 / float(app_settings.KILLSTATS_MAX_ZKB_PER_SEC)
                elapsed = (timezone.now() - last_dt).total_seconds()
                if elapsed >= min_interval:
                    return True

                # Need to wait the remaining time (single sleep)
                wait = min_interval - elapsed
                if (
                    app_settings.KILLSTATS_ZKB_RATE_TIMEOUT
                    and app_settings.KILLSTATS_ZKB_RATE_TIMEOUT > 0
                ):
                    if wait <= app_settings.KILLSTATS_ZKB_RATE_TIMEOUT:
                        logger.debug("ZKB rate limit requires waiting %.3fs", wait)
                        time.sleep(wait)
                        return True
                    logger.warning(
                        "ZKB rate limit requires waiting %.3fs which exceeds RATE_TIMEOUT (%.3fs). Skipping fetch.",
                        wait,
                        app_settings.KILLSTATS_ZKB_RATE_TIMEOUT,
                    )
                    return False
                logger.warning(
                    "ZKB rate limit reached (need %.3fs wait). Skipping fetch.",
                    wait,
                )
                return False
        # if no last_request_key provided or no usable timestamp found, allow the request.
        return True

    @staticmethod
    def _too_many_requests_delay(response: requests.Response) -> bool:
        """
        Handles HTTP 429 Too Many Requests responses from ZKB.
        If the response includes a 'Retry-After' header, sets a delay in the cache and returns True to indicate the operation should be retried later.
        If the header is missing, uses a default delay value.
        Returns False if the response status is not 429, indicating the operation can continue.
        """
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            try:
                wait_time = int(response.headers.get("Retry-After"))
                logger.debug(
                    "Received 429 Too Many Requests. Retrying after %s seconds.",
                    wait_time,
                )
            except KeyError:
                logger.debug(
                    "Received 429 Too Many Requests without Retry-After header. Waiting default %s seconds.",
                    constants.RETRY_DELAY,
                )
                wait_time = constants.RETRY_DELAY
            # Set the retry after time in cache
            cache.set(
                f"{__title__.upper()}_RETRY_AFTER",
                timezone.now() + timezone.timedelta(seconds=wait_time),
            )
            return True
        return False

    @classmethod
    def get_sequence(cls):
        """Fetches and returns a sequence ID from ZKB endpoint.

        Returns None if no sequence is received.
        """
        # Check rate limit before attempting to fetch
        if not cls._rate_limit():
            return None
        logger.debug("Trying to fetch sequence from zKB...")

        sequence = requests.get(
            app_settings.ZKILLBOARD_SEQUENCE_URL,
            timeout=constants.REQUESTS_TIMEOUT,
            headers={"User-Agent": USER_AGENT_TEXT},
        )

        # Attempt to parse the JSON response into a Sequence object
        try:
            data = Sequence.model_validate(sequence.json())
        except (JSONDecodeError, ValidationError):
            logger.error("Error from ZKB R2Z2 Sequence:\n%s", sequence.text)
            return None

        # Log this request timestamp for rate limiting
        cache.set(constants.LAST_REQUEST_KEY, timezone.now().isoformat())

        # Handle 429 Too Many Requests
        if cls._too_many_requests_delay(sequence):
            return None

        # Check if the sequence is present in the parsed data
        logger.debug("Received sequence from zKB: %s", data.sequence)
        return data.sequence

    @classmethod
    def create_from_sequence(cls, sequence_id: int):
        """
        Fetches killmail data from zKB using the provided sequence ID
        creates a KillmailBody object, and returns it.

        Returns None if no killmail data is received or if the killmail cannot be created.
        """
        # Check rate limit and worker shutdown before proceeding
        if not cls._rate_limit() or cache.get(f"{__title__.upper()}_WORKER_SHUTDOWN"):
            logger.debug(
                "Worker shutdown detected or rate limit not met; stopping zKB processing"
            )
            return None

        logger.debug("Trying to fetch killmail from zKB...")
        # Log this request timestamp for rate limiting
        cache.set(constants.LAST_REQUEST_KEY, timezone.now().isoformat())
        response = requests.get(
            app_settings.ZKILLBOARD_URL + str(sequence_id) + ".json",
            timeout=constants.REQUESTS_TIMEOUT,
            headers={"User-Agent": USER_AGENT_TEXT},
        )

        # Handle 429 Too Many Requests and 404 Not Found
        if (
            KillmailBody._too_many_requests_delay(response)
            or response.status_code == HTTPStatus.NOT_FOUND
        ):
            if response.status_code == HTTPStatus.NOT_FOUND:
                logger.debug("No killmail found for sequence ID %s", sequence_id)
            return None

        try:
            return cls.model_validate(response.json())
        except (requests.JSONDecodeError, ValidationError):
            logger.error("Error from ZKB API:\n%s", response.text)
            return None

    @classmethod
    def _storage_key(cls, cache_id: int) -> str:
        return cls._STORAGE_BASE_KEY + str(cache_id)

    @classmethod
    def get(cls, cache_id: int) -> "KillmailBody":
        """Fetch a killmail from temporary storage."""
        data = cache.get(key=cls._storage_key(cache_id))
        if not data:
            raise KillmailDoesNotExist(
                f"Killmail with ID {cache_id} does not exist in storage."
            )
        try:
            if isinstance(data, str):
                return cls.model_validate_json(data)
            return cls.model_validate(data)
        except ValidationError as exc:
            logger.error(
                "Error validating killmail data from storage for ID %s: %s and data: %s",
                cache_id,
                repr(exc.errors()[0]["type"]),
                data,
            )
            raise KillboardException(
                f"Killmail with ID {cache_id} could not be validated."
            ) from exc

    def save(self) -> None:
        """Save this killmail to temporary storage."""
        cache.set(
            key=self._storage_key(self.killmail_id),
            value=self.model_dump_json(),
            timeout=app_settings.KILLSTATS_STORAGE_LIFETIME,
        )
        logger.debug("Cache created for %s", self.killmail_id)

    def delete(self) -> None:
        """Delete this killmail from temporary storage."""
        cache.delete(self._storage_key(self.killmail_id))

    def create_names_bulk(self, eve_ids: list):
        """
        Create EveEntity objects in bulk from a list of Eve IDs.

        Returns True if any EveEntity objects were created, False otherwise.
        """
        if len(eve_ids) > 0:
            # pylint: disable=import-outside-toplevel
            # AA Killstats
            from killstats.models import EveEntity

            EveEntity.objects.create_bulk_from_esi(eve_ids)
            return True
        return False

    @staticmethod
    def get_or_create_entity(eve_id: int) -> "EveEntity":
        """Get or create an entity from Eve ID."""
        # pylint: disable=import-outside-toplevel
        # AA Killstats
        from killstats.models import EveEntity

        entity, new_entry = EveEntity.objects.get_or_create_esi(eve_id=eve_id)
        if new_entry:
            logger.debug("Killstats Manager EveName: %s added", entity.name)
        return entity

    @staticmethod
    def get_region_id(solar_system_id: int) -> int | None:
        """Get or create region ID from solar system ID."""
        try:
            solar_system = SolarSystem.objects.get(id=solar_system_id)
            region_id = solar_system.constellation.region
        except ObjectDoesNotExist:
            return None
        return region_id.id

    def get_or_create_attackers(
        self, killmail: "Killmail", killmail_body: "KillmailBody"
    ):
        """Get or create attackers for a given killmail from the killmail body."""
        # pylint: disable=import-outside-toplevel
        # AA Killstats
        from killstats.models import Attacker

        attacker_list = []
        for attacker in killmail_body.esi.attackers:
            character = None
            if attacker.character_id:
                character = self.get_or_create_entity(attacker.character_id)

            corporation = None
            if attacker.corporation_id:
                corporation = self.get_or_create_entity(attacker.corporation_id)

            alliance = None
            if attacker.alliance_id:
                alliance = self.get_or_create_entity(attacker.alliance_id)

            ship = None
            if attacker.ship_type_id:
                ship = ItemType.objects.filter(id=attacker.ship_type_id).first()

            attacker_obj = Attacker(
                killmail=killmail,
                character=character,
                corporation=corporation,
                alliance=alliance,
                ship=ship,
                damage_done=attacker.damage_done,
                final_blow=attacker.final_blow,
                security_status=attacker.security_status,
                weapon_type_id=attacker.weapon_type_id,
            )
            attacker_list.append(attacker_obj)
        # Bulk create all attacker objects to optimize database operations.
        Attacker.objects.bulk_create(attacker_list, ignore_conflicts=True)
        return True


class zKBWebKillmail(BaseModel):  # pylint: disable=invalid-name
    """Helper class for interacting with the zKillboard API."""

    attackers: list[KillmailAttacker] = []
    killmail_id: int
    killmail_time: datetime
    solar_system_id: int
    victim: KillmailVictim | None = None
    zkb: zKBKillmail | None = None

    @property
    def create_esi_killmail(self) -> esiKillmail:
        """Creates a esiKillmail compatible object from the zKBWebKillmail instance."""
        return esiKillmail(
            attackers=self.attackers,
            killmail_id=self.killmail_id,
            killmail_time=self.killmail_time,
            solar_system_id=self.solar_system_id,
            victim=self.victim,
        )

    @property
    def id(self) -> int:
        """Return the killmail ID."""
        return self.killmail_id

    def as_dict(self) -> dict:
        """Return the web killmail as a JSON-serializable dictionary."""
        return self.model_dump(mode="json")

    def to_dict(self) -> dict:
        """Alias for as_dict."""
        return self.as_dict()

    def as_json(self) -> str:
        """Return the web killmail as a JSON string."""
        return self.model_dump_json()

    def to_json(self) -> str:
        """Alias for as_json."""
        return self.as_json()

    def convert_to_killmail_body(self) -> KillmailBody:
        """Convert the zKBWebKillmail instance as a KillmailBody object."""
        return KillmailBody(
            killmail_id=self.killmail_id,
            hash=self.zkb.hash if self.zkb and self.zkb.hash else "",
            esi=self.create_esi_killmail,
            zkb=self.zkb,
        )
