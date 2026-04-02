"""
URLs for AJAX calls
These URLs are used for AJAX calls and are prefixed with `{INTERNAL_URL_PREFIX}/ajax/`
"""

# Django
from django.urls import path

# Alliance Auth AFAT
from afat.views import dashboard, datatables, fatlinks, statistics

urls = [
    # Ajax calls :: Dashboard
    path(
        route="dashboard/get-recent-fatlinks/",
        view=dashboard.ajax_get_recent_fatlinks,
        name="dashboard_ajax_get_recent_fatlinks",
    ),
    path(
        route="dashboard/get-recent-fats-by-character/<int:charid>/",
        view=dashboard.ajax_recent_get_fats_by_character,
        name="dashboard_ajax_get_recent_fats_by_character",
    ),
    # Ajax calls :: Fat links
    path(
        route="fatlinks/get-fatlinks-by-year/<int:year>/",
        view=datatables.FatLinksTableView.as_view(),
        name="fatlinks_ajax_get_fatlinks_by_year",
    ),
    path(
        route="fatlinks/get-fats-by-fatlink/<str:fatlink_hash>/",
        view=fatlinks.ajax_get_fats_by_fatlink,
        name="fatlinks_ajax_get_fats_by_fatlink",
    ),
    # Ajax calls :: Logs
    path(
        route="logs/get-logs/",
        view=datatables.LogsTableView.as_view(),
        name="logs_ajax_get_logs",
    ),
    # Ajax calls :: Statistics
    path(
        route="statistics/get-monthly-fats-for-main-character/<int:corporation_id>/<int:character_id>/<int:year>/<int:month>/",
        view=statistics.ajax_get_monthly_fats_for_main_character,
        name="statistics_ajax_get_monthly_fats_for_main_character",
    ),
]
