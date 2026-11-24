"""App URLs"""

# Django
from django.urls import path, re_path

# Alliance Auth
from allianceauth.authentication.decorators import decorate_url_patterns

# AA Killstats
from killstats import views
from killstats.api import api
from killstats.api.auth import basic_access_required

app_name: str = "killstats"  # pylint: disable=invalid-name

# Every URL of the API (endpoints, schema and docs) requires `basic_access`
api_patterns, api_app_name, api_namespace = api.urls
api_patterns = decorate_url_patterns(
    (api_patterns, api_app_name), basic_access_required
)[0]

urlpatterns = [
    # -- API System (excluded from catch-all)
    re_path(r"^api/", (api_patterns, api_app_name, api_namespace)),
    # -- Killstats Audit
    path("add_corp/", views.add_corp, name="add_corp"),
    path("add_alliance/", views.add_alliance, name="add_alliance"),
    # -- Named SPA Routes for direct redirects
    path("corporation/<int:entity_id>/", views.react_base, name="corporation"),
    path("alliance/<int:entity_id>/", views.react_base, name="alliance"),
    # -- React Frontend (V2)
    re_path(
        r"^(?!api/|add_corp|add_alliance).*$",
        views.react_base,
        name="react_base",
    ),
]
