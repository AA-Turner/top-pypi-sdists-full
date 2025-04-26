import sys
from os import path

from setuptools import find_packages, setup

from aniso8601 import __version__

TESTS_REQUIRE = []

# Mock is only required for Python 2
PY2 = sys.version_info[0] == 2

if PY2:
    TESTS_REQUIRE.append("mock>=2.0.0")

THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, "README.rst")) as f:
    README_TEXT = f.read()

setup(
    name="aniso8601",
    version=__version__,
    description="A library for parsing ISO 8601 strings.",
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author="Brandon Nielsen",
    author_email="nielsenb@jetfuse.net",
    url="https://codeberg.org/nielsenb-jf/aniso8601",
    packages=find_packages(),
    extras_require={
        "dev": TESTS_REQUIRE
        + [
            "black",
            "coverage",
            "isort",
            "pre-commit",
            "pyenchant",
            "pylint",
        ]
    },
    test_suite="aniso8601",
    tests_require=TESTS_REQUIRE,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="iso8601 parser",
    project_urls={
        "Changelog": "https://codeberg.org/nielsenb-jf/aniso8601/src/branch/main/CHANGELOG.rst",
        "Documentation": "https://aniso8601.readthedocs.io/",
        "Source": "https://codeberg.org/nielsenb-jf/aniso8601",
        "Tracker": "https://codeberg.org/nielsenb-jf/aniso8601/issues",
    },
)
