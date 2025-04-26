import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="listcrunch",
    version="1.0.1",
    author="Dylan Freedman",
    author_email="freedmand@gmail.com",
    description="A simple human-readable way to compress redundant sequential data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MuckRock/listcrunch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
