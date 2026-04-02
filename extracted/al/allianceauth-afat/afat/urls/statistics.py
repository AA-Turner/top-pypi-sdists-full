"""
Statistics URLs
These URLs are used for static pages and are prefixed with `static/`
"""

# Django
from django.urls import path

# Alliance Auth AFAT
from afat.views import statistics

urls = [
    # Stats main page
    path(
        route="",
        view=statistics.overview,
        name="statistics_overview",
    ),
    path(
        route="<int:year>/",
        view=statistics.overview,
        name="statistics_overview",
    ),
    # Stats corp
    path(
        route="corporation/",
        view=statistics.corporation,
        name="statistics_corporation",
    ),
    path(
        route="corporation/<int:corpid>/",
        view=statistics.corporation,
        name="statistics_corporation",
    ),
    path(
        route="corporation/<int:corpid>/<int:year>/",
        view=statistics.corporation,
        name="statistics_corporation",
    ),
    path(
        route="corporation/<int:corpid>/<int:year>/<int:month>/",
        view=statistics.corporation,
        name="statistics_corporation",
    ),
    # Stats char
    path(
        route="character/",
        view=statistics.character,
        name="statistics_character",
    ),
    path(
        route="character/<int:charid>/",
        view=statistics.character,
        name="statistics_character",
    ),
    path(
        route="character/<int:charid>/<int:year>/<int:month>/",
        view=statistics.character,
        name="statistics_character",
    ),
    # Stats alliance
    path(
        route="alliance/",
        view=statistics.alliance,
        name="statistics_alliance",
    ),
    path(
        route="alliance/<int:allianceid>/",
        view=statistics.alliance,
        name="statistics_alliance",
    ),
    path(
        route="alliance/<int:allianceid>/<int:year>/",
        view=statistics.alliance,
        name="statistics_alliance",
    ),
    path(
        route="alliance/<int:allianceid>/<int:year>/<int:month>/",
        view=statistics.alliance,
        name="statistics_alliance",
    ),
]
