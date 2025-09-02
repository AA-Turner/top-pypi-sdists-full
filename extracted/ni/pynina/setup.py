from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

setup(
    name="pynina",
    version="0.3.6",
    description="A Python API wrapper to retrieve warnings from the german NINA app.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DeerMaximum/pynina",
    author="DeerMaximum",
    author_email="git983456@parabelmail.de",
    license=license,
    packages=["pynina"],
    install_requires=["aiohttp>=3.11.6"],
)
