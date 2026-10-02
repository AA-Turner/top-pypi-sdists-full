from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    rust_extensions=[
        RustExtension(
            "chalk_remote_call._native",
            path="chalk-remote-call-rs/chalk-remote-call-server/Cargo.toml",
            binding=Binding.PyO3,
        )
    ],
)
