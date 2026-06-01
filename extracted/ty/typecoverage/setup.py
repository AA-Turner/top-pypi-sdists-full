
from pathlib import Path

from setuptools import find_packages, setup

# Read long description from README
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="typecoverage",
    version="1.0.1",
    author="Joao Lopes",
    author_email="joaslopes@gmail.com",
    maintainer="Joao Lopes",
    maintainer_email="joaslopes@gmail.com",
    description="A strict CLI + library API to report untyped variables, arguments, and function returns in Python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kairos-xx/typecoverage",
    project_urls={
        "Homepage": "https://github.com/kairos-xx/typecoverage",
        "Repository": "https://github.com/kairos-xx/typecoverage",
        "Documentation": "https://github.com/kairos-xx/typecoverage/docs",
        "Issues": "https://github.com/kairos-xx/typecoverage/issues",
        "Changelog": "https://github.com/kairos-xx/typecoverage/releases",
    },
    packages=find_packages(include=["typecoverage", "typecoverage.*"]),
    package_data={
        "typecoverage": ["py.typed"],
    },
    include_package_data=True,
    install_requires=[
        "pytest>=7.0.0",
        "replit==4.1.0",
        "black",
        "flake8", 
        "build",
        "requests",
        "pyright",
        "toml",
        "pyyaml",
        "isort",
        "pyproject-flake8",
        "zipfile38==0.0.3",
    ],
    extras_require={
        "dev": [
            "pytest-cov",
            "pytest-xdist",
            "mypy",
            "ruff",
            "pre-commit",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov",
            "coverage[toml]",
        ],
    },
    entry_points={
        "console_scripts": [
            "typecoverage=typecoverage.core:typecoverage.parse_and_run",
        ],
    },
    python_requires=">=3.11",
    license="MIT",
    keywords=[
        "type-checking",
        "static-analysis", 
        "type-annotations",
        "code-quality",
        "python-typing",
        "ast-analysis",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Debuggers",
        "Environment :: Console",
        "Environment :: Web Environment",
    ],
    zip_safe=False,
    platforms=["any"],
)
