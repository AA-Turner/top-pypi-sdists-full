from __future__ import annotations

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeq",
    version="66.41.2.20250828",
    author="Seeq Corporation",
    author_email="support@seeq.com",
    description="The Seeq SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.seeq.com",
    project_urls={
        'Documentation': 'https://python-docs.seeq.com/',
        'Changelog': 'https://python-docs.seeq.com/changelog.html'
    },
    packages=setuptools.find_namespace_packages(include=['seeq.sdk', 'seeq.sdk.*']),
    include_package_data=True,
    install_requires=[
        # These requirements are for seeq.sdk and should match target/python/requirements.txt
        'certifi >= 14.05.14',
        'six >= 1.10',
        'urllib3 >= 1.15.1, < 3.0.0',
        'requests >= 2.21.0',
        'cryptography >= 3.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
