from fastapi import FastAPI

from csrd.versioning import (
    UNVERSIONED,
    VersionedApiConfig,
    VersionedAppComposeConfig,
    compose_versioned_apps,
)

from .settings import settings
from .views import app as unversioned_app


def build_app() -> FastAPI:
    app = compose_versioned_apps(
        version_mapping={UNVERSIONED: unversioned_app},
        config=VersionedAppComposeConfig(
            title="{{ cookiecutter.service_name }}",
            app_state={"settings": settings},
            api=VersionedApiConfig(
                prefix="/",
                app_name=settings.app_name,
                include_actuator_endpoints=settings.include_actuator_endpoints,
            ),
        ),
    )
    return app


__all__ = ("build_app",)
