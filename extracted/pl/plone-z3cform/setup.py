from pathlib import Path
from setuptools import find_packages
from setuptools import setup


__version__ = "2.0.5"


def read(path):
    with open(path) as file_handle:
        return file_handle.read()


def description():
    base_path = Path(".") / "src" / "plone" / "z3cform"
    return (
        read("README.rst")
        + "\n"
        + read(base_path / "fieldsets" / "README.rst")
        + "\n"
        + read(base_path / "crud" / "README.txt")
        + "\n"
        + read("CHANGES.rst")
        + "\n"
    )


setup(
    name="plone.z3cform",
    version=__version__,
    description="plone.z3cform is a library that allows use of z3c.form "
    "with Zope and the CMF.",
    long_description=description(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="Plone CMF Python Zope CMS Webapplication",
    author="Plone Foundation",
    author_email="releasemanager@plone.org",
    url="https://github.com/plone/plone.z3cform",
    license="GPL version 2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "plone.batching",
        "z3c.form>=4.0",
        "zope.browserpage",
        "zope.pagetemplate",
        "Zope",
    ],
    extras_require={"test": ["persistent", "plone.testing", "zope.annotation"]},
)
