# Django libraries
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
# 3rd party libraries
from graphene_django.views import GraphQLView
# Standard/core python libraries
# Our custom libraries
from .api import schema

# GENERAL URLS name_version
urlpatterns = [
    url(r'^', csrf_exempt(GraphQLView.as_view(
        graphiql=settings.DEBUG, schema=schema))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
