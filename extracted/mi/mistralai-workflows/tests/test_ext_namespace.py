"""
Test suite for the mistralai.workflows.plugins namespace package functionality.

This module tests the PEP 420 namespace package implementation that allows
external packages to extend the mistralai.workflows.plugins namespace without requiring
a central registration or modification of the core workflows package.
"""

import importlib
import pkgutil
from pathlib import Path
from unittest.mock import MagicMock, patch

from mistralai.workflows.plugins._discovery import PLUGIN_NAMESPACE

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent.parent


class TestContribNamespace:
    def test_ext_is_namespace_package(self):
        """
        Verify mistralai.workflows.plugins is a PEP 420 namespace package.
        """
        ext_module = importlib.import_module(PLUGIN_NAMESPACE)
        assert ext_module.__file__ is None, "__file__ should be None for PEP420 modules"
        assert ext_module.__path__ is not None, "__path__ should not be None for PEP420 modules"

    def test_contribution_can_extend_namespace(self, tmp_path):
        test_module_name = "_test_module_name"

        external_ext_dir = tmp_path / "plugins"
        external_ext_dir.mkdir()
        external_pkg = external_ext_dir / test_module_name
        external_pkg.mkdir()
        (external_pkg / "__init__.py").write_text("CONTRIBUTED = True\n")

        ext_module = importlib.import_module(PLUGIN_NAMESPACE)
        original_path = list(ext_module.__path__)

        try:
            # FAKE: Manually extend namespace __path__ (normally done by pip/uv at install time)
            ext_module.__path__.append(str(external_ext_dir))

            from mistralai.workflows.plugins._discovery import list_plugins

            plugins = {c.name for c in list_plugins()}
            assert test_module_name in plugins

        finally:
            ext_module.__path__[:] = original_path

    def test_list_contributions(self):
        fake_distributions = {
            "mistralai.workflows.plugins.foo": ["workflows-plugins-foo"],
            "mistralai.workflows.plugins.bar": ["workflows-plugins-bar"],
        }

        fake_modules = [
            pkgutil.ModuleInfo(MagicMock(), "foo", True),
            pkgutil.ModuleInfo(MagicMock(), "bar", True),
            pkgutil.ModuleInfo(MagicMock(), "_discovery", True),  # SELF, should be excluded
        ]

        fake_versions = {
            "workflows-plugins-foo": "1.0.0",
            "workflows-plugins-bar": "2.3.1",
        }

        with (
            patch("importlib.metadata.packages_distributions", return_value=fake_distributions),
            patch("importlib.metadata.version", side_effect=lambda name: fake_versions[name]),
            patch("pkgutil.iter_modules", return_value=fake_modules),
        ):
            import mistralai.workflows.plugins._discovery

            importlib.reload(mistralai.workflows.plugins._discovery)

            plugins = mistralai.workflows.plugins._discovery.list_plugins()

            assert len(plugins) == 2

            foo = next(r for r in plugins if r.name == "foo")
            assert foo.dist_name == "workflows-plugins-foo"
            assert foo.dist_version == "1.0.0"
            assert foo.ispkg is True

            bar = next(r for r in plugins if r.name == "bar")
            assert bar.dist_name == "workflows-plugins-bar"
            assert bar.dist_version == "2.3.1"
            assert bar.ispkg is True
