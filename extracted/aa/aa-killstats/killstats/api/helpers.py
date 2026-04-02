# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__, models
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


# NOTE: not implemented yet
def get_permission(request, entity_type: str):  # pragma: no cover
    """Get permission for the entity"""
    if entity_type == "corporation":
        entities = get_corporations(request)
    else:
        entities = get_alliances(request)

    if not entities:
        output = [{"No Data": "No data available for the entity"}]
        return False, output
    return True, entities


def get_corporations(request):
    linked_characters = request.user.profile.main_character.character_ownership.user.character_ownerships.select_related(
        "character", "user"
    ).all()

    linked_characters = linked_characters.values_list("character_id", flat=True)
    chars = EveCharacter.objects.filter(id__in=linked_characters)

    # Get all corporations and ensure they are not NPC corporations
    corporations = (
        chars.filter(corporation_id__gt=10_000_000)
        .values_list("corporation_id", flat=True)
        .distinct()
    )

    main_corp = models.CorporationsAudit.objects.filter(
        corporation__corporation_id__in=corporations
    )

    # Check access
    visible = models.CorporationsAudit.objects.visible_to(request.user)

    common_corps = main_corp.intersection(visible)
    if not common_corps.exists():
        return []

    return list(corporations)


def get_alliances(request):
    linked_characters = request.user.profile.main_character.character_ownership.user.character_ownerships.select_related(
        "character", "user"
    ).all()

    linked_characters = linked_characters.values_list("character_id", flat=True)
    chars = EveCharacter.objects.filter(id__in=linked_characters)

    alliances = chars.values_list("alliance_id", flat=True).distinct()

    main_corp = models.AlliancesAudit.objects.filter(
        alliance__alliance_id__in=alliances
    )

    # Check access
    visible = models.AlliancesAudit.objects.visible_to(request.user)

    common_corps = main_corp.intersection(visible)

    if not common_corps.exists():
        return []

    return list(alliances)
