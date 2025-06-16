import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="presto-types-parser",
    version="0.0.2",
    author="Ofek Ben-Yaish",
    description="Presto types parser for input rows returned by presto rest api",
    license="Apache License, Version 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ofekby/presto-types-parser",
    packages=setuptools.find_packages(exclude=["*.tests"]),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Database :: Front-Ends",
    ],
    test_suite="presto_types_parser.tests"
)
