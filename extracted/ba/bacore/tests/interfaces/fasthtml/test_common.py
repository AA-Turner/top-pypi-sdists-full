"""FastHTML web interface tests."""

import httpx
import pytest
from bacore.domain.source_code import DirectoryModel, ModuleModel
from bacore.interfaces.fasthtml.common import (
    Documentation,
    MarkdownFT,
    SrcDirFT,
    flexboxgrid,
    map_uri_to_module,
    uri_to,
)
from bacore.web.main import app
from fasthtml.common import FT
from pathlib import Path
from random import choice
from starlette.testclient import TestClient

client = TestClient(app)


def test_flexboxgrid_exists_on_cdn(fixt_internet_connection_established):
    """Testing that flexbox grid still exists on the content delivery network."""
    try:
        response = httpx.get(flexboxgrid().href)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        pytest.fail(f"HTTP error occurred: {exc}")
    except httpx.RequestError as exc:
        pytest.fail(f"Request error occurred: {exc}")

    assert response, f"\nHeaders: {response.headers}\nContent: {response.content}"


@pytest.mark.parametrize(
    "file_path, package_root, expected_url",
    [
        ("python/bacore/__init__.py", "bacore", ""),
        ("python/bacore/domain/source_code.py", "bacore", "domain/source-code"),
        (
            "python/bacore/interactors/source_code_reader.py",
            "bacore",
            "interactors/source-code-reader",
        ),
        ("tests/conftest.py", "tests", "conftest"),
        ("tests/domain/test_source_code.py", "tests", "domain/test-source-code"),
    ],
)
def test_uri_to(file_path, package_root, expected_url):
    """Test that the documentation path is correctly generated."""
    src_module = ModuleModel(path=Path(file_path), package_root=package_root)
    uri = uri_to(module=src_module)

    assert uri == expected_url


def test_map_uri_to_module():
    src_dir = DirectoryModel(path=Path("python/bacore"), package_root="bacore")
    test_dir = DirectoryModel(path=Path("tests"), package_root="tests")

    src_mapping = map_uri_to_module(directory_model=src_dir)
    src_path = choice(list(src_mapping.keys()))
    assert isinstance(src_mapping.get(src_path), ModuleModel), src_mapping.get(src_path)

    test_mapping = map_uri_to_module(directory_model=test_dir)
    test_path = choice(list(test_mapping.keys()))
    assert isinstance(test_mapping.get(test_path), ModuleModel), test_mapping.get(test_path)


def test_markdown_file():
    """Verify that a readme page is of type FT."""
    readme_file = MarkdownFT(path=Path("README.md"), skip_title=True)
    assert isinstance(readme_file.__ft__(), FT), readme_file.__ft__()


class TestSrcDirFT:
    src_docs = SrcDirFT(path=Path("python/bacore"), package_root="bacore")
    test_docs = SrcDirFT(path=Path("tests"), package_root="tests")

    # def test_src_docs_tree(self):
    #     url = choice(list(self.src_docs.docs_tree().keys()))
    #     assert isinstance(url, str), url
    #     assert isinstance(self.src_docs.docs_tree().get(url), ModuleModel), self.src_docs.docs_tree()

    # def test_test_docs_tree(self):
    #     url = choice(list(self.src_docs.docs_tree().keys()))
    #     assert isinstance(url, str), url
    #     assert isinstance(self.src_docs.docs_tree().get(url), ModuleModel), self.src_docs.docs_tree()

    # def test_ft(self):
    #     from pprint import pprint

    #     assert self.src_docs.__ft__ == [], pprint(self.src_docs.model_dump())


class TestDocumentation:
    src_docs = Documentation(path=Path("python/bacore"), package_root="bacore")
    test_docs = Documentation(path=Path("tests"), package_root="tests")

    def test_src_docs_tree(self):
        url = choice(list(self.src_docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.src_docs.docs_tree().get(url), ModuleModel), self.src_docs.docs_tree()

    def test_test_docs_tree(self):
        url = choice(list(self.test_docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.test_docs.docs_tree().get(url), ModuleModel), self.test_docs.docs_tree()
