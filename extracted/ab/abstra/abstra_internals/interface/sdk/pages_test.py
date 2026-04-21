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
