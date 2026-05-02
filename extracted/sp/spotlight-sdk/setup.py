import subprocess

import setuptools

try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError):
    long_description = open("README.md").read()


def get_tag():
    tag = subprocess.getoutput("git tag --sort=version:refname | tail -n1")
    commits = subprocess.getoutput(f"git rev-list {tag}..HEAD --count")
    return f"{tag}.{commits}"


setuptools.setup(
    name="spotlight-sdk",
    version=get_tag(),
    author="Spotlight",
    author_email="hello@spotlight.dev",
    description="Spotlight Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://spotlight.dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    packages=setuptools.find_packages(include=["spotlight*"], exclude=["tests.*"]),
    install_requires=[
        "requests>=2.31.0",
        "aiohttp>=3.8.4",
        "pandas>=2.0.1",
        "duckdb>=0.7.1",
        "trycast>=1.0.0",
        "pydash>=7.0.3",
        "cachetools>=5.3.0",
        "pytz>=2022.1",
        "pydantic==1.10.17",
        "aiocache>=0.12.1",
        "backoff>=2.2.1",
        "asyncstdlib>=3.10.7",
    ],
)
