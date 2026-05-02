# Django libraries
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# 3rd party libraries
# Standard/core python libraries
# Our custom libraries (Managed by SPRINGLABS_DJANGO)
from .users import views as users_views

# name_version PATTERNS (Managed by SPRINGLABS_DJANGO)
# START USERS URLS name_version (Managed by SPRINGLABS_DJANGO)
users_patterns = [
    # USERS URLS (Managed by SPRINGLABS_DJANGO)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# END USERS URLS name_version (Managed by SPRINGLABS_DJANGO)

# PUBLIC URLS name_version
public_urls = [
    # PATTERNS URLS (Managed by SPRINGLABS_DJANGO)
    url(r'^', include(users_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
