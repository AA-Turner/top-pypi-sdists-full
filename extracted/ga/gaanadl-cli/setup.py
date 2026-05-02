"""
gaanadl-cli setup script.
"""

from setuptools import find_packages, setup
import os

VERSION = "1.4.0"

def read_file(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def get_requirements():
    if os.path.isfile("requirements.txt"):
        with open("requirements.txt", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    return [
        "requests>=2.32.0",
        "mutagen>=1.47.0",
        "rich>=14.0.0",
        "pathvalidate>=3.3.0",
        "pyfiglet>=1.0.3",
    ]

setup(
    name="gaanadl-cli",
    version=VERSION,
    description="Download high-quality music from Gaana with metadata and synced lyrics",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="notdelta_xd",
    url="https://github.com/notdeltaxd/gaanadl-cli",
    project_urls={
        "Bug Reports": "https://github.com/notdeltaxd/gaanadl-cli/issues",
        "Source": "https://github.com/notdeltaxd/gaanadl-cli",
    },
    license="MIT",
    keywords=["gaana", "music", "downloader", "cli", "flac", "lyrics"],
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "gaana=gaana.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)

