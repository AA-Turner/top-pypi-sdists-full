"""
Updated fork of jsonsubschema.
Originally created on August 6, 2019 by Andrew Habib.
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jsonsubschema-master',
    version='0.0.7',
    author='Andrew Habib, Avraham Shinnar, Martin Hirzel (updated by Your Name)',
    author_email='your.email@example.com',
    description="An up-to-date fork of jsonsubschema synced with the latest master branch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/jsonsubschema',  # Link to your fork
    packages=['jsonsubschema'],
    license='Apache License 2.0',
    install_requires=[
        'portion',
        'greenery>=4.0.0',
        'jsonschema',
        'jsonref'
    ],
    entry_points={
        'console_scripts': 'jsonsubschema=jsonsubschema.cli:main'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
