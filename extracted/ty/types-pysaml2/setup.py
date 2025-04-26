"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""
from os import path

from setuptools import glob
from setuptools import setup

# Always prefer setuptools over distutils

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="types-pysaml2",
    description="Type Stubs for pysaml2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cex-solutions/pysaml2",
    author="Binovate Labs",
    author_email="cex-dev@binovate.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Typing :: Stubs Only",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="GPLv3",
    keywords="stubs pysaml2 pysaml saml2 saml",
    package_data={
        "saml2-stubs": [item.split("saml2-stubs/")[-1] for item in glob.glob("**/*.pyi", recursive=True)]
        + ["METADATA.toml"]
    },
    packages=["saml2-stubs"],
    python_requires=">=3.7, <4",
    install_requires=[],
    extras_require={
        "dev": [
            "pysaml2==7.2.1",
            "types-six==1.16.21.4",
            "types-requests==2.28.11.7",
            "mypy==0.991",
            "pipenv-setup==3.2.0",
            "twine==4.0.2",
        ]
    },
    dependency_links=[],
    project_urls={
        "Bug Reports": "https://github.com/cex-solutions/types-pysaml2/issues",
        "Source": "https://github.com/cex-solutions/types-pysaml2",
    },
)
