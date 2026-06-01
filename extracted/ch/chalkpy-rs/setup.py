from setuptools import setup
from setuptools_rust import RustExtension

setup(
    rust_extensions=[
        RustExtension(
            "chalk_rs",
            path="Cargo.toml",
            features=["python"],
        )
    ],
)
