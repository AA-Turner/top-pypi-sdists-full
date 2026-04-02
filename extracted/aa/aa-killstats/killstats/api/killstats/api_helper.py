# Standard Library
import hashlib

# Django
from django.core.cache import cache
from django.db.models import Count, Q, Sum

# Alliance Auth
from allianceauth.services.hooks import ObjectDoesNotExist, get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.api.account_manager import AccountManager
from killstats.api.helpers import get_alliances, get_corporations
from killstats.app_settings import KILLSTATS_API_CACHE_LIFETIME
from killstats.models.killboard import Attacker, Killmail
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)

KILLMAIL_MAPPING = {
    0: "killmail_id",
    1: "victim_ship__name",
    2: "victim",
    3: "victim__name",
    4: "victim_total_value",
    5: "killmail_date",
}


def set_cache_key(cache_key, output, timeout=KILLSTATS_API_CACHE_LIFETIME):
    if not cache_key:
        return False

    logger.debug("Cache Set: %s", cache_key)
    cache.set(
        key=cache_key,
        value=output,
        timeout=60 * timeout,
    )
    return True


def cache_sytem(request, cache_name, entity_id) -> tuple:
    cache_id = get_unique_id(request, entity_id)

    cache_key = f"{cache_name}_{cache_id}"
    output = cache.get(cache_key)

    if output is not None:
        logger.debug("Cache hit: %s", cache_key)
        return output, None
    return None, cache_key


def get_unique_id(request, entity_id) -> str:
    if entity_id != 0:
        return entity_id

    corp = get_corporations(request)
    ally = get_alliances(request)
    corp_ids = CorporationsAudit.objects.filter(
        corporation__corporation_id__in=corp
    ).values_list("corporation__corporation_id", flat=True)
    ally_ids = AlliancesAudit.objects.filter(
        alliance__alliance_id__in=ally
    ).values_list("alliance__alliance_id", flat=True)
    entities = list(corp_ids) + list(ally_ids)

    # Combine all IDs into a single string
    combined_ids = "_".join(map(str, sorted(entities)))

    # Create a unique ID from the combined IDs
    unique_id = hashlib.md5(combined_ids.encode()).hexdigest()
    return unique_id


def get_entities(request, entity_type: str, entity_id: int):
    if entity_id == 0:
        if entity_type == "alliance":
            entities = get_alliances(request)
        else:
            entities = get_corporations(request)
    else:
        entities = [entity_id]
    return entities


# pylint: disable=too-many-locals, too-many-positional-arguments
def get_killmails_data(request, month, year, entity_type: str, entity_id: int, mode):
    entities = get_entities(request, entity_type, entity_id)

    # Datatables parameters
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 25))
    limit = start + length

    search_value = request.GET.get("search[value]", "")
    order_column_index = int(request.GET.get("order[0][column]", 0))
    order_dir = request.GET.get("order[0][dir]", "desc")
    order_column = KILLMAIL_MAPPING.get(order_column_index, "killmail_date")
    order_by = f"{'-' if order_dir == 'desc' else ''}{order_column}"

    killmails = (
        Killmail.objects.prefetch_related("victim", "victim_ship")
        .filter(killmail_date__year=year, killmail_date__month=month)
        .order_by(order_by)
    ).filter_entities(entities)

    if mode == "losses":
        killmails = killmails.filter_entities_losses(entities)
    else:
        killmails = killmails.filter_entities_kills(entities)

    totalvalue = (
        killmails.aggregate(totalvalue=Sum("victim_total_value"))["totalvalue"],
    )

    if search_value:
        killmails = killmails.filter(
            Q(victim__name__icontains=search_value)
            | Q(victim_ship__name__icontains=search_value)
            | Q(victim_total_value__icontains=search_value)
            | Q(killmail_date__icontains=search_value)
        )

    total_count = killmails.count()
    record_count = killmails.count()
    killmails = killmails[start:limit]

    output = []
    for killmail in killmails:
        output.append(
            {
                "killmail_id": killmail.killmail_id,
                "killmail_date": killmail.killmail_date,
                "victim": {
                    "id": killmail.victim_id,
                    "name": killmail.victim.name if killmail.victim else "Unknown",
                },
                "victim_ship": {
                    "id": killmail.victim_ship_id,
                    "name": (
                        killmail.victim_ship.name if killmail.victim_ship else "Unknown"
                    ),
                },
                "victim_corporation_id": killmail.victim_corporation_id,
                "victim_alliance_id": killmail.victim_alliance_id,
                "hash": killmail.hash,
                "victim_total_value": killmail.victim_total_value,
                "victim_fitted_value": killmail.victim_fitted_value,
                "victim_destroyed_value": killmail.victim_destroyed_value,
                "victim_dropped_value": killmail.victim_dropped_value,
                "victim_region_id": killmail.victim_region_id,
                "victim_solar_system_id": killmail.victim_solar_system_id,
                "victim_position_x": killmail.victim_position_x,
                "victim_position_y": killmail.victim_position_y,
                "victim_position_z": killmail.victim_position_z,
            }
        )

    return {
        "draw": int(request.GET.get("draw", 1)),
        "recordsTotal": total_count,
        "recordsFiltered": total_count if not search_value else record_count,
        "data": output,
        "totalvalue": totalvalue,
    }


def get_killstats_halls(request, month, year, entity_type: str, entity_id: int):
    entities = get_entities(request, entity_type, entity_id)
    account = AccountManager()
    mains, _ = account.get_mains_alts()

    shame = (
        Killmail.objects.filter(
            killmail_date__year=year,
            killmail_date__month=month,
        )
        .filter(
            Q(victim_corporation_id__in=entities)
            | Q(victim_alliance_id__in=entities)
            | Q(victim_id__in=entities)
        )
        .order_by("-victim_total_value")[:5]
    )

    fame = (
        Attacker.objects.filter(
            killmail__killmail_date__year=year,
            killmail__killmail_date__month=month,
        )
        .filter(
            Q(corporation_id__in=entities)
            | Q(alliance_id__in=entities)
            | Q(character_id__in=entities)
        )
        .order_by("-killmail__victim_total_value")[:5]
    )

    shame_data = []
    fame_data = []

    for killmail in shame:
        zkillboard = killmail.evaluate_zkb_link()

        try:
            character_id = killmail.victim.id
            character_name = killmail.victim.name
            for main_id, data in mains.items():
                alts = [alt.character_id for alt in data["alts"]]
                if character_id in alts and character_id != main_id:
                    main_name = data["main"].character_name
                    # Hauptcharaktername verwenden
                    character_name = f"{character_name} ({main_name})"
                    break
        except AttributeError:
            character_id = 0
            character_name = "Unknown"

        shame_data.append(
            {
                "killmail_id": killmail.killmail_id,
                "character_id": character_id,
                "character_name": character_name,
                "ship": killmail.get_or_unknown_victim_ship_id(),
                "ship_name": killmail.get_or_unknown_victim_ship_name(),
                "totalValue": killmail.victim_total_value,
                "portrait": killmail.victim.icon_url(512),
                "zkb_link": zkillboard,
            }
        )

    for killmail in fame:
        zkillboard = killmail.killmail.evaluate_zkb_link()
        portrait = ""

        try:
            character_id = killmail.character.id
            character_name = killmail.character.name
            for main_id, data in mains.items():
                alts = [alt.character_id for alt in data["alts"]]
                if character_id in alts and character_id != main_id:
                    main_name = data["main"].character_name
                    # Hauptcharaktername verwenden
                    character_name = f"{character_name} ({main_name})"
                    portrait = killmail.character.icon_url(512)
                    break
        except (AttributeError, ObjectDoesNotExist):
            character_id = 0
            character_name = "Unknown"

        fame_data.append(
            {
                "killmail_id": killmail.killmail.killmail_id,
                "character_id": character_id,
                "character_name": character_name,
                "ship": killmail.killmail.get_or_unknown_victim_ship_id(),
                "ship_name": killmail.killmail.get_or_unknown_victim_ship_name(),
                "totalValue": killmail.killmail.victim_total_value,
                "portrait": portrait,
                "zkb_link": zkillboard,
            }
        )

    halls = []
    halls.append(
        {
            "shame": shame_data,
            "fame": fame_data,
        }
    )

    return halls


def get_top_10(request, month, year, entity_type: str, entity_id: int) -> list:
    entities = get_entities(request, entity_type, entity_id)
    account = AccountManager()
    mains_dict, _ = account.get_mains_alts()

    killmail = (
        Killmail.objects.prefetch_related("victim", "victim_ship")
        .filter(killmail_date__year=year, killmail_date__month=month)
        .order_by("-killmail_date")
    ).filter_entities(entities)

    km_ids = killmail.values_list("killmail_id", flat=True)

    top_characters = (
        Attacker.objects.filter(
            killmail__killmail_date__year=year,
            killmail__killmail_date__month=month,
            killmail_id__in=km_ids,
        )
        .filter(
            Q(corporation_id__in=entities)
            | Q(alliance_id__in=entities)
            | Q(character_id__in=entities)
        )
        .values("character_id", "character__name")
        .annotate(kill_count=Count("character_id"))
        .order_by("-kill_count", "character__name")[:10]
    )

    if not top_characters:
        return {}

    # Convert QuerySet to list
    top_10_list = list(top_characters)

    # Add character_name to each entry
    for entry in top_10_list:
        character_id = entry["character_id"]

        try:
            # Check if the character is an alt and add the main character's name
            for main_id, data in mains_dict.items():
                alts = [alt.character_id for alt in data["alts"]]
                if character_id in alts and character_id != main_id:
                    main_character = data["main"]
                    entry["character__name"] += f" ({main_character.character_name})"
                    break
        except AttributeError:
            entry["character__name"] = "Unknown"

    return top_10_list
