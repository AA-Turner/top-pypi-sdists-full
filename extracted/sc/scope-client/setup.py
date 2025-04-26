from setuptools import setup, find_packages
import os

setup(
    name="scope_client",
    version=os.environ.get("SCOPE_CLIENT_VERSION", "0.0.0"),
    packages=find_packages("scope_client", exclude=["scope_client.api_bindings.test"]),
    package_dir={"": "scope_client"},
)
