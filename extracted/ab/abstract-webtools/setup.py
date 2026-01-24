from pathlib import Path
from setuptools import setup, find_packages

README = Path("README.md").read_text(encoding="utf-8")

setup(
    name="abstract_webtools",
    version='0.1.6.383',  # bump once per release
    author="putkoff",
    author_email="partners@abstractendeavors.com",
    description="Utilities for fetching/parsing web content with requests/urllib3/BS4 and helpers.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/AbstractEndeavors/abstract_webtools",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    # Keep runtime deps to real, installable PyPI packages only.
    install_requires=[
        "requests>=2.31.0",
        "urllib3>=2.0.4",
        "beautifulsoup4>=4.12.0",
    ],
    extras_require={
        "gui": [
            "PySimpleGUI>=4.60.5",
            "PyQt5>=5.15.0",
        ],
        "drivers": [
            "selenium>=4.15.2",
            "webdriver-manager>=4.0.0",
        ],
        "media": [
            "yt-dlp>=2024.4.9",
            "m3u8>=4.0.0",
        ],
    },
)
