import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="spoton_generator",
    version="0.1.5",
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A tool to generate data for Spot-On",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.forge.hefr.ch/pa-spot-on-demeusy/spot-on-generator",
    packages=["spoton_generator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["spoton-soozaccess", "matplotlib", "numpy"],
)
