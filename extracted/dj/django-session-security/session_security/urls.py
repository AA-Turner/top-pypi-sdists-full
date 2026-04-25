"""
One url meant to be used by JavaScript.

session_security_ping
    Connects the PingView.

To install this url, include it in ``urlpatterns`` in your ``urls.py``::

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('session_security/', include('session_security.urls')),
        # ...
    ]

"""
from django.urls import path

from .views import PingView

urlpatterns = [
    path('ping/', PingView.as_view(), name='session_security_ping'),
]
