# Standard Library
import json
import time
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime
from http import HTTPStatus
from json import JSONDecodeError
from typing import Optional

# Third Party
import requests
from dacite import DaciteError, from_dict

# Django
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from eve_sde.models.map import SolarSystem
from eve_sde.models.types import ItemType

# AA Killstats
from killstats import USER_AGENT_TEXT, __title__, __version__
from killstats.app_settings import (
    KILLSTATS_MAX_ZKB_PER_SEC,
    KILLSTATS_STORAGE_LIFETIME,
    KILLSTATS_ZKB_RATE_TIMEOUT,
    STORAGE_BASE_KEY,
    ZKILLBOARD_API_URL,
    ZKILLBOARD_R2Z2_SEQUENCE_URL,
    ZKILLBOARD_R2Z2_URL,
)
from killstats.constants import (
    LAST_REQUEST_KEY,
    REQUESTS_TIMEOUT,
    RETRY_AFTER_KEY,
    RETRY_DELAY,
)
from killstats.helpers.core import JSONDateTimeDecoder, JSONDateTimeEncoder
from killstats.models.general import EveEntity
from killstats.models.killboard import Attacker
from killstats.providers import AppLogger, esi

logger = AppLogger(get_extension_logger(__name__), __title__)


# Example usage:
#    attackers=[FWDe5e7e5ed_5ccd_420d_8787_68168325bcdb(
#   alliance_id=99001383,
#   character_id=273213517,
#   corporation_id=1372265539,
#   damage_done=377,
#   faction_id=None,
#   final_blow=True,
#   security_status=4.8,
#   ship_type_id=32878,
#   weapon_type_id=27381
# )
# ]
#    killmail_id=113104645
#    killmail_time=datetime.datetime(2023, 11, 13, 21, 20, 42, tzinfo=TzInfo(0))
#    moon_id=None
#    solar_system_id=30004642
#    victim=FWDb837ecde_43ff_4d28_a889_5e693ad28f1a(
#   alliance_id=99011239,
#   character_id=95826959,
#   corporation_id=98702221,
#   damage_taken=460,
#   faction_id=None,
#   items=[],
#   position=Xbaea3f48_d232_4dc3_99c4_faafefc93a00(x=3373168445550.001, y=1645232080255.205, z=5872593829858.347),
#   ship_type_id=670)
#   war_id=None
class KillboardException(Exception):
    """Exception from Killboard"""


class KillmailDoesNotExist(KillboardException):
    """Killmail does not exist in storage."""


@dataclass
class _KillmailBase:
    """Base class for all Killmail."""

    def asdict(self) -> dict:
        """Return this object as dict, recursively converting nested objects."""
        return to_serializable_dict(self)


def to_serializable_dict(obj):
    """Recursively convert dataclasses and custom objects to dicts."""
    if isinstance(obj, datetime):
        return obj
    if is_dataclass(obj):
        return {k: to_serializable_dict(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: to_serializable_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_serializable_dict(v) for v in obj]
    if hasattr(obj, "__dict__"):
        data = {}
        for k, v in obj.__dict__.items():
            if not k.startswith("_"):
                k = to_serializable_dict(k)
                data[k] = to_serializable_dict(v)
        return data
    return obj


@dataclass
class KillmailItems:
    flag: int
    item_type_id: int
    items: list | None
    quantity_dropped: int
    quantity_destroyed: int
    singleton: int


@dataclass
class _KillmailCharacter(_KillmailBase):
    ENTITY_PROPS = [
        "character_id",
        "corporation_id",
        "alliance_id",
        "faction_id",
        "ship_type_id",
    ]

    character_id: int | None = None
    corporation_id: int | None = None
    alliance_id: int | None = None
    faction_id: int | None = None
    ship_type_id: int | None = None


@dataclass
class KillmailPosition(_KillmailBase):
    "A position for a killmail."

    x: float | None = None
    y: float | None = None
    z: float | None = None


@dataclass
class KillmailVictim(_KillmailCharacter):
    """A victim on a killmail."""

    items: list[KillmailItems] = field(default_factory=list)
    position: KillmailPosition | None = field(default=None)
    damage_taken: int | None = None


@dataclass
class KillmailAttacker(_KillmailCharacter):
    """An attacker on a killmail."""

    ENTITY_PROPS = _KillmailCharacter.ENTITY_PROPS + ["weapon_type_id"]

    damage_done: int | None = None
    final_blow: bool | None = None
    security_status: float | None = None
    weapon_type_id: int | None = None


@dataclass
class KillmailZkb(_KillmailBase):
    """A ZKB entry for a killmail."""

    location_id: int | None = None
    hash: str | None = None
    fitted_value: float | None = None
    dropped_value: float | None = None
    destroyed_value: float | None = None
    total_value: float | None = None
    points: int | None = None
    is_npc: bool | None = None
    is_solo: bool | None = None
    is_awox: bool | None = None


@dataclass
class KillmailBody(_KillmailBase):
    """A killmail body as returned from ZKB or ZKB API."""

    _STORAGE_BASE_KEY = "killboard_storage_killmail_"

    id: int
    time: datetime
    victim: KillmailVictim
    attackers: list[KillmailAttacker]
    position: KillmailPosition
    zkb: KillmailZkb

    solar_system_id: int | None = None
    moon_id: int | None = None
    war_id: int | None = None

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id})"

    def attackers_distinct_alliance_ids(self) -> set[int]:
        """Return distinct alliance IDs of all attackers."""
        return {obj.alliance_id for obj in self.attackers if obj.alliance_id}

    def attackers_distinct_corporation_ids(self) -> set[int]:
        """Return distinct corporation IDs of all attackers."""
        return {obj.corporation_id for obj in self.attackers if obj.corporation_id}

    def asjson(self) -> str:
        """Convert killmail into JSON data, ensuring all nested objects are serializable."""
        return json.dumps(to_serializable_dict(self), cls=JSONDateTimeEncoder)

    @staticmethod
    def _process_killmail_data(data: dict) -> dict | None:
        try:
            killmail_id = data["killmail_id"]
            killmail_hash = data["zkb"]["hash"]
            esi_killmail = esi.client.Killmails.GetKillmailsKillmailIdKillmailHash(
                killmail_hash=killmail_hash,
                killmail_id=killmail_id,
            )

            # Get killmail data from ESI
            killmail_item = esi_killmail.result(use_etag=False)
            # Convert to dict
            killmail_item = to_serializable_dict(killmail_item)

            data["esi"] = killmail_item
            # Convert killmail_time to ISO format for JSON serialization
            data["esi"]["killmail_time"] = killmail_item["killmail_time"].strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            return data
        # pylint: disable=broad-exception-caught
        except Exception as exc:
            logger.error("Killmail can't fetch %s", exc)
            return None

    # pylint: disable=too-many-locals
    @classmethod
    def get_single_killmail(cls, killmail_id: int):
        """Get kill data from zKillboard"""
        # pylint: disable=import-outside-toplevel
        # AA Killstats
        from killstats.models.killboard import Killmail

        cache_key = f"{STORAGE_BASE_KEY}_KILLMAIL_{killmail_id}"
        killmail_json = cache.get(cache_key)
        if killmail_json:
            return KillmailBody.from_json(killmail_json)

        logger.debug("Fetching killmail %s from zKillboard", killmail_id)

        url = f"{ZKILLBOARD_API_URL}killID/{killmail_id}/"
        headers = {"User-Agent": USER_AGENT_TEXT, "Content-Type": "application/json"}
        request_result = requests.get(url=url, headers=headers, timeout=5)

        try:
            request_result.raise_for_status()
            zkb_killmail = request_result.json()[0]
        except requests.HTTPError as exc:
            error_str = str(exc)

            logger.warning(
                msg=f"Unable to get killmail details from zKillboard. Error: {error_str}",
                exc_info=True,
            )

            raise ValueError(error_str) from exc
        except requests.Timeout as exc:
            error_str = str(exc)

            logger.warning(msg="Connection to zKillboard timed out …")

            raise ValueError(error_str) from exc

        killmail_id = zkb_killmail["killmail_id"]

        # Check if killmail already exists
        existing_killmail = Killmail.objects.filter(killmail_id=killmail_id).first()
        if existing_killmail:
            logger.debug("Killmail %s exists already..", killmail_id)
            return None

        # Convert killmail data to our internal format and save to cache
        zkb_killmail = cls._process_killmail_data(zkb_killmail)
        if not zkb_killmail:
            logger.warning(
                "Killmail %s could not be processed from zKillboard data.", killmail_id
            )
            return None

        killmail = cls._create_from_dict(zkb_killmail)
        if killmail:
            cache.set(key=cache_key, value=killmail.asjson())
        return killmail

    @staticmethod
    def _rate_limit() -> bool:
        """
        Check and wait for zKB rate limit.
        Returns True if it's ok to proceed, False if the rate limit was reached and
        the operation should be skipped.
        """
        # pylint: disable=too-many-nested-blocks
        last_iso = cache.get(LAST_REQUEST_KEY)
        retry_after = cache.get(RETRY_AFTER_KEY)

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
            cache.delete(RETRY_AFTER_KEY)

        if last_iso is not None:
            last_dt = parse_datetime(last_iso)
            if last_dt is not None:
                # Minimum interval between requests in seconds
                min_interval = 1.0 / float(KILLSTATS_MAX_ZKB_PER_SEC)
                elapsed = (timezone.now() - last_dt).total_seconds()
                if elapsed >= min_interval:
                    return True

                # Need to wait the remaining time (single sleep)
                wait = min_interval - elapsed
                if KILLSTATS_ZKB_RATE_TIMEOUT and KILLSTATS_ZKB_RATE_TIMEOUT > 0:
                    if wait <= KILLSTATS_ZKB_RATE_TIMEOUT:
                        logger.debug("ZKB rate limit requires waiting %.3fs", wait)
                        time.sleep(wait)
                        return True
                    logger.warning(
                        "ZKB rate limit requires waiting %.3fs which exceeds RATE_TIMEOUT (%.3fs). Skipping fetch.",
                        wait,
                        KILLSTATS_ZKB_RATE_TIMEOUT,
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
                    RETRY_DELAY,
                )
                wait_time = RETRY_DELAY
            # Set the retry after time in cache
            cache.set(
                f"{__title__.upper()}_R2Z2_LAST_REQUEST_RETRY_AFTER",
                timezone.now() + timezone.timedelta(seconds=wait_time),
            )
            return True
        return False

    @classmethod
    def get_sequence_from_r2z2(cls) -> Optional["KillmailBody"]:
        """Fetches and returns a sequence ID from ZKB R2Z2 endpoint.

        Returns None if no sequence is received.
        """

        # Check rate limit before attempting to fetch
        if not cls._rate_limit():
            return None

        logger.debug("Trying to fetch sequence from ZKB R2Z2...")

        sequence = requests.get(
            ZKILLBOARD_R2Z2_SEQUENCE_URL,
            timeout=REQUESTS_TIMEOUT,
            headers={"User-Agent": USER_AGENT_TEXT},
        )

        try:
            data = sequence.json()
        except JSONDecodeError:
            logger.error("Error from ZKB R2Z2 Sequence:\n%s", sequence.text)
            return None

        # Log this request timestamp for rate limiting
        cache.set(LAST_REQUEST_KEY, timezone.now().isoformat())

        # Handle 429 Too Many Requests
        if cls._too_many_requests_delay(sequence):
            return None

        if data and "sequence" in data:
            sequence_id = data["sequence"]
            logger.debug("Received sequence from ZKB R2Z2: %s", sequence_id)
            return sequence_id

        logger.debug("Did not received a sequence from ZKB R2Z2")
        return None

    # pylint: disable=too-many-return-statements
    @classmethod
    def create_from_r2z2_sequence(cls, sequence_id: int) -> Optional["KillmailBody"]:
        """Fetches killmail data from ZKB R2Z2 using the provided sequence ID, creates a KillmailBody object, and returns it.

        Returns None if no killmail data is received or if the killmail cannot be created.
        """
        if not cls._rate_limit():
            return None

        if not cache.get(f"{__title__.upper()}_WORKER_SHUTDOWN") is None:
            logger.debug("Worker shutdown detected; stopping zKB RedisQ processing")
            return None

        logger.debug("Trying to fetch killmail from ZKB R2Z2...")

        # Log this request timestamp for rate limiting
        cache.set(LAST_REQUEST_KEY, timezone.now().isoformat())

        response = requests.get(
            ZKILLBOARD_R2Z2_URL + str(sequence_id) + ".json",
            timeout=REQUESTS_TIMEOUT,
            headers={"User-Agent": USER_AGENT_TEXT},
        )

        # Handle 429 Too Many Requests
        if KillmailBody._too_many_requests_delay(response):
            return None

        if response.status_code == HTTPStatus.NOT_FOUND:
            logger.debug("No killmail found for sequence ID %s", sequence_id)
            return None

        try:
            data = response.json()
        except requests.JSONDecodeError:
            logger.error("Error from ZKB API:\n%s", response.text)
            return None

        if data and "killmail_id" in data:
            return cls._create_from_dict(data)
        return None

    def save(self) -> None:
        """Save this killmail to temporary storage."""
        cache.set(
            key=self._storage_key(self.id),
            value=self.asjson(),
            timeout=KILLSTATS_STORAGE_LIFETIME,
        )
        logger.debug("Cache created for %s", self.id)

    def delete(self) -> None:
        """Delete this killmail from temporary storage."""
        cache.delete(self._storage_key(self.id))

    def create_names_bulk(self, eve_ids: list):
        if len(eve_ids) > 0:
            EveEntity.objects.create_bulk_from_esi(eve_ids)
            return True
        return False

    @staticmethod
    def get_or_create_entity(eve_id: int) -> EveEntity:
        """Get or create an entity from Eve ID."""
        entity, new_entry = EveEntity.objects.get_or_create_esi(eve_id=eve_id)
        if new_entry:
            logger.debug("Killstats Manager EveName: %s added", entity.name)
        return entity

    @staticmethod
    def get_region_id(solar_system_id: int) -> int:
        """Get or create region ID from solar system ID."""
        try:
            solar_system = SolarSystem.objects.get(id=solar_system_id)
            region_id = solar_system.constellation.region
        except SolarSystem.DoesNotExist:
            return None
        return region_id.id

    def get_or_create_attackers(self, killmail, killmail_body):
        for attacker in killmail_body.attackers:
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
                ship = ItemType.objects.get(id=attacker.ship_type_id)

            Attacker.objects.get_or_create(
                killmail=killmail,
                character=character,
                corporation=corporation,
                alliance=alliance,
                defaults={
                    "ship": ship,
                    "damage_done": attacker.damage_done,
                    "final_blow": attacker.final_blow,
                    "security_status": attacker.security_status,
                    "weapon_type_id": attacker.weapon_type_id,
                },
            )
        return True

    @classmethod
    def get(cls, cache_id: int) -> "KillmailBody":
        """Fetch a killmail from temporary storage."""
        data = cache.get(key=cls._storage_key(cache_id))
        if not data:
            raise KillmailDoesNotExist(
                f"Killmail with ID {cache_id} does not exist in storage."
            )
        return cls.from_json(data)

    @classmethod
    def _storage_key(cls, cache_id: int) -> str:
        return cls._STORAGE_BASE_KEY + str(cache_id)

    @classmethod
    def from_dict(cls, data: dict) -> "KillmailBody":
        """Create new object from dictionary."""
        try:
            return from_dict(data_class=KillmailBody, data=data)
        except DaciteError as ex:
            logger.error("Failed to convert dict to %s", type(cls), exc_info=True)
            raise ex

    @classmethod
    def from_json(cls, json_str: str) -> "KillmailBody":
        """Create new object from JSON data."""
        return cls.from_dict(json.loads(json_str, cls=JSONDateTimeDecoder))

    @classmethod
    def _extract_victim_and_position(cls, killmail_data: dict):
        victim = KillmailVictim()
        position = KillmailPosition()
        if "victim" in killmail_data:
            victim_data = killmail_data["victim"]
            params = {}
            for prop in KillmailVictim.ENTITY_PROPS + ["damage_taken"]:
                if prop in victim_data:
                    params[prop] = victim_data[prop]

            victim = KillmailVictim(**params)

            if "position" in victim_data:
                position_data = victim_data["position"]
                params = {}
                for prop in ["x", "y", "z"]:
                    if prop in position_data:
                        params[prop] = position_data[prop]

                position = KillmailPosition(**params)

        return victim, position

    @classmethod
    def _extract_attackers(cls, killmail_data: dict) -> list[KillmailAttacker]:
        attackers = []
        for attacker_data in killmail_data.get("attackers", []):
            params = {}
            for prop in KillmailAttacker.ENTITY_PROPS + [
                "damage_done",
                "security_status",
            ]:
                if prop in attacker_data:
                    params[prop] = attacker_data[prop]

            if "final_blow" in attacker_data:
                params["final_blow"] = attacker_data["final_blow"]

            attackers.append(KillmailAttacker(**params))
        return attackers

    @classmethod
    def _extract_zkb(cls, package_data):
        params = {}
        for prop, mapping in (
            ("locationID", "location_id"),
            ("hash", None),
            ("fittedValue", "fitted_value"),
            ("droppedValue", "dropped_value"),
            ("destroyedValue", "destroyed_value"),
            ("totalValue", "total_value"),
            ("points", None),
            ("npc", "is_npc"),
            ("solo", "is_solo"),
            ("awox", "is_awox"),
        ):
            if prop in package_data:
                if mapping:
                    params[mapping] = package_data[prop]
                else:
                    params[prop] = package_data[prop]

        return KillmailZkb(**params)

    @classmethod
    def _create_from_dict(cls, package_data: dict) -> Optional["KillmailBody"]:
        """creates a new object from given dict.
        Needs to confirm with data structure returned from ZKB API
        """
        if not package_data:
            return None

        try:
            killmail_id = package_data["killmail_id"]
            esi_data = package_data["esi"]
            zkb = package_data["zkb"]
            killmail_time = esi_data["killmail_time"]
        except KeyError:
            logger.warning("Incomplete Response: %s", package_data)
            return None
        victim, position = cls._extract_victim_and_position(esi_data)
        attackers = cls._extract_attackers(esi_data)
        zkb = cls._extract_zkb(zkb)

        params = {
            "id": killmail_id,
            "time": parse_datetime(killmail_time),
            "victim": victim,
            "position": position,
            "attackers": attackers,
            "zkb": zkb,
        }
        if "solar_system_id" in package_data:
            params["solar_system_id"] = package_data["solar_system_id"]

        killmail = KillmailBody(**params)
        return killmail
