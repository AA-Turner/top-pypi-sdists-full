from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = (
    "A simple modern Python logger based on Rich."
)

def get_read_me():
    with open("README.md", "r") as f:
        return f.read()

# Setting up
setup(
    name="rich-logging",
    version=VERSION,
    author="Prerit Das",
    author_email="<preritdas@gmail.com>",
    description=DESCRIPTION,
    long_description=get_read_me(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = ["rich==12.5.1"],
    keywords=["python", "tools", "logging"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
