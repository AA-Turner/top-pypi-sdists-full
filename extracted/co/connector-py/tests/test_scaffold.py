import importlib
import sys
import tempfile
from argparse import Namespace
from unittest.mock import MagicMock, patch

import pytest
from connector.scaffold.create import ScaffoldError, scaffold


class TestScaffold:
    def test_scaffold(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: ["Test Author"])
        monkeypatch.setattr("builtins.input", lambda _: ["test@test.com"])
        with tempfile.TemporaryDirectory() as tmpdirname:
            scaffold(
                Namespace(
                    directory=tmpdirname,
                    name="Test",
                    tests_only=False,
                    author_name=None,
                    author_email=None,
                )
            )

    def test_scaffold_generates_importable_modules(self, monkeypatch):
        """Scaffold + import every generated module to catch stale template imports."""
        connector_name = "scaffold_test_connector"
        with tempfile.TemporaryDirectory() as tmpdirname:
            scaffold(
                Namespace(
                    directory=tmpdirname,
                    name=connector_name,
                    tests_only=False,
                    force_overwrite=False,
                    author_name="Test Author",
                    author_email="test@test.com",
                )
            )
            sys.path.insert(0, tmpdirname)
            try:
                for module in [
                    f"{connector_name}.integration",
                    f"{connector_name}.capabilities_read",
                    f"{connector_name}.capabilities_write",
                    f"{connector_name}.client",
                    f"{connector_name}.settings",
                    f"{connector_name}.pagination",
                ]:
                    importlib.import_module(module)
                integration_mod = sys.modules[f"{connector_name}.integration"]
                info = integration_mod.integration.info()
                assert info.response.app_id == connector_name.replace("_", "-")
            finally:
                sys.path.remove(tmpdirname)
                for key in list(sys.modules):
                    if key.startswith(connector_name):
                        del sys.modules[key]

    @patch("connector.scaffold.create.TEMPLATE_DIR")
    def test_scaffold_failure(self, mock_template_dir, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: ["Test Author"])
        monkeypatch.setattr("builtins.input", lambda _: ["test@test.com"])
        fake_path = MagicMock()
        fake_path.is_file.return_value = True
        mock_template_dir.rglob.return_value = [fake_path]
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(ScaffoldError):
                scaffold(
                    Namespace(
                        directory=tmpdirname,
                        name="Test",
                        tests_only=False,
                        author_name=None,
                        author_email=None,
                    )
                )
