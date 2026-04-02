"""
URL patterns for the logs
These URLs are prefixed with `logs/`
"""

# Django
from django.urls import path

# Alliance Auth AFAT
from afat.views import logs

urls = [path(route="", view=logs.overview, name="logs_overview")]
