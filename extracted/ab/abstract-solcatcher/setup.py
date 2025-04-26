from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="abstract_solcatcher",
    version='0.0.3.233',  # Consider using dynamic versioning
    author="putkoff",
    author_email="partners@abstractendeavors.com",
    description=(
        "`abstract_solcatcher` provides a comprehensive solution for making HTTP requests "
        "specifically tailored for interacting with Solcatcher.io's APIs. It simplifies "
        "complex tasks such as data fetching, data manipulation, and interacting with the "
        "Flask backend of Solcatcher.io."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbstractEndeavors/abstract_solcatcher",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "abstract_solcatcher": ["database_calls/*.json"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
    ],
    install_requires=[
        "abstract_utilities",
        "abstract_solana",
        "abstract_apis",
        "requests",
        "abstract_security",
    ],
    extras_require={
        "dev": ["pytest", "flake8", "mypy"],
    },
    python_requires=">=3.6",
    license="MIT",
    license_files=("LICENSE",),
    setup_requires=["wheel"],
)
