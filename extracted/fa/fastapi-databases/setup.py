# -*- coding: utf-8 -*-
import io
import re
import os
from setuptools import setup


with io.open("README.md") as f:
    long_description = f.read()


def get_version(package):
    with io.open(f"{package}/__init__.py", "rt", encoding="utf8") as f:
        return re.search(r'__version__ = "(.*?)"', f.read()).group(1)


def get_packages(package):
    """Return root package and all sub-packages."""
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="fastapi-databases",
    version=get_version("fastapi_databases"),
    description="handling database transactions in asynchronously with databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ahmednafies.github.io/fastapi-databases/",
    author="Ahmed Nafies",
    author_email="ahmed.nafies@gmail.com",
    license="MIT",
    packages=get_packages("fastapi_databases"),
    install_requires=["fastapi", "databases", "alembic", "typer"],
    extras_require={
        "postgresql": ["asyncpg", "psycopg2"],
        "mysql": ["aiomysql", "pymysql"],
        "sqlite": ["aiosqlite"],
        "postgresql+aiopg": ["aiopg"],
    },
    project_urls={
        "Documentation": "https://ahmednafies.github.io/fastapi-databases/",
        "Source": "https://github.com/ahmednafies/fastapi-databases",
    },
    entry_points={"console_scripts": ["database = fastapi_databases.cli:app"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
    python_requires=">=3.6",
)
