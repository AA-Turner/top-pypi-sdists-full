from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "1.0.7"

"""Perform the package airflow-provider-kettle-operator setup."""
setup(
    name="apache_airflow_providers_kettle",
    version=__version__,
    description="A simple Apache Airflow Kettle Operator that can invoke jobs and transformations for Linux based systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"apache_airflow_provider": ["provider_info=kettle_provider.__init__:get_provider_info"]},
    license="Apache License 2.0",
    packages=find_packages(exclude=["*tests.*", "*tests"]),
    install_requires=["apache-airflow>=2.0"],
    setup_requires=["setuptools", "wheel"],
    author="Robert Bryśkiewicz",
    author_email="bryskiewiczr@pm.me",
    url="",
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires="~=3.7",
)
