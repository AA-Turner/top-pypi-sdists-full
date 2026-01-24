import os
import re
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")

REQUIRES = ["urllib3 >= 1.15", "requests"]


def read(*args):
    """Reads complete file contents."""
    return open(os.path.join(HERE, *args)).read()


def get_version():
    """Reads the version from this module."""
    init = read("akeyless_cloud_id", "__init__.py")
    return VERSION_RE.search(init).group(1)


setup(
    name="akeyless_cloud_id",
    version=get_version(),
    description="AKEYLESS Cloud ID Retriever",
    author="Akeyless Security",
    author_email="support@akeyless.io",
    url="https://www.akeyless.io/",
    keywords=["AKEYLESS Cloud ID"],
    install_requires=REQUIRES,
    extras_require={
        'aws': [
            'boto3',
        ],
        'gcp': [
            'google-auth',
        ],
        'azure': [
            'azure-identity'  
        ],
    },
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0",
    long_description_content_type="text/markdown",
    long_description=read("README.rst"),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",        
        "Topic :: Security",
    ],
)
