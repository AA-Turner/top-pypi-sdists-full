import os
from setuptools import setup, find_packages
import persisting_theory as package

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="persisting-theory",
    version=package.__version__,
    packages=find_packages(),
    include_package_data=True,
    license="BSD",  # example license
    description="Registries that can autodiscover values accross your project apps",
    long_description=README,
    url="https://code.agate.blue/agate/persisting-theory",
    author="Agate Blue",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
