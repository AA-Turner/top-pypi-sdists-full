# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.patches import string_templatelib
from contrast_vendor import structlog as logging

from . import (
    cgi_patch,
    chaining_patches,
    concurrent_futures_thread_patch,
    cs_io,
    encodings_patch,
    exec_and_eval,
    genshi_patch,
    jinja2_patch,
    # graphene_patch,  # TODO: PYT-3819 uncomment when ready
    lxml_patch,
    operator,
    os_patch,
    pathlib_patch,
    re_patch,
    str_new,
    sys_patch,
    threading_patch,
)
from .databases import (
    mysql_connector_patch,
    psycopg2_patch,
    pymysql_patch,
    sqlalchemy_patch,
    sqlite3_patch,
)
from .frameworks import (
    bottle_patches,
    django_patches,
    drf_patches,
    falcon_patches,
    flask_and_quart_patches,
    pyramid_patch,
    starlette_patches,
)
from .middleware import aiohttp, django, mod_wsgi
from .middleware.common import AppInterfaceType, CommonMiddlewarePatch

logger = logging.getLogger("contrast")

COMMON_PATCH_MODULES = (
    pathlib_patch,
    sqlalchemy_patch,
    sqlite3_patch,
    mysql_connector_patch,
    pymysql_patch,
    psycopg2_patch,
    concurrent_futures_thread_patch,
)


ASSESS_PATCH_MODULES = (
    operator,
    threading_patch,
    cs_io,
    encodings_patch,
    re_patch,
    exec_and_eval,
    genshi_patch,
    lxml_patch,
    pyramid_patch,
    django_patches,
    drf_patches,
    bottle_patches,
    flask_and_quart_patches,
    falcon_patches,
    sys_patch,
    cgi_patch,
    starlette_patches,
    str_new,
    string_templatelib,
    os_patch,
    jinja2_patch,
    # graphene_patch,  # TODO: PYT-3819 uncomment when ready
)


MIDDLEWARE_PATCH_MODULES = (
    django,
    mod_wsgi,
    CommonMiddlewarePatch("flask"),
    CommonMiddlewarePatch("bottle"),
    CommonMiddlewarePatch(
        "pyramid.router",
        application_class_name="Router",
        framework_name="pyramid",
    ),
    CommonMiddlewarePatch(
        "fastapi",
        application_class_name="FastAPI",
        app_interface=AppInterfaceType.ASGI,
    ),
    CommonMiddlewarePatch(
        "starlette.applications",
        application_class_name="Starlette",
        framework_name="starlette",
        app_interface=AppInterfaceType.ASGI,
    ),
    aiohttp,
    CommonMiddlewarePatch(
        "falcon",
        application_class_name="App",
        framework_name="falcon",
        app_interface=AppInterfaceType.AUTO_DETECT,
    ),
    # NOTE: falcon.asgi.App is a subclass of falcon.App. Because of this, registering
    # this patch can cause multiple middleware initializations - for this case, it
    # doesn't cause any issues. We still need this patch, since the two classes do not
    # share any code for `__call__` (only for `__init__`)
    CommonMiddlewarePatch(
        "falcon.asgi",
        application_class_name="App",
        framework_name="falcon",
        app_interface=AppInterfaceType.ASGI,
    ),
    CommonMiddlewarePatch("quart", app_interface=AppInterfaceType.ASGI),
)


def _register_module_patches(module, patch_group):
    logger.debug("registering %s patches for %s", patch_group, module.__name__)

    try:
        module.register_patches()
    except Exception:
        logger.exception("failed to register patches for %s", module.__name__)


def register_common_monkeypatches():
    for module in COMMON_PATCH_MODULES:
        _register_module_patches(module, "common")


def register_assess_monkeypatches():
    for module in ASSESS_PATCH_MODULES:
        _register_module_patches(module, "assess")


def register_automatic_middleware_monkeypatches():
    for module in MIDDLEWARE_PATCH_MODULES:
        _register_module_patches(module, "middleware")


def register_chaining_monkeypatches():
    """
    Register patches to support chaining with other runners.

    Currently supports runners that use os.execl and PYTHONOPATH manipulation for
    sitecustomize loading.
    """
    chaining_patches.register_patches()
