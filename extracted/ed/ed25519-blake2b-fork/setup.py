import os
from setuptools import setup, Extension

sources = ["src/ed25519-glue/ed25519module.c"]
sources.extend(
    "src/ed25519-supercop-ref/" + s
    for s in os.listdir("src/ed25519-supercop-ref")
    if s.endswith(".c") and s != "test.c"
)

setup(
    ext_modules=[
        Extension(
            "ed25519_blake2b._ed25519",
            include_dirs=["src/ed25519-supercop-ref"],
            sources=sources,
        )
    ],
)
