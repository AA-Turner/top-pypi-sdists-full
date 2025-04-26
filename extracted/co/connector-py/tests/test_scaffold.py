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
