import os
from setuptools import find_packages, setup

setup(
    name="generic-etl",
    entry_points={"console_scripts": ["etl=etl.etl:main"]},
    version=os.environ.get("RELEASE"),
    packages=find_packages(),
    install_requires=[
        "dynamic-yaml==1.3.3",
        "greenlet==1.1.3.post0",
        "numpy==1.23.4",
        "pandas==1.5.1",
        "psycopg2-binary==2.9.4",
        "pyaml==21.10.1",
        "python-dateutil==2.8.2",
        "pytz==2022.5",
        "PyYAML==6.0",
        "six==1.16.0",
        "SQLAlchemy==1.4.42",
        "cx-Oracle==8.3.0",
    ],
    author="Christian Decker",
)
