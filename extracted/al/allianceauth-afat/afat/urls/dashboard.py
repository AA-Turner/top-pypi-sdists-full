"""
URL patterns for the dashboard
"""

# Django
from django.urls import path

# Alliance Auth AFAT
from afat.views import dashboard

urls = [path(route="", view=dashboard.overview, name="dashboard")]
