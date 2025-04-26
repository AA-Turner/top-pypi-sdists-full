import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="primePy",
    version="1.3",
    author="Indrajit Jana",
    author_email="ijana@temple.edu",
    description="This module contains several useful functions to work with prime numbers. from primePy import primes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janaindrajit/primePy",
    packages=setuptools.find_packages(),
    keywords=['fast', 'prime', 'facorization', 'Eular phi', 'prime check'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)