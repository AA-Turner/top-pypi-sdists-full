import io

from setuptools import setup, find_packages

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("VERSION") as version_file:
    version = version_file.read().strip().lower()
    if version.startswith("v"):
        version = version[1:]

setup(
    name="sqlalchemy-orm",
    version=version,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    author="Robert Parker",
    author_email="rob@parob.com",
    url="https://gitlab.com/parob/sqlalchemy-orm",
    download_url=f"https://gitlab.com/parob/sqlalchemy-orm/-/archive/v{version}"
    f"/sqlalchemy-orm-v{version}.tar.gz",
    keywords=["SQLAlchemy", "ORM"],
    description="Data Relation Mapping framework for Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=["SQLAlchemy", "inflection", "cached-property", "typing_inspect"],
    extras_require={"dev": ["pytest", "pytest-cov", "coverage", "faker"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
