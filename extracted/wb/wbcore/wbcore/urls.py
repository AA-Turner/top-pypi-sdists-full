from django.urls import include, path
from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet

from wbcore.cache.views import clear_cache
from wbcore.contrib.dynamic_preferences.viewsets import UserPreferencesViewSet
from wbcore.shares.views import ShareAPIView

from .configs.views import ConfigAPIView
from .crontab.viewsets import CrontabScheduleRepresentationViewSet
from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .markdown.views import (
    AssetCreateView,
    AssetRetrieveView,
    TemplateTagView,
)
from .menus.views import MenuAPIView
from .metadata.configs.display.views import PresetAPIView
from .release_notes.viewsets import ReleaseNoteReadOnlyModelViewSet
from .reversion.viewsets.viewsets import (
    RevisionModelViewSet,
    RevisionRepresentationViewSet,
    VersionModelViewSet,
    VersionRepresentationViewSet,
    VersionRevisionModelViewSet,
)
from .routers import WBCoreRouter
from .views import Profile

router = WBCoreRouter()
router.register(
    r"frontenduserconfiguration",
    FrontendUserConfigurationModelViewSet,
    basename="frontenduserconfiguration",
)
router.register(r"global_preferences", GlobalPreferencesViewSet, basename="global_preferences")
router.register(r"user_preferences", UserPreferencesViewSet, basename="user_preferences")

router.register(r"version", VersionModelViewSet, basename="version")
router.register(r"revision", RevisionModelViewSet, basename="revision")
router.register(r"revisionrepresentation", RevisionRepresentationViewSet, basename="revisionrepresentation")
router.register(r"versionrepresentation", VersionRepresentationViewSet, basename="versionrepresentation")
router.register(r"releasenote", ReleaseNoteReadOnlyModelViewSet, basename="releasenote")

router.register(
    r"crontabschedulerepresentation", CrontabScheduleRepresentationViewSet, basename="crontabschedulerepresentation"
)

revision_router = WBCoreRouter()
revision_router.register(r"version", VersionRevisionModelViewSet, basename="revision-version")


urlpatterns = [
    path("config/", ConfigAPIView.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", MenuAPIView.as_view(), name="menu"),
    path("preset/<str:display_identifier_path>/", PresetAPIView.as_view(), name="preset"),
    path("share/", ShareAPIView.as_view(), name="share"),
    path("markdown/asset/", AssetCreateView.as_view(), name="markdown-asset-upload"),
    path("markdown/asset/<uuid>/", AssetRetrieveView.as_view(), name="asset-retrieve"),
    path("markdown/templatetag/", TemplateTagView.as_view(), name="markdown-tags"),
    path("", include(router.urls)),
    path("revision/<int:revision_id>/", include(revision_router.urls)),
    path(
        "authentication/",
        include(("wbcore.contrib.authentication.urls", "wbcore.contrib.authentication"), namespace="authentication"),
    ),
    path(
        "content_type/",
        include(("wbcore.contrib.content_type.urls", "wbcore.contrib.content_type"), namespace="content_type"),
    ),
    path(
        "notifications/",
        include(("wbcore.contrib.notifications.urls", "wbcore.contrib.notifications"), namespace="notifications"),
    ),
    path(
        "io/",
        include(("wbcore.contrib.io.urls", "wbcore.contrib.io"), namespace="io"),
    ),
    path(
        "geography/",
        include(("wbcore.contrib.geography.urls", "wbcore.contrib.geography"), namespace="geography"),
    ),
    path(
        "currency/",
        include(("wbcore.contrib.currency.urls", "wbcore.contrib.currency"), namespace="currency"),
    ),
    path(
        "tags/",
        include(("wbcore.contrib.tags.urls", "wbcore.contrib.tags"), namespace="tags"),
    ),
    path(
        "documents/",
        include(("wbcore.contrib.documents.urls", "wbcore.contrib.documents"), namespace="documents"),
    ),
    path(
        "directory/",
        include(("wbcore.contrib.directory.urls", "wbcore.contrib.directory"), namespace="directory"),
    ),
    path(
        "agenda/",
        include(("wbcore.contrib.agenda.urls", "wbcore.contrib.agenda"), namespace="agenda"),
    ),
    path(
        "workflow/",
        include(("wbcore.contrib.workflow.urls", "wbcore.contrib.workflow"), namespace="workflow"),
    ),
    path(
        "guardian/",
        include(("wbcore.contrib.guardian.urls", "wbcore.contrib.guardian"), namespace="guardian"),
    ),
    path("clear_cache/<str:cache_key>/", clear_cache, name="clear_cache"),
]
