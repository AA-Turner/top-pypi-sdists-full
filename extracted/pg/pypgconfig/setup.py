from setuptools import setup, find_packages
import os

PACKAGE_NAME = "PyPgConfig"
VERSION = "0.1.0a2"
SHORT_DESCRIPTION = "Access pg_config from Python"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name=PACKAGE_NAME,
    description=SHORT_DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florents Tselai",
    author_email="florents@tselai.com",
    url=f"https://github.com/Florents-Tselai/{PACKAGE_NAME}",
    project_urls={
        "Documentation": f"https://github.com/Florents-Tselai/{PACKAGE_NAME}",
        "Issues": f"https://github.com/Florents-Tselai/{PACKAGE_NAME}/issues",
        "CI": f"https://github.com/Florents-Tselai/{PACKAGE_NAME}/actions",
        "Changelog": f"https://github.com/Florents-Tselai/{PACKAGE_NAME}/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "pip",
    ],
    extras_require={"test": ["pytest", "pytest-cov", "black", "ruff"]},
    python_requires=">=3.7",
)
