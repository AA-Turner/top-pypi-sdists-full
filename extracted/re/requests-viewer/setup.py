from setuptools import find_packages
from setuptools import setup

MAJOR_VERSION = "0"
MINOR_VERSION = "1"
MICRO_VERSION = "0"
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(
    name="requests_viewer",
    version=VERSION,
    description="requests_viewer!",
    url="https://github.com/kootenpv/requests_viewer",
    author="Pascal van Kooten",
    author_email="kootenpv@gmail.com",
    license="MIT",
    install_requires=["requests", "lxml", "beatifulsoup4"],
    extras_require={"fancy": ["tldextract"]},
    packages=find_packages(),
    zip_safe=False,
    platforms="any",
)
