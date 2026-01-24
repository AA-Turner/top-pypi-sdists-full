import os.path

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="apkutils2",
    version="1.0.0",
    description=("Utils for parsing apk."),
    # long_description=read('README.md'),
    url="https://github.com/codeskyblue/apkutils2",
    author="mikusjelly, codeskyblue",
    author_email="mikusjelly@gmail.com, codeskyblue@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="apk dex axml",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        "pyelftools",
        "cigam",
        "xmltodict",
    ],
)
