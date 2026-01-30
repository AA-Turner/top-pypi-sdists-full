from django.urls import include, path

from wbcore.contrib.permission.viewsets import PivotUserObjectPermissionModelViewSet
from wbcore.routers import WBCoreRouter

router = WBCoreRouter()
router.register(
    r"pivoteduserobjectpermission", PivotUserObjectPermissionModelViewSet, basename="pivoteduserobjectpermission"
)

urlpatterns = [
    path("<int:content_type_id>/<int:object_pk>/", include(router.urls)),
]
