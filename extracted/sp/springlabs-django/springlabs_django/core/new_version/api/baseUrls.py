# Django libraries
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# 3rd party libraries
# Standard/core python libraries
# Our custom libraries
from .private_urls import private_urls
from .public_urls import public_urls
from core.customDocumentation import include_docs_urls
from core.documentation import (
    title_name_version_0,
    description_name_version_0,
    namespace_name_version_0,
    urls_name_version_0,
    title_name_version_0_private,
    description_name_version_0_private,
    namespace_name_version_0_private,
    urls_name_version_0_private,
)

# PUBLIC URLS name_version
urls_name_version_0 = [
    url(r'^name_version/', include(public_urls)),
]
# PRIVATE URLS name_version
urls_name_version_0_private = [
    url(r'^name_version/', include(private_urls)),
]

# DOCUMENTATION URLS name_version
doc_patterns = [
    url(r'^', include_docs_urls(title=title_name_version_0,
        patterns=urls_name_version_0,
        description=description_name_version_0,
        namespace=namespace_name_version_0)),
    url(r'^private', include_docs_urls(title=title_name_version_0_private,
        patterns=urls_name_version_0_private,
        description=description_name_version_0_private,
        namespace=namespace_name_version_0_private)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# GENERAL URLS name_version
urlpatterns = [
    url(r'^', include(doc_patterns)),
    url(r'^', include(public_urls)),
    url(r'^', include(private_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
