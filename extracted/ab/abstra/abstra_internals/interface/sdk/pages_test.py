"""Regression tests for the pages SDK import surface.

Motivated by a customer report on version 3.30.20:
    ImportError: cannot import name 'register_function' from
    'abstra_internals.interface.sdk.pages'

Tests assert that every name advertised in __all__ is importable both
from abstra.pages (the public entrypoint) and from the internal module.
They also cover subprocess imports, which is how the executor loads
user code -- a fresh interpreter is the scenario closest to what the
customer hit.
"""

import os
import subprocess
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from abstra_internals.interface.sdk import pages as internal_pages

_PUBLIC_NAMES = ("register_function", "register_static", "get_user", "get_query_params")


def _subprocess_env():
    """Force subprocesses to resolve `abstra` / `abstra_internals` from this
    working tree rather than from site-packages, so tests exercise the
    code under review instead of the published wheel."""
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
    return env


class TestPagesImportSurface(TestCase):
    def test_all_declares_expected_names(self):
        self.assertEqual(set(internal_pages.__all__), set(_PUBLIC_NAMES))

    def test_internal_module_exposes_all_public_names(self):
        for name in _PUBLIC_NAMES:
            self.assertTrue(
                hasattr(internal_pages, name),
                f"abstra_internals.interface.sdk.pages.{name} is missing",
            )
            self.assertTrue(
                callable(getattr(internal_pages, name)),
                f"abstra_internals.interface.sdk.pages.{name} is not callable",
            )

    def test_public_abstra_pages_reexports_all_names(self):
        import abstra.pages as public_pages

        for name in _PUBLIC_NAMES:
            self.assertTrue(
                hasattr(public_pages, name),
                f"abstra.pages.{name} is missing",
            )
            self.assertIs(
                getattr(public_pages, name),
                getattr(internal_pages, name),
                f"abstra.pages.{name} is not the same object as the internal one",
            )

    def test_from_import_in_fresh_interpreter(self):
        """Reproduce the customer scenario: import from a clean process.

        The customer ran `abstra editor`, which spawns executor subprocesses
        that load user code in a fresh interpreter. If the module's top-level
        code raises during import, Python leaves a partially-initialized
        module in sys.modules and the `from X import Y` statement fails with
        exactly the message the customer reported.
        """
        for name in _PUBLIC_NAMES:
            with self.subTest(name=name):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        f"from abstra_internals.interface.sdk.pages import {name}",
                    ],
                    capture_output=True,
                    text=True,
                    env=_subprocess_env(),
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    f"import of {name} failed:\nstdout={result.stdout}\nstderr={result.stderr}",
                )

    def test_from_abstra_pages_import_in_fresh_interpreter(self):
        for name in _PUBLIC_NAMES:
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, "-c", f"from abstra.pages import {name}"],
                    capture_output=True,
                    text=True,
                    env=_subprocess_env(),
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    f"import of {name} failed:\nstdout={result.stdout}\nstderr={result.stderr}",
                )

    def test_import_survives_missing_transport_dependencies(self):
        """Reproduces the 3.30.20 regression.

        In 3.30.20, importing abstra.pages transitively loaded producer.py,
        which loaded nats_connection.py, which imported `nats`. If any link
        in that chain fails at import time (missing wheel, version skew,
        corrupted install), the user sees:

            ImportError: cannot import name 'register_function' from
            'abstra_internals.interface.sdk.pages'

        Users of the pages SDK should not pay the cost of the entire
        execution/transport stack at import time. This test forces `nats`
        and `pika` to look missing and asserts the import still succeeds.
        """
        script = r"""
import builtins, sys
_real_import = builtins.__import__
_BLOCKED = ("nats", "pika")
def _import(name, *a, **kw):
    top = name.split(".", 1)[0]
    if top in _BLOCKED:
        raise ModuleNotFoundError(f"No module named '{name}' (simulated)")
    return _real_import(name, *a, **kw)
builtins.__import__ = _import
from abstra.pages import register_function, register_static, get_user, get_query_params
print("OK")
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            env=_subprocess_env(),
        )
        self.assertEqual(
            result.returncode,
            0,
            "abstra.pages must be importable without transport deps.\n"
            f"stdout={result.stdout}\nstderr={result.stderr}",
        )
        self.assertIn("OK", result.stdout)


class TestRegisterFunctionCacheDecorator(TestCase):
    """The cache= kwarg on register_function lets the generated JS stub cache
    results in memory for N seconds. Validation runs at decoration time so
    misconfigured pages fail fast at import, not on first browser call."""

    def _patched_sdk(self):
        # The public register_function calls _get_page_sdk() which expects an
        # active SDKContext. Tests patch it to a MagicMock so we can exercise
        # validation and attribute-setting without standing up a full context.
        sdk_mock = MagicMock()
        sdk_mock.register_function.side_effect = lambda f: f
        return patch.object(internal_pages, "_get_page_sdk", return_value=sdk_mock)

    def test_bare_decorator_still_works(self):
        with self._patched_sdk():

            @internal_pages.register_function
            def get_data():
                return None

            self.assertFalse(hasattr(get_data, "_abstra_cache_ttl"))

    def test_cache_kwarg_sets_ttl_attribute(self):
        with self._patched_sdk():

            @internal_pages.register_function(cache=60)
            def get_data():
                return None

            self.assertEqual(get_data._abstra_cache_ttl, 60.0)  # type: ignore[attr-defined]

    def test_cache_accepts_float(self):
        with self._patched_sdk():

            @internal_pages.register_function(cache=0.5)
            def get_data():
                return None

            self.assertEqual(get_data._abstra_cache_ttl, 0.5)  # type: ignore[attr-defined]

    def test_cache_negative_rejected(self):
        with self.assertRaises(ValueError):
            internal_pages.register_function(cache=-1)

    def test_cache_zero_rejected(self):
        with self.assertRaises(ValueError):
            internal_pages.register_function(cache=0)

    def test_cache_inf_rejected(self):
        with self.assertRaises(ValueError):
            internal_pages.register_function(cache=float("inf"))

    def test_cache_nan_rejected(self):
        with self.assertRaises(ValueError):
            internal_pages.register_function(cache=float("nan"))

    def test_cache_bool_rejected(self):
        # bool is a subclass of int; reject explicitly so cache=True doesn't
        # silently become "cache for 1 second".
        with self.assertRaises(TypeError):
            internal_pages.register_function(cache=True)
        with self.assertRaises(TypeError):
            internal_pages.register_function(cache=False)

    def test_cache_string_rejected(self):
        with self.assertRaises(TypeError):
            internal_pages.register_function(cache="60")  # type: ignore[arg-type]

    def test_cache_on_generator_rejected(self):
        with self._patched_sdk():
            with self.assertRaises(ValueError) as cm:

                @internal_pages.register_function(cache=60)
                def stream_data():
                    yield 1

            self.assertIn("generator", str(cm.exception).lower())

    def test_cache_on_render_rejected(self):
        with self._patched_sdk():
            with self.assertRaises(ValueError) as cm:

                @internal_pages.register_function(cache=60)
                def __render__():
                    return "<h1>Hi</h1>"

            self.assertIn("__render__", str(cm.exception))

    def test_register_function_passes_through_to_sdk(self):
        # The decorator must still call sdk.register_function so the function
        # is actually registered for dispatch — not just decorated.
        sdk_mock = MagicMock()
        sdk_mock.register_function.side_effect = lambda f: f
        with patch.object(internal_pages, "_get_page_sdk", return_value=sdk_mock):

            @internal_pages.register_function(cache=60)
            def get_data():
                return None

            sdk_mock.register_function.assert_called_once_with(get_data)
