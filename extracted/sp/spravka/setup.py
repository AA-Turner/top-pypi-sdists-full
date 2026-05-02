import setuptools
import os

version_path = os.path.join('spravka', 'VERSION')
with open("README.md", "r") as fh:
    long_description = fh.read()
try:
    with open('VERSION', "r") as fh:
        version = fh.read()
except FileNotFoundError:
    try:
        with open('spravka/VERSION', "r") as fh:
            version = fh.read()
    except FileNotFoundError:
        with open(version_path, "r") as fh:
            version = fh.read()

setuptools.setup(
    name="spravka",
    version=version,
    author="Bilenko Olexiy",
    author_email="bilenko_ol@ukr.net",
    description="Autogen for your python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prestonbrodus/spravka",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['spravka=spravka.main:main'],
    },
    install_requires=[
        'sphinx',
        'PyYAML',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
