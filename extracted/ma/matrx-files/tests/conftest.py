"""Pytest configuration for matrx-utils tests.

``cloud_sync_test.py`` is a manual, live-credential integration script (it talks
to real AWS S3 + Supabase as the test admin (``TEST_ADMIN_USER_ID`` from ``.env``) and is meant
to be run with ``python tests/cloud_sync_test.py``). Its ``test_*`` functions
take an ``engine`` argument that pytest would try — and fail — to resolve as a
fixture. It is intentionally excluded from automated collection so the unit
suite stays green without cloud credentials; run it by hand when validating the
cloud-sync round-trip.
"""

collect_ignore = ["cloud_sync_test.py", "load_env_for_test.py"]

import types

import pytest


@pytest.fixture(autouse=True)
def _base_dir_settings(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Point ``matrx_utils.conf.settings.BASE_DIR`` at an isolated ``tmp_path``
    for every test via the sanctioned ``configure_settings`` mechanism.

    BASE_DIR is config, not an environment variable — matrx_utils no longer
    reads a ``BASE_DIR`` env var at all (see repo CLAUDE.md doctrine). Tests
    that previously did ``monkeypatch.setenv("BASE_DIR", str(tmp_path))`` now
    get isolation by monkeypatching the settings singleton directly instead;
    ``monkeypatch`` restores the original attributes after the test, so this
    never leaks between tests or requires calling the (non-reentrant)
    ``configure_settings()`` function itself.

    Only ``BASE_DIR``/``TEMP_DIR`` are stubbed — every other setting (AWS/S3
    keys, etc.) still falls through to the real environment exactly as
    before, since ``LazySettings.__getattr__`` catches ``AttributeError`` on
    the stub object and re-checks the environment for any name other than
    BASE_DIR.
    """
    from matrx_utils.conf import settings

    stub = types.SimpleNamespace(
        BASE_DIR=tmp_path,
        TEMP_DIR=tmp_path / "temp",
        DEBUG=False,
    )
    monkeypatch.setattr(settings, "_settings_object", stub, raising=False)
    monkeypatch.setattr(settings, "_configured", True, raising=False)


@pytest.fixture(autouse=True)
def _request_context_never_leaks_between_tests():
    """Restore ``matrx_utils.ctx``'s host seam after every test.

    The package READS the organization off the active request context and
    REFUSES a write when there is none, so a context getter left installed by
    one test would silently supply a tenant to the next one — exactly the class
    of silent mis-tenanting this suite exists to catch.
    """
    from matrx_utils import ctx as matrx_ctx

    previous = matrx_ctx._context_getter
    try:
        yield
    finally:
        matrx_ctx._context_getter = previous
