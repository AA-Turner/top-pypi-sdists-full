"""
Fatlinks URLs
These URLs are prefixed with `fatlinks/` and are used for FAT links management
"""

# Django
from django.urls import path

# Alliance Auth AFAT
from afat.views import fatlinks

urls = [
    # Fat links list actions
    path(
        route="",
        view=fatlinks.overview,
        name="fatlinks_overview",
    ),
    path(
        route="<int:year>/",
        view=fatlinks.overview,
        name="fatlinks_overview",
    ),
    # Fat link actions
    path(
        route="add/",
        view=fatlinks.add_fatlink,
        name="fatlinks_add_fatlink",
    ),
    path(
        route="link/create/esi-fatlink/",
        view=fatlinks.create_esi_fatlink,
        name="fatlinks_create_esi_fatlink",
    ),
    path(
        route="link/create/esi-fatlink/callback/<str:fatlink_hash>/",
        view=fatlinks.create_esi_fatlink_callback,
        name="fatlinks_create_esi_fatlink_callback",
    ),
    path(
        route="link/create/clickable-fatlink/",
        view=fatlinks.create_clickable_fatlink,
        name="fatlinks_create_clickable_fatlink",
    ),
    path(
        route="<str:fatlink_hash>/process/fatlink-name-change/",
        view=fatlinks.process_fatlink_name_change,
        name="fatlinks_process_fatlink_name_change",
    ),
    path(
        route="<str:fatlink_hash>/process/manual-fat/",
        view=fatlinks.process_manual_fat,
        name="fatlinks_process_manual_fat",
    ),
    path(
        route="<str:fatlink_hash>/details/",
        view=fatlinks.details_fatlink,
        name="fatlinks_details_fatlink",
    ),
    path(
        route="<str:fatlink_hash>/delete/",
        view=fatlinks.delete_fatlink,
        name="fatlinks_delete_fatlink",
    ),
    path(
        route="<str:fatlink_hash>/stop-esi-tracking/",
        view=fatlinks.close_esi_fatlink,
        name="fatlinks_close_esi_fatlink",
    ),
    path(
        route="<str:fatlink_hash>/re-open/",
        view=fatlinks.reopen_fatlink,
        name="fatlinks_reopen_fatlink",
    ),
    # Fat actions
    path(
        route="<str:fatlink_hash>/register/",
        view=fatlinks.add_fat,
        name="fatlinks_add_fat",
    ),
    path(
        route="<str:fatlink_hash>/fat/<int:fat_id>/delete/",
        view=fatlinks.delete_fat,
        name="fatlinks_delete_fat",
    ),
]
