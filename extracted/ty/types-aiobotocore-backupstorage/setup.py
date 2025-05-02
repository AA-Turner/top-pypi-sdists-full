"""
Setup script for types-aiobotocore-backupstorage.
"""

from pathlib import Path

from setuptools import setup

LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()


setup(
    name="types-aiobotocore-backupstorage",
    version="2.13.0",
    packages=["types_aiobotocore_backupstorage"],
    url="https://github.com/youtype/mypy_boto3_builder",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Type annotations for aiobotocore.BackupStorage 2.13.0 service generated with mypy-boto3-builder 7.24.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Stubs Only",
    ],
    keywords="aiobotocore backupstorage type-annotations botocore mypy typeshed autocomplete",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={"types_aiobotocore_backupstorage": ["py.typed", "*.pyi"]},
    python_requires=">=3.8",
    project_urls={
        "Documentation": "https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backupstorage/",
        "Source": "https://github.com/youtype/mypy_boto3_builder",
        "Tracker": "https://github.com/youtype/mypy_boto3_builder/issues",
    },
    install_requires=[
        'typing-extensions>=4.1.0; python_version<"3.12"',
    ],
    zip_safe=False,
)
