from setuptools import setup
import importlib.metadata
setup(
    name = 'python-csv',
    packages = ['pcsv'],
    version = "0.0.14",
    description = 'Python tools for manipulating csv files',
    author = "Jason Trigg",
    author_email = "jasontrigg0@gmail.com",
    url = "https://github.com/jasontrigg0/python-csv",
    download_url = 'https://github.com/jasontrigg0/python-csv/tarball/0.0.14',
    scripts=[
        "pcsv/pcsv",
        "pcsv/pagg",
        "pcsv/pgraph",
        "pcsv/pjoin",
        "pcsv/plook",
        "pcsv/psort",
        "pcsv/pset",
        "pcsv/ptable",
        "pcsv/pindent",
        "pcsv/pconcat",
        "pcsv/ptr",
        "pcsv/pcat",
        "pcsv/any2csv"
    ],
    install_requires=[
        "argparse",
        "numpy",
        "pandas",
        "matplotlib",
        "xlrd",
        "xmltodict",
        "demjson3",
        "levenshtein",
        "jtutils"
    ],
    keywords = [],
    classifiers = [],
)
