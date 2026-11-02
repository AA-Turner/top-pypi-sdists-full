"""Assemble the reports/ tree published beside the docs site.

pytest-cov already writes Cobertura XML and an HTML view, and pytest writes
JUnit XML, so this only lays them out under reports/ and adds index pages.

    python hack/reports.py site/reports
"""

import shutil
import sys
from html import escape
from pathlib import Path


def _page(title: str, body: str) -> str:
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{title}</title></head>\n"
        f"<body><main><h1>{title}</h1>{body}</main></body></html>\n"
    )


def build_reports(
    *,
    coverage_xml: Path,
    coverage_html: Path,
    junit_paths: list[Path],
    out_dir: Path,
) -> None:
    for source in (coverage_xml, coverage_html, *junit_paths):
        if not source.exists():
            raise FileNotFoundError(source)

    coverage = out_dir / "coverage"
    tests = out_dir / "tests"
    shutil.copytree(coverage_html, coverage, dirs_exist_ok=True)
    shutil.copy(coverage_xml, coverage / "coverage.xml")
    tests.mkdir(parents=True, exist_ok=True)
    for path in junit_paths:
        shutil.copy(path, tests / path.name)

    links = "".join(f'<li><a href="{escape(p.name)}">{escape(p.name)}</a></li>' for p in junit_paths)
    (tests / "index.html").write_text(_page("Tests", f"<p>JUnit XML from each test runner.</p><ul>{links}</ul>"))
    (out_dir / "index.html").write_text(
        _page(
            "Reports",
            '<ul><li><a href="tests/">Tests</a></li><li><a href="coverage/">Coverage</a></li></ul>',
        )
    )


if __name__ == "__main__":
    build_reports(
        coverage_xml=Path("coverage.xml"),
        coverage_html=Path("htmlcov"),
        junit_paths=[Path("junit.xml")],
        out_dir=Path(sys.argv[1] if len(sys.argv) > 1 else "reports"),
    )
