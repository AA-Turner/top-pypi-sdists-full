from setuptools import setup
from setuptools_rust import RustExtension

# All package metadata, including dependencies, is specified in
# the pyproject.toml file

setup(
    rust_extensions=[
        RustExtension(
            "chalk_rs",
            path="chalk-rs/Cargo.toml",
            features=["python"],
        )
    ],
)
