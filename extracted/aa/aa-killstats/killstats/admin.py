"""Admin models"""

# Third Party
from django_redis import get_redis_connection

# Django
from django.contrib import admin
from django.utils.html import format_html

# Alliance Auth
from allianceauth.eveonline.evelinks import eveimageserver
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


@admin.register(CorporationsAudit)
class CorporationsAuditAdmin(admin.ModelAdmin):
    list_display = (
        "_entity_pic",
        "_corporation__corporation_id",
        "_last_update",
    )

    list_display_links = (
        "_entity_pic",
        "_corporation__corporation_id",
    )

    list_select_related = ("corporation",)

    ordering = ["corporation__corporation_name"]

    search_fields = ["corporation__corporation_name", "corporation__corporation_id"]

    actions = ["delete_objects", "clear_cache_for_selected"]

    @admin.display(description="")
    def _entity_pic(self, obj: CorporationsAudit):
        eve_id = obj.corporation.corporation_id
        return format_html(
            '<img src="{}" class="img-circle">',
            eveimageserver._eve_entity_image_url("corporation", eve_id, 32),
        )

    @admin.display(description="Corporation ID", ordering="corporation__corporation_id")
    def _corporation__corporation_id(self, obj: CorporationsAudit):
        return obj.corporation.corporation_id

    @admin.display(description="Last Update", ordering="last_update")
    def _last_update(self, obj: CorporationsAudit):
        return obj.last_update

    # pylint: disable=unused-argument
    def has_add_permission(self, request):
        return False

    # pylint: disable=unused-argument
    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description="Clear cache for selected Corporations")
    def clear_cache_for_selected(self, request, queryset: CorporationsAudit):
        for obj in queryset:
            clear_cache_zkb(obj.corporation.corporation_id)
            logger.debug("Clearing cache for selected Corporations %s", obj.corporation)
        self.message_user(
            request, "Cache successfully cleared for selected Corporations."
        )


@admin.register(AlliancesAudit)
class AlliancesAuditAdmin(admin.ModelAdmin):
    list_display = (
        "_entity_pic",
        "_alliance__alliance_id",
        "_last_update",
    )

    list_display_links = (
        "_entity_pic",
        "_alliance__alliance_id",
    )

    list_select_related = ("alliance",)

    ordering = ["alliance__alliance_name"]

    search_fields = ["alliance__alliance_name", "alliance__alliance_id"]

    actions = ["delete_objects", "clear_cache_for_selected"]

    @admin.display(description="")
    def _entity_pic(self, obj: AlliancesAudit):
        eve_id = obj.alliance.alliance_id
        return format_html(
            '<img src="{}" class="img-circle">',
            eveimageserver._eve_entity_image_url("alliance", eve_id, 32),
        )

    @admin.display(description="Alliance ID", ordering="alliance__alliance_id")
    def _alliance__alliance_id(self, obj: AlliancesAudit):
        return obj.alliance.alliance_id

    @admin.display(description="Last Update", ordering="last_update")
    def _last_update(self, obj: AlliancesAudit):
        return obj.last_update

    # pylint: disable=unused-argument
    def has_add_permission(self, request):
        return False

    # pylint: disable=unused-argument
    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description="Clear cache for selected Alliances")
    def clear_cache_for_selected(self, request, queryset: AlliancesAudit):
        for obj in queryset:
            clear_alliance_cache_zkb(obj.alliance.alliance_id)
            logger.debug("Clearing cache for selected Alliances %s", obj.alliance)
        self.message_user(request, "Cache successfully cleared for selected Alliances.")


def clear_cache_zkb(corporation_id: int):
    conn = get_redis_connection("default")
    for key in conn.scan_iter(
        f"*:zkb_page_cache_https://zkillboard.com/api/npc/0/corporationID/{corporation_id}*"
    ):
        conn.delete(key)
        logger.debug("Deleting key %s", key)
    return True


def clear_alliance_cache_zkb(alliance_id: int):
    conn = get_redis_connection("default")
    for key in conn.scan_iter(
        f"*:zkb_page_cache_https://zkillboard.com/api/npc/0/allianceID/{alliance_id}*"
    ):
        conn.delete(key)
        logger.debug("Deleting key %s", key)
    return True
