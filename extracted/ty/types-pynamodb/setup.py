from pathlib import Path
from setuptools import setup

setup(
    name="types-pynamodb",
    version="0.1",
    description="A dummy package.",
    long_description=Path("README.rst").read_text(),
    keywords="types",
    author="Jelle Zijlstra",
    author_email="jelle.zijlstra@gmail.com",
    license="MIT",
    packages=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ]
)
