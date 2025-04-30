from setuptools import setup, find_packages

setup(
    name="prophecy-libs",
    version="1.9.49",
    url="https://github.com/SimpleDataLabsInc/prophecy-python-libs",
    packages=find_packages(exclude=["test.*", "test"]),
    description="Helper library for prophecy generated code",
    long_description=open("README.md").read(),
    install_requires=["pyhocon>=0.3.59", "requests>=2.10.0"],
    keywords=["python", "prophecy"],
    classifiers=[],
    zip_safe=False,
    license="GPL-3.0",
)
