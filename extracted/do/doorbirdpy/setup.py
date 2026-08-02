"""DoorBirdPy setup script."""
from setuptools import setup

setup(
    name="DoorBirdPy",
    version="3.0.12",
    author="Andy Castille",
    author_email="andy@robiotic.net",
    maintainer="J. Nick Koston",
    maintainer_email="nick@koston.org",
    packages=["doorbirdpy"],
    install_requires=[
        "aiohttp",
        "tenacity>=8",
    ],
    url="https://gitlab.com/klikini/doorbirdpy",
    download_url="https://gitlab.com/klikini/doorbirdpy/-/archive/master/doorbirdpy-master.zip",
    license="MIT",
    python_requires=">=3.9",
    description="Python wrapper for the DoorBird LAN API",
    platforms="Cross Platform",
)
