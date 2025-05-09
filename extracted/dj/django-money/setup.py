import codecs
import os
import re

from setuptools import find_packages, setup


test_requirements = [
    "pytest>=8.2,<8.3",
    "pytest-django",
    "pytest-cov",
    "mixer",
    "mypy",
    "django-stubs",
]

extras_requirements = {
    "test": test_requirements,
    "exchange": ["certifi"],
}


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


def find_version():
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", read("djmoney/__init__.py"), re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find __version__ string.")


setup(
    name="django-money",
    version=find_version(),
    description=(
        "Adds support for using money and currency fields in django models and forms. "
        "Uses py-moneyed as the money implementation."
    ),
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    url="https://github.com/django-money/django-money",
    maintainer="Greg Reinbach",
    maintainer_email="greg@reinbach.com",
    license="BSD",
    packages=find_packages(include=["djmoney", "djmoney.*"]),
    install_requires=["setuptools", "Django>=2.2", "py-moneyed>=2.0,<3.1"],
    python_requires=">=3.7",
    platforms=["Any"],
    keywords=["django", "py-money", "money"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    tests_require=test_requirements,
    extras_require=extras_requirements,
)
