from setuptools import setup, find_packages

setup(
    name="prophecy-libs",
    version="2.0.6",
    url="https://github.com/SimpleDataLabsInc/prophecy-python-libs",
    packages=find_packages(exclude=["test.*", "test"]),
    description="Helper library for prophecy generated code",
    long_description=open("README.md").read(),
    install_requires=[
        "pyhocon>=0.3.59",
        "requests>=2.10.0",
        "hvac==2.3.0",
        "zstandard>=0.23.0",
        "msgspec>=0.18.6",
    ],
    keywords=["python", "prophecy"],
    classifiers=[],
    zip_safe=False,
    license="GPL-3.0",
)
