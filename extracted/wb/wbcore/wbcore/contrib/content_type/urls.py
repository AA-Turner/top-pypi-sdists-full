from django.urls import include, path

from wbcore.contrib.content_type.viewsets import ContentTypeRepresentationViewSet, DynamicObjectIDRepresentationViewSet
from wbcore.routers import WBCoreRouter

router = WBCoreRouter()

router.register(r"contenttyperepresentation", ContentTypeRepresentationViewSet, basename="contenttyperepresentation")
router.register(
    r"dynamiccontenttyperepresentation",
    DynamicObjectIDRepresentationViewSet,
    basename="dynamiccontenttyperepresentation",
)

urlpatterns = [path("", include(router.urls))]
