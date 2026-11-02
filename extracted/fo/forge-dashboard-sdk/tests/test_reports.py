"""hack/reports.py assembles the reports/ tree published beside the docs."""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def reports() -> ModuleType:
    spec = importlib.util.spec_from_file_location("reports", ROOT / "hack" / "reports.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def inputs(tmp_path: Path) -> Path:
    (tmp_path / "coverage.xml").write_text('<coverage line-rate="0.9"/>')
    (tmp_path / "junit.xml").write_text("<testsuites/>")
    html = tmp_path / "htmlcov"
    html.mkdir()
    (html / "index.html").write_text("<html>cov</html>")
    return tmp_path


def test_builds_the_published_tree(reports: ModuleType, inputs: Path, tmp_path: Path) -> None:
    out = tmp_path / "out" / "reports"
    reports.build_reports(
        coverage_xml=inputs / "coverage.xml",
        coverage_html=inputs / "htmlcov",
        junit_paths=[inputs / "junit.xml"],
        out_dir=out,
    )
    assert (out / "coverage" / "coverage.xml").read_text() == '<coverage line-rate="0.9"/>'
    assert (out / "coverage" / "index.html").read_text() == "<html>cov</html>"
    assert (out / "tests" / "junit.xml").read_text() == "<testsuites/>"
    assert 'href="tests/"' in (out / "index.html").read_text()
    assert 'href="coverage/"' in (out / "index.html").read_text()
    assert 'href="junit.xml"' in (out / "tests" / "index.html").read_text()


def test_missing_input_fails_loudly(reports: ModuleType, inputs: Path, tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        reports.build_reports(
            coverage_xml=inputs / "nope.xml",
            coverage_html=inputs / "htmlcov",
            junit_paths=[inputs / "junit.xml"],
            out_dir=tmp_path / "out",
        )
