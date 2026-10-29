from django.urls import include, path

from allianceauth.authentication.decorators import decorate_url_patterns
from allianceauth.hooks import get_hooks
from allianceauth.impersonate.decorators import not_while_impersonating

from . import views

urlpatterns = [
    # Services
    path('services/', include(([
        path('', views.services_view, name='services'),
        # Tools
        path('tool/fleet_formatter_tool/', views.fleet_formatter_view, name='fleet_format_tool'),
    ], 'services'), namespace='services')),
]

# Append hooked service urls
# Blocked while impersonating, so the impersonator's external accounts can't be bound to the impersonated user
services = get_hooks('services_hook')
for svc in services:
    urlpatterns += [path('', decorate_url_patterns(svc().urlpatterns, not_while_impersonating))]
