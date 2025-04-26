import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rust_demangler", 
    version="1.0",
    author="bi0s",
    author_email="amritabi0s1@example.com",
    description="A package for demangling Rust symbols",
    packages=["rust_demangler"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teambi0s/rust_demangler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)