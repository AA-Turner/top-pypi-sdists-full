from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="spotipy-pandas",
    version="0.2.0",
    description="A Spotipy-based Pandas wrapper for Spotify API calls",
    url="https://github.com/opbenesh/spotipy-pandas",
    author="Ben Esh",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="spotify pandas",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
