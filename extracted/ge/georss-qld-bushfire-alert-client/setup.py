"""Setup of georss_qld_bushfire_alert_client library."""
import os

from setuptools import find_packages, setup

NAME = "georss_qld_bushfire_alert_client"
AUTHOR = "Malte Franken"
AUTHOR_EMAIL = "coding@subspace.de"
DESCRIPTION = "A GeoRSS client library for the Queensland Bushfire Alert feed."
URL = "https://github.com/exxamalte/python-georss-qld-bushfire-alert-client"

REQUIRES = [
    "georss_client>=0.17",
]

with open("README.md") as fh:
    long_description = fh.read()

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = {}
with open(os.path.join(HERE, NAME, "__version__.py")) as f:
    exec(f.read(), VERSION)  # pylint: disable=exec-used

setup(
    name=NAME,
    version=VERSION["__version__"],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRES,
)
