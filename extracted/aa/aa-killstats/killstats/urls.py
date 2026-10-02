"""App URLs"""

# Django
from django.urls import path, re_path

# AA Killstats
from killstats import views
from killstats.api import api

app_name: str = "killstats"  # pylint: disable=invalid-name

urlpatterns = [
    # -- API System (excluded from catch-all)
    re_path(r"^api/", api.urls),
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
