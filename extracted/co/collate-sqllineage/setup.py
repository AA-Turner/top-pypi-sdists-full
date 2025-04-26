from setuptools import find_packages, setup

from collate_sqllineage import NAME, STATIC_FOLDER, VERSION

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    author="Collate Committers",
    description="Collate SQL Lineage for Analysis Tool powered by Python and sqlfluff based on sqllineage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    package_data={"": [f"{STATIC_FOLDER}/*", f"{STATIC_FOLDER}/**/**/*", "data/**/*"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sqlparse>=0.5,<0.6",
        "networkx>=2.4",
        "collate-sqlfluff==3.3.4",
    ],
    entry_points={"console_scripts": ["sqllineage = collate_sqllineage.cli:main"]},
    extras_require={
        "ci": [
            "bandit",
            "black",
            "flake8",
            "flake8-blind-except",
            "flake8-builtins",
            "flake8-import-order",
            "flake8-logging-format",
            "mypy",
            "pytest",
            "pytest-cov",
            "tox",
            "twine",
            "wheel",
        ],
        "docs": ["Sphinx>=3.2.0", "sphinx_rtd_theme>=0.5.0"],
    },
)
