from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="checkHash",
    version="1.0.1",
    description="Python package to check if a string is a valid hash.",
    py_modules=["checkHash"],
    package_dir={'': 'src'},
    install_requires=[
        "isHex>=1.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev": [
            "pytest>=3.7",
            "check-manifest>=0.48",
            "twine>=3.8.0",
        ],
    },
    url="https://github.com/xhelphin/checkHash",
    author="Jack Greenacre",
    author_email="jaxk.programmer@gmail.com",
)
