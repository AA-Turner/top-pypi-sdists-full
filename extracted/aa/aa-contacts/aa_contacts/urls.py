from django.urls import path, re_path

from . import views
from .api import api

app_name = "aa_contacts"


urlpatterns = [
    path("", views.index, name="index"),
    path("api/", api.urls),
    re_path("^r/", views.react_view, name="react_view"),
    path("alliance/add_token/", views.add_alliance_token, name="add_alliance_token"),
    path(
        "corporation/add_token/",
        views.add_corporation_token,
        name="add_corporation_token",
    ),
]
