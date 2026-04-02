"""Routes for Inactivity."""

from django.urls import path

from . import views

app_name = "inactivity"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_requests", views.my_requests, name="my_requests"),
    path("manage_requests", views.manage_requests, name="manage_requests"),
    path(
        "open_requests_data", views.my_open_requests_data, name="my_open_requests_data"
    ),
    path(
        "competed_requests_data",
        views.my_completed_requests_data,
        name="my_completed_requests_data",
    ),
    path(
        "loa_requests/pending",
        views.list_pending_loa_requests,
        name="list_pending_loa_requests",
    ),
    path(
        "loa_requests/approved",
        views.list_processed_loa_requests,
        name="list_processed_loa_requests",
    ),
    path("loa_requests/create", views.create_loa_request, name="create_loa_request"),
    path(
        "loa_requests/<int:loa_request_pk>/cancel",
        views.cancel_loa_request,
        name="cancel_loa_request",
    ),
    path(
        "loa_requests/<int:loa_request_pk>/approve",
        views.approve_loa_request,
        name="approve_loa_request",
    ),
    path(
        "loa_requests/<int:loa_request_pk>/reject",
        views.deny_loa_request,
        name="deny_loa_request",
    ),
    path("inactive_users", views.inactive_users, name="inactive_users"),
    path("inactive_users_data", views.inactive_users_data, name="inactive_users_data"),
]
