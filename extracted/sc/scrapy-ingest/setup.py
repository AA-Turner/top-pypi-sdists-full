from __future__ import annotations

from pathlib import Path
from typing import Protocol

from setuptools import find_packages, setup
from setuptools.command.install import install

BASE_DIR = Path(__file__).parent
_BOOTSTRAP_PTH = BASE_DIR / "scrapy_ingest" / "scrapy_bootstrap.pth"
_SITE_PTH = "scrapy_ingest_scrapy_bootstrap.pth"


class _InstallCommand(Protocol):
    install_lib: str | None

    def copy_file(
        self, infile: str, outfile: str, preserve_mode: bool = True
    ) -> tuple[str, bool]: ...


def _site_packages(install_lib: str) -> Path:
    root = Path(install_lib)
    return root.parent if root.name == "scrapy_ingest" else root


def _bootstrap_pth_dest(install_lib: str | None) -> Path | None:
    if install_lib is None:
        return None
    return _site_packages(install_lib) / _SITE_PTH


def _install_bootstrap_pth(cmd: _InstallCommand) -> None:
    dest = _bootstrap_pth_dest(cmd.install_lib)
    if dest is None:
        return
    cmd.copy_file(str(_BOOTSTRAP_PTH), str(dest), preserve_mode=False)


def _outputs_with_bootstrap_pth(cmd: _InstallCommand, outputs: list[str]) -> list[str]:
    dest = _bootstrap_pth_dest(cmd.install_lib)
    if dest is not None and dest.is_file():
        return outputs + [str(dest)]
    return outputs


class InstallWithBootstrap(install):
    def run(self):
        super().run()
        _install_bootstrap_pth(self)

    def get_outputs(self) -> list[str]:
        return _outputs_with_bootstrap_pth(self, install.get_outputs(self))


PACKAGE_DATA: dict[str, list[str]] = {
    "ingest_dashboard": ["static/**/*"],
    "scrapy_ingest": ["scrapy_bootstrap.pth"],
}

try:
    long_description = (BASE_DIR / "README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = (
        "A comprehensive Scrapy extension for ingesting scraped items, "
        "requests, logs, and stats into PostgreSQL databases."
    )

setup(
    name="scrapy-ingest",
    version="2.0.0",
    description="One pipeline. Full crawl observability in SQL or Elasticsearch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fawad Ali",
    author_email="fawadstar6@gmail.com",
    url="https://github.com/fawadss1/scrapy-ingest",
    project_urls={
        "Documentation": "https://scrapy-ingest.readthedocs.io/",
        "Source": "https://github.com/fawadss1/scrapy-ingest",
        "Tracker": "https://github.com/fawadss1/scrapy-ingest/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Scrapy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Database",
    ],
    keywords="scrapy, database, postgresql, mysql, web-scraping, data-pipeline",
    install_requires=[
        "scrapy>=2.18.0",
        "psycopg2-binary>=2.9.12",
        "itemadapter>=0.13.1",
        "pytz>=2026.3",
        "w3lib>=2.4.1",
        "PyMySQL>=1.2.0",
        "opensearch-py>=3.2.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=5.0.0",
            "sphinx_rtd_theme>=1.2.0",
            "myst-parser>=0.18.0",
            "sphinx-autodoc-typehints>=1.19.0",
            "sphinx-copybutton>=0.5.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.8.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.8.0",
        ],
        "dashboard": [
            "fastapi>=0.115.0",
            "httpx>=0.27.0",
            "uvicorn[standard]>=0.32.0",
        ],
    },
    package_data=PACKAGE_DATA,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "scrapy-ingest=scrapy_ingest.cli:main",
        ],
        "scrapy.pipelines": [
            "ingest = scrapy_ingest.pipelines.main:IngestPipeline",
        ],
        "scrapy.extensions": [
            "logging_ext = scrapy_ingest.extensions.logging:LoggingExtension",
            "stats_ext = scrapy_ingest.extensions.stats:StatsExtension",
        ],
    },
    python_requires=">=3.10",
    zip_safe=False,
    cmdclass={"install": InstallWithBootstrap},
)
