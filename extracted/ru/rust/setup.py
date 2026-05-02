"""The setup script."""

from setuptools import setup, find_packages

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="Jack Tierney",
    author_email="jackcurragh@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Unit step transformation of Ribo-Seq data",
    entry_points={
        "console_scripts": [
            "RUST=RUST.__main__:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    # long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="RUST",
    name="RUST",
    packages=find_packages(include=["RUST", "RUST.*"],
                           exclude=["sample_data/*", ]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/JackCurragh/RUST",
    version="1.3.1",
    zip_safe=False,
)
