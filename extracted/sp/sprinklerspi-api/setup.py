import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sprinklerspi-api",
    version="0.0.4",
    author="Reda",
    author_email="reda@aissaoui.org",
    description="Python library to interface with Sprinkler PI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-reda/sprinklerspi-api",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)