"""
    Library setup file
"""
import subprocess
from setuptools import setup


try:
    subprocess.check_output(['pip', 'show', 'psycopg2'])
    PSYCOPG2_INSTALLED = True
except subprocess.CalledProcessError:
    PSYCOPG2_INSTALLED = False


install_requires = [
    "charset-normalizer",
    "numpy>=1.26.4",
    "pandas>=2.1.0",
    "sqlalchemy>=2.0.27",
    "optilogic>=2.13.0",
    "PyJWT>=2.8.0",
    "httpx>=0.24.1",
    "splitio_client==9.7.0",
    "opentelemetry-api>=1.27.0",
    "opentelemetry-sdk>=1.27.0",
    "azure-monitor-opentelemetry-exporter>=1.0.0b31",
    "opentelemetry-instrumentation-asgi==0.48b0",      # Align versions
    "opentelemetry-instrumentation-fastapi==0.48b0",   # Align versions
    "opentelemetry-instrumentation-dbapi==0.48b0",     # Align versions
    "opentelemetry-instrumentation-httpx==0.48b0",     # Align versions
    "opentelemetry-semantic-conventions==0.48b0",      # Align to 0.48b0
]

# If psycopg2 is not installed let's check if we should use the binary version instead
if not PSYCOPG2_INSTALLED:
    import os

    # Look for USE_PSYCOPG2_BINARY, if not set, default to True, otherwise, use the value
    USE_BINARY = os.getenv('USE_PSYCOPG2_BINARY', 'True').lower() == 'true'

    if USE_BINARY:
        install_requires.append('psycopg2-binary>=2.9.9')
    else:
        install_requires.append('psycopg2>=2.9.9')


setup(
    name="cosmicfrog",
    include_package_data=True,
    version="1.0.21",
    description="Helpful utilities for working with Cosmic Frog models",
    url="https://cosmicfrog.com",
    author="Optilogic",
    packages=["cosmicfrog"],
    package_data={
        "cosmicfrog": [
            "anura27/*.json",
            "anura27/table_definitions/*.json",
            "anura28/*.json",
            "anura28/table_definitions/*.json",
        ],
    },
    license="MIT",
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
