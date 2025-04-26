from setuptools import setup, find_packages
from qpd_version import __version__
import os


def get_version() -> str:
    tag = os.environ.get("RELEASE_TAG", "")
    if "dev" in tag.split(".")[-1]:
        return tag
    if tag != "":
        assert tag == __version__, "release tag and version mismatch"
    return __version__


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="qpd",
    version=get_version(),
    packages=find_packages(include=["qpd*", "_qpd*"]),
    description="Query Pandas Using SQL",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    author="Han Wang",
    author_email="goodwanghan@gmail.com",
    keywords="pandas sql",
    url="http://github.com/goodwanghan/qpd",
    install_requires=[
        "pandas>=1.2.0",
        "triad>=0.9.0",
        "adagio",
        "antlr4-python3-runtime>=4.11.1,<4.12",
    ],
    extras_require={
        "dask": ["dask[dataframe,distributed]", "cloudpickle>=1.4.0"],
        # "ray": ["pandas>=1.1.2", "modin[ray]>=0.8.1.1"],
        "all": [
            "dask[dataframe,distributed]",
            "cloudpickle>=1.4.0",
            # "modin[ray]",
        ],
    },
    package_data={"qpd": ["py.typed"]},
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.7",
)
