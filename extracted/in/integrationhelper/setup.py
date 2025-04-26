"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()

setuptools.setup(
    name="integrationhelper",
    version="0.2.2",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="A set of helpers for integrations.",
    install_requires=["aiohttp", "async_timeout", "backoff"],
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/integrationhelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
