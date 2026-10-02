import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urdf_parser_py",
    version="0.0.4",
    author="Thomas Moulard, David Lu, Kelsey Hawkins, Antonio El Khoury, Eric Cousineau",
    author_email="tmoulard@amazon.com",
    description="This package contains a python parser for the Unified Robot Description Format (URDF), which is an XML format for representing a robot model. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ros/urdf_parser_py",
    packages=setuptools.find_packages(),
    install_requires=["pyyaml", "lxml"],
    zip_safe=False)
