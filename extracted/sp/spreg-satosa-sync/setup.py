import setuptools


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="spreg-satosa-sync",
    python_requires=">=3.6.2",
    url="https://gitlab.ics.muni.cz/perun-proxy-aai/python/spreg-satosa-sync.git",
    description="Script to sync SATOSA clients from Perun RPC to mongoDB",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "spreg_satosa_sync = spreg_satosa_sync.spreg_satosa_sync:main",
        ],
    },
    install_requires=[
        "setuptools",
        "pycryptodomex~=3.11",
        "pymongo>=3.12.1,<5",
        "requests~=2.26",
        "PyYAML~=6.0",
        "perun.connector~=3.4",
    ],
)
