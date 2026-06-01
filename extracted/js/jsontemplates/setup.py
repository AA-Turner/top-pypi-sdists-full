from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jsontemplates",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author='Jon Keatley',
    description='A small python module for populating json template files.',
    url='https://gitlab.com/Jon.Keatley.Folio/json-templates',
    project_urls={'Source Code':'https://gitlab.com/Jon.Keatley.Folio/json-templates'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
