from django.urls import include, path

from allianceauth import urls

# Alliance auth urls
urlpatterns = [
    path("", include(urls)),
]
